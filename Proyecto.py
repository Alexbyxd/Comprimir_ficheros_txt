from huffman import HuffmanCoding
import sys

path = "sample.txt"

h = HuffmanCoding(path)

output_path = h.compress()
print("El archivo comprimido esta en: " + output_path)

decom_path = h.decompress(output_path)
print("El archivo descomprimido esta en: " + decom_path)
