from ..extensions import db
import uuid

class Modelo (db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    algoritmo = db.Column(db.String(255))
    modelo = db.Column(db.PickleType())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())
