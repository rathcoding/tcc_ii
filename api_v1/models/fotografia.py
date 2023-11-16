from ..extensions import db
import uuid

class Fotografia (db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knn_index = db.Column(db.Integer())
    origem = db.Column(db.String())
    dt_aquisicao = db.Column(db.DateTime())
    cpf = db.Column(db.String(11))
    nome = db.Column(db.String())
    base64 = db.Column(db.Text())
    emb128 = db.Column(db.PickleType())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())
