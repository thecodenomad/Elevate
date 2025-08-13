# window.py
#
# Copyright 2025 thecodenomad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Elevate application window module.

Provides the :class:`ElevateWindow` class which composes UI elements, binds
settings, and controls playback of visual and audio stimuli.
"""

import time

from gi.repository import Adw, Gtk, Gio, GLib, GObject
from elevate.backend.state_induction_controller import StateInductionController
from elevate.view.stimuli_renderer import StimuliRenderer
from elevate.view.epileptic_warning_dialog import EpilepticWarningDialog
from elevate.view.sidebar import Sidebar


@Gtk.Template(resource_path="/org/thecodenomad/elevate/window.ui")
class ElevateWindow(Adw.Window):
    """Main application window.

    Hosts the toolbar, sidebar, and stimuli renderer. Wires UI controls to the
    StateInductionController and manages transient UI behavior such as toolbar
    fade animations and warning dialogs.
    """

    __gtype_name__ = "ElevateWindow"

    # Header bar and buttons
    header_bar = Gtk.Template.Child()
    sidebar_toggle_button = Gtk.Template.Child()
    play_button = Gtk.Template.Child()
    volume_button = Gtk.Template.Child()
    volume_scale = Gtk.Template.Child()
    fullscreen_button = Gtk.Template.Child()
    preferences_button = Gtk.Template.Child()

    # Sidebar controls
    scrolled_window = Gtk.Template.Child()
    split_view = Gtk.Template.Child()

    # Main content area
    run_time_label = Gtk.Template.Child()
    overlay_area = Gtk.Template.Child()
    toolbar = Gtk.Template.Child()
    time_scale = Gtk.Template.Child()
    content_area = Gtk.Template.Child()
    stimuli_renderer = Gtk.Template.Child()
    volume_popover = Gtk.Template.Child()

    def __init__(self, settings, **kwargs):
        """Initialize the ElevateWindow.

        Args:
          **kwargs: Keyword args forwarded to Adw.Window initializer.
        """
        super().__init__(**kwargs)
        self._settings = settings

        self.controller = StateInductionController()
        self.sidebar = Sidebar(self.controller, self.settings)
        self.scrolled_window.set_child(self.sidebar)

        self._setup_bindings()
        self._setup_signals()

        self.controller._visual_stimulus.set_widget(self.stimuli_renderer)
        self.stimuli_renderer.connect("resize", self._on_renderer_resize)
        self.stimuli_renderer.set_draw_func(self._on_draw)

        self._bind_volume()
        # Cache frequently accessed UI elements for performance
        self._minutes_spin_button = getattr(self.sidebar, "minutes_spin_button", None)
        self._time_adjustment = self.time_scale.get_adjustment()

        # Initialize max runtime (seconds)
        self._max_seconds = 3600
        if self._minutes_spin_button:
            try:
                self._max_seconds = self._minutes_spin_button.get_value() * 60
                # Keep max_seconds in sync when minutes change
                self._minutes_spin_button.connect(
                    "notify::selected-item", lambda *args: self._update_max_seconds()
                )

                # Bind minutes_spin_button value to time_scale upper limit
                self._minutes_spin_button.bind_property(
                    "value",
                    self._time_adjustment,
                    "upper",
                    GObject.BindingFlags.DEFAULT,
                    lambda binding, value: value * 60,  # Convert minutes to seconds
                    None,
                )
            except Exception as e:
                print(f"[ElevateWindow] Warning initializing minutes binding: {e}")
                self._time_adjustment.set_upper(3600)  # Default to 1 hour
        else:
            self._time_adjustment.set_upper(3600)  # Default to 1 hour

        # Set fixed width for timer label to avoid layout changes
        self.run_time_label.set_width_chars(6)  # Fits "00:00"
        self.time_scale.set_draw_value(False)  # Look like progress bar
        self.time_scale.set_sensitive(False)  # Read-only
        self.time_scale.set_digits(0)  # Avoid fractional display

        # Apply CSS for fade-out transition
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(
            b"""
        #toolbar {
            opacity: 1.0;
            transition: none;  /* Instant fade-in */
        }
        #toolbar.faded {
            opacity: 0.0;
            transition: opacity 2000ms ease-in-out;  /* 2-second fade-out */
        }
        #run-time-label {
            font-family: monospace;  /* Consistent digit spacing */
        }
        """
        )
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.toolbar.set_name("toolbar")
        self.run_time_label.set_name("run-time-label")

        self.motion_controller = Gtk.EventControllerMotion()
        self.motion_controller.connect("motion", self._on_mouse_motion)
        self.content_area.add_controller(self.motion_controller)

        self._toolbar_motion = Gtk.EventControllerMotion()
        self._toolbar_motion.connect("enter", self._on_toolbar_enter)
        self._toolbar_motion.connect("leave", self._on_toolbar_leave)
        self.toolbar.add_controller(self._toolbar_motion)

        self.toolbar_visible = True
        self._pointer_in_toolbar = False
        self._volume_popover_open = False
        self._fade_timeout_id = None
        self.timeout_id = None
        self._last_motion_pos = None  # Track last mouse position for debouncing
        self._last_elapsed = None  # Track last elapsed time for UI updates
        self._last_motion_time = None  # Track last motion time for rate limiting

        # Fallback timer if controller.elapsed_time fails
        self._start_time = time.monotonic()

    @property
    def settings(self):
        return self._settings

    def _update_max_seconds(self):
        """Update cached max_seconds from minutes spin button."""
        if self._minutes_spin_button:
            try:
                self._max_seconds = self._minutes_spin_button.get_value() * 60
            except Exception:
                pass

    def update_timer(self):
        """Update the run time label and scale with elapsed time."""
        try:
            # Use controller's elapsed time as primary source
            elapsed = self.controller.elapsed_time
            if elapsed is None:
                elapsed = time.monotonic() - self._start_time
        except Exception:
            elapsed = time.monotonic() - self._start_time

        # Ensure elapsed is a numeric value
        try:
            elapsed = float(elapsed)
        except (TypeError, ValueError):
            elapsed = 0.0

        # Get max runtime from minutes_spin_button
        max_seconds = self._max_seconds

        # Cap elapsed time
        if elapsed >= max_seconds:  # type: ignore
            elapsed = max_seconds
            self.controller.stop()
            if self.play_button.get_active():
                self.play_button.set_active(False)
            if self.timeout_id:
                GLib.source_remove(self.timeout_id)
                self.timeout_id = None

            # Reset the controller
            self.controller._elapsed_time = 0.0
            self.time_scale.set_value(0)
            self.run_time_label.set_text("00:00")
            # Max runtime reached, stopping playback

        # Use divmod for efficiency and avoid redundant UI updates
        minutes, seconds = divmod(int(elapsed), 60)
        # Update UI only if time changed significantly (avoid sub-second updates)
        last_elapsed = self._last_elapsed if self._last_elapsed is not None else -1
        last_minutes, last_seconds = divmod(int(last_elapsed), 60)
        if (minutes, seconds) != (last_minutes, last_seconds):
            self.run_time_label.set_text(f"{minutes:02d}:{seconds:02d}")
            self.time_scale.set_value(elapsed)
            self._last_elapsed = elapsed

        return True  # Continue updating

    def destroy(self):
        """Clean up timeout sources."""
        # Stop playback if active
        if self.controller.is_playing:
            self.controller.stop()
            if self.play_button.get_active():
                self.play_button.set_active(False)

        # Clean up all timeout sources
        for attr in ["timeout_id", "_fade_timeout_id"]:
            timeout_id = getattr(self, attr, None)
            if timeout_id is not None:
                GLib.source_remove(timeout_id)
                setattr(self, attr, None)

        super().destroy()

    def _setup_bindings(self):
        """Bind GSettings keys to UI controls and internal properties."""
        self.controller._settings.bind_property(
            "base-frequency",
            self.sidebar.frequency_scale.get_adjustment(),
            "value",
            0,  # Gio.SettingsBindFlags.DEFAULT
        )
        self.controller._settings.bind_property(
            "channel-offset",
            self.sidebar.channel_offset_scale.get_adjustment(),
            "value",
            0,  # Gio.SettingsBindFlags.DEFAULT
        )
        self.controller._settings.bind_property(
            "enable-visual-stimuli",
            self.sidebar.visual_stimuli_switch,
            "active",
            0,  # Gio.SettingsBindFlags.DEFAULT
        )
        self._init_stimuli_type_binding()

        self.fullscreen_button.bind_property(
            "active", self.header_bar, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )

    def _setup_signals(self):
        """Connect UI signals to their handlers and controller notifications."""
        self.sidebar_toggle_button.connect("clicked", self._on_sidebar_toggle_clicked)
        self.play_button.connect("toggled", self._on_play_toggled)
        self.volume_scale.connect("value-changed", self._on_volume_changed)
        self.preferences_button.connect("clicked", self._on_preferences_clicked)
        self.controller.connect("notify::is-playing", self._on_playing_state_changed)
        self.sidebar.stimuli_type_combo.connect("notify::selected", self._on_stimuli_type_changed)
        self.volume_button.connect("notify::active", self._on_volume_popover_active)
        self.fullscreen_button.connect("toggled", self._on_fullscreen_toggled)

    def _reset_toolbar_visible(self):
        """Reset toolbar to visible state instantly and start fade timeout."""
        self.toolbar.remove_css_class("faded")
        self.toolbar_visible = True
        if self._fade_timeout_id is not None:
            GLib.source_remove(self._fade_timeout_id)
            self._fade_timeout_id = None
        if self.controller.is_playing:
            self._fade_timeout_id = GLib.timeout_add(3000, self._start_fade_if_inactive)

    def _start_fade_if_inactive(self):
        """Start fade-out if mouse is outside toolbar, no popover, and playing."""
        if self._pointer_in_toolbar or self._volume_popover_open or not self.controller.is_playing:
            return False
        self.toolbar.add_css_class("faded")
        self.toolbar_visible = False
        self._fade_timeout_id = None
        return False

    def _safe_queue_draw(self):
        """Queue a redraw of the stimuli renderer, ignoring non-fatal errors."""
        try:
            self.stimuli_renderer.queue_draw()
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Silently ignore queue_draw failures

    def _on_fullscreen_toggled(self, button):
        """Toggle fullscreen state."""
        if button.get_active():
            self.fullscreen()
            button.set_icon_name("view-restore-symbolic")
        else:
            self.unfullscreen()
            button.set_icon_name("view-fullscreen-symbolic")

    def _on_stimuli_type_changed(self, *_):
        """Persist selected stimuli type to settings."""
        self.controller._settings.set_stimuli_type(self.sidebar.stimuli_type_combo.get_selected())

    def _bind_volume(self):
        """Initialize volume slider from audio stimulus if available."""
        try:
            self.volume_scale.set_value(self.controller._audio_stimulus.get_volume())
        except AttributeError:
            pass

    def _init_stimuli_type_binding(self):
        """Initialize sidebar combo selection from settings, defaulting to 0."""
        try:
            sel = self.controller._settings.get_stimuli_type()
        except AttributeError:
            sel = 0
        self.sidebar.stimuli_type_combo.set_selected(int(sel))

    def _on_draw(self, widget, cr, width, height):
        """Render visual stimuli on the drawing area."""
        self.controller._visual_stimulus.render(widget, cr, width, height)

    def _on_renderer_resize(self, *_args):
        """Handle renderer resize by scheduling a redraw."""
        self.stimuli_renderer.queue_draw()

    def _on_mouse_motion(self, controller, x, y):
        """Show toolbar on significant mouse motion."""
        if x is None or y is None:  # Handle programmatic calls
            self._reset_toolbar_visible()
            return

        # Rate limit: only process once per 100ms
        current_time = time.monotonic()
        if (
            hasattr(self, "_last_motion_time")
            and self._last_motion_time is not None
            and (current_time - self._last_motion_time) < 0.1
        ):
            return
        self._last_motion_time = current_time

        # Debounce: only reset if mouse moved significantly
        if (
            self._last_motion_pos is None
            or abs(self._last_motion_pos[0] - x) > 5
            or abs(self._last_motion_pos[1] - y) > 5
        ):
            self._last_motion_pos = (x, y)
            self._reset_toolbar_visible()

    def _on_toolbar_enter(self, controller, _x, _y):
        """Keep toolbar visible when mouse enters."""
        self._pointer_in_toolbar = True
        self._reset_toolbar_visible()

    def _on_toolbar_leave(self, controller):
        """Start fade timeout when mouse leaves toolbar."""
        self._pointer_in_toolbar = False
        if self.controller.is_playing and not self._volume_popover_open:
            self._reset_toolbar_visible()  # Start 3s timeout

    def _on_sidebar_toggle_clicked(self, button):
        """Show or hide the sidebar."""
        self.split_view.set_show_sidebar(button.get_active())

    def _on_play_toggled(self, button):
        """Handle play/pause toggle."""
        if button.get_active():
            self._handle_start(button)
        else:
            self._handle_stop(button)
        self._on_mouse_motion(None, None, None)

    def _handle_start(self, button):
        """Initialize play state and optionally show warning dialog."""
        self._start_time = time.monotonic()  # Reset fallback timer
        self.time_scale.set_value(0)
        self.run_time_label.set_text("00:00")
        if self.sidebar.visual_stimuli_switch.get_active():
            self._show_warning_and_start(button)
        else:
            self._start_playback(button)

    def _show_warning_and_start(self, button):
        """Show epileptic warning dialog before starting playback."""

        if not self.settings.epileptic_warning:
            self._start_playback(button)
            return

        dlg = EpilepticWarningDialog()
        dlg.present(self)

        def _on_warning_response(dialog, result):
            try:
                response = dialog.choose_finish(result)
            except Exception:
                response = "proceed"
            if response == "cancel":
                button.set_active(False)
                return
            self._start_playback(button)

        try:
            dlg.choose(self, None, _on_warning_response)
        except Exception:
            # Fallback if choose() not available
            self._start_playback(button)

    def _start_playback(self, button):
        """Start playback, update UI, and schedule timer updates."""
        button.set_icon_name("media-playback-stop-symbolic")
        self.sidebar_toggle_button.set_active(False)
        self.split_view.set_show_sidebar(False)
        self.controller.play()
        if self.timeout_id is None:
            self.timeout_id = GLib.timeout_add(100, self.update_timer, priority=GLib.PRIORITY_DEFAULT)
        self._safe_queue_draw()

    def _handle_stop(self, button):
        """Handle pause/stop state when play button is toggled off."""
        button.set_icon_name("media-playback-start-symbolic")
        self.controller.pause()
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self._safe_queue_draw()

    def _on_stop_clicked(self, button):
        """Stop playback and reset play button state."""
        self.controller.stop()
        self._start_time = time.monotonic()  # Reset fallback timer
        self.time_scale.set_value(0)  # Reset scale
        self.run_time_label.set_text("00:00")  # Reset label
        if self.play_button.get_active():
            self.play_button.set_active(False)
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self._on_mouse_motion(None, None, None)

    def _on_playing_state_changed(self, controller, param):
        """Enable/disable stop button based on playing state."""
        is_playing = controller.is_playing
        # self.stop_button.set_sensitive(is_playing)

    def _on_volume_changed(self, scale):
        """Update audio volume when the slider changes."""
        self.controller._audio_stimulus.set_volume(scale.get_value())
        self._reset_toolbar_visible()

    def _on_volume_popover_active(self, *_):
        """Keep toolbar visible when volume popover is open."""
        self._volume_popover_open = self.volume_button.get_active()
        if self._volume_popover_open:
            self._reset_toolbar_visible()

    def _on_preferences_clicked(self, *_):
        """Open the Preferences window dialog."""
        from .view.preferences_window import PreferencesWindow

        dlg = PreferencesWindow(self.settings)
        dlg.present(self)
