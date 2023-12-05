""" CODIFICACION HUFFMAN """

import heapq
import os


class CodigoHuffman:
    """Clase para operaciones de codificacion y decodificaion Huffman"""

    def __init__(self, ruta):
        self.ruta = ruta  # tomara el valor de la ruta
        self.heap = []
        self.codigo = {}  # iniciar codigo vacio
        self.mapa = {}  # iniciar mapa vacio

    class NodoHeap:
        """Clase que inicializa el nodo de monticulo principal"""

        def __init__(self, char, frecuencia):
            self.char = char
            self.frecuencia = frecuencia
            self.izq = None
            self.der = None

        # definimos los comparadores
        def __lt__(self, otro):
            # comparamos las freciencias
            return self.frecuencia < otro.frecuencia

        # compara las instancias
        def __eq__(self, otro):
            if otro == None:
                return False
            if not isinstance(otro, NodoHeap):
                return False
            return self.frecuencia == otro.frecuencia

    # funciones de compresion
    def diccionario_frec(self, texto):
        """Funcion que crea el diccionario de las frecuencia"""
        frecuencia = {}
        for caracter in texto:
            if not caracter in frecuencia:
                frecuencia[caracter] = 0
            frecuencia[caracter] += 1
        return frecuencia

    def hacer_heap(self, frecuencia):
        """Creamos los heap de nodos"""
        for key in frecuencia:
            nodo = self.NodoHeap(key, frecuencia[key])
            heapq.heappush(self.heap, nodo)

    def fusionar_nodos(self):
        """Funcion para fusionar los nodos heap"""
        while len(self.heap) > 1:
            nodo1 = heapq.heappop(self.heap)
            nodo2 = heapq.heappop(self.heap)

            fusionado = self.NodoHeap(None, nodo1.frecuencia + nodo2.frecuencia)
            fusionado.izq = nodo1
            fusionado.der = nodo2

            heapq.heappush(self.heap, fusionado)

    def generar_cod_huffman(self, nodo_actual, codigo_actual):
        """Funcion para generar el codigo huffman"""
        if nodo_actual == None:
            return

        if nodo_actual.char != None:
            self.codigo[nodo_actual.char] = codigo_actual
            self.mapa[codigo_actual] = nodo_actual.char
            return

        self.generar_cod_huffman(nodo_actual.izq, codigo_actual + "0")
        self.generar_cod_huffman(nodo_actual.der, codigo_actual + "1")

    def hacer_codigo(self):
        """Inicializamos el cod huffman"""
        nodo_actual = heapq.heappop(self.heap)
        codigo_actual = ""
        self.generar_cod_huffman(nodo_actual, codigo_actual)

    def codificar_texo(self, texto):
        """Funcion para tomar un texto y codificarlo"""
        texto_codificado = ""
        for caracter in texto:
            texto_codificado += self.codigo[caracter]
        return texto_codificado

    def imprimir_codigo_huffman(self):
        """Funcion para imprimir codigo"""
        print("Codigos de Huffman:")
        for char, code in self.codigo.items():
            print(f"Caracter: {char}, Codigo: {code}")

    def mostrar_byte(self, texto_original, texto_comprimido):
        print("\nBytes iniciales")
        bytes_iniciales = [ord(byte) for byte in texto_original]
        print(f"Total de bytes iniciales: {len(bytes_iniciales)} bytes")
        print("\nBytes comprimidos")
        bytes_comprimidos = [byte for byte in texto_comprimido]
        print(f"Total de bytes comprimidos: {len(bytes_comprimidos)}  bytes")
        print("--------------------------------------------------------------")

    def rellenar_codigo(self, texto_codificado):
        """Funcion para rellenar y hacerlo multiplo de 8"""
        relleno_extra = 8 - len(texto_codificado) % 8
        for i in range(relleno_extra):
            texto_codificado += "0"

        relleno_info = "{0:08b}".format(relleno_extra)
        texto_codificado = relleno_info + texto_codificado
        return texto_codificado

    def convertir_byte_array(self, texto_codificado):
        """Funcion para convertir a array byte"""
        if len(texto_codificado) % 8 != 0:
            print("Texto codificado con relleno incorrecto")
            exit(0)

        b = bytearray()
        for i in range(0, len(texto_codificado), 8):
            byte = texto_codificado[i : i + 8]
            b.append(int(byte, 2))
        return b

    def comprimido(self):
        """Funcion para implementar cod. Huffman"""
        nombreArchivo, file_extension = os.path.splitext(self.ruta)
        salida = nombreArchivo + ".bin"

        with open(self.ruta, "r+") as archivo, open(salida, "wb") as output:
            text = archivo.read()
            text = text.rstrip()

            frequency = self.diccionario_frec(text)
            self.hacer_heap(frequency)
            self.fusionar_nodos()
            self.hacer_codigo()
            self.imprimir_codigo_huffman()

            encoded_text = self.codificar_texo(text)
            padded_encoded_text = self.rellenar_codigo(encoded_text)

            b = self.convertir_byte_array(padded_encoded_text)
            output.write(bytes(b))

            texto_original = text.encode("utf-8")
            texto_comprimido = bytes(b)

            self.mostrar_byte((texto_original.decode("utf-8")), texto_comprimido)

        print("Comprimido")
        return salida

    def remover_relleno(self, texto_codificado):
        """Funcionpara remover el relleno de la codificacion"""
        relleno_info = texto_codificado[:8]
        relleno_extra = int(relleno_info, 2)

        texto_codificado = texto_codificado[8:]
        texto_cod = texto_codificado[: -1 * relleno_extra]

        return texto_cod

    def decodificar_texto(self, texto_codificado):
        """Funcion para decodificar el texto"""
        codigo_actual = ""
        texto_codificado = ""
        for bit in texto_codificado:
            codigo_actual += bit
            if codigo_actual in self.mapa:
                caracter = self.mapa[codigo_actual]
                texto_codificado += caracter
                codigo_actual = ""

        return texto_codificado

    def descomprimir(self, ruta_entrada):
        nombre_archivo, file_extension = os.path.splitext(self.ruta)
        ruta_salida = nombre_archivo + "_descomprimido" + ".txt"

        with open(ruta_entrada, "rb") as archivo, open(ruta_salida, "w") as output:
            bit_cadena = ""

            byte = archivo.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, "0")
                bit_cadena += bits
                byte = archivo.read(1)

            texto_codificado = self.remover_relleno(bit_cadena)

            texto_descomprimido = self.decodificar_texto(texto_codificado)

            output.write(texto_descomprimido)

        print("Descomprimido")
        return ruta_salida
