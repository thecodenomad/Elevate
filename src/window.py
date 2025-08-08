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

from gi.repository import Adw, Gtk, Gio, GLib, GObject
from .backend.state_induction_controller import StateInductionController
from .view.stimuli_renderer import StimuliRenderer
from .view.sidebar import Sidebar


@Gtk.Template(resource_path='/org/thecodenomad/elevate/window.ui')
class ElevateWindow(Adw.Window):
    """Main application window.

    Hosts the toolbar, sidebar, and stimuli renderer. Wires UI controls to the
    StateInductionController and manages transient UI behavior such as toolbar
    fade animations and warning dialogs.
    """

    __gtype_name__ = 'ElevateWindow'

    # Header bar and buttons
    header_bar = Gtk.Template.Child()
    sidebar_toggle_button = Gtk.Template.Child()
    play_button = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()
    volume_button = Gtk.Template.Child()
    volume_scale = Gtk.Template.Child()
    fullscreen_button = Gtk.Template.Child()
    preferences_button = Gtk.Template.Child()

    # Sidebar controls
    scrolled_window = Gtk.Template.Child()
    split_view = Gtk.Template.Child()

    # Main content area
    overlay_area = Gtk.Template.Child()
    toolbar = Gtk.Template.Child()
    content_area = Gtk.Template.Child()
    stimuli_renderer = Gtk.Template.Child()
    volume_popover = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """Initialize the ElevateWindow.

        Args:
          **kwargs: Keyword args forwarded to Adw.Window initializer.
        """
        super().__init__(**kwargs)

        self.controller = StateInductionController()
        self.sidebar = Sidebar(controller=self.controller)
        self.scrolled_window.set_child(self.sidebar)

        self._setup_bindings()
        self._setup_signals()

        self.controller._visual_stimulus.set_widget(self.stimuli_renderer)
        self.stimuli_renderer.connect("resize", self._on_renderer_resize)
        self.stimuli_renderer.set_draw_func(self._on_draw)

        self._bind_volume()

        self.toolbar.set_opacity(1.0)

        animation_target = Adw.PropertyAnimationTarget.new(self.toolbar, "opacity")

        self.fade_out_animation = Adw.TimedAnimation(
            widget=self.toolbar,
            value_from=1.0,
            value_to=0.0,
            duration=2000,
            easing=Adw.Easing.EASE_IN_OUT_CUBIC,
            target=animation_target,
        )
        self.fade_in_animation = Adw.TimedAnimation(
            widget=self.toolbar,
            value_from=0.0,
            value_to=1.0,
            duration=500,
            easing=Adw.Easing.EASE_IN_OUT_CUBIC,
            target=animation_target,
        )

        self.motion_controller = Gtk.EventControllerMotion()
        self.motion_controller.connect("motion", self._on_mouse_motion)
        self.content_area.add_controller(self.motion_controller)

        self._toolbar_motion = Gtk.EventControllerMotion()
        self._toolbar_motion.connect("motion", self._on_toolbar_motion)
        self.toolbar.add_controller(self._toolbar_motion)

        self._toolbar_motion_outside = Gtk.EventControllerMotion()
        self._toolbar_motion_outside.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self._toolbar_motion_outside.connect("motion", self._on_global_motion)
        self.content_area.add_controller(self._toolbar_motion_outside)

        self.toolbar_visible = True
        self._pointer_in_toolbar = False
        self._volume_popover_open = False

    def _setup_bindings(self):
        """Bind GSettings keys to UI controls and internal properties."""
        self.controller._settings.bind_property(
            "base-frequency",
            self.sidebar.frequency_scale.get_adjustment(),
            "value",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.controller._settings.bind_property(
            "channel-offset",
            self.sidebar.channel_offset_scale.get_adjustment(),
            "value",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self.controller._settings.bind_property(
            "enable-visual-stimuli",
            self.sidebar.visual_stimuli_switch,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )
        self._init_stimuli_type_binding()

        self.fullscreen_button.bind_property(
            "active", self.header_bar, "visible", GObject.BindingFlags.INVERT_BOOLEAN
        )

    def _setup_signals(self):
        """Connect UI signals to their handlers and controller notifications."""
        self.sidebar_toggle_button.connect("clicked", self._on_sidebar_toggle_clicked)
        self.play_button.connect("toggled", self._on_play_toggled)
        self.stop_button.connect("clicked", self._on_stop_clicked)
        self.volume_scale.connect("value-changed", self._on_volume_changed)
        self.preferences_button.connect("clicked", self._on_preferences_clicked)

        self.controller.connect("notify::is-playing", self._on_playing_state_changed)
        self.sidebar.stimuli_type_combo.connect("notify::selected", self._on_stimuli_type_changed)
        self.volume_button.connect("notify::active", self._on_volume_popover_active)
        self.fullscreen_button.connect("toggled", self._on_fullscreen_toggled)

    def on_fade_animation_update(self, value):
        """Update toolbar opacity during animations.

        Args:
          value: The new opacity value (0..1).
        """
        self.toolbar.set_opacity(value)

    def _reset_toolbar_visible(self):
        """Reset toolbar to visible state and pause any fade-out animation."""
        self.fade_out_animation.pause()
        self.fade_out_animation.reset()
        self.toolbar.set_opacity(1.0)
        self.toolbar_visible = True

    def _safe_queue_draw(self):
        """Queue a redraw of the stimuli renderer, ignoring non-fatal errors."""
        try:
            self.stimuli_renderer.queue_draw()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("[ElevateWindow] queue_draw failed:", e)

    def _on_fullscreen_toggled(self, button):
        """Toggle fullscreen state.

        Args:
          button: The toggle button that triggered the action.
        """
        if button.get_active():
            print("Setting to fullscreen")
            self.fullscreen()
            button.set_icon_name("view-restore-symbolic")
        else:
            print("Unset fullscreen")
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
        """Render visual stimuli on the drawing area.

        Args:
          widget: The drawing widget.
          cr: Cairo context.
          width: Allocated width.
          height: Allocated height.
        """
        self.controller._visual_stimulus.render(widget, cr, width, height)

    def _on_renderer_resize(self, *_args):
        """Handle renderer resize by scheduling a redraw."""
        self.stimuli_renderer.queue_draw()

    def _on_mouse_motion(self, controller, x, y):
        """Handle mouse motion to auto-hide/show toolbar.

        Args:
          controller: Motion controller emitting the event.
          x: Pointer x-coordinate.
          y: Pointer y-coordinate.
        """
        if self._pointer_in_toolbar or self._volume_popover_open:
            self._reset_toolbar_visible()
            return
        if self.play_button.get_active():
            self.fade_in_animation.pause()
            self.fade_in_animation.reset()
            self.fade_out_animation.play()
            self.toolbar_visible = False
        elif not self.toolbar_visible:
            self._reset_toolbar_visible()

    def _on_sidebar_toggle_clicked(self, button):
        """Show or hide the sidebar.

        Args:
          button: The toggle button controlling sidebar visibility.
        """
        self.split_view.set_show_sidebar(button.get_active())

    def _on_play_toggled(self, button):
        """Handle play/pause toggle and display safety warning if needed.

        Args:
          button: The play/pause toggle button.
        """
        if button.get_active():
            if self.sidebar.visual_stimuli_switch.get_active():
                from .view.epileptic_warning_dialog import EpilepticWarningDialog
                dlg = EpilepticWarningDialog()
                dlg.present(self)

                def _on_warning_response(dialog, result):
                    """Process alert dialog result and start playback on proceed."""
                    try:
                        response = dialog.choose_finish(result)
                    except Exception:
                        response = "proceed"
                    if response == "cancel":
                        button.set_active(False)
                        return
                    print("[ElevateWindow] Play toggled ON")
                    button.set_icon_name("media-playback-pause-symbolic")
                    self.sidebar_toggle_button.set_active(False)
                    self.split_view.set_show_sidebar(False)
                    self.controller.play()
                    try:
                        print("[ElevateWindow] queue_draw after play")
                        self.stimuli_renderer.queue_draw()
                    except Exception as e:  # pylint: disable=broad-exception-caught
                        print("[ElevateWindow] queue_draw failed:", e)

                try:
                    dlg.choose(self, None, _on_warning_response)
                except Exception:
                    print("[ElevateWindow] Warning choose() not available; proceeding")
                    print("[ElevateWindow] Play toggled ON")
                    button.set_icon_name("media-playback-pause-symbolic")
                    self.sidebar_toggle_button.set_active(False)
                    self.split_view.set_show_sidebar(False)
                    self.controller.play()
                    try:
                        print("[ElevateWindow] queue_draw after play")
                        self.stimuli_renderer.queue_draw()
                    except Exception as e:  # pylint: disable=broad-exception-caught
                        print("[ElevateWindow] queue_draw failed:", e)
                return
            print("[ElevateWindow] Play toggled ON")
            button.set_icon_name("media-playback-pause-symbolic")
            self.sidebar_toggle_button.set_active(False)
            self.split_view.set_show_sidebar(False)
            self.controller.play()
            try:
                print("[ElevateWindow] queue_draw after play")
                self.stimuli_renderer.queue_draw()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("[ElevateWindow] queue_draw failed:", e)
        else:
            print("[ElevateWindow] Play toggled OFF")
            button.set_icon_name("media-playback-start-symbolic")
            self.controller.pause()
            try:
                print("[ElevateWindow] queue_draw after pause")
                self.stimuli_renderer.queue_draw()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("[ElevateWindow] queue_draw failed:", e)

        self._on_mouse_motion(None, None, None)

    def _on_stop_clicked(self, button):
        """Stop playback and reset play button state.

        Args:
          button: The stop button.
        """
        self.controller.stop()
        if self.play_button.get_active():
            self.play_button.set_active(False)
        self._on_mouse_motion(None, None, None)

    def _on_playing_state_changed(self, controller, param):
        """Enable/disable stop button based on playing state.

        Args:
          controller: The StateInductionController instance.
          param: The GObject.ParamSpec that changed.
        """
        is_playing = controller.is_playing
        self.stop_button.set_sensitive(is_playing)

    def _on_volume_changed(self, scale):
        """Update audio volume when the slider changes.

        Args:
          scale: The Gtk.Scale used to control volume.
        """
        self.controller._audio_stimulus.set_volume(scale.get_value())
        self.toolbar.set_opacity(1.0)
        self.toolbar_visible = True

    def _on_toolbar_motion(self, *_):
        """Keep toolbar visible while the pointer is over it."""
        self._pointer_in_toolbar = True
        self._reset_toolbar_visible()

    def _on_global_motion(self, controller, x, y):
        """Hide toolbar after inactivity when pointer leaves toolbar region.

        Args:
          controller: Motion controller emitting the event.
          x: Pointer x-coordinate.
          y: Pointer y-coordinate.
        """
        alloc = self.toolbar.get_allocation()
        in_x = alloc.x <= x <= alloc.x + alloc.width
        in_y = alloc.y <= y <= alloc.y + alloc.height
        inside = in_x and in_y
        if not inside:
            self._pointer_in_toolbar = False
            if self.play_button.get_active() and not self._volume_popover_open:
                self.fade_out_animation.play()
                self.toolbar_visible = False

    def _on_volume_popover_active(self, *_):
        """Pause fade-out when volume popover is open; resume when closed."""
        self._volume_popover_open = self.volume_button.get_active()
        if self._volume_popover_open:
            self._reset_toolbar_visible()
        elif self.play_button.get_active() and not self._pointer_in_toolbar:
            self.fade_out_animation.play()
            self.toolbar_visible = False

    def _on_preferences_clicked(self, *_):
        """Open the Preferences window dialog."""
        from .view.preferences_window import PreferencesWindow

        dlg = PreferencesWindow()
        dlg.present(self)
