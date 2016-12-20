# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.


import unittest


from stixmarker import api


class AddMarkingTests(unittest.TestCase):

    def test_add_markings_one_marking(self):
        before = {
            "title": "test title",
            "description": "test description"
        }

        after = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1"]
        }

        api.add_markings(before, None, "marking-definition--1")

        self.assertEqual(before, after)

    def test_add_markings_multiple_marking(self):
        before = {
            "title": "test title",
            "description": "test description"
        }

        after = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2"]
        }

        api.add_markings(before, None, ["marking-definition--1", "marking-definition--2"])

        for m in before["object_marking_refs"]:
            self.assertTrue(m in after["object_marking_refs"])

    def test_add_markings_combination(self):
        before = {
            "title": "test title",
            "description": "test description"
        }

        after = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2"],
            "granular_markings": [
                {
                    "selectors": ["title"],
                    "marking_ref": "marking-definition--3"
                },
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--4"
                },
            ]
        }

        api.add_markings(before, None, "marking-definition--1")
        api.add_markings(before, None, "marking-definition--2")
        api.add_markings(before, "title", "marking-definition--3")
        api.add_markings(before, "description", "marking-definition--4")

        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

        for m in before["object_marking_refs"]:
            self.assertTrue(m in after["object_marking_refs"])

    def test_add_markings_bad_markings(self):
        before = {
            "title": "test title",
            "description": "test description"
        }

        self.assertRaises(AssertionError, api.add_markings, before, None, [""])
        self.assertRaises(AssertionError, api.add_markings, before, None, "")
        self.assertRaises(AssertionError, api.add_markings, before, None, [])
        self.assertRaises(AssertionError, api.add_markings, before, None, ["marking-definition--1", 456])

        self.assertTrue("object_marking_refs" not in before)


class GetMarkingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_tlo = \
            {
                "a": 333,
                "b": "value",
                "c": [
                    17,
                    "list value",
                    {
                        "g": "nested",
                        "h": 45
                    }
                ],
                "x": {
                    "y": [
                        "hello",
                        88
                    ],
                    "z": {
                        "foo1": "bar",
                        "foo2": 65
                    }
                },
                "object_marking_refs": ["11"],
                "granular_markings": [
                    {
                        "marking_ref": "1",
                        "selectors": ["a"]
                    },
                    {
                        "marking_ref": "2",
                        "selectors": ["c"]
                    },
                    {
                        "marking_ref": "3",
                        "selectors": ["c.[1]"]
                    },
                    {
                        "marking_ref": "4",
                        "selectors": ["c.[2]"]
                    },
                    {
                        "marking_ref": "5",
                        "selectors": ["c.[2].g"]
                    },
                    {
                        "marking_ref": "6",
                        "selectors": ["x"]
                    },
                    {
                        "marking_ref": "7",
                        "selectors": ["x.y"]
                    },
                    {
                        "marking_ref": "8",
                        "selectors": ["x.y.[1]"]
                    },
                    {
                        "marking_ref": "9",
                        "selectors": ["x.z"]
                    },
                    {
                        "marking_ref": "10",
                        "selectors": ["x.z.foo2"]
                    },
                ]
            }

    def test_get_markings_object_marking(self):
        self.assertEqual(set(api.get_markings(self.test_tlo, None)), set(["11"]))

    def test_get_markings_object_and_granular_combinations(self):
        """Test multiple combinations for inherited and descendant markings."""
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", False, False)), set(["1"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", True, False)), set(["1", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", True, True)), set(["1", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", False, True)), set(["1"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "b", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", True, False)), set(["11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", True, True)), set(["11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c", False, False)), set(["2"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", True, False)), set(["2", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", True, True)), set(["2", "3", "4", "5", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", False, True)), set(["2", "3", "4", "5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", True, False)), set(["2", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", True, True)), set(["2", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", False, False)), set(["3"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", True, False)), set(["2", "3", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", True, True)), set(["2", "3", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", False, True)), set(["3"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", False, False)), set(["4"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", True, False)), set(["2", "4", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", True, True)), set(["2", "4", "5", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", False, True)), set(["4", "5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", False, False)), set(["5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", True, False)), set(["2", "4", "5", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", True, True)), set(["2", "4", "5", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", False, True)), set(["5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x", False, False)), set(["6"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", True, False)), set(["6", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", True, True)), set(["6", "7", "8", "9", "10", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", False, True)), set(["6", "7", "8", "9", "10"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", False, False)), set(["7"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", True, False)), set(["6", "7", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", True, True)), set(["6", "7", "8", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", False, True)), set(["7", "8"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", True, False)), set(["6", "7", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", True, True)), set(["6", "7", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", False, False)), set(["8"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", True, False)), set(["6", "7", "8", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", True, True)), set(["6", "7", "8", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", False, True)), set(["8"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", False, False)), set(["9"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", True, False)), set(["6", "9", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", True, True)), set(["6", "9", "10", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", False, True)), set(["9", "10"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", True, False)), set(["6", "9", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", True, True)), set(["6", "9", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", False, False)), set(["10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", True, False)), set(["6", "9", "10", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", True, True)), set(["6", "9", "10", "11"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", False, True)), set(["10"]))


class RemoveMarkingTests(unittest.TestCase):

    def test_remove_markings_object_level(self):
        after = {
            "title": "test title",
            "description": "test description"
        }

        before = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1"]
        }

        api.remove_markings(before, None, "marking-definition--1")

        self.assertEqual(before, after)

    def test_remove_markings_multiple(self):
        after = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--2"]
        }

        before = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2", "marking-definition--3"]
        }

        api.remove_markings(before, None, ["marking-definition--1", "marking-definition--3"])

        self.assertEqual(before, after)

    def test_remove_markings_bad_markings(self):
        before = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2", "marking-definition--3"]
        }

        self.assertRaises(AssertionError, api.remove_markings, before, None, ["marking-definition--5"])


class ClearMarkingTests(unittest.TestCase):

    def test_clear_markings(self):
        after = {
            "title": "test title",
            "description": "test description"
        }

        before = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2", "marking-definition--3"]
        }

        api.clear_markings(before, None)

        self.assertTrue(before, after)


class IsMarkedMarkingTests(unittest.TestCase):

    def test_is_marked_object_and_granular_combinations(self):
        """Test multiple combinations for inherited and descendant markings."""
        test_tlo = \
            {
                "a": 333,
                "b": "value",
                "c": [
                    17,
                    "list value",
                    {
                        "g": "nested",
                        "h": 45
                    }
                ],
                "x": {
                    "y": [
                        "hello",
                        88
                    ],
                    "z": {
                        "foo1": "bar",
                        "foo2": 65
                    }
                },
                "object_marking_refs": "11",
                "granular_markings": [
                    {
                        "marking_ref": "1",
                        "selectors": ["a"]
                    },
                    {
                        "marking_ref": "2",
                        "selectors": ["c"]
                    },
                    {
                        "marking_ref": "3",
                        "selectors": ["c.[1]"]
                    },
                    {
                        "marking_ref": "4",
                        "selectors": ["c.[2]"]
                    },
                    {
                        "marking_ref": "5",
                        "selectors": ["c.[2].g"]
                    },
                    {
                        "marking_ref": "6",
                        "selectors": ["x"]
                    },
                    {
                        "marking_ref": "7",
                        "selectors": ["x.y"]
                    },
                    {
                        "marking_ref": "8",
                        "selectors": ["x.y.[1]"]
                    },
                    {
                        "marking_ref": "9",
                        "selectors": ["x.z"]
                    },
                    {
                        "marking_ref": "10",
                        "selectors": ["x.z.foo2"]
                    },
                ]
            }

        self.assertTrue(api.is_marked(test_tlo, "a", ["1"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "a", ["1", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "a", ["1", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "a", ["1"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "b", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "b", ["11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "b", ["11"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "b", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "c", ["2"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2", "3", "4", "5", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2", "3", "4", "5"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "c.[0]", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "c.[0]", ["2", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[0]", ["2", "11"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "c.[0]", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["3"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["2", "3", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["2", "3", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["3"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["4"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["2", "4", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["2", "4", "5", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["4", "5"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["5"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["2", "4", "5", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["2", "4", "5", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["5"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x", ["6"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6", "7", "8", "9", "10", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6", "7", "8", "9", "10"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x.y", ["7"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["6", "7", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["6", "7", "8", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["7", "8"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "x.y.[0]", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[0]", ["6", "7", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[0]", ["6", "7", "11"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "x.y.[0]", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["8"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["6", "7", "8", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["6", "7", "8", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["8"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x.z", ["9"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["6", "9", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["6", "9", "10", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["9", "10"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "x.z.foo1", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo1", ["6", "9", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo1", ["6", "9", "11"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "x.z.foo1", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["10"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["6", "9", "10", "11"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["6", "9", "10", "11"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["10"], False, True))


class SetMarkingTests(unittest.TestCase):

    def test_set_marking(self):
        before = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--1", "marking-definition--2", "marking-definition--3"]
        }
        after = {
            "title": "test title",
            "description": "test description",
            "object_marking_refs": ["marking-definition--7", "marking-definition--9"]
        }

        api.set_markings(before, None, ["marking-definition--7", "marking-definition--9"])

        for m in before["object_marking_refs"]:
            self.assertTrue(m in ["marking-definition--7", "marking-definition--9"])

        self.assertTrue(["marking-definition--1", "marking-definition--2", "marking-definition--3"] not in before["object_marking_refs"])

        for x in before["object_marking_refs"]:
            self.assertTrue(x in after["object_marking_refs"])

    def test_set_marking_bad_input(self):
        before = {
            "description": "test description",
            "title": "foo",
            "object_marking_refs": ["marking-definition--1"]
        }

        after = {
            "description": "test description",
            "title": "foo",
            "object_marking_refs": ["marking-definition--1"]
        }

        self.assertRaises(AssertionError, api.set_markings, before, None, [])
        self.assertRaises(AssertionError, api.set_markings, before, None, [""])
        self.assertRaises(AssertionError, api.set_markings, before, None, "")
        self.assertRaises(AssertionError, api.set_markings, before, None, ["marking-definition--7", 687])
        self.assertEqual(before, after)
