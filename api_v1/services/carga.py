# ---------------------------------------------------------------------------------------
#    Serviço de carga de imagens no banco de dados.
#    O serviço é executado semanalmente.
#    Ele segue os seguintes passos:
#        1. Obtem a lista de pessoas da API de Usuários da PCSC
#        2. Obtem as fotos de CNH da API do CIASC
#        4. Extrai os embeddings das fotos
#        5. Salva as fotos no banco de dados PostgreSQL
# ---------------------------------------------------------------------------------------

import io
import base64
import face_recognition

from ..extensions import db, scheduler
from ..models.fotografia import Fotografia

# ---------------------------------------------------------------------------------------
# Token da API_USUARIOS
#     Esta função é responsável por obter o token da API de Usuários
# ---------------------------------------------------------------------------------------
def get_token_api_usuarios():
    token = None
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    return token


# ---------------------------------------------------------------------------------------
# Token da API_CIASC
#     Esta função é responsável por obter o token da API do CIASC
#     Primeiro ...
#     Se não existir, ela faz uma requisição para a API do CIASC
#     Depois verifica se o token está expirado
#     Se estiver expirado, ela faz uma requisição para a API do CIASC
# ---------------------------------------------------------------------------------------
def get_token_api_ciasc():
    token = None
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    return token


# ---------------------------------------------------------------------------------------
# Função para buscar a lista de pessoas na API da PCSC
# ---------------------------------------------------------------------------------------
def get_pessoas():
    pessoas = []
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    return pessoas


# ---------------------------------------------------------------------------------------
# Função para buscar uma fotografia na API do CIASC através de um CPF
#
# Payload da API da CIASC: ['CodRetorno', 'DescRetorno', 'DataAquisicao', 'Imagem']
# Retorno desta função: {'foto64': '', 'DataAquisicao': ''}
# ---------------------------------------------------------------------------------------
def get_foto_cnh(cpf):
    foto = {'foto64': '', 'DataAquisicao': ''}
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
    return foto


# ---------------------------------------------------------------------------------------
#     Esta função é responsável por orquestrar a obtenção das imagens de CNH das pessoas
#     da API de Usuários da PCSC. Ela faz o seguinte:
#         1. Obtem a lista de pessoas da API de Usuários da PCSC
#         2. Obtem as fotos de CNH da API do CIASC
#         3. Salva as fotos no banco de dados PostgreSQL
# ---------------------------------------------------------------------------------------
@scheduler.task("cron", id="carga_cnh", week="*", day_of_week="mon", hour=2, minute=30)
def carga_cnh():
    with scheduler.app.app_context():

        # Obtem lista de policiais na ativa da API de Usuários da PCSC
        pessoas = get_pessoas()

        
        # Obtendo as fotos de CNH da API do CIASC e salvando no PostgreSQL
        inseridos = 0

        for pessoa in pessoas:

            foto = get_foto_cnh(pessoa['cpf'])
            
            if foto:
                # Verificar se já existe uma foto para esta pessoa com a mesma data de aquisição
                query = db.select(Fotografia).filter_by(
                            cpf=pessoa['cpf'],
                            dt_aquisicao=foto['DataAquisicao']
                        )
                result = db.session.execute(query).first()

                if result:
                    continue

                
                # Extração de embeddings
                try:
                    img_decoded = base64.b64decode(foto['foto64'])
                    img_file = io.BytesIO(img_decoded)
                    img = face_recognition.load_image_file(img_file)
                    embeddings = face_recognition.face_encodings(img)[0].tolist()
                except:
                    embeddings = None

                
                if embeddings:
                    # Salvar no banco de dados
                    fotografia = Fotografia()
                    fotografia.origem = 'CNH'
                    fotografia.dt_aquisicao = foto['DataAquisicao']
                    fotografia.cpf = pessoa['cpf']
                    fotografia.nome = pessoa['nome']
                    fotografia.base64 = foto['foto64']
                    fotografia.emb128 = embeddings
                    
                    db.session.add(fotografia)
                    db.session.commit()
                    
                    inseridos += 1
