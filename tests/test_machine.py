import unittest
from enigma.machine import Enigma, ALPHABET


class TestEnigmaMachine(unittest.TestCase):

    def setUp(self):
        self.default_rotors = ["I", "II", "III"]
        self.default_reflector = "B"
        self.default_plugboard = ""  # no plugboard swaps
        self.default_positions = "aaa"
        self.default_rings = "aaa"
        self.enigma = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=self.default_plugboard
        )

    def test_empty_message(self):
        """
        Processing an empty string should return an empty string.
        """
        result = self.enigma.process("")
        self.assertEqual(result, "",
                         "Expected an empty message to return an empty string.")

    def test_uppercase_and_special_characters_handled_correctly(self):
        """
        If an input contains characters outside of the allowed alphabet,
        the machine should process non-alphabetic characters unchanged 
        and handle uppercase letters by treating them as their lowercase equivalents.
        """
        special_message = "Hello, World!"
        expected_result = self.enigma.process("hello, world!")
        new_enigma = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=self.default_plugboard
        )

        result = new_enigma.process(special_message)
        self.assertEqual(result, expected_result,
                         "Processing failed to handle non-alphabetic and uppercase characters correctly.")

    def test_encryption_decryption_symmetry(self):
        """
        The Enigma machine is symmetric. Encrypting a message and then re-encrypting
        the result with a machine in the same initial configuration should recover
        the original message.
        """
        plaintext = "helloworld"
        # Encrypt the message with one machine.
        ciphertext = self.enigma.process(plaintext)

        # Reinitialize a new machine with the same configuration.
        enigma_decrypt = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=self.default_plugboard
        )
        # Encrypting the ciphertext with the fresh machine should recover the plaintext.
        recovered_text = enigma_decrypt.process(ciphertext)
        self.assertEqual(plaintext, recovered_text,
                         "Re-encrypting the ciphertext did not recover the original plaintext.")

    def test_rotor_stepping_behavior(self):
        """
        Process a message long enough to force rotor stepping. Verify that rotor positions
        change in a manner that does not equal the initial rotor positions.
        """
        # Grab the initial positions from each rotor.
        initial_positions = [rotor.position for rotor in self.enigma.rotors]

        # Process a message long enough to force rotor(s) to step.
        message = "a" * 30  # 30 letters; adjust as needed if your stepping differs.
        _ = self.enigma.process(message)

        # Check that at least one rotor position is different.
        new_positions = [rotor.position for rotor in self.enigma.rotors]
        self.assertNotEqual(initial_positions, new_positions,
                            "Rotor positions did not change after processing multiple letters.")

    def test_plugboard_effect(self):
        """
        Validate that a non-trivial plugboard configuration causes letter swaps
        in the encryption process while still ensuring overall reversibility.
        """
        # Use a plugboard with one connection, for example swapping 'a' and 'b'.
        plugboard_config = "ab"
        enigma_with_plug = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=plugboard_config
        )
        plaintext = "aardvark"
        ciphertext = enigma_with_plug.process(plaintext)

        # Reinitialize to decrypt.
        enigma_decrypt = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=plugboard_config
        )
        recovered_text = enigma_decrypt.process(ciphertext)
        self.assertEqual(plaintext, recovered_text,
                         "Plugboard configuration affected reversibility of encryption.")

    def test_long_message_consistency(self):
        """
        Process a longer message and ensure that reinitializing the Enigma machine
        to its initial state and processing the resulting ciphertext recovers the original.
        """
        plaintext = "".join(ALPHABET * 10)  # 260 characters.
        ciphertext = self.enigma.process(plaintext)

        # Reinitialize a new machine with the same starting configuration.
        enigma_reset = Enigma(
            rotors=self.default_rotors,
            initial_positions=self.default_positions,
            ring_settings=self.default_rings,
            reflector=self.default_reflector,
            plugboard_connections=self.default_plugboard
        )
        recovered_text = enigma_reset.process(ciphertext)
        self.assertEqual(plaintext, recovered_text,
                         "Long message encryption/decryption failed to recover the original text.")


if __name__ == '__main__':
    unittest.main()
