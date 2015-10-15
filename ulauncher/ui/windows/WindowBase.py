from gi.repository import Gio, Gtk  # pylint: disable=E0611
import logging
logger = logging.getLogger(__name__)

from . import get_builder


# This class is meant to be subclassed by UlauncherWindow.  It provides
# common functions and some boilerplate.
class WindowBase(Gtk.Window):
    __gtype_name__ = "Window"

    _prefsWereActivated = False

    # To construct a new instance of this method, the following notable
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your initialization code in finish_initializing

    def __new__(cls):
        """Special static method that's automatically called by Python when
        constructing a new instance of this class.

        Returns a fully instantiated BaseUlauncherWindow object.
        """
        builder = get_builder('UlauncherWindow')
        new_object = builder.get_object("ulauncher_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a UlauncherWindow object with it in order to finish
        initializing the start of the new UlauncherWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.PreferencesDialog = None  # class
        self.preferences_dialog = None  # instance
        self.AboutDialog = None  # class

    def on_mnu_about_activate(self, widget, data=None):
        """Display the about box for ulauncher."""
        if self.AboutDialog is not None:
            about = self.AboutDialog()  # pylint: disable=E1102
            response = about.run()
            about.destroy()

    def on_mnu_preferences_activate(self, widget, data=None):
        """Display the preferences window for ulauncher."""

        """ From the PyGTK Reference manual
           Say for example the preferences dialog is currently open,
           and the user chooses Preferences from the menu a second time;
           use the present() method to move the already-open dialog
           where the user can see it."""
        self._prefsWereActivated = True
        if self.preferences_dialog is not None:
            logger.debug('show existing preferences_dialog')
            self.preferences_dialog.present()
        elif self.PreferencesDialog is not None:
            logger.debug('create new preferences_dialog')
            self.preferences_dialog = self.PreferencesDialog()  # pylint: disable=E1102
            self.preferences_dialog.connect('destroy', self.on_preferences_dialog_destroyed)
            self.preferences_dialog.show()
        # destroy command moved into dialog to allow for a help button

    def on_mnu_close_activate(self, widget, data=None):
        """Signal handler for closing the UlauncherWindow."""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """Called when the UlauncherWindow is closed."""
        # Clean up code for saving application state should be added here.
        Gtk.main_quit()

    def on_preferences_dialog_destroyed(self, widget, data=None):
        '''only affects gui

        logically there is no difference between the user closing,
        minimising or ignoring the preferences dialog'''
        logger.debug('on_preferences_dialog_destroyed')
        # to determine whether to create or present preferences_dialog
        self.preferences_dialog = None