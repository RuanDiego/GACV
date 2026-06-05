"""
* Autor............: Ruan Diego de Morais Bomfim
* Matricula........: 202511061
* Inicio...........: 27/04/2025
* Ultima alteracao.: 04/05/2025
* Nome.............: GACV
* Funcao...........: Carregar imagens no formado pbm e permitir a rotação usando operações com matrizes
"""

from PIL import Image

class pbm():
    def __init__(self, path=''):
        self.header = ["P1\n", "# comentario\n"]
        self.matrix = list()
        self.path = path
        
        with Image.open(self.path) as img:
            img = img.convert('1')
            self.dimentions = list(img.size)
            if (self.dimentions[0] == self.dimentions[1]):
                self.quadradicity = True
            else:
                self.quadradicity = False

            for y in range(self.dimentions[1]):
                linha = []
                for x in range(self.dimentions[0]):
                    pixel = img.getpixel((x, y))
                    if pixel == 0:
                        linha.append('1')
                    else:
                        linha.append('0')
                self.matrix.append(linha)

    def transponse(self):
        matrix_ = [list() for x in range(len(self.matrix[0]))]

        for line in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                # print(len(self.matrix[0]))
                matrix_[col].append(self.matrix[line][col])
        
        # Se a matrix não for quadrada, é necessário inverter também as dimensões
        if (not self.quadradicity):
            self.dimentions = [self.dimentions[1], self.dimentions[0]]

        self.matrix = matrix_

    def mirror(self):
        matrix_ = list()
        for line in range(len(self.matrix)):
            line_ = list()
            for col in range(len(self.matrix[0])):
                # print(col, line)
                line_.append(self.matrix[line][len(self.matrix[0])-1-col])
            matrix_.append(line_)

        self.matrix = matrix_

    def rotate90DegreesRight(self):
        self.transponse()
        self.mirror()
    
    def rotate90DegreesLeft(self):
        self.mirror()
        self.transponse()

    def printMatrix(self):
        # print(self.matrix)
        for line in self.matrix:
            print(line)
    
    def getMatrix(self):
        # organização das dimensões no padrão pbm
        dimentions_ = [str(self.dimentions[0]) + ' ' + str(self.dimentions[1]) + '\n']
        
        # construção da matriz no padrão pbm
        matrix_ = self.matrix.copy()
        for index, line in enumerate(matrix_):
            matrix_[index] = ''.join(line) + '\n'

        return (self.header + dimentions_ + matrix_)

    def save(self, path=''):
        # registrando mudanças no arquivo
        with open(path, "w", encoding="utf8") as file:
            file.writelines(self.getMatrix())
        
if __name__ == "__main__":
    img = pbm("converted_image.pbm")
    img.transponse()
