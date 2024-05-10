import math

def lzw_compress(text):
    if not text:
        return []

    dictionary = {chr(i): i for i in range(128)}
    current_code = 128
    compressed = []
    current_string = ""

    for char in text:
        if current_string + char in dictionary:
            current_string += char
        else:
            compressed.append(dictionary[current_string])
            # Assign the code corresponding to the prefix of the new sequence
            dictionary[current_string + char] = current_code
            current_code += 1
            # Update current string for the next iteration
            current_string = char

    if current_string:
        compressed.append(dictionary[current_string])

    return compressed



def lzw_decompress(compressed):
    if not compressed:
        return ""

    dictionary = {i: chr(i) for i in range(128)}  # ASCII characters from 0 to 127
    current_code = 128  # Start new codes from 128
    decompressed = []

    previous = chr(compressed.pop(0))
    decompressed.append(previous)

    for code in compressed:
        if code in dictionary:
            entry = dictionary[code]
        elif code == current_code:
            entry = previous + previous[0]
        else:
            raise ValueError("Bad compressed sequence")

        decompressed.append(entry)

        if current_code < 256:  # Max code value in 0-128 range
            dictionary[current_code] = previous + entry[0]
            current_code += 1

        previous = entry

    return ''.join(decompressed)


def compute_original_size(original_data):
    if isinstance(original_data, str):
        
        result = 0
        for char in str(original_data):
            if char.isdigit():
                result += 1
            elif char.isalpha():
                result += 8
            else:
                print(f"Unsupported character '{char}'")
                raise ValueError("Unsupported character")
        return result  
    elif isinstance(original_data, (int, float)):
        return math.ceil(math.log2(original_data + 1))  
    else:
        print("Unsupported data type for original data")
        raise ValueError("Unsupported data type for original data")
    

def compute_cr(original_data, compressed_data):
    original_size = compute_original_size(original_data)

 

    encoding = math.ceil(math.log2(max(compressed_data) + 1))
    compressed_size = (len(compressed_data)+1) * encoding  
    print("Bits before:" ,original_size)
    print("encoding:" ,encoding)
    print("compressed_size:" ,len(compressed_data)+1)

    print("Bits After:" ,compressed_size)

    return original_size / compressed_size if compressed_size > 0 else 0


def freq(Text):
    freq_map = {}
    total_symbols = 0
    for symbol in Text:
        freq_map[symbol] = freq_map.get(symbol, 0) + 1
        total_symbols += 1
    return freq_map
lol=freq("wabbawabba")
lol


def compute_entropy(data):
    if not data:
        return 0
    
    freq_map = {}
    total_symbols = 0
    for symbol in data:
        freq_map[symbol] = freq_map.get(symbol, 0) + 1
        total_symbols += 1
    
    entropy = 0
    for freq in freq_map.values():
        probability = freq / total_symbols 
        entropy -= probability * math.log2(probability)
    
    return entropy


def compute_efficiency(compressed_data,data):
    
    if not compressed_data:
        return 0
    
    encoding = math.ceil(math.log2(max(compressed_data) + 1))
    compressed_size = (len(compressed_data)+1) * encoding  
    original_size = compute_original_size(data)

    
    print("compressed_size" ,compressed_size)
    print("original_size:" ,original_size)
  
    if original_size > 0:
        return ((original_size-compressed_size) / original_size)*100
    else:
        print("original_size is zero")
        return 0
    

#text = "ABAABABBAABAABAAAABABBBBBBBB" 
text="wabbawabba"
compressed = lzw_compress(text)
print("Compressed:", compressed)

decompressed = lzw_decompress(compressed)
print("Decompressed:", decompressed)


cr = compute_cr(text, compressed)
entropy = compute_entropy(text)
efficiency = compute_efficiency(compressed,text)

print("Compression Ratio (CR):", round(cr,4))
print("Entropy:", round(entropy,4))
print("Efficiency:", round(efficiency,4),"%")