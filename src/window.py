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

from gi.repository import Adw, Gtk, Gio, GLib
from .backend.state_induction_controller import StateInductionController
from .view.stimuli_renderer import StimuliRenderer


@Gtk.Template(resource_path='/org/thecodenomad/elevate/window.ui')
class ElevateWindow(Adw.Window):
    __gtype_name__ = 'ElevateWindow'

    # Header bar and buttons
    header_bar = Gtk.Template.Child()
    sidebar_toggle_button = Gtk.Template.Child()
    play_button = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()

    # Sidebar controls
    split_view = Gtk.Template.Child()
    frequency_scale = Gtk.Template.Child()
    channel_offset_scale = Gtk.Template.Child()
    visual_stimuli_switch = Gtk.Template.Child()
    stimuli_type_combo = Gtk.Template.Child()

    # Main content area
    toolbar = Gtk.Template.Child()
    content_area = Gtk.Template.Child()
    stimuli_renderer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize controller
        self.controller = StateInductionController()

        self._setup_bindings()
        self._setup_signals()

        self.controller._visual_stimulus.set_widget(self.stimuli_renderer)
        self.stimuli_renderer.connect("resize", self._on_renderer_resize)
        self.stimuli_renderer.set_draw_func(self._on_draw)

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

        # Track toolbar visibility state
        self.toolbar_visible = True

    def _setup_bindings(self):
        """Setup property bindings between UI and controller settings."""
        # Bind frequency scale to controller settings
        self.controller._settings.bind_property(
            "base-frequency",
            self.frequency_scale.get_adjustment(),
            "value",
            Gio.SettingsBindFlags.DEFAULT
        )

        # Bind channel offset scale to controller settings
        self.controller._settings.bind_property(
            "channel-offset",
            self.channel_offset_scale.get_adjustment(),
            "value",
            Gio.SettingsBindFlags.DEFAULT
        )

        # Bind visual stimuli switch to controller settings
        self.controller._settings.bind_property(
            "enable-visual-stimuli",
            self.visual_stimuli_switch,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )
        self._init_stimuli_type_binding()

    def _setup_signals(self):
        """Setup signal handlers for UI elements."""
        # Connect button signals
        self.sidebar_toggle_button.connect("clicked", self._on_sidebar_toggle_clicked)
        self.play_button.connect("toggled", self._on_play_toggled)
        self.stop_button.connect("clicked", self._on_stop_clicked)

        # Connect controller property changes
        self.controller.connect("notify::is-playing", self._on_playing_state_changed)
        self.stimuli_type_combo.connect("notify::selected", self._on_stimuli_type_changed)

    def on_fade_animation_update(self, value):
        self.toolbar.set_opacity(value)

    def _on_stimuli_type_changed(self, *_):
        self.controller._settings.set_stimuli_type(self.stimuli_type_combo.get_selected())

    def _init_stimuli_type_binding(self):
        try:
            sel = self.controller._settings.get_stimuli_type()
        except Exception:
            sel = 0
        self.stimuli_type_combo.set_selected(int(sel))

    def _on_draw(self, widget, cr, width, height):
        self.controller._visual_stimulus.render(widget, cr, width, height)

    def _on_renderer_resize(self, *_args):
        self.stimuli_renderer.queue_draw()

    def _on_mouse_motion(self, controller, x, y):
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
            button.set_icon_name("media-playback-pause-symbolic")
            self.sidebar_toggle_button.set_active(False)
            self.split_view.set_show_sidebar(False)
            self.controller.play()
        else:
            button.set_icon_name("media-playback-start-symbolic")
            self.controller.pause()

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
