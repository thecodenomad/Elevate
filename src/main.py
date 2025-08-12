"""Main application module for Elevate.

This module contains the main application class and entry point for the Elevate application.
"""

import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw
from elevate.window import ElevateWindow
from elevate.view.preferences_window import PreferencesWindow

class ElevateApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="org.thecodenomad.elevate", flags=0  # Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.create_action("quit", self.on_quit_action, ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)
        self._settings = Gio.Settings.new("org.thecodenomad.elevate")

    @property
    def settings(self):
        return self._settings

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = ElevateWindow(self.settings, application=self)
        win.present()

    def on_quit_action(self, *args):
        """Callback for the app.quit action."""
        self.quit()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog.new()
        about.set_application_name("Elevate")
        about.set_application_icon("org.thecodenomad.elevate")
        about.set_developer_name("thecodenomad")
        about.set_version("0.1.0")
        about.set_developers(["thecodenomad"])
        about.set_copyright("© 2025 thecodenomad")
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        # about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""

        win = PreferencesWindow(self.settings)
        win.set_transient_for(self.props.active_window)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point.

    Args:
        version: The version of the application

    Returns:
        int: The exit code of the application
    """
    app = ElevateApplication()
    return app.run(sys.argv)
