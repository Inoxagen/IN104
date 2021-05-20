from .. import World, Body
from ..utils.vector import Vector2
import unittest
import random as rd

class WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_add(self):
        body = Body(Vector2(0, 0))
        id_ = self.world.add(body)

        body_ = self.world.get(id_)
        self.assertEqual(body, body_)

    def test_add_set(self):
        bodies = [Body(Vector2(0,0)),Body(Vector2(0,1)),Body(Vector2(1,0))]
        id_ = self.world.add_set(bodies)
        bodies_=[]
        for id_body in id_:
            body=self.world.get(id_body)
            bodies_.append(body)
        self.assertEqual(bodies,bodies_)

    def test_add_multiple(self):
        body1 = Body(Vector2(0, 0))
        body2 = Body(Vector2(0, 0))
        body3 = Body(Vector2(0, 0))

        id1 = self.world.add(body1)
        id2 = self.world.add(body2)
        id3 = self.world.add(body3)

        body1_ = self.world.get(id1)
        self.assertEqual(body1, body1_)

        body2_ = self.world.get(id2)
        self.assertEqual(body2, body2_)

        body3_ = self.world.get(id3)
        self.assertEqual(body3, body3_)

    def test_add_N_corps_aleat_diff(self):
        nb_corps=rd.randint(2,10)
        self.world.add_N_corps_aleat_diff(nb_corps)
        self.assertEqual(len(self.world),nb_corps)

        list_pos=[]
        for body in self.world._bodies:
            self.assertFalse(body.position in list_pos)
            list_pos.append(body.position)


    def test_pop(self):
        body = [Body(Vector2(0,0)),Body(Vector2(0,1)),Body(Vector2(1,0))]
        self.world.add_set(body)
        l=len(self.world._bodies)
        world_=self.world.pop(1)
        l_=len(self.world._bodies)
        self.assertEqual(l-1,l_)

    def test_clear_all(self):
        self.world.clear_all()
        self.assertEqual(len(self.world),0)

    def test_clear_all_seuil(self):
        self.world.clear_all(2)
        self.assertEqual(self.world.seuil_collision,2)

    def test_clear_all_bg_color(self):
        self.world.clear_all(-1,(246,141,15))
        self.assertEqual(self.world.bg_color,(246,141,15))

    def test_get_none(self):
        body = self.world.get(3714)
        self.assertIsNone(body)
