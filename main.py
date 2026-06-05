"""
* Autor............: Ruan Diego de Morais Bomfim
* Matricula........: 202511061
* Inicio...........: 27/04/2025
* Ultima alteracao.: 04/05/2025
* Nome.............: GACV
* Funcao...........: Carregar imagens no formado pbm e permitir a rotação usando operações com matrizes
"""

import io
import os
import traceback
from PIL import Image
import FreeSimpleGUI as sg
from back import *
TEMP_FILE = 'temp.pbm'

image_ = Image.new(mode="RGB", size=(1, 1), color="#64778d")
with io.BytesIO() as output_:
    image_.save(output_, format="PNG")
    data_ = output_.getvalue()

layout_btn = [
    [sg.Button("90° à esquerda", key="--90DEGREELEFT--"), sg.Button("90° à direita", key="--90DEGREERIGHT--"), sg.Button("Girar 180° e espelhar", key="--180DEGREEMIRROR--"), sg.Button("Girar 180°", key="--180DEGREE--")],
    [sg.Button("Espelhar", key="--MIRROR--"), sg.Button("90° à direita e espelhar", key="--90DEGREERIGHTMIRROR--"), sg.Button("Forma original", key='--ORIGINAL--'), sg.Button("90° à esquerda e espelhar", key="--90DEGREELEFTMIRROR--")],
    ]

layout_header = [
    [sg.Column([[sg.Image(data=data_, key="--IMG1--")]], justification="center")],
    [sg.Text("Caminho"), sg.Input(key="--EXPLORER--", enable_events=True)],
    [sg.FileBrowse("Explorador de arquivos", target='--EXPLORER--')],
]

layout_img = [
    [sg.Column(layout_header, element_justification='center', justification='center')],
    [sg.Column(layout_btn, element_justification="center", justification='center')],
    [sg.Column([[sg.Image(data=data_, key="--IMG2--")]], justification="center")],
    ]

layout_matrix = [
    [sg.Multiline(size=(80, 25), key='--FIRSTMATRIX--', font='Calibri 8')],
    [sg.Multiline(size=(80, 25), key='--SECONDMATRIX--', font='Calibri 8')],
]

layout = [
    [sg.Column(layout_matrix), sg.Column(layout_img)],
]

window = sg.Window("GACV", layout, element_justification="center", text_justification="center", location=(20, 20))
# print()

while True:

    event, values = window.Read()
    
    # print(event, values)

    if (event == None):
        window.Close()
        if (TEMP_FILE in os.listdir(os.getcwd())):
            os.remove(TEMP_FILE)
        break
    elif (event == "--EXPLORER--" and values["--EXPLORER--"].strip() != ''):
        image = Image.open(values["--EXPLORER--"])
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            data = output.getvalue()
            window["--IMG1--"].Update(data=data)
    else:
        try:
            img = pbm(values["--EXPLORER--"])
            window['--FIRSTMATRIX--'].Update(''.join(img.getMatrix()))
            # Forma original não precisa de condicional, apenas é necessário apresentar a imagem sem aplicar nenhuma alteração
            if (event == "--90DEGREERIGHT--"):
                img.rotate90DegreesRight()
            elif (event == "--90DEGREELEFT--"):
                img.rotate90DegreesLeft()
            elif (event == "--MIRROR--"):
                img.mirror()
            elif (event == "--TRANSPOSE--"):
                img.transposta()
            elif (event == "--180DEGREEMIRROR--"):
                img.rotate90DegreesRight()
                img.rotate90DegreesRight()
                img.mirror()
            elif (event == "--180DEGREE--"):
                img.rotate90DegreesRight()
                img.rotate90DegreesRight()
            elif (event == "--90DEGREELEFTMIRROR--"):
                img.rotate90DegreesLeft()
                img.mirror()
            elif (event == "--90DEGREERIGHTMIRROR--"):
                img.rotate90DegreesRight()
                img.mirror()
            img.save(path=TEMP_FILE)
            image = Image.open(TEMP_FILE)
            with io.BytesIO() as output:
                image.save(output, format="PNG")
                data = output.getvalue()
                window["--IMG2--"].Update(data=data)
            window['--SECONDMATRIX--'].Update(''.join(img.getMatrix()))
        except Exception as exc:
            # traceback.print_exception(exc)
            pass
