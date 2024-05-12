import math

class LZWEncoder:
    def __init__(self, text):
        self.text = text
        self.encoded_string = self.compress()
        self.bits_before = self.compute_bits_before()
        self.bits_after = self.compute_bits_after()
        self.compression_ratio = self.compute_cr()
        self.probabilities = self.compute_probabilities()
        self.entropy = self.compute_entropy()
        self.efficiency = self.compute_efficiency()

    def compress(self):
        if not self.text:
            return []

        dictionary = {chr(i): i for i in range(128)}
        current_code = 128
        compressed = []
        current_string = ""

        for char in self.text:
            if current_string + char in dictionary:
                current_string += char
            else:
                compressed.append(dictionary[current_string])
                dictionary[current_string + char] = current_code
                current_code += 1
                current_string = char

        if current_string:
            compressed.append(dictionary[current_string])

        return compressed

    def compute_bits_before(self):
        bits_before = 0
        for char in self.text:
            if char.isdigit():
                bits_before += 1
            elif char.isalpha():
                bits_before += 8
        return bits_before

    def compute_bits_after(self):
        encoding = math.ceil(math.log2(max(self.encoded_string) + 1))
        bits_after = (len(self.encoded_string) ) * encoding
        return bits_after

    def compute_cr(self):
        original_size = self.bits_before
        compressed_size = self.bits_after
        return original_size / compressed_size if compressed_size > 0 else 0

    def compute_probabilities(self):
        freq_map = {}
        total_symbols = 0
        for symbol in self.text:
            freq_map[symbol] = freq_map.get(symbol, 0) + 1
            total_symbols += 1
        char_prob = {symbol: freq / total_symbols for symbol, freq in freq_map.items()}
        return char_prob

    def compute_entropy(self):
        entropy = 0
        total_symbols = len(self.text)
        char_prob = self.probabilities
        for freq in char_prob.values():
            entropy -= freq * math.log2(freq)
        return entropy

    def compute_efficiency(self):
        original_size = self.bits_before
        compressed_size = self.bits_after
        return ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0

    def get_results(self):
        return {
            "encoded_text": self.encoded_string,
            "bits_before": self.bits_before,
            "bits_after": self.bits_after,
            "average_length": '',
            "compression ratio (%)": round(self.compression_ratio * 100, 1),
            "probabilities": self.probabilities,
            "entropy": round(self.entropy, 3),
            "efficiency": round(self.efficiency, 1),
        }
