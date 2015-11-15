from src.detection.BoxWalker import BoxWalker
import unittest
from src.base.Bbox import Bbox
from src.base.TileDrawer import TileDrawer




class testBoxWalker(unittest.TestCase):
    def test_load_tile(self):
        walker = BoxWalker(self.smallTestBbox(), False)
        walker.load_tiles()
        self.assertIsNotNone(walker.tile)

    def test_load_streets(self):
        walker = BoxWalker(self.smallTestBbox(), False)
        walker.load_streets()
        self.assertIsNotNone(walker.streets)

    def test_walk(self):
        walker = BoxWalker(self.smallTestBbox2(), False)
        walker.load_convnet()
        walker.load_tiles()
        walker.load_streets()

        crosswalkNodes = walker.walk()
        self.assertIsNotNone(crosswalkNodes)
        self.assertGreater(len(crosswalkNodes), 0)


    def test_walk_with_show(self):
        walker = BoxWalker(self.ZurichUhuereGross3())
        walker.load_convnet()
        walker.load_tiles()
        walker.load_streets()

        crosswalkNodes = walker.walk()

        self.printResults(walker.tile, crosswalkNodes)

    def printResults(self, tile, crosswalkNodes):
        drawer = TileDrawer.from_tile(tile)
        for node in crosswalkNodes:
            drawer.draw_point(node)
        drawer.drawsection.save("boxsave.jpg")
        drawer.drawsection.show()

    def smallTestBbox(self):
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)

    def smallTestBbox2(self):
        return Bbox.from_bltr(47.226327, 8.818031, 47.227014, 8.818868)

    def ZurichBellvue(self):
        #Trainset
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Rappi(self):

        return Bbox.from_lbrt(8.814650, 47.222553, 8.825035, 47.228935)

    def Luzern(self):
        return Bbox.from_lbrt(8.301307, 47.046349, 8.305528, 47.051053)

    def BernAltStadt(self):
        #TrainSet
        return Bbox.from_lbrt(7.444389, 46.947913, 7.448316, 46.949693)

    def ChurBhfAltstadt(self):
        #TrainSet
        return Bbox.from_lbrt(9.528281, 46.850342, 9.532599, 46.853980)

    def Zurich2(self):
        #Trainset
        return Bbox.from_lbrt(8.530470, 47.366188, 8.537807, 47.372053)

    def BernKoeniz(self):
        return Bbox.from_lbrt(7.406960, 46.920077, 7.415008, 46.924285)

    def Lausanne(self):
        return Bbox.from_lbrt(6.555186, 46.508591, 6.563499, 46.516437)

    def Lyss(self):
        #Trainset
        return Bbox.from_lbrt(7.304337, 47.072818, 7.308200, 47.075229)

    def zh1(self):
        return Bbox.from_lbrt(8.522537, 47.375915, 8.526331, 47.376639)

    def zh_schlieren_test(self):
        return Bbox.from_lbrt(8.441207, 47.394649, 8.449643, 47.399710)

    def zh_hardbrucke_test(self):
        return Bbox.from_lbrt(8.517822, 47.386440, 8.520540, 47.388008)

    def zh_hardbrucke_test2(self):
        return Bbox.from_lbrt(8.521436, 47.390424, 8.524241, 47.391289)

    def zh_quartier1(self):
        return Bbox.from_lbrt(8.528067, 47.393102, 8.532648, 47.394939)

    def zh_europabrucke(self):
        return Bbox.from_lbrt(8.492554, 47.391842, 8.503230, 47.394553)

    def winti1(self):
        return Bbox.from_lbrt(8.716155, 47.511909, 8.721038, 47.515722)

    def winti_innenstadt(self):
        return Bbox.from_lbrt(8.723835, 47.497560, 8.733661, 47.501156)

    def thun_innenstadt(self):
        return Bbox.from_lbrt(7.624835, 46.758937, 7.630741, 46.762592)

    def heiligkreuz(self):
        return Bbox.from_lbrt(9.408957, 47.055055, 9.418505, 47.060288)

    def staefa(self):
        return Bbox.from_lbrt(8.729157, 47.233379, 8.741170, 47.238049)

    def zh_buchs(self):
        return  Bbox.from_lbrt(8.432206, 47.456906, 8.441375, 47.461262)

    def ag_baden(self):
        return Bbox.from_lbrt(8.308925, 47.464633, 8.317642, 47.467798)

    def ag_baden2(self):
        return Bbox.from_lbrt( 8.314834, 47.462698, 8.324612, 47.468880)

    def zh_frauental_quartier(self):
        return Bbox.from_lbrt(8.507748, 47.355263, 8.510934, 47.358226)

    def zh_quartier2(self):
        return Bbox.from_lbrt(8.520495, 47.369944, 8.523971, 47.372846)

    def RappiUhuereGross(self):
        return Bbox.from_lbrt(8.804742, 47.215446, 8.850833, 47.237799)

    def ZurichUhuereGross(self):
        return Bbox.from_lbrt(8.523379, 47.368823, 8.553379, 47.390823)

    def ZurichUhuereGross2(self):
        return Bbox.from_lbrt(8.523379, 47.368823, 8.573379, 47.390823)

    def ZurichUhuereGross3(self):
        return Bbox.from_bltr(47.372759, 8.473965, 47.399972, 8.510429)