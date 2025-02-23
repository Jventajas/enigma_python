import string

ALPHABET = string.ascii_lowercase


class Reflector:
    """
    A reflector maps each letter to another letter, providing symmetry.
    """

    REFLECTOR_CONFIGS = {
        "A": "ejmzalyxvbwfcrquontspikhgd",
        "B": "yruhqsldpxngokmiebfzcwvjat",
        "C": "fvpjiaoyedrzxwgctkuqsbnmhl",
    }

    def __init__(self, reflector_type):
        """
        Initialize the reflector.

        :param reflector_type: A string in [A, B, C] indicating the reflector type.
        """
        self.mapping = dict(zip(ALPHABET, self.REFLECTOR_CONFIGS[reflector_type]))

    def reflect(self, letter):
        """
        Reflect a letter according to the reflector's wiring.

        :param letter: The letter to reflect.
        :return: The reflected letter.
        """
        return self.mapping[letter]