#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import unittest
import thecpa


class TestSimpleParser(unittest.TestCase):
    def test_empty_string(self):
        parsed = thecpa.parse("")
        assert list(parsed) == []
        assert parsed.__dict__ == {}

    def test_whitespace_only_string(self):
        parsed = thecpa.parse(" \t\n")
        assert list(parsed) == []
        assert parsed.__dict__ == {}

    def test_single_key_value_pair(self):
        parsed = thecpa.parse("foo: bar")
        assert set(parsed) == set(["foo"])
        assert parsed.__dict__ == {'foo': 'bar'}
        assert parsed['foo'] == 'bar'
        assert parsed.foo == 'bar'

    def test_two_key_value_pairs(self):
        parsed = thecpa.parse("""
parrot: dead
slug: mute
""")
        assert set(parsed) == set(["parrot", "slug"])
        assert parsed.__dict__ == {"parrot": "dead", "slug": "mute"}
        assert parsed['parrot'] == parsed.parrot == 'dead'
        assert parsed['slug'] == parsed.slug == 'mute'

    def test_keys_are_case_insensitive(self):
        parsed = thecpa.parse("Parrot: dead")
        assert parsed.Parrot == "dead"
        assert parsed.parrot == "dead"

    def test_values_with_whitespace(self):
        parsed = thecpa.parse("""
parrot: is no more
it: has\tceased\tto\tbe
it_has: expired\tand gone\tmeet its\tmaker
""")
        assert parsed.parrot == "is no more"
        assert parsed.it == "\t".join(["has", "ceased", "to", "be"])
        assert parsed.it_has == "expired\tand gone\tmeet its\tmaker"

    def test_values_with_leading_and_trailing_whitespace(self):
        parsed = thecpa.parse("""
customer: 'ello Miss    \t
clerk:    what do you mean, miss?  \t
customer_again:    I'm sorry, I have a cold.    \t\t
""")
        assert parsed.customer == "'ello Miss"
        assert parsed.clerk == "what do you mean, miss?"
        assert parsed.customer_again == "I'm sorry, I have a cold."


class TestInterpolation(unittest.TestCase):
    def test_simple_interpolation(self):
        parsed = thecpa.parse("""
pet: parrot
this_is: a dead {pet}
        """)
        assert parsed.pet == "parrot"
        assert parsed.this_is == "a dead parrot"

    def test_interpolate_same_key_twice(self):
        parsed = thecpa.parse("""
parrot: Polly
wakeup_call: {parrot}, wake up! {parrot}!
        """)
        assert parsed.wakeup_call == 'Polly, wake up! Polly!'
