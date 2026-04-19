import cv2 as cv2
import numpy as numpy
from pathlib import Path
from datetime import date
from re import search, IGNORECASE
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pandas.core.interchange.dataframe_protocol import DataFrame

# FIXME: Ajustar se necessário
templates_cracha = {
    "frente": "templates/cracha_frente.png",
    "verso": "templates/cracha_verso.png"
}

def crop_face(image_path: str, factor=1.7):

    # Carregar o modelo de detecção de face baseado em Caffe
    prototxt_path = "models/deploy.prototxt.txt"
    model_path = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"

    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    # Carregar a imagem usando o PIL
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)

    # Converter a imagem para o formato do OpenCV (BGR)
    cv_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

    # Obter as dimensões da imagem
    (h, w) = cv_image.shape[:2]

    # Redimensionar a imagem para 300x300 pixels e preparar a blob para a rede neural
    blob = cv2.dnn.blobFromImage(cv_image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)

    # Executar a detecção
    detections = net.forward()

    # Verificar se ao menos uma face foi detectada
    if detections.shape[2] > 0:

        # Assumindo que a primeira detecção é a face de interesse (você pode ajustar isso)
        i = 0
        confidence = detections[0, 0, i, 2]

        # Definir um limiar de confiança para filtrar detecções fracas
        if confidence > 0.5:

            # Obter as coordenadas da bounding box da face detectada
            box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")

            # Calcular o centro e o tamanho para recorte com o fator desejado
            center_x = x + (x1 - x) // 2
            center_y = y + (y1 - y) // 2
            size = int(max(x1 - x, y1 - y) * factor)
            x_new = max(0, center_x - size // 2)
            y_new = max(0, center_y - size // 2)

            # Fazer o recorte da face com proporção 1:1
            cropped_head = cv_image[y_new:y_new + size, x_new:x_new + size]

            # Converter o recorte de volta para o formato PIL
            cropped_head_pil = Image.fromarray(cv2.cvtColor(cropped_head, cv2.COLOR_BGR2RGB))

            return cropped_head_pil

    # Caso não tenha detecção, retorna None
    return None


def generate_cracha(dataframe: DataFrame):

    try:

        for index, row in dataframe.iterrows():

            erro = False
            matricula = None

            for tipo_template, template_cracha in templates_cracha.items():

                try:
                    image = Image.open(template_cracha)

                except FileNotFoundError:
                    raise FileNotFoundError(f"Matricula: '{matricula}', Funcionario: '{nome_completo}'  --->  Template de cracha não encontrado no diretorio: '{template_cracha}'")

                width, height = image.size

                data_emissao = date.today()
                data_emissao = data_emissao.strftime("%d/%m/%Y")

                cargo = dataframe.loc[index, 'cargo']
                matricula = dataframe.loc[index, 'matricula']

                nome_completo = dataframe.loc[index, 'nome']

                partes_nome = nome_completo.split()
                primeiro_nome = partes_nome[0]

                if not data_emissao or not cargo or not matricula or not nome_completo or not primeiro_nome:
                    erro = True
                    print(f"Matricula: '{matricula}', Funcionario: '{nome_completo}'  --->  Erro no preenchimento na planilha. Por favor, verifique os dados")
                    break

                elif len(nome_completo) > 30:
                    erro = True
                    print(f"Matricula: '{matricula}', Funcionario: '{nome_completo}'  --->  Nome completo maior que 48 caracteres. Necessario abreviacao manual")
                    break

                # FIXME: Ajustar se necessário
                dados_servidor = {
                    "frente": {
                        "foto_servidor_frente": {
                            "caminho": f"faces/{matricula}.jpg",
                            "x_offset": 0,
                            "y_offset": 400,
                            "size": (360, 360)
                        },
                        "nome_servidor_frente": {
                            "texto": primeiro_nome,
                            "tamanho_fonte": 55,
                            "tipo_fonte": "fonts/arial_bold.ttf",
                            "x_offset": 0,
                            "y_offset": 740
                        },
                        "cargo_servidor_frente": {
                            "texto": cargo,
                            "tamanho_fonte": 35,
                            "tipo_fonte": "fonts/arial_narrow_bold.ttf",
                            "x_offset": 0,
                            "y_offset": 810
                        }
                    },
                    "verso": {
                        "nome_servidor_verso": {
                            "texto": nome_completo,
                            "tamanho_fonte": 35,
                            "tipo_fonte": "fonts/arial_narrow_bold.ttf",
                            "x_offset": 0,
                            "y_offset": 220
                        },
                        "matricula_servidor_verso": {
                            "texto": matricula,
                            "tamanho_fonte": 35,
                            "tipo_fonte": "fonts/arial_narrow_bold.ttf",
                            "x_offset": 0,
                            "y_offset": 365
                        },
                        "data_emissao_verso": {
                            "texto": data_emissao,
                            "tamanho_fonte": 35,
                            "tipo_fonte": "fonts/arial_narrow_bold.ttf",
                            "x_offset": -180,
                            "y_offset": 805
                        }
                    }
                }

                # Configurar a posição inicial para o texto
                for nome_campo, campo in dados_servidor.get(tipo_template).items():

                    caminho = campo.get('caminho')

                    if nome_campo == 'foto_servidor_frente':

                        # Carregar a imagem do rosto
                        try:
                            face_image = crop_face(caminho)

                        except FileNotFoundError:
                            raise FileNotFoundError(f"Matricula: '{matricula}', Funcionario: '{nome_completo}'  --->  Imagem de rosto '{caminho}' nao foi encontrada nesse diretorio")

                        # Recortar a região do rosto
                        face_image = face_image.resize(campo.get('size'))

                        # Obtenha as dimensões da imagem do template e da imagem do rosto
                        template_width, template_height = image.size
                        face_width, face_height = face_image.size

                        # Calcular posição x e y centralizadas com offset ajustado
                        x = (template_width - face_width) / 2 + campo.get('x_offset')  # Ajuste horizontal com centralização
                        y = campo.get('y_offset') - (face_height / 2)  # Ajuste vertical com centralização

                        # Criar uma nova imagem vazia com o mesmo tamanho do template
                        base_image = Image.new('RGBA', image.size, (255, 255, 255, 0))  # Fundo transparente

                        # Colar a imagem do rosto na nova imagem vazia
                        base_image.paste(face_image, (int(x), int(y)))

                        # Sobrepor o layout do crachá por cima da nova imagem com a foto
                        base_image = Image.alpha_composite(base_image, image.convert('RGBA'))

                        # Agora a base_image contém a foto e o layout do crachá sobrepostos
                        image = base_image.convert('RGB')  # Converte de volta para RGB se não precisar de transparência

                    else:

                        draw = ImageDraw.Draw(image)

                        try:
                            fonte = ImageFont.truetype(
                                campo.get('tipo_fonte'),
                                campo.get('tamanho_fonte')
                            )

                        except IOError:
                            fonte = ImageFont.load_default()

                        # Calcular o bounding box do texto
                        bbox = draw.textbbox((0, 0), campo.get('texto'), font=fonte)

                        # Largura e altura do texto a partir do bounding box
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]

                        # Calcular posição x e y centralizadas com offset ajustado
                        x = (width - text_width) / 2 + campo.get('x_offset')  # Centraliza horizontalmente com ajuste de offset
                        y = campo.get('y_offset') - (text_height / 2)  # Ajuste vertical com centralização

                        # Desenhar o texto na posição calculada
                        draw.text((x, y), campo.get('texto'), font=fonte, fill="black")

                # Salvar a imagem modificada
                Path("output").mkdir(parents=True, exist_ok=True)

                output_path = f"output/{dataframe.loc[index, 'matricula']}_{tipo_template}.png"
                image.save(output_path)

            if not erro:
                print(f"Matricula: '{matricula}', Funcionario: '{nome_completo}'  --->  Cracha gerado com sucesso")

    except FileNotFoundError as e:
        print(e)
