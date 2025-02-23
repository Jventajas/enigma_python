import string

from enigma.plugboard import Plugboard
from enigma.reflector import Reflector
from enigma.rotor import Rotor

ALPHABET = string.ascii_lowercase


class Enigma:
    """
    The Enigma machine: a combination of rotors, a reflector, and a plugboard,
    providing a letter substitution cipher with moving parts.
    """

    def __init__(self, rotors, initial_positions, ring_settings, reflector, plugboard_connections):
        """
        Initialize the Enigma machine.

        :param rotors: A list of three rotor number strings [left, middle, right].
        :param initial_positions: A list of three initial position strings [left, middle, right].
        :param ring_settings: A list of three ring setting strings [left, middle, right].
        :param reflector: A reflector string (e.g., "B").
        :param plugboard_connections: A list of two-letter strings (e.g., ['ab', 'cd', 'ef'])
        """


        # Create rotor objects from letter strings
        self.rotors = [
            Rotor(number, position, ring) for number, position, ring in zip(rotors, initial_positions, ring_settings)
        ]
        self.reflector = Reflector(reflector)
        self.plugboard = Plugboard(plugboard_connections)


    def step_rotors(self):
        """
        Implement the Enigma stepping mechanism (double-stepping):

        Rules:
        - The rightmost rotor steps on every key press.
        - If the rightmost rotor hits its notch, it causes the middle rotor to step on the next press.
        - The middle rotor hitting its notch also causes the left rotor to step simultaneously
          (the double-step).

        Procedure each key press:
          1. If the middle rotor is at notch, advance the left rotor as well (double-step).
          2. If the middle rotor is at notch OR the right rotor is at notch, advance the middle rotor.
          3. Always advance the right rotor.
        """
        left, middle, right = self.rotors

        middle_at_notch = (ALPHABET[middle.position] == middle.notch)
        right_at_notch = (ALPHABET[right.position] == right.notch)

        if middle_at_notch:
            left.rotate()

        if middle_at_notch or right_at_notch:
            middle.rotate()

        right.rotate()

    def process(self, text):
        """
        Encrypt or decrypt the given text using the Enigma machine.

        :param text: The input text to process (string).
        :return: The resulting encrypted or decrypted text.
        """
        output = []
        for letter in text.lower():

            if letter not in ALPHABET:
                # Non-letter characters pass unchanged
                output.append(letter)
                continue

            # Step rotors before each letter is processed
            self.step_rotors()

            # Pass through plugboard
            letter = self.plugboard.swap(letter)

            # Pass forward through the rotors (right to left)
            for rotor in reversed(self.rotors):
                letter = rotor.encode_forward(letter)

            # Reflect
            letter = self.reflector.reflect(letter)

            # Pass backward through the rotors (left to right)
            for rotor in self.rotors:
                letter = rotor.encode_backward(letter)

            # Pass through plugboard again
            letter = self.plugboard.swap(letter)

            output.append(letter)

        return ''.join(output)

























# class EnigmaMachine:
#     def __init__(self, rotors, positions, reflector, plugboard_connections):
#         # Rotor wirings (fixed maps for Enigma I)
#         rotor_wirings = {
#             "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
#             "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
#             "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
#         }
#
#         # Reflector wiring
#         reflectors = {
#             "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT"
#         }
#
#         # Validate input configurations
#         if len(rotors) != 3 or any(r not in rotor_wirings for r in rotors):
#             raise ValueError("Invalid rotor configurations.")
#         if len(positions) != 3 or any(p not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for p in positions):
#             raise ValueError("Invalid rotor positions.")
#         if reflector not in reflectors:
#             raise ValueError("Invalid reflector configuration.")
#
#         # Store rotor configurations
#         self.rotors = [rotor_wirings[r] for r in rotors]
#         self.rotor_positions = [ord(p) - ord('A') for p in positions]
#         self.reflector = reflectors[reflector]
#
#         # Setup plugboard
#         self.plugboard = self.create_plugboard(plugboard_connections)
#
#     def create_plugboard(self, connections):
#         # Map plugboard connections (e.g., "A-B C-D")
#         plugboard_map = {char: char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
#         for pair in connections.split():
#             a, b = pair.split('-')
#             plugboard_map[a], plugboard_map[b] = b, a
#         return plugboard_map
#
#     def shift_rotor(self, rotor_index):
#         """Shifts the rotor at a given index. Handles carrying over to next rotor."""
#         self.rotor_positions[rotor_index] = (self.rotor_positions[rotor_index] + 1) % 26
#         # Return True if the rotor completes a full cycle
#         return self.rotor_positions[rotor_index] == 0
#
#     def encode_character(self, char, rotor, position, reverse=False):
#         """Encodes a single character through a rotor."""
#         offset = ord(char) - ord('A')
#         if not reverse:
#             # Forward translation
#             encoded = (ord(rotor[(offset + position) % 26]) - ord('A') - position) % 26
#         else:
#             # Reverse translation
#             encoded = (rotor.index(chr((offset + position) % 26 + ord('A'))) - position) % 26
#         return chr(encoded + ord('A'))
#
#     def encrypt_character(self, char):
#         """Encrypt a single character (forward and backward path through the machine)."""
#         if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#             return char  # Ignore non-alphabetic characters
#
#         # Pass through plugboard
#         char = self.plugboard[char]
#
#         # Pass through rotors (forward)
#         for i in range(3):
#             char = self.encode_character(char, self.rotors[i], self.rotor_positions[i])
#
#         # Pass through reflector
#         char = self.reflector[ord(char) - ord('A')]
#
#         # Pass back through rotors (reverse)
#         for i in range(2, -1, -1):
#             char = self.encode_character(char, self.rotors[i], self.rotor_positions[i], reverse=True)
#
#         # Pass back through plugboard
#         char = self.plugboard[char]
#
#         # Rotate the rightmost rotor
#         if self.shift_rotor(2):  # Step the middle rotor if the rightmost rotor completes a full cycle
#             if self.shift_rotor(1):  # Step the leftmost rotor if the middle rotor also completes a full cycle
#                 self.shift_rotor(0)
#
#         return char
#
#     def encrypt_message(self, message):
#         """Encrypts an entire message."""
#         return ''.join(self.encrypt_character(char) for char in message.upper())
