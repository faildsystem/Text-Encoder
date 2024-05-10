from functions import Functions


class ArithmeticEncoder:

    @staticmethod
    def Arithmetic_encoding(text):

        def process_stage(probability_table, stage_min, stage_max):
            stage_probs = {}
            stage_domain = stage_max - stage_min
            for symbol, probability in probability_table.items():
                cum_prob = probability * stage_domain + stage_min
                stage_probs[symbol] = [stage_min, cum_prob]
                stage_min = cum_prob
            return stage_probs

        probability_table = Functions.calc_probabilities(text)

        def encode(message):
            encoder = []
            stage_min = 0.0
            stage_max = 1.0
            for symbol in message:
                stage_probs = process_stage(probability_table, stage_min, stage_max)
                stage_min = stage_probs[symbol][0]
                stage_max = stage_probs[symbol][1]
                encoder.append(stage_probs)
            encoded_value = (stage_min + stage_max) / 2
            return encoded_value

        encoded_value = encode(text)

        # Calculate sizes
        bits_before = len(text) * 8
        bits_after = len('{:b}'.format(int(encoded_value))) + len(str(encoded_value).split('.')[1])

        # Compression Ratio Calculation
        compression_ratio = round(bits_before / bits_after * 100, 1)

        # Calculate entropy
        entropy = Functions.calc_entropy(probability_table)

        return {
            "encoded_value": encoded_value,
            "bits_before": bits_before,
            "bits_after": bits_after,
            "compression ratio (%)": compression_ratio,
            "probabilities": probability_table,
            "average_length": 8,
            "entropy": round(entropy, 3),
            "efficiency": round(entropy / 8 * 100, 1)
        }