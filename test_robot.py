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

        gallery = 'https://www.imagefap.com/pictures/9157754/The-Simpson%27s-Merry-Christmas'

        name = utilities.getGalleryName(gallery)

        self.assertEqual("The-Simpson's-Merry-Christmas", name)

    def test_cleanURL(self):
        list = [
            ('https://www.imagefap.com/pictures/8320839/Brittany-Bardot-gets-Rachels-fist-up-her-bum',
             'https://www.imagefap.com/pictures/8320839/Brittany-Bardot-gets-Rachels-fist-up-her-bum'),
            ("https://www.imagefap.com/photo/683150892/?pgid=&gid=8021417&page=0&idx=18",
             "https://www.imagefap.com/photo/683150892/"),
            ('https://www.imagefap.com/photo/872088544/?pgid=&gid=8068100&page=0&idx=2',
             'https://www.imagefap.com/photo/872088544/')
        ]

        for tuple in list:
            cleaned = utilities.getCleanURL(tuple[0])
            self.assertEqual(cleaned, tuple[1])

if __name__ == '__main__':
    unittest.main()
