"""
PROYECTO INF 2610
COMPRESION DE FICHEROS
Autor: Baltazar Castellón Alex
"""


from huffman import CodigoHuffman
import sys

entrada = "sample.txt"

h = CodigoHuffman(entrada)
ruta_salida = h.comprimido()
print("El archivo comprimido esta en: " + ruta_salida)

ruta_descom_salida = h.descomprimir(ruta_salida)
print("El archivo descomprimido esta en: " + ruta_descom_salida)
