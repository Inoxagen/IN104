from ..utils.vector import Vector2


class ICamera:
    def __init__(self, screen_size,id_ref=-1):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1
        self.id_ref=id_ref

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        raise NotImplementedError

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        raise NotImplementedError


class Camera(ICamera):

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        return self.scale*(position - self.position) + 1/2 *self.screen_size

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        return 1/self.scale*(position - 1/2 *self.screen_size) + self.position

