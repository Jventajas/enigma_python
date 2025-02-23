# test_plugboard.py

import unittest
import string
from enigma.plugboard import Plugboard

ALPHABET = string.ascii_lowercase


class TestPlugboard(unittest.TestCase):

    def test_identity_mapping_when_no_connections(self):
        """
        Ensure that if no connections are provided, each letter maps to itself.
        """
        plugboard = Plugboard("")
        for letter in ALPHABET:
            self.assertEqual(letter, plugboard.swap(letter),
                             f"Expected letter '{letter}' to map to itself when no connections are provided.")

    def test_none_as_connections(self):
        """
        Ensure that if None is passed as connections, the plugboard behaves as if no connections are provided.
        """
        plugboard = Plugboard(None)
        for letter in ALPHABET:
            self.assertEqual(letter, plugboard.swap(letter),
                             f"Expected letter '{letter}' to map to itself when connections are None.")

    def test_valid_connections_swap(self):
        """
        Test that plugboard swaps letters as per the given connections.
        """
        connections = 'ab cd'
        plugboard = Plugboard(connections)
        # For a pair, letters should be swapped.
        self.assertEqual(plugboard.swap('a'), 'b', "Expected 'a' to map to 'b'.")
        self.assertEqual(plugboard.swap('b'), 'a', "Expected 'b' to map to 'a'.")
        self.assertEqual(plugboard.swap('c'), 'd', "Expected 'c' to map to 'd'.")
        self.assertEqual(plugboard.swap('d'), 'c', "Expected 'd' to map to 'c'.")

        # Other letters should remain unchanged.
        for letter in ALPHABET:
            if letter not in 'abcd':
                self.assertEqual(letter, plugboard.swap(letter),
                                 f"Expected letter '{letter}' to remain unchanged.")

    def test_multiple_connections(self):
        """
        Checks correct swapping on a plugboard with multiple pairs.
        """
        connections = 'ab cd ef'
        plugboard = Plugboard(connections)
        # Test for each pair
        self.assertEqual(plugboard.swap('a'), 'b')
        self.assertEqual(plugboard.swap('b'), 'a')
        self.assertEqual(plugboard.swap('c'), 'd')
        self.assertEqual(plugboard.swap('d'), 'c')
        self.assertEqual(plugboard.swap('e'), 'f')
        self.assertEqual(plugboard.swap('f'), 'e')

    def test_duplicate_letters_raise_error(self):
        """
        Checks that initializing the plugboard with duplicate letters in the connections raises an error.
        """
        connections = 'ab ac'  # 'a' is duplicated.
        with self.assertRaises(ValueError, msg="Expected ValueError due to duplicate letters in connections."):
            Plugboard(connections)

    def test_invalid_letter_input(self):
        """
        Ensure that passing an invalid character (e.g., uppercase or non-letter) to swap raises a KeyError.
        """
        plugboard = Plugboard('ab')
        invalid_inputs = ['A', '1', '!', ' ']
        for invalid in invalid_inputs:
            with self.assertRaises(KeyError, msg=f"Expected KeyError for invalid input '{invalid}'."):
                plugboard.swap(invalid)


if __name__ == '__main__':
    unittest.main()