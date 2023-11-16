
# """
# Este módulo exporá o endpoint para identificar pessoas em fotos.
# """
from flask import Blueprint, jsonify, request
from ..utils import verify_token
from ..models import Modelo, Fotografia
from ..extensions import db
import io
import face_recognition
import base64

identifica = Blueprint('identifica', __name__)


# ============================================================
# Identifica uma pessoa em uma imagem:
# - Recebe:
#     - "imagem": a foto em base64 contendo somente um rosto
# - Retorna:
#     - "resultado": lista dos 3 indivíduos mais semelhantes semelhantes
#         - "cpf": CPF do indivíduo
#         - "nome": Nome do indivíduo
#         - "similaridade": Similaridade com a pessoa da foto
# ============================================================
@identifica.route('/identifica', methods=['POST'])
@verify_token
def identifica_pessoa():

    try:
        req = request.get_json(force=True)
        img_base64 = req.get('imagem', None)
    except:
        return jsonify({'message': 'Erro ao tentar obter imagem da requisição.'}), 400

    if not img_base64:
        return jsonify({'message': 'Imagem não fornecida.'}), 400


    # Decodificando imagem em Base64 e abrindo com face_recognition
    try:
        img_decoded = base64.b64decode(img_base64)
        img_file = io.BytesIO(img_decoded)
        img = face_recognition.load_image_file(img_file)
    except:
        return jsonify({'message': 'Erro ao tentar decodificar a imagem.'}), 400


    
    # Encontra localização do rostos na imagem.
    try:
        boxes = face_recognition.face_locations(img, model='cnn')
    except:
        return jsonify({'message': 'Erro ao tentar encontrar rostos na imagem.'}), 400

    if not boxes:
        return jsonify({'message': 'Nenhum rosto encontrado na imagem.'}), 400

    if len(boxes) > 1:
        return jsonify({'message': 'Mais de um rosto encontrado na imagem. Máximo permitido: 01'}), 400



    # Extrai os embeddings do rosto encontrado na imagem
    try:
        embeddings = face_recognition.face_encodings(img, boxes)
    except:
        return jsonify({'message': 'Erro ao tentar extrair pontos para reconhecimento de rostos.'}), 500

    if not embeddings:
        return jsonify({'message': 'Não foi possível extrair pontos suficientes para reconhecimento de rostos.'}), 500



    # Busca no banco de dados o Modelo treinado com o algoritmo KNN com a data mais recente.
    try:
        query = db.select(Modelo.modelo).filter_by(algoritmo='KNN').order_by(Modelo.updated_at.desc()).limit(1)

        modelo = db.session.execute(query).scalar()
        
    except:
        return jsonify({'message': 'Erro ao tentar obter modelo KNN no banco de dados.'}), 500

    # Se não encontrar, retorna erro 500
    if not modelo:
        return jsonify({'message': 'Nenhum modelo encontrado na base de dados.'}), 500
    


    # Predição com o modelo KNN
    try:
        result = modelo.kneighbors(embeddings, n_neighbors=3, return_distance=True)
    except:
        return jsonify({'message': 'Erro ao tentar encontrar pessoas semelhantes.'}), 500


    # Itera sobre os resultados e monta o JSON de retorno
    # D = array de array com distâncias
    # I = array de array com índices (index_knn)
    D, I = result

    resultado = []

    for distancia, knn_index in zip(D[0], I[0]):

        # Busca fotografia da base de dados através do knn_index
        try:
            query = db.select(Fotografia).filter_by(knn_index=int(knn_index)).limit(1)
            fotografia = db.session.execute(query).scalar()
        except:
            fotografia = None

        if fotografia:
            pessoa = {}
            pessoa['cpf'] = fotografia.cpf
            pessoa['nome'] = fotografia.nome
            pessoa['similaridade'] = (1 - distancia)
            resultado.append(pessoa)
    
    json = {'resultado': resultado}

    return jsonify(json), 200

