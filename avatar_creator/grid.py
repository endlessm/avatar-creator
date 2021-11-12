from gi.repository import Gtk


@Gtk.Template.from_resource('/org/endlessos/avatarCreator/grid.ui')
class Grid(Gtk.Grid):
    __gtype_name__ = 'AvatarCreatorGrid'

    grid_00 = Gtk.Template.Child()
    grid_01 = Gtk.Template.Child()
    grid_02 = Gtk.Template.Child()

    grid_10 = Gtk.Template.Child()
    grid_11 = Gtk.Template.Child()
    grid_12 = Gtk.Template.Child()

    grid_20 = Gtk.Template.Child()
    grid_21 = Gtk.Template.Child()
    grid_22 = Gtk.Template.Child()

    image_00 = Gtk.Template.Child()
    image_01 = Gtk.Template.Child()
    image_02 = Gtk.Template.Child()

    image_10 = Gtk.Template.Child()
    image_11 = Gtk.Template.Child()
    image_12 = Gtk.Template.Child()

    image_20 = Gtk.Template.Child()
    image_21 = Gtk.Template.Child()
    image_22 = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_widget = None

    @Gtk.Template.Callback()
    def _on_select_grid(self, widget):

        self.selected_widget = widget

        for r in range(3):
            for c in range(3):
                w = getattr(self, f'grid_{r}{c}')
                w.get_style_context().remove_class('selected')

        widget.get_style_context().add_class('selected')
