import unittest

'''
Description: An implementation of a dictionary in Python
Author: Andrew Peña
Version: 1
Help provided to: Kelly Trujillo, Stuart Griffin, Ze Liu
Help received from: Stack Exchange
'''

'''
    Implement a dictionary using chaining.
    You may assume every key has a hash() method, e.g.:
    >>> hash(1)
    1
    >>> hash('hello world')
    -2324238377118044897
'''


class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        if init:
            while len(init) > self.__limit * 0.75:
                self.__limit *= 2
        self.build_dict(self.__limit, init)

    def max_length(self):
        return self.__limit

    def __len__(self):
        return self.__count

    def flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return iter(self.flattened())

    def __str__(self):
        return str(self.flattened())

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for self_item, other_item in zip(self.items(), other.items()):
            if self_item != other_item:
                return False
        return True

    def __setitem__(self, key, value):
        spot = self.find_spot(key)
        for pair in self.__items[spot]:
            if pair[0] == key:
                pair[1] = value
                return
        self.__items[spot].append([key, value])
        self.__count += 1
        if self.__count > self.__limit * 0.75:
            self.double_size()

    def __getitem__(self, key):
        spot = self.find_spot(key)
        for first, second in self.__items[spot]:
            if first == key:
                return second
        raise RuntimeError

    def __delitem__(self, key):
        if key not in self:
            raise RuntimeError
        spot = self.find_spot(key)
        self.__items[spot] = [pair for pair in self.__items[spot] if pair[0] != key]
        self.__count -= 1
        if self.__limit > 10 and self.__count < self.__limit * 0.25:
            self.halve_size()

    def build_dict(self, size, initial=None):
        self.__items = [[] for _ in range(size)]
        self.__count = 0

        if initial:
            for i in initial:
                self.__setitem__(i[0], i[1])

    def __contains__(self, key):
        spot = self.find_spot(key)
        for pair in self.__items[spot]:
            if pair[0] == key:
                return True
        return False

    def find_spot(self, key):
        return hash(key) % self.__limit

    def double_size(self):
        new = self.flattened()
        self.__limit *= 2
        self.build_dict(self.__limit, new)

    def halve_size(self):
        new = self.flattened()
        self.__limit //= 2
        self.build_dict(self.__limit, new)

    def keys(self):
        return [pair[0] for inner in self.__items for pair in inner]

    def values(self):
        return [pair[1] for inner in self.__items for pair in inner]

    def items(self):
        return [(pair[0], pair[1]) for inner in self.__items for pair in inner]


''' C-level work '''


class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")


class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")


class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertFalse(s[1])


class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)


class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)


class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)


class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)


''' B-level work
'''


class test_init(unittest.TestCase):
    def test(self):
        test_list = [[1, "one"], [2, "two"], [3, "three"]]
        s = dictionary(test_list)
        self.assertEqual(len(s), 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)


class test_resize(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"], [4, "four"],
                        [10, "ten"], [15, "fifteen"], [19, "nineteen"]])
        self.assertEqual(len(s), 7)
        self.assertEqual(s.max_length(), 10)
        s[5] = "five"
        self.assertEqual(len(s), 8)
        self.assertEqual(s.max_length(), 20)
        self.assertTrue(5 in s)


class test_init_rehash(unittest.TestCase):
    def test(self):
        init_list = [[1, "one"], [2, "two"], [3, "three"], [4, "four"], [5, "five"],
                     [6, "six"], [7, "seven"], [8, "eight"], [9, "nine"], [10, "ten"]]
        s = dictionary(init_list)
        self.assertEqual(s.max_length(), 20)
        self.assertEqual(len(s), 10)
        self.assertTrue(9 in s)


class test_delete_not_found(unittest.TestCase):
    def test(self):
        s = dictionary()
        self.assertRaises(RuntimeError, lambda: s.__delitem__(1))


class test_delete(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"], [4,"four"], [10, "ten"], [14, "fourteen"], [19, "nineteen"]])
        self.assertTrue(4 in s)
        self.assertTrue(14 in s)
        s.__delitem__(4)
        self.assertFalse(4 in s)
        self.assertTrue(14 in s)


''' A-level work
'''


class test_del_rehash(unittest.TestCase):
    def test(self):
        init_list = [[1, "one"], [2, "two"], [3, "three"], [4, "four"], [5, "five"],
                     [6, "six"], [7, "seven"], [8, "eight"], [9, "nine"], [10, "ten"]]
        s = dictionary(init_list)
        s.__delitem__(10)
        s.__delitem__(9)
        s.__delitem__(8)
        self.assertEqual(s.max_length(), 20)
        s.__delitem__(7)
        s.__delitem__(6)
        s.__delitem__(5)
        self.assertEqual(s.max_length(), 10)


class test_keys(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"]])
        self.assertEqual(s.keys(), [1, 2, 3])


class test_empty_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        self.assertEqual(s.keys(), [])


class test_values(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"]])
        self.assertEqual(s.values(), ['one', 'two', 'three'])


class test_empty_values(unittest.TestCase):
    def test(self):
        s = dictionary()
        self.assertEqual(s.values(), [])

''' Extra credit
'''

class test_items(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"]])
        self.assertEqual(s.items(), [(1, 'one'), (2, 'two'), (3, 'three')])


class test_empty_items(unittest.TestCase):
    def test(self):
        s = dictionary()
        self.assertEqual(s.items(), [])


class test_eq(unittest.TestCase):
    def test(self):
        s = dictionary([[1, "one"], [2, "two"], [3, "three"]])
        t = dictionary()
        self.assertFalse(s == t)
        t[1] = "one"
        t[2] = "two"
        t[3] = "three"
        self.assertTrue(s == t)
        s[1] = "won"
        self.assertFalse(s == t)


if __name__ == '__main__':
    unittest.main()