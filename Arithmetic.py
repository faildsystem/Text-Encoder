from decimal import Decimal
from functions import Functions

class ArithmeticEncoder:
    """
    ArithmeticEncoding is a class for building arithmetic encoding.
    """

    def __init__(self, frequency_table):
        self.probability_table = self.get_probability_table(frequency_table)

    def get_probability_table(self, frequency_table):
        """
        Calculates the probability table out of the frequency table.
        """
        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value/total_frequency

        return probability_table

    def get_encoded_value(self, encoder):
        """
        After encoding the entire message, this method returns the single value that represents the entire message.
        """
        last_stage = list(encoder[-1].values())
        last_stage_values = []
        for sublist in last_stage:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)

        return (last_stage_min + last_stage_max)/2

    def process_stage(self, probability_table, stage_min, stage_max):
        """
        Processing a stage in the encoding/decoding process.
        """
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(probability_table.items())):
            term = list(probability_table.keys())[term_idx]
            term_prob = Decimal(probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs

    def encode(self, msg, probability_table):
        """
        Encodes a message.
        """

        encoder = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for msg_term_idx in range(len(msg)):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)

            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            encoder.append(stage_probs)

        stage_probs = self.process_stage(probability_table, stage_min, stage_max)
        encoder.append(stage_probs)

        encoded_msg = self.get_encoded_value(encoder)

        entropy = Functions.calc_entropy(probability_table)

        bits_before = len(msg) * 8
        bits_after = len('{:b}'.format(int(encoded_msg))) + len(str(encoded_msg).split('.')[1])

        return {
            'encoded_text': encoded_msg,  
            'bits_before': bits_before,
            'bits_after': bits_after,
            'compression ratio (%)': round(bits_before / bits_after * 100, 1),
            'average_length': 8,
            'probabilities': probability_table,
            'entropy': entropy, 
            'efficiency': round(entropy / 8 * 100, 1)
        }


































# from functions import Functions


# class ArithmeticEncoder:

#     @staticmethod
#     def Arithmetic_encoding(text):

#         def process_stage(probability_table, stage_min, stage_max):
#             stage_probs = {}
#             stage_domain = stage_max - stage_min
#             for symbol, probability in probability_table.items():
#                 cum_prob = probability * stage_domain + stage_min
#                 stage_probs[symbol] = [stage_min, cum_prob]
#                 stage_min = cum_prob
#             return stage_probs

#         probability_table = Functions.calc_probabilities(text)

#         def encode(message):
#             encoder = []
#             stage_min = 0.0
#             stage_max = 1.0
#             for symbol in message:
#                 stage_probs = process_stage(probability_table, stage_min, stage_max)
#                 stage_min = stage_probs[symbol][0]
#                 stage_max = stage_probs[symbol][1]
#                 encoder.append(stage_probs)
#             encoded_value = (stage_min + stage_max) / 2
#             return encoded_value

#         encoded_value = encode(text)

#         # Calculate sizes
#         bits_before = len(text) * 8
#         bits_after = len('{:b}'.format(int(encoded_value))) + len(str(encoded_value).split('.')[1])

#         # Compression Ratio Calculation
#         compression_ratio = round(bits_before / bits_after * 100, 1)

#         # Calculate entropy
#         entropy = Functions.calc_entropy(probability_table)

#         return {
#             "encoded_text": encoded_value,
#             "bits_before": bits_before,
#             "bits_after": bits_after,
#             "compression ratio (%)": compression_ratio,
#             "probabilities": probability_table,
#             "average_length": 8,
#             "entropy": round(entropy, 3),
#             "efficiency": round(entropy / 8 * 100, 1)
#         }