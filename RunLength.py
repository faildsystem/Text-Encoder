from functions import Functions


class RunLengthEncoder:

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
        try:
            if not text:
                raise ValueError("Input text is empty.")

            encoded_string = ""
            count = 1
            bits_before = len(text) * 8
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

            bits_after = Functions.bits_after_RLE(number_of_vectors, biggest_vector)  
            char_prob = Functions.calc_probabilities(text, len(text))
            entropy = Functions.calc_entropy(char_prob) 

            return {
                "encoded_string": encoded_string,
                "number_of_vectors": number_of_vectors,
                "biggest_vector": biggest_vector,
                "bits_before": bits_before,
                "bits_after": bits_after,
                "compression ratio (%)": round(bits_before / bits_after * 100, 1),
                "probabilities": char_prob,
                "entropy": round(entropy, 3),
                "average_length": 8,
                "efficiency": round(entropy / 8 * 100, 1),
            }

        except ValueError as ve:
            print("Error:", ve)
        except Exception as e:
            print("Error:", e)