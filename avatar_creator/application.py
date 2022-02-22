# Copyright © 2021 Endless OS Foundation LLC.
#
# This file is part of clubhouse
# (see https://github.com/endlessm/clubhouse).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gi
import sys
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import GLib, Gio, Gtk, GObject, Adw

from .grid import Grid
GObject.type_register(Grid)

from .main_window import MainWindow


class Application(Adw.Application):
    window = NotImplemented
    file_list = []
    development_mode = False
    application_id = 'org.endlessos.avatarCreator'
    localedir = None

    def __init__(self, *args, **kwargs):
        self.localedir = kwargs.pop('localedir')
        super().__init__(*args, application_id=self.application_id)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        Adw.init()

        GLib.set_application_name('Avatar Creator')
        GLib.set_prgname('Avatar Creator')

        self.assemble_application_menu()

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self,
                                     icon_name=self.application_id)
        self.window.present()

    def get_logger(self):
        logger = logging.getLogger()
        if self.development_mode is True:
            logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
        return logger

    def assemble_application_menu(self):
        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.on_about_menu_clicked)

        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', self.on_quit_menu_clicked)

        save_action = Gio.SimpleAction.new('save', None)
        save_action.connect('activate', self.on_save_menu_clicked)

        self.add_action(about_action)
        self.add_action(quit_action)
        self.add_action(save_action)

    def on_about_menu_clicked(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/endlessos/avatarCreator/about_dialog.ui')
        about_dialog = builder.get_object('about_dialog')
        about_dialog.set_modal(True)
        if self.window is not NotImplemented:
            about_dialog.set_transient_for(self.window)
        about_dialog.present()

    def on_save_menu_clicked(self, action, param):
        if self.window is NotImplemented:
            return
        self.window.on_save_menu_clicked()

    def on_quit_menu_clicked(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
