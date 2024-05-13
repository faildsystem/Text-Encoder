from functions import Functions
import math


from functions import Functions
import math


class RunLengthEncoder:
    
    def bits_before_RLE(text, bits=8):
        """
        Calculate the number of bits before RLE.

        Args:
            text: The text to calculate the number of bits for.
            bits: The number of bits per character.
        
        Returns:
            The number of bits before RLE.
        """
        return len(text) * bits

    @staticmethod
    def RLE_encoding(text):
        """
        Perform Run-Length Encoding (RLE) on the contents of a file.

        Args:
            file_name: The name of the file to read.
        
        Returns:
            A dictionary containing the following
            - encoded_string: The encoded string after RLE.
            - number_of_vectors: The number of vectors.
            - biggest_vector: The biggest vector.
            - bits_before: The number of bits before RLE.
            - bits_after: The number of bits after RLE.
            - compression ratio: The compression ratio.
            - probabilities: The probabilities of each character.
            - entropy: The entropy of the file.
            - average_length: The average length of the encoded string.
            - efficiency: The efficiency of the encoding.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the user does not have permission to read the file.
            Exception: For any other errors.
        """
        bits = 1 if text.isdigit() else 8
        encoded_string = ""
        count = 1
        number_of_vectors = 0
        biggest_vector = 0
        prev_char = text[0]

        for char in text[1:]:
            if char == prev_char:
                count += 1
            else:
                if count > biggest_vector:
                    biggest_vector = count

                encoded_string += str(count) + prev_char + ","
                number_of_vectors += 1

                count = 1
                prev_char = char

        # Handling the last character
        if count > biggest_vector:
            biggest_vector = count

        encoded_string += str(count) + prev_char
        number_of_vectors += 1
        
        bits_before = RunLengthEncoder.bits_before_RLE(text, bits)
        bits_after = number_of_vectors * (bits + math.ceil(math.log2(biggest_vector + 1))) + number_of_vectors * 8
        char_prob = Functions.calc_probabilities(text)
        entropy = Functions.calc_entropy(char_prob) 
        compression_ratio = round((bits_before / bits_after) * 100, 2)
        average_length = math.ceil(math.log2(biggest_vector + 1))
        efficiency = (entropy / average_length) * 100

        return {
            "encoded_text": encoded_string,
            "number_of_vectors": number_of_vectors,
            "biggest_vector": biggest_vector,
            "bits_before": bits_before,
            "bits_after": bits_after,
            "compression ratio (%)": round(compression_ratio, 1),
            "probabilities": char_prob,
            "entropy": round(entropy, 3),
            "average_length": average_length,
            "efficiency": round(efficiency, 1),
        }