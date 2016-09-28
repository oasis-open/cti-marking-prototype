# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.


import unittest


from stixmarker import api


class AddMarkingTests(unittest.TestCase):
    # Smoke test add_marking does not fail
    # One selector multiple refs
    # Multiple selector, multiple refs
    # Multiple selectors, one ref
    # One selector, one ref
    # Verify granular_marking are added correctly
    # Assert bad selector
    # Assert good selector

    # Rich

    def test_add_marking_mark_one_selector_multiple_refs(self):
        before = {
            "description": "test description",
            "title": "foo",
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.add_markings(before, ["description"], ["marking-definition--1", "marking-definition--2"])

        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_add_marking_mark_multiple_selector_one_refs(self):
        before = {
            "description": "test description",
            "title": "foo",
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        api.add_markings(before, ["description", "title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_add_marking_mark_multiple_selector_multiple_refs(self):
        before = {
            "description": "test description",
            "title": "foo",
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.add_markings(before, ["description", "title"], ["marking-definition--1", "marking-definition--2"])

        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_add_marking_mark_another_property_same_marking(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        api.add_markings(before, ["title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_add_marking_mark_same_property_same_marking(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        api.add_markings(before, ["description"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_add_marking_bad_selector(self):
        before = {
            "description": "test description",
        }

        self.assertRaises(AssertionError, api.add_markings, before, ["title"], ["marking-definition--1", "marking-definition--2"])
        self.assertRaises(AssertionError, api.add_markings, before, "", ["marking-definition--1", "marking-definition--2"])
        self.assertRaises(AssertionError, api.add_markings, before, [], ["marking-definition--1", "marking-definition--2"])
        self.assertRaises(AssertionError, api.add_markings, before, [""], ["marking-definition--1", "marking-definition--2"])

        self.assertRaises(AssertionError, api.add_markings, before, ["description"], [""])
        self.assertRaises(AssertionError, api.add_markings, before, ["description"], "")
        self.assertRaises(AssertionError, api.add_markings, before, ["description"], [])
        self.assertRaises(AssertionError, api.add_markings, before, ["description"], ["marking-definition--1", 456])


class GetMarkingTests(unittest.TestCase):

    # Emmanuelle

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

    def test_get_markings_smoke(self):
        """Test get_markings does not fail."""
        self.assertTrue(len(api.get_markings(self.test_tlo, "a")) >= 1)

        self.assertTrue(api.get_markings(self.test_tlo, "a") == ["1"])

    def test_get_markings_not_marked(self):
        """Test selector that is not marked returns empty list."""
        results = api.get_markings(self.test_tlo, "b")
        self.assertTrue(len(results) == 0)

    def test_get_markings_multiple_selectors(self):
        """Test multiple selectors return combination of markings."""
        total = api.get_markings(self.test_tlo, ["x.y", "x.z"])
        xy_markings = api.get_markings(self.test_tlo, ["x.y"])
        xz_markings = api.get_markings(self.test_tlo, ["x.z"])

        self.assertTrue(set(xy_markings).issubset(total))
        self.assertTrue(set(xz_markings).issubset(total))
        self.assertTrue(set(xy_markings).union(xz_markings).issuperset(total))

    def test_get_markings_bad_selector(self):
        """Test bad selectors raise exception"""
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "foo")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, [])
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, [""])
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "x.z.[-2]")

        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "c.f")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "c.[2].i")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "c.[3]")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "d")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "x.[0]")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "x.y.w")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "x.z.[1]")
        self.assertRaises(AssertionError, api.get_markings, self.test_tlo, "x.z.foo3")

    def test_get_markings_positional_arguments_combinations(self):
        """Test multiple combinations for inherited and descendant markings."""
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", False, False)), set(["1"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", True, False)), set(["1"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", True, True)), set(["1"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "a", False, True)), set(["1"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "b", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", True, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", True, True)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "b", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c", False, False)), set(["2"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", True, False)), set(["2"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", True, True)), set(["2","3","4","5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c", False, True)), set(["2","3","4","5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", True, False)), set(["2"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", True, True)), set(["2"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[0]", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", False, False)), set(["3"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", True, False)), set(["2", "3"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", True, True)), set(["2", "3"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[1]", False, True)), set(["3"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", False, False)), set(["4"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", True, False)), set(["2", "4"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", True, True)), set(["2", "4", "5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2]", False, True)), set(["4", "5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", False, False)), set(["5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", True, False)), set(["2", "4", "5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", True, True)), set(["2", "4", "5"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "c.[2].g", False, True)), set(["5"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x", False, False)), set(["6"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", True, False)), set(["6"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", True, True)), set(["6", "7", "8", "9", "10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x", False, True)), set(["6", "7", "8", "9", "10"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", False, False)), set(["7"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", True, False)), set(["6", "7"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", True, True)), set(["6", "7", "8"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y", False, True)), set(["7", "8"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", True, False)), set(["6", "7"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", True, True)), set(["6", "7"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[0]", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", False, False)), set(["8"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", True, False)), set(["6", "7", "8"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", True, True)), set(["6", "7", "8"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.y.[1]", False, True)), set(["8"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", False, False)), set(["9"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", True, False)), set(["6", "9"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", True, True)), set(["6", "9", "10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z", False, True)), set(["9", "10"]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", False, False)), set([]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", True, False)), set(["6", "9"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", True, True)), set(["6", "9"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo1", False, True)), set([]))

        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", False, False)), set(["10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", True, False)), set(["6", "9", "10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", True, True)), set(["6", "9", "10"]))
        self.assertEqual(set(api.get_markings(self.test_tlo, "x.z.foo2", False, True)), set(["10"]))


