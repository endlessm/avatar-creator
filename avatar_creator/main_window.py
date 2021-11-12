from gi.repository import Gtk, Gdk


@Gtk.Template.from_resource('/org/endlessos/avatarCreator/main_window.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AvatarCreatorWindow'

    headerbar = Gtk.Template.Child()
    grid = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(300, 500)
        self.set_titlebar(self.headerbar)
        self.custom_css()

    def custom_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/org/endlessos/avatarCreator/avatar-creator.css")

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER)
