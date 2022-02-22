import os
from gi.repository import Gtk, Gdk, GLib, Gio
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

        self.get_style_context().add_class('module-image')


@Gtk.Template.from_resource('/org/endlessos/avatarCreator/main_window.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AvatarCreatorWindow'

    headerbar = Gtk.Template.Child()
    grid = Gtk.Template.Child()
    modules = Gtk.Template.Child()
    scrolled_window = Gtk.Template.Child()
    button_box = Gtk.Template.Child()
    filter_box = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(300, 500)
        self.set_titlebar(self.headerbar)
        self.custom_css()

        self._all_colors = set()
        self._all_types = set()
        self._all_placements = set()

        self._modules_groups = {}
        self.filters = {}
        self.flowboxes = []
        self.populate_modules(DEFAULT_VARIANT)
        self.populate_filters()

    @Gtk.Template.Callback()
    def on_rotate(self, *args):
        self.grid.rotate()

    @Gtk.Template.Callback()
    def on_hmirror(self, *args):
        print("Horizontal Mirror")

    @Gtk.Template.Callback()
    def on_vmirror(self, *args):
        print("Vertical Mirror")

    def custom_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/org/endlessos/avatarCreator/avatar-creator.css")

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def populate_modules(self, variant):
        assets = os.path.join(config.DATA_DIR, 'assets', variant)
        groups = os.listdir(assets)
        modules_groups = {}
        for group in groups:
            group_path = os.path.join(assets, group)
            images = os.listdir(group_path)
            images = [ModuleImage(os.path.join(group_path, i)) for i in images]
            self._modules_groups[group] = images

        for g, images in self._modules_groups.items():
            flowbox = Gtk.FlowBox()
            flowbox.set_filter_func(self._modules_filter)
            label = Gtk.Label()
            label.set_markup(f'<b>{g}</b>')
            label.set_xalign(0.0)

            self.modules.append(label)
            self.modules.append(flowbox)
            self.flowboxes.append(flowbox)

            # Buttons
            group_button = Gtk.Button(label=g)
            group_button.connect('clicked', self.scroll_to_group, label)
            self.button_box.append(group_button)

            for i, img in enumerate(images):
                img.connect('clicked', self._on_module_image_clicked)
                flowbox.insert(img, i)
                self._all_colors.add(img.color)
                self._all_types.add(img.type)
                self._all_placements.add(img.placement)

    def _invalidate_filter(self, widget, data):
        for f in self.flowboxes:
            f.invalidate_filter()

    def populate_filters(self):
        color = Gtk.DropDown.new_from_strings(['Color'] + list(self._all_colors))
        color.connect('notify::selected-item', self._invalidate_filter)
        self.filters['color'] = color

        typef = Gtk.DropDown.new_from_strings(['Type'] + list(self._all_types))
        typef.connect('notify::selected-item', self._invalidate_filter)
        self.filters['type'] = typef

        placement = Gtk.DropDown.new_from_strings(['Placement'] + list(self._all_placements))
        placement.connect('notify::selected-item', self._invalidate_filter)
        self.filters['placement'] = placement

        self.filter_box.append(color)
        self.filter_box.append(typef)
        self.filter_box.append(placement)

    def _filter_by(self, child, filter_name, default):
        filter = self.filters[filter_name]
        value = filter.get_selected_item().get_string()
        if value != default:
            return getattr(child, filter_name) == value
        return True

    def _modules_filter(self, child):
        if not 'color' in self.filters:
            return True

        show = True
        object = child.get_child()
        show = show and self._filter_by(object, 'color', 'Color')
        show = show and self._filter_by(object, 'type', 'Type')
        show = show and self._filter_by(object, 'placement', 'Placement')

        return show

    def scroll_to_group(self, button, group):
        adj = self.scrolled_window.get_vadjustment()
        alloc = group.get_allocation()
        adj.set_value(alloc.y)

    def _on_module_image_clicked(self, widget):
        self.grid.set(widget.path)

    def on_save_menu_clicked(self, *args):
        # TODO: show export dialog? Maybe something to define the size and location
        dest_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOCUMENTS)

        # TODO: use native dialog?
        dialog = Gtk.FileChooserDialog(title='Save avatar',
                                       action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('_Save', Gtk.ResponseType.ACCEPT,
                           '_Cancel', Gtk.ResponseType.CANCEL)
        dialog.set_transient_for(self)
        dialog.set_modal(True)

        filter = Gtk.FileFilter()
        filter.set_name('Image')
        filter.add_pattern('*.png')
        dialog.set_filter(filter)
        dialog.set_current_folder(Gio.File.new_for_path(dest_dir))
        dialog.set_current_name('avatar.png')
        dialog.connect('response', self._on_save)
        dialog.show()

    def _on_save(self, widget, response):
        size = 256
        if response == Gtk.ResponseType.ACCEPT:
            path = widget.get_file().get_path()
            self.grid.export_to_png(path, size)

        widget.destroy()
