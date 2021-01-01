import unittest
import utilities
import configData


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

 # Returns True if the string is in upper case.
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_fail(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_galleryName(self):

        galleries = [('https://www.imagefap.com/pictures/9157754/The-Simpson%27s-Merry-Christmas', "The-Simpson's-Merry-Christmas"),
                     ('https://www.imagefap.com/pictures/9171882/Nathalie-la-petite-hotesse.-French-comic-%2F-BD', "Nathalie-la-petite-hotesse.-French-comic-/-BD")]

        for tuple in galleries:
            cleaned = utilities.getGalleryNameFromURL(tuple[0])
            self.assertEqual(cleaned, tuple[1])

    def test_cleanURL(self):
        testlist = [
            ('https://www.imagefap.com/pictures/8320839/Brittany-Bardot-gets-Rachels-fist-up-her-bum',
             'https://www.imagefap.com/pictures/8320839/Brittany-Bardot-gets-Rachels-fist-up-her-bum'),
            ("https://www.imagefap.com/photo/683150892/?pgid=&gid=8021417&page=0&idx=18",
             "https://www.imagefap.com/photo/683150892/"),
            ('https://www.imagefap.com/photo/872088544/?pgid=&gid=8068100&page=0&idx=2',
             'https://www.imagefap.com/photo/872088544/')
        ]

        for tuple in testlist:
            cleaned = utilities.getCleanURL(tuple[0])
            self.assertEqual(cleaned, tuple[1])

    def test_generatePicStr(self):
        testlist = [
            (2,   'pic_{:01d}'),
            (20,  'pic_{:02d}'),
            (200, 'pic_{:03d}'),
            (56,  'pic_{:02d}'),
            (99,  'pic_{:02d}'),
            (100, 'pic_{:03d}'),
            (101, 'pic_{:03d}'),
            (1041,'pic_{:04d}')
        ]

        for tuple in testlist:
            outStr = configData.generatePicStr(tuple[0])
            self.assertEqual(outStr, tuple[1], "size: {}".format(tuple[0]))


if __name__ == '__main__':
    unittest.main()
