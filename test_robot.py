import unittest
import utilities


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
                     ('https://www.imagefap.com/pictures/9171882/Nathalie-la-petite-hotesse.-French-comic-%2F-BD', "Nathalie-la-petite-hotesse.-French-comic-_-BD")]

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


if __name__ == '__main__':
    unittest.main()
