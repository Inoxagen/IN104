import unittest
from ..utils.vector import Vector2
from ..graphics.camera import Camera


class CameraTestCase(unittest.TestCase):
    def test_position1(self):
        camera = Camera(Vector2(100, 100))

        screen_coord = camera.to_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), 50)
        self.assertEqual(screen_coord.get_y(), 50)

    def test_position2(self):
        camera = Camera(Vector2(100, 100))

        screen_coord = camera.to_screen_coords(Vector2(50, 50))
        self.assertEqual(screen_coord.get_x(), 100)
        self.assertEqual(screen_coord.get_y(), 100)

    def test_position3(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(100, 100)

        screen_coord = camera.to_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), -50)
        self.assertEqual(screen_coord.get_y(), -50)

    def test_position4(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(-100, -100)

        screen_coord = camera.to_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), 150)
        self.assertEqual(screen_coord.get_y(), 150)

    def test_scale1(self):
        camera = Camera(Vector2(100, 100))
        camera.scale = 2

        screen_coord = camera.to_screen_coords(Vector2(50, 50))
        self.assertEqual(screen_coord.get_x(), 150)
        self.assertEqual(screen_coord.get_y(), 150)

    def test_scale2(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(100, 100)
        camera.scale = 2

        screen_coord = camera.to_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), -150)
        self.assertEqual(screen_coord.get_y(), -150)

    def test_scale3(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(-100, -100)
        camera.scale = 2

        screen_coord = camera.to_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), 250)
        self.assertEqual(screen_coord.get_y(), 250)

    def test_position_from_1(self):
        camera = Camera(Vector2(100, 100))

        screen_coord = camera.from_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), -50)
        self.assertEqual(screen_coord.get_y(), -50)

    def test_position_from_2(self):
        camera = Camera(Vector2(100, 100))

        screen_coord = camera.to_screen_coords(Vector2(50, 50))
        self.assertEqual(screen_coord.get_x(), 100)
        self.assertEqual(screen_coord.get_y(), 100)

    def test_position_from_3(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(100, 100)

        screen_coord = camera.from_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), 50)
        self.assertEqual(screen_coord.get_y(), 50)

    def test_position_from_4(self):
        camera = Camera(Vector2(100, 100))
        camera.position = Vector2(-100, -100)

        screen_coord = camera.from_screen_coords(Vector2(0, 0))
        self.assertEqual(screen_coord.get_x(), -150)
        self.assertEqual(screen_coord.get_y(), -150)