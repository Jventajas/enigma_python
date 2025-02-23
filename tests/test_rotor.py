# test_rotor.py

import unittest
import string
from enigma.rotor import Rotor

ALPHABET = string.ascii_lowercase


class TestRotor(unittest.TestCase):

    def setUp(self):
        # Initialize a Rotor of type "I" with position 'a' and ring setting 'a'.
        self.rotor = Rotor("I", "a", "a")

    def test_encode_forward_then_backward_returns_input(self):
        """
        Encoding a letter forward and then backward should return the original letter.
        """
        for letter in ALPHABET:
            encoded = self.rotor.encode_forward(letter)
            decoded = self.rotor.encode_backward(encoded)
            self.assertEqual(letter, decoded,
                             f"Expected '{letter}' to be recovered after forward and backward encoding, got '{decoded}' instead.")

    def test_rotate_updates_position(self):
        """
        Rotating the rotor should increment its position by one (modulo 26).
        """
        initial_position = self.rotor.position
        self.rotor.rotate()
        expected_position = (initial_position + 1) % 26
        self.assertEqual(self.rotor.position, expected_position,
                         "Rotor rotation did not update the position correctly.")

    def test_encode_changes_after_rotation_forward(self):
        """
        The forward encoding of a given letter should change after the rotor is rotated.
        """
        letter = 'a'
        before_rotation = self.rotor.encode_forward(letter)
        self.rotor.rotate()
        after_rotation = self.rotor.encode_forward(letter)
        self.assertNotEqual(before_rotation, after_rotation,
                            "Forward encoding did not change after rotor rotation.")

    def test_encode_changes_after_rotation_backward(self):
        """
        The backward encoding of a given letter should change after the rotor is rotated.
        """
        letter = 'a'
        before_rotation = self.rotor.encode_backward(letter)
        self.rotor.rotate()
        after_rotation = self.rotor.encode_backward(letter)
        self.assertNotEqual(before_rotation, after_rotation,
                            "Backward encoding did not change after rotor rotation.")

    def test_full_rotation_returns_to_initial_position(self):
        """
        After 26 rotations, the rotor should return to its initial position.
        """
        initial_position = self.rotor.position
        for _ in range(26):
            self.rotor.rotate()
        self.assertEqual(self.rotor.position, initial_position,
                         "Rotor did not return to the initial position after 26 rotations.")


if __name__ == '__main__':
    unittest.main()