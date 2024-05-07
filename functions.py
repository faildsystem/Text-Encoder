import math
from collections import Counter

class Functions:
    @staticmethod
    def calc_probabilities(text, length):
        """
        Calculate the probabilities of each character in the file.

        Args:
            file_contents: The contents of the file as a string.
            file_length: The length of the file.

        Returns:
            A dictionary where the keys are characters and the values are the probabilities of each character.
        """
        char_counter = Counter(text)
        char_prob = {}
        for ch, count in char_counter.items():
            char_prob[ch] = count / length
        return char_prob
    
    @staticmethod
    def bits_after_RLE(number_of_vectors, biggest_vector):
        """
        Calculate the number of bits needed to store the vectors after RLE.

        Args:
            number_of_vectors: The number of vectors.
            biggest_vector: The biggest vector.

        Returns:
            The number of bits needed to store the vectors after RLE.    
        """
        return number_of_vectors * (8 + math.ceil(math.log2(biggest_vector + 1)))
    
    @staticmethod
    def calc_entropy(probabilities):
        """
        Calculate the entropy of a given list of probabilities.

        Args:
        probabilities (list): A list of probabilities.

        Returns:
        float: The entropy value.
        """
        entropy_val = 0
        for prob in probabilities.values():
            if prob != 0:
                entropy_val -= prob * math.log2(prob)
        return entropy_val
    
    