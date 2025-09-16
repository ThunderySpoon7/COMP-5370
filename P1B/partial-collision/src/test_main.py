import unittest
import main

class TestMainModule(unittest.TestCase):
    def test_get_random_suffixes_1(self):
        s1, s2 = main.get_random_suffixes()
        self.assertTrue(isinstance(s1, bytes))
        self.assertTrue(isinstance(s2, bytes))

    def test_get_random_suffixes_2(self):
        s1, s2 = main.get_random_suffixes()
        self.assertTrue(len(s1) == main.SUFFIX_LENGTH)
        self.assertTrue(len(s2) == main.SUFFIX_LENGTH)

    def test_check_partial_collision(self):
        self.assertTrue(main.check_partial_collision("asdfasdf1234", "lkajsdfkjsdflkj1234"))    

    def test_write_to_file(self):
        main.write_to_file("test.txt", "test test")

if __name__ == "__main__":
    unittest.main()