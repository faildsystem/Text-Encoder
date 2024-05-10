from functions import Functions
import math


class GolombEncoder:

    @staticmethod
    def golomb_encode(text, M):
        """
        Encodes a value using Golomb coding for a given parameter M.
        If M is a power of 2, it encodes the remainder in binary with length log2(M) bits.
        If not, it encodes the remainder differently based on the specified rules.

        :param value: The integer value to encode.
        :param M: The parameter M.
        :return: The encoded binary string.
        """
        binary_str = ''.join(format(ord(char), '08b') for char in text)
        # N = value
        value = len(binary_str)

        quotient = value // M
        remainder = value % M

        # Encode quotient in unary; a sequence of 1s followed by a 0.
        unary = '1' * quotient + '0'

        # Check if M is a power of 2
        if M > 0 and (M & (M - 1)) == 0:  # M is a power of 2
            binary_length = M.bit_length() - 1
            binary = format(remainder, f'0{binary_length}b')
        else:  # M is not a power of 2
            x = 2 ** math.ceil(math.log2(M)) - M
            if 0 <= remainder < x:  # Remainder can be represented with log2(M) bits
                binary_length = math.floor(math.log2(M))
                binary = format(remainder, f'0{binary_length}b')
            else:  # Remainder + x is encoded with ceil(log2(M)) bits
                binary_length = math.ceil(math.log2(M))
                binary = format(remainder + x, f'0{binary_length}b') 

        encoded_string = unary + binary
        bits_before = len(text) * 8
        bits_after = len(encoded_string)

        char_prob = Functions.calc_probabilities(text)
        entropy = Functions.calc_entropy(char_prob) 

        return {
            "encoded_text": encoded_string,
            "bits_before": bits_before,
            "bits_after": bits_after,
            "entropy": round(entropy, 3),
            "average_length": 8,
            "compression ratio (%)": round(bits_before / bits_after * 100, 1),
            "efficiency": round(entropy / 8 * 100, 1),
            "probabilities": char_prob,
        }