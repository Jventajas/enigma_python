import string

ALPHABET = string.ascii_lowercase


class Plugboard:
    """
    The plugboard swaps pairs of letters before and after passing through the rotors.
    """

    def __init__(self, connections):
        """
        Initialize the plugboard with given connections (pairs of letters).

        :param connections: A list of two-letter strings (e.g., ['ab', 'cd', 'ef'])
        """
        if connections:
            connections = connections.lower().split(" ")
        else:
            connections = []

        self.mapping = dict(zip(ALPHABET, ALPHABET))

        # Check for duplicate letters in the connections
        all_plug_letters = ''.join(connections)
        if len(set(all_plug_letters)) != len(all_plug_letters):
            raise ValueError("Duplicate letters detected in plugboard connections")

        # Set up swaps
        for pair in connections:
            a, b = pair
            self.mapping[a] = b
            self.mapping[b] = a

    def swap(self, letter):
        """
        Swap a letter if it is plugged on the plugboard, otherwise return it unchanged.

        :param letter: The letter to potentially swap.
        :return: The swapped or original letter.
        """
        return self.mapping[letter]