from collections import Counter
import heapq
import math


class HuffmanEncoder:
    def __init__(self, text):
        # Constructor to initialize the HuffmanCoding object with the input text
        self.text = text
        # Calculate character probabilities and build Huffman tree
        self.chars, self.freq = self.character_probabilities()
        self.nodes = []
        self.huffman_tree = None
        self.build_tree()

    def character_probabilities(self):
        # Count occurrences of each character in the text
        char_counts = Counter(self.text)
        # Total number of characters in the text
        total_chars = sum(char_counts.values())
        # Calculate probabilities for each character
        probabilities = {}
        for char, count in char_counts.items():
            probabilities[char] = count / total_chars
        chars = list(probabilities.keys())
        freq = list(probabilities.values())
        return chars, freq

    class Node:
        # Node class to represent nodes in the Huffman tree
        def __init__(self, freq, symbol, left=None, right=None):
            # Constructor to initialize a node with frequency, symbol, and optional left and right children
            self.freq = freq  # Frequency of symbol
            self.symbol = symbol  # Symbol name (character)
            self.left = left  # Node left of current node
            self.right = right  # Node right of current node
            self.huff = ''  # Tree direction (0/1)

        def __lt__(self, nxt):
            # Less than comparison for nodes based on frequency
            return self.freq < nxt.freq

    def build_tree(self):
        # Build Huffman tree using character frequencies
        for x in range(len(self.chars)):
            heapq.heappush(self.nodes, self.Node(self.freq[x], self.chars[x]))
        while len(self.nodes) > 1:
            left = heapq.heappop(self.nodes)
            right = heapq.heappop(self.nodes)
            left.huff = 0
            right.huff = 1
            newNode = self.Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
            heapq.heappush(self.nodes, newNode)
        self.huffman_tree = self.nodes[0]

    def huffman_codes(self):
        # return Huffman codes for each character
        huffman_codes = self.get_huffman_codes()
        code = ""
        for char in self.chars:
            code += char + " : " + huffman_codes[char] + "\n"
        return code  

    def get_huffman_codes(self):
        # Get Huffman codes for each character
        huffman_codes = {}
        self._generate_codes(self.huffman_tree, "", huffman_codes)
        return huffman_codes

    def _generate_codes(self, node, code, huffman_codes):
        # Recursively generate Huffman codes for each character
        if not node.left and not node.right:
            huffman_codes[node.symbol] = code
            return
        self._generate_codes(node.left, code + "0", huffman_codes)
        self._generate_codes(node.right, code + "1", huffman_codes)

    def bits_before(self):
        # Calculate the number of bits before Huffman encoding
        bits_before = len(self.text) * 8
        return bits_before
    
    def bits_after(self):
        # Get Huffman codes for each character
        huffman_codes = self.get_huffman_codes()
        # Encode the text using Huffman codes
        encoded_text = "".join(huffman_codes[char] for char in self.text)
        # Calculate the number of bits after encoding
        bits_after = len(encoded_text)
        return bits_after

    def average_length(self):
        # Calculate the average length of the encoded symbols
        huffman_codes = self.get_huffman_codes()
        avg_length = sum(len(code) * freq for code, freq in zip(huffman_codes.values(), self.freq))
        return avg_length

    def calc_entropy(self):
        # Calculate the entropy of the text
        entropy_val = 0
        for prob in self.freq:
            if prob != 0:
                entropy_val -= prob * math.log2(prob)
        return entropy_val
    
    def compression_ratio(self):
        # Calculate the compression ratio
        bits_before = self.bits_before()
        bits_after = self.bits_after()
        compression_ratio = (bits_after / bits_before) * 100
        return compression_ratio
    
    def efficiency(self):
        # Calculate the efficiency of the Huffman coding
        bits_before = self.bits_before()
        bits_after = self.bits_after()
        return (bits_before - bits_after) / bits_before

    def probabilities(self):
        # Return the probabilities of characters
        probabilities_dict = {char: prob for char, prob in zip(self.chars, self.freq)}
        return probabilities_dict
    
    def results(self):
        # Return results dictionary
        encoded_text = self.huffman_codes()
        bits_before = self.bits_before()
        bits_after = self.bits_after()
        avg_length = self.average_length()
        compression_ratio = self.compression_ratio()
        probabilities = self.probabilities()
        entropy = self.calc_entropy()
        efficiency = self.efficiency()

        return {
            "encoded_text": encoded_text,
            "bits_before": bits_before,
            "bits_after": bits_after,
            "average_length": round(avg_length, 2),
            "compression ratio (%)": round(compression_ratio, 1),
            "probabilities": probabilities,
            "entropy": round(entropy, 3),
            "efficiency": round(efficiency * 100, 1)
        }