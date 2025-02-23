import string

ALPHABET = string.ascii_lowercase


class Rotor:
    """
    Represents an Enigma rotor. Each rotor:
    - Has a specific wiring configuration mapping A-Z to a permuted A-Z.
    - Has a notch indicating where it will cause the next rotor to step.
    - Has a ring setting and a position that affect how letters are encoded.
    """

    ROTOR_CONFIGS = {
        "I": {"wiring": "ekmflgdqvzntowyhxuspaibrcj", "notch": "q"},
        "II": {"wiring": "ajdksiruxblhwtmcqgznpyfvoe", "notch": "e"},
        "III": {"wiring": "bdfhjlcprtxvznyeiwgakmusqo", "notch": "v"},
        "IV": {"wiring": "esovpzjayquirhxlnftgkdcmwb", "notch": "j"},
        "V": {"wiring": "vzbrgityupsdnhlxawmjqofeck", "notch": "z"},
    }

    def __init__(self, number, position, ring):
        """
        Initialize a rotor.

        :param number: A string in [I, II, III, IV, V] indicating the rotor number.
        :param position: The initial position (letter) of the rotor.
        :param ring: The ring setting (letter) of the rotor.
        """
        self.wiring = self.ROTOR_CONFIGS[number]["wiring"]
        self.notch = self.ROTOR_CONFIGS[number]["notch"]
        self.position = ALPHABET.index(position)
        self.ring = ALPHABET.index(ring)

    def rotate(self):
        """
        Rotate the rotor by one step and return True if this rotor is now at its notch.
        :return: Boolean indicating if the notch is reached.
        """
        self.position = (self.position + 1) % 26

    def encode_forward(self, letter):
        """
        Encode a letter passing forward (right-to-left through the rotor stack).

        :param letter: The input letter to be encoded.
        :return: The encoded letter.
        """
        # Calculate the offset from the ring setting and current position
        offset = self.position - self.ring

        # Find the letter's index in the alphabet, then adjust by the offset
        input_index = ALPHABET.index(letter)
        adjusted_input_index = (input_index + offset) % 26

        # Use adjusted index to pick a letter from the wiring
        encoded_letter = self.wiring[adjusted_input_index]

        # Find encoded letter's index and reverse the offset
        encoded_index = ALPHABET.index(encoded_letter)
        final_index = (encoded_index - offset) % 26

        # Return the encoded letter after reversing the offset
        return ALPHABET[final_index]

    def encode_backward(self, letter):
        """
        Encode a letter passing backward (left-to-right through the rotor stack).

        :param letter: The input letter to be encoded backward.
        :return: The encoded letter.
        """
        # Calculate the offset from the ring setting and current position
        offset = self.position - self.ring

        # Adjust the input letter's index by the offset
        input_index = ALPHABET.index(letter)
        adjusted_input_index = (input_index + offset) % 26
        adjusted_letter = ALPHABET[adjusted_input_index]

        # Determine which wiring index produces this adjusted letter
        wiring_index = self.wiring.index(adjusted_letter)

        # Reverse the offset and return the corresponding alphabet letter
        final_index = (wiring_index - offset) % 26

        # Return the encoded letter after reversing the offset
        return ALPHABET[final_index]