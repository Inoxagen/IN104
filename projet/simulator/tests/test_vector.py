from ..utils.vector import Vector
import unittest


class VectorTestCase(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(2)
        self.v1[0] = 5
        self.v1[1] = 3

        self.v2 = Vector(2)
        self.v2[0] = -2
        self.v2[1] = 39

    def test_neg(self):
        v = -self.v1

        self.assertEqual(v[0], -5)
        self.assertEqual(v[1], -3)

    def test_add(self):
        v = self.v1 + self.v2

        self.assertEqual(v[0], 3)
        self.assertEqual(v[1], 42)

    def test_sub(self):
        v = self.v1 - self.v2

        self.assertEqual(v[0], 7)
        self.assertEqual(v[1], -36)

    def test_mul_int(self):
        v = self.v1 * 2

        self.assertEqual(v[0], 10)
        self.assertEqual(v[1], 6)

    def test_mul_float(self):
        v = self.v1 * 2.0

        self.assertEqual(v[0], 10)
        self.assertEqual(v[1], 6)

    def test_copy(self):
        #Vecteurs identiques mais adresses différentes (palie au problème d'étiquette)
        V=Vector(20)
        V_=V.copy()
        self.assertNotEqual(V,V_)