
import unittest
from src.base.Node import Node
from src.base.Street import Street



class StreetTest(unittest.TestCase):
    def test_getAngle1(self):
        node1 = Node(0, 47.356575, 8.540188) #Zurich
        node2 = Node(0, 47.933899, 8.479763) #Donaueschwingen
        street = Street()
        street.nodes.append(node1)
        street.nodes.append(node2)
        angle = street.getAngle()
        diff = angle - 1.46581443147
        if(diff < 0): diff *= -1
        self.assertLess(diff, 0.1)

    def test_getAngle2(self):
        node1 = Node(0, 47.356575, 8.540188) #Zurich
        node2 = Node(0, 47.378898, 8.141934) #Aarau
        street = Street()
        street.nodes.append(node1)
        street.nodes.append(node2)
        angle = street.getAngle()
        diff = angle - 0.0556
        if(diff < 0): diff *= -1
        self.assertLess(diff, 0.1)

    def test_getAngle3(self):
        node1 = Node(0, 47.181874, 8.490140) #Zug
        node2 = Node(0, 47.041177, 8.556022) #Arth
        street = Street()
        street.nodes.append(node1)
        street.nodes.append(node2)
        angle = street.getAngle()
        diff = angle - -1.13028096328
        if(diff < 0): diff *= -1
        self.assertLess(diff, 0.1)


