# test_reflector.py

import unittest
import string
from enigma.reflector import Reflector  # Replace 'your_module_name' with the actual module name.

ALPHABET = string.ascii_lowercase


class TestReflector(unittest.TestCase):

    def test_symmetry_for_all_letters(self):
        """
        For a properly set up reflector, reflecting a letter twice
        should yield the original letter.
        This test is run for each reflector type.
        """
        for reflector_type in ["A", "B", "C"]:
            reflector = Reflector(reflector_type)
            for letter in ALPHABET:
                reflected = reflector.reflect(letter)
                double_reflected = reflector.reflect(reflected)
                self.assertEqual(letter, double_reflected,
                                 f"Symmetry fails for reflector type {reflector_type} on letter '{letter}'")

    def test_known_mapping_config_a(self):
        """
        Verifies specific mappings for reflector type 'A'.
        For example, if 'a' maps to 'e', then 'e' should map back to 'a'.
        """
        reflector = Reflector("A")
        # Test specific known mappings for configuration A.
        # The reflector wiring for type A is "ejmzalyxvbwfcrquontspikhgd"
        mapping_a = dict(zip(ALPHABET, "ejmzalyxvbwfcrquontspikhgd"))
        for letter in ALPHABET:
            expected = mapping_a[letter]
            result = reflector.reflect(letter)
            self.assertEqual(expected, result,
                             f"For reflector type A: expected '{letter}' -> '{expected}' but got '{result}'")

    def test_known_mapping_config_b(self):
        """
        Verifies specific mappings for reflector type 'B'.
        For example, if 'a' maps to 'y', then 'y' should map back to 'a'.
        """
        reflector = Reflector("B")
        # Test specific known mappings for configuration B.
        # The reflector wiring for type B is "yruhqsldpxngokmiebfzcwvjat"
        mapping_b = dict(zip(ALPHABET, "yruhqsldpxngokmiebfzcwvjat"))
        for letter in ALPHABET:
            expected = mapping_b[letter]
            result = reflector.reflect(letter)
            self.assertEqual(expected, result,
                             f"For reflector type B: expected '{letter}' -> '{expected}' but got '{result}'")

    def test_known_mapping_config_c(self):
        """
        Verifies specific mappings for reflector type 'C'.
        For example, if 'a' maps to 'f', then 'f' should map back to 'a'.
        """
        reflector = Reflector("C")
        # Test specific known mappings for configuration C.
        # The reflector wiring for type C is "fvpjiaoyedrzxwgctkuqsbnmhl"
        mapping_c = dict(zip(ALPHABET, "fvpjiaoyedrzxwgctkuqsbnmhl"))
        for letter in ALPHABET:
            expected = mapping_c[letter]
            result = reflector.reflect(letter)
            self.assertEqual(expected, result,
                             f"For reflector type C: expected '{letter}' -> '{expected}' but got '{result}'")

    def test_invalid_letter_raises_error(self):
        """
        Passing an invalid input (like a digit or a non-a-z character) should raise a KeyError.
        """
        reflector = Reflector("B")
        invalid_inputs = ["1", "!", "A", " "]
        for invalid in invalid_inputs:
            with self.assertRaises(KeyError,
                                   msg=f"Expected KeyError for invalid input '{invalid}'"):
                reflector.reflect(invalid)

    def test_invalid_reflector_type_raises_error(self):
        """
        Initializing the reflector with an invalid configuration type should raise a KeyError.
        """
        with self.assertRaises(KeyError,
                               msg="Expected KeyError for invalid reflector type"):
            Reflector("D")  # 'D' is not a supported reflector configuration.


if __name__ == '__main__':
    unittest.main()