class RemoveMarkingTests(unittest.TestCase):
    # Rich

    def test_remove_marking_remove_one_selector_with_multiple_refs(self):
        after = {
            "description": "test description",
            "title": "foo",
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.remove_markings(before, ["description"], ["marking-definition--1", "marking-definition--2"])
        self.assertEqual(before, after)

    def test_remove_marking_remove_multiple_selector_one_ref(self):
        after = {
            "description": "test description",
            "title": "foo",
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        api.remove_markings(before, ["description", "title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_remove_marking_mark_one_selector_from_multiple_ones(self):
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        api.remove_markings(before, ["title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_remove_marking_mark_one_selector_markings_from_multiple_ones(self):
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.remove_markings(before, ["title"], ["marking-definition--1"])

        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_remove_marking_mark_mutilple_selector_multiple_refs(self):
        after = {
            "description": "test description",
            "title": "foo",
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.remove_markings(before, ["description", "title"], ["marking-definition--1", "marking-definition--2"])
        self.assertEqual(before, after)

    def test_remove_marking_mark_another_property_same_marking(self):
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["title"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        api.remove_markings(before, ["title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_remove_marking_mark_same_property_same_marking(self):
        after = {
            "description": "test description",
            "title": "foo",
        }
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        api.remove_markings(before, ["description"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_remove_marking_bad_selector(self):
        before = {
            "description": "test description",
        }

        self.assertRaises(AssertionError, api.remove_markings, before, ["title"], ["marking-definition--1", "marking-definition--2"])


class IsMarkedTests(unittest.TestCase):

    # Emmanuelle

    @classmethod
    def setUpClass(cls):
        cls.test_tlo = \
            {
                "title": "test title",
                "description": "test description",
                "revision": 2,
                "type": "test",
                "granular_markings": [
                    {
                        "selectors": ["description"],
                        "marking_ref": "marking-definition--1"
                    },
                    {
                        "selectors": ["revision", "description"],
                        "marking_ref": "marking-definition--2"
                    },
                    {
                        "selectors": ["revision", "description"],
                        "marking_ref": "marking-definition--3"
                    },
                ]
            }

    def test_is_marked_smoke(self):
        """Smoke test is_marked call does not fail."""
        self.assertTrue(api.is_marked(self.test_tlo, ["description"]))
        self.assertFalse(api.is_marked(self.test_tlo, ["title"]))

    def test_is_marked_invalid_selector(self):
        """Test invalid selector raises an error."""
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, ["foo"])
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, [])
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, [""])

        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "c.f")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "c.[2].i")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "c.[3]")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "d")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "x.[0]")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "x.y.w")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "x.z.[1]")
        self.assertRaises(AssertionError, api.is_marked, self.test_tlo, "x.z.foo3")

    def test_is_marked_mix_selector(self):
        """Test valid selector, one marked and one not marked returns True."""
        self.assertTrue(api.is_marked(self.test_tlo, ["description", "revision"]))

        self.assertTrue(api.is_marked(self.test_tlo, ["description"]))

    def test_is_marked_valid_selector_no_refs(self):
        """Test that a valid selector return True when it has marking refs and
            False when not."""
        self.assertTrue(api.is_marked(self.test_tlo, ["description"]))
        self.assertTrue(api.is_marked(self.test_tlo, ["description"], ["marking-definition--2", "marking-definition--3"]))
        self.assertTrue(api.is_marked(self.test_tlo, ["description"], ["marking-definition--2"]))
        self.assertFalse(api.is_marked(self.test_tlo, ["description"], ["marking-definition--2", "marking-definition--8"]))

    def test_is_marked_valid_selector_and_refs(self):
        """Test that a valid selector returns True when marking_refs match."""
        self.assertTrue(api.is_marked(self.test_tlo, ["description"], ["marking-definition--1"]))
        self.assertFalse(api.is_marked(self.test_tlo, ["title"], ["marking-definition--1"]))

    def test_is_marked_valid_selector_multiple_refs(self):
        """Test that a valid selector returns True if aall marking_refs match.
            Otherwise False."""
        self.assertTrue(api.is_marked(self.test_tlo, ["revision"], ["marking-definition--2", "marking-definition--3"]))
        self.assertFalse(api.is_marked(self.test_tlo, ["revision"], ["marking-definition--2", "marking-definition--1"]))
        self.assertTrue(api.is_marked(self.test_tlo, ["revision"], "marking-definition--2"))

        self.assertFalse(api.is_marked(self.test_tlo, ["revision"], ["marking-definition--1234"]))

    def test_is_marked_no_marking_refs(self):
        """Test that a valid content selector with no marking_refs returns True
            if there is a granular_marking that asserts that field, False
            otherwise."""
        self.assertFalse(api.is_marked(self.test_tlo, ["type"]))
        self.assertTrue(api.is_marked(self.test_tlo, ["revision"]))

    def test_is_marked_positional_arguments_combinations(self):
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
        self.assertTrue(api.is_marked(test_tlo, "a", ["1"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "a", ["1"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "a", ["1"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "b", inherited=False, descendants=False))
        self.assertFalse(api.is_marked(test_tlo, "b", inherited=True, descendants=False))
        self.assertFalse(api.is_marked(test_tlo, "b", inherited=True, descendants=True))
        self.assertFalse(api.is_marked(test_tlo, "b", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "c", ["2"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2", "3", "4", "5"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c", ["2", "3", "4", "5"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "c.[0]", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "c.[0]", ["2"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[0]", ["2"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "c.[0]", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["3"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["2", "3"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["2", "3"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[1]", ["3"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["4"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["2", "4"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["2", "4", "5"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[2]", ["4", "5"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["5"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["2", "4", "5"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["2", "4", "5"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "c.[2].g", ["5"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x", ["6"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6", "7", "8", "9", "10"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x", ["6", "7", "8", "9", "10"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x.y", ["7"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["6", "7"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["6", "7", "8"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.y", ["7", "8"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "x.y.[0]", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[0]", ["6", "7"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[0]", ["6", "7"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "x.y.[0]", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["8"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["6", "7", "8"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["6", "7", "8"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.y.[1]", ["8"], False, True))

        self.assertTrue(api.is_marked(test_tlo, "x.z", ["9"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["6", "9"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["6", "9", "10"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.z", ["9", "10"], False, True))

        self.assertFalse(api.is_marked(test_tlo, "x.z.foo1", inherited=False, descendants=False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo1", ["6", "9"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo1", ["6", "9"], True, True))
        self.assertFalse(api.is_marked(test_tlo, "x.z.foo1", inherited=False, descendants=True))

        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["10"], False, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["6", "9", "10"], True, False))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["6", "9", "10"], True, True))
        self.assertTrue(api.is_marked(test_tlo, "x.z.foo2", ["10"], False, True))


class SetMarkingTests(unittest.TestCase):

    # Rich

    def test_set_marking_mark_one_selector_multiple_refs(self):
        before = {
            "description": "test description",
            "title": "foo",
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.set_markings(before, ["description"], ["marking-definition--1", "marking-definition--2"])
        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_set_marking_mark_multiple_selector_one_refs(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--3"
                },
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        api.set_markings(before, ["description", "title"], ["marking-definition--1"])
        self.assertEqual(before, after)

    def test_set_marking_mark_multiple_selector_multiple_refs_from_none(self):
        before = {
            "description": "test description",
            "title": "foo",
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--1"
                },
                {
                    "selectors": ["description", "title"],
                    "marking_ref": "marking-definition--2"
                },
            ]
        }
        api.set_markings(before, ["description", "title"], ["marking-definition--1", "marking-definition--2"])
        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_set_marking_mark_another_property_same_marking(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--7"
                },
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--8"
                },
            ]
        }
        api.set_markings(before, ["description"], ["marking-definition--7", "marking-definition--8"])

        for m in before["granular_markings"]:
            self.assertTrue(m in after["granular_markings"])

    def test_set_marking_bad_selector(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                },
            ]
        }
        self.assertRaises(AssertionError, api.set_markings, before, ["foo"], ["marking-definition--7", "marking-definition--8"])
        self.assertRaises(AssertionError, api.set_markings, before, "", ["marking-definition--7", "marking-definition--8"])
        self.assertRaises(AssertionError, api.set_markings, before, [], ["marking-definition--7", "marking-definition--8"])
        self.assertRaises(AssertionError, api.set_markings, before, [""], ["marking-definition--7", "marking-definition--8"])
        self.assertEqual(before, after)

    def test_set_marking_mark_same_property_same_marking(self):
        before = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        after = {
            "description": "test description",
            "title": "foo",
            "granular_markings": [
                {
                    "selectors": ["description"],
                    "marking_ref": "marking-definition--1"
                }
            ]
        }
        api.set_markings(before, ["description"], ["marking-definition--1"])
        self.assertEqual(before, after)


class ClearMarkingTests(unittest.TestCase):

    # Emmanuelle

    @classmethod
    def setUpClass(cls):
        cls.test_tlo = \
            {
                "title": "test title",
                "description": "test description",
                "revision": 2,
                "type": "test",
                "granular_markings": [
                    {
                        "selectors": ["description"],
                        "marking_ref": "marking-definition--1"
                    },
                    {
                        "selectors": ["revision", "description"],
                        "marking_ref": "marking-definition--2"
                    },
                    {
                        "selectors": ["revision", "description", "type"],
                        "marking_ref": "marking-definition--3"
                    },
                ]
            }

    def test_clear_marking_smoke(self):
        """Test clear_marking call does not fail."""
        self.setUpClass()
        api.clear_markings(self.test_tlo, "revision")
        self.assertFalse(api.is_marked(self.test_tlo, "revision"))

    def test_clear_marking_multiple_selectors(self):
        """Test clearing markings for multiple selectors effectively removes
            associated markings."""
        self.setUpClass()
        api.clear_markings(self.test_tlo, ["type", "description"])
        self.assertFalse(api.is_marked(self.test_tlo, ["type", "description"]))

    def test_clear_marking_one_selector(self):
        """Test markings associated with one selector were removed."""
        self.setUpClass()
        api.clear_markings(self.test_tlo, "description")
        self.assertFalse(api.is_marked(self.test_tlo, "description"))

    def test_clear_marking_all_selectors(self):
        self.setUpClass()
        api.clear_markings(self.test_tlo, ["description", "type", "revision"])
        self.assertFalse(api.is_marked(self.test_tlo, "description"))
        self.assertTrue("granular_markings" not in self.test_tlo)

    def test_clear_marking_bad_selector(self):
        """Test bad selector raises exception."""
        self.assertRaises(AssertionError, api.clear_markings, self.test_tlo, "foo")
        self.assertRaises(AssertionError, api.clear_markings, self.test_tlo, "")
        self.assertRaises(AssertionError, api.clear_markings, self.test_tlo, [])
        self.assertRaises(AssertionError, api.clear_markings, self.test_tlo, [""])

if __name__ == "__main__":
    unittest.main()
