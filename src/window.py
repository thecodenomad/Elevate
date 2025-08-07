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
    __gtype_name__ = 'ElevateWindow'

    # Header bar and buttons
    header_bar = Gtk.Template.Child()
    sidebar_toggle_button = Gtk.Template.Child()
    play_button = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()
    volume_button = Gtk.Template.Child()
    volume_scale = Gtk.Template.Child()
    fullscreen_button = Gtk.Template.Child()

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
        super().__init__(**kwargs)

        # Initialize controller
        self.controller = StateInductionController()

        # Setup Sidebar
        self.sidebar = Sidebar()

        self.scrolled_window.set_child(self.sidebar)

        self._setup_bindings()
        self._setup_signals()

        self.controller._visual_stimulus.set_widget(self.stimuli_renderer)
        self.stimuli_renderer.connect("resize", self._on_renderer_resize)
        self.stimuli_renderer.set_draw_func(self._on_draw)

        # Bind volume scale to controller/audio
        self._bind_volume()

        # Set initial opacity
        self.toolbar.set_opacity(1.0)

        # Animation target for opacity
        animation_target = Adw.PropertyAnimationTarget.new(self.toolbar, "opacity")

        # Animation setup
        self.fade_out_animation = Adw.TimedAnimation(
            widget=self.toolbar,
            value_from=1.0,
            value_to=0.0,
            duration=3000,  # 3000ms fade-out
            easing=Adw.Easing.EASE_IN_OUT_CUBIC,
            target=animation_target
        )
        self.fade_in_animation = Adw.TimedAnimation(
            widget=self.toolbar,
            value_from=0.0,
            value_to=1.0,
            duration=500,  # 500ms fade-in
            easing=Adw.Easing.EASE_IN_OUT_CUBIC,
            target=animation_target
        )

        # Set up motion controller
        self.motion_controller = Gtk.EventControllerMotion()
        self.motion_controller.connect("motion", self._on_mouse_motion)
        self.content_area.add_controller(self.motion_controller)

        # Pointer tracking over toolbar using motion + leave
        self._toolbar_motion = Gtk.EventControllerMotion()
        self._toolbar_motion.connect("motion", self._on_toolbar_motion)
        self.toolbar.add_controller(self._toolbar_motion)

        self._toolbar_motion_outside = Gtk.EventControllerMotion()
        self._toolbar_motion_outside.set_propagation_phase(Gtk.PropagationPhase.BUBBLE)
        self._toolbar_motion_outside.connect("motion", self._on_global_motion)
        self.content_area.add_controller(self._toolbar_motion_outside)

        # Track toolbar visibility/state
        self.toolbar_visible = True
        self._pointer_in_toolbar = False
        self._volume_popover_open = False

    def _setup_bindings(self):
        """Setup property bindings between UI and controller settings."""
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

        self.fullscreen_button.bind_property("active", self.header_bar, "visible", GObject.BindingFlags.INVERT_BOOLEAN)

    def _setup_signals(self):
        """Setup signal handlers for UI elements."""
        # Connect button signals
        self.sidebar_toggle_button.connect("clicked", self._on_sidebar_toggle_clicked)
        self.play_button.connect("toggled", self._on_play_toggled)
        self.stop_button.connect("clicked", self._on_stop_clicked)
        self.volume_scale.connect("value-changed", self._on_volume_changed)

        # Connect controller property changes
        self.controller.connect("notify::is-playing", self._on_playing_state_changed)
        self.sidebar.stimuli_type_combo.connect("notify::selected", self._on_stimuli_type_changed)
        self.volume_button.connect("notify::active", self._on_volume_popover_active)
        self.fullscreen_button.connect("toggled", self._on_fullscreen_toggled)


    def on_fade_animation_update(self, value):
        self.toolbar.set_opacity(value)

    def _on_fullscreen_toggled(self, button):

        if button.get_active():
            print("Setting to fullscreen")
            self.fullscreen()
            button.set_icon_name("view-restore-symbolic")
        else:
            print("Unset fullscreen")
            self.unfullscreen()
            button.set_icon_name("view-fullscreen-symbolic")

    def _on_stimuli_type_changed(self, *_):
        self.controller._settings.set_stimuli_type(self.sidebar.stimuli_type_combo.get_selected())

    def _bind_volume(self):
        try:
            self.volume_scale.set_value(self.controller._audio_stimulus.get_volume())
        except Exception:
            pass

    def _init_stimuli_type_binding(self):
        try:
            sel = self.controller._settings.get_stimuli_type()
        except Exception:
            sel = 0
        self.sidebar.stimuli_type_combo.set_selected(int(sel))

    def _on_draw(self, widget, cr, width, height):
        self.controller._visual_stimulus.render(widget, cr, width, height)

    def _on_renderer_resize(self, *_args):
        self.stimuli_renderer.queue_draw()

    def _on_mouse_motion(self, controller, x, y):
        if self._pointer_in_toolbar or self._volume_popover_open:
            self.fade_out_animation.pause()
            self.fade_out_animation.reset()
            self.toolbar.set_opacity(1.0)
            self.toolbar_visible = True
            return
        if self.play_button.get_active():
            self.fade_in_animation.pause()
            self.fade_in_animation.reset()
            self.fade_out_animation.play()
            self.toolbar_visible = False
        elif not self.toolbar_visible:
            self.fade_out_animation.pause()
            self.fade_out_animation.reset()
            self.toolbar.set_opacity(1.0)
            self.toolbar_visible = True

    def _on_sidebar_toggle_clicked(self, button):
        """Handler for sidebar toggle button click."""
        self.split_view.set_show_sidebar(button.get_active())

    def _on_play_toggled(self, button):
        """Handler for play button click."""
        if button.get_active():
            print("[ElevateWindow] Play toggled ON")
            button.set_icon_name("media-playback-pause-symbolic")
            self.sidebar_toggle_button.set_active(False)
            self.split_view.set_show_sidebar(False)
            self.controller.play()
            try:
                print("[ElevateWindow] queue_draw after play")
                self.stimuli_renderer.queue_draw()
            except Exception as e:
                print("[ElevateWindow] queue_draw failed:", e)
        else:
            print("[ElevateWindow] Play toggled OFF")
            button.set_icon_name("media-playback-start-symbolic")
            self.controller.pause()
            try:
                print("[ElevateWindow] queue_draw after pause")
                self.stimuli_renderer.queue_draw()
            except Exception as e:
                print("[ElevateWindow] queue_draw failed:", e)

        # Trigger the animations
        self._on_mouse_motion(None, None, None)

    def _on_stop_clicked(self, button):
        """Handler for stop button click."""
        self.controller.stop()
        # User clicked stop, so update play
        if self.play_button.get_active():
            self.play_button.set_active(False)

        # Trigger the animations
        self._on_mouse_motion(None, None, None)

    def _on_playing_state_changed(self, controller, param):
        is_playing = controller.is_playing
        self.stop_button.set_sensitive(is_playing)

    def _on_volume_changed(self, scale):
        self.controller._audio_stimulus.set_volume(scale.get_value())
        self.toolbar.set_opacity(1.0)
        self.toolbar_visible = True

    def _on_toolbar_motion(self, *_):
        self._pointer_in_toolbar = True
        self.fade_out_animation.pause()
        self.fade_out_animation.reset()
        self.toolbar.set_opacity(1.0)

    def _on_global_motion(self, controller, x, y):
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
        # MenuButton.active reflects popover visibility
        self._volume_popover_open = self.volume_button.get_active()
        if self._volume_popover_open:
            self.fade_out_animation.pause()
            self.fade_out_animation.reset()
            self.toolbar.set_opacity(1.0)
            self.toolbar_visible = True
        elif self.play_button.get_active() and not self._pointer_in_toolbar:
            self.fade_out_animation.play()
            self.toolbar_visible = False
