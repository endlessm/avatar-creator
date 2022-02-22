import math
import cairo
import gi
gi.require_version('Rsvg', '2.0')

from gi.repository import Gtk, Rsvg


class GridImage:
    def __init__(self):
        self.rotation = 0
        self.hmirror = False
        self.vmirror = False
        self.accent_color = None
        self.path = None


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
        self._grid = [[GridImage() for _ in range(3)] for _ in range(3)]

    @property
    def selected_grid_image(self):
        if not self.selected_widget:
            return None

        _, (r, c) = self.selected_widget.get_name().split('_')
        return self._grid[int(r)][int(c)]

    @property
    def selected_image(self):
        if not self.selected_widget:
            return None

        _, pos = self.selected_widget.props.name.split('_')
        return getattr(self, f'image_{pos}')

    @Gtk.Template.Callback()
    def _on_select_grid(self, widget):

        self.selected_widget = widget

        for r in range(3):
            for c in range(3):
                w = getattr(self, f'grid_{r}{c}')
                w.get_style_context().remove_class('selected')

        widget.get_style_context().add_class('selected')

    def set(self, path):
        if not self.selected_widget:
            return

        self.selected_grid_image.path = path
        self.selected_image.set_from_file(path)

    def rotate(self):
        if not self.selected_widget:
            return

        angle = self.selected_grid_image.rotation
        angle = (angle + 90) % 360
        self.selected_grid_image.rotation = angle
        ctx = self.selected_image.get_style_context()
        ctx.remove_class('rotate-90')
        ctx.remove_class('rotate-180')
        ctx.remove_class('rotate-270')

        if angle:
            ctx.add_class(f'rotate-{angle}')

    def export_to_png(self, path, size=256):
        w3 = size / 3
        surface = cairo.ImageSurface(cairo.Format.ARGB32, size, size)
        cr = cairo.Context(surface)
        rect = Rsvg.Rectangle()
        rect.width = w3
        rect.height = w3

        for r in range(3):
            for c in range(3):
                grid_image = self._grid[r][c]
                rect.x = c * w3
                rect.y = r * w3
                if grid_image.path:
                    handle = Rsvg.Handle.new_from_file(grid_image.path)
                    # cr.rotate(grid_image.rotation * math.pi / 180)
                    handle.render_document(cr, rect)

        surface.write_to_png(path)
