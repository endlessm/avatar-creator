import os
from gi.repository import Gtk, Gdk
from . import config


DEFAULT_VARIANT = 'robots'


class ModuleImage(Gtk.Button):
    def __init__(self, path):
        super().__init__()

        self.placement = 'any'
        self.color = 'java'
        self.type = 'square'
        self.path = path

        # metadata from name
        metadata = os.path.splitext(os.path.basename(path))[0]
        metadata = [i.strip() for i in metadata.split(',')]
        for m in metadata:
            k, v = m.split('=')
            setattr(self, k.lower(), v.lower())

        self.image = Gtk.Image.new_from_file(path)
        self.set_child(self.image)


@Gtk.Template.from_resource('/org/endlessos/avatarCreator/main_window.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AvatarCreatorWindow'

    headerbar = Gtk.Template.Child()
    grid = Gtk.Template.Child()
    modules = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(300, 500)
        self.set_titlebar(self.headerbar)
        self.custom_css()

        self._modules_groups = {}
        self.populate_modules(DEFAULT_VARIANT)

    def custom_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/org/endlessos/avatarCreator/avatar-creator.css")

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def populate_modules(self, variant):
        assets = os.path.join(config.DATA_DIR, 'assets', variant)
        groups = os.listdir(assets)
        for group in groups:
            group_path = os.path.join(assets, group)
            images = os.listdir(group_path)
            images = [ModuleImage(os.path.join(group_path, i)) for i in images]
            self._modules_groups[group] = images

        # TODO: Add widgets grouped in a stack
        for g, images in self._modules_groups.items():
            for img in images:
                img.connect('clicked', self._on_module_image_clicked)
                self.modules.insert(img, 0)

    def _on_module_image_clicked(self, widget):
        self.grid.set(widget.path)
