import datetime
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import func
from ..extensions import db, scheduler
from ..models import Fotografia, Modelo


# Funções para treinamento periódico dos modelos.
@scheduler.task("cron", id="treina_modelos", week="*", day_of_week="mon", hour=5, minute=30)
def treina_modelos():
    MINIMO = 100

    with scheduler.app.app_context():

        # Verificar se há novos dados para treinar os modelos.
        query = db.select(func.count(Fotografia.id)).filter_by(knn_index=None)
        novos = db.session.execute(query).scalar()
        
        # Se houver menos do que X novos registros, não treinar.
        if novos < MINIMO:
            return
        
        
        # Obter dataset completo: as colunas id e emb128 de todos os registros.
        query = db.select(Fotografia.id, Fotografia.emb128)
        dataset = db.session.execute(query).fetchall()
        
        
        # Prepara o dataset para treinamento e atualiza o índice KNN de cada registro.
        X = []
        for i, row in enumerate(dataset):
            id, embedding = row
            X.append(embedding)
            query = db.update(Fotografia).where(Fotografia.id == id).values(knn_index=i)
            db.session.execute(query)

        
        # Treinar modelo KNN.
        params = {
            "algorithm": "auto",
            "leaf_size": 30,
            "metric": "minkowski",
            "metric_params": None,
            "n_jobs": None,
            "n_neighbors": 1,
            "p": 2,
            "radius": 1.0
        }
        knn_model = NearestNeighbors(**params)
        knn_model.fit(X)
        # Salvar o modelo KNN treinado no Postgres.
        modelo = Modelo()
        modelo.algoritmo = "KNN"
        modelo.modelo = knn_model
        modelo.created_at = datetime.datetime.now()
        modelo.updated_at = datetime.datetime.now()
        db.session.add(modelo)
        db.session.commit()
