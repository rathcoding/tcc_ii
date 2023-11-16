from functools import wraps
from flask import jsonify, request
import requests
import json

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA
        # TRECHO DE CÓDIGO SUPRIMIDO POR SEGURANÇA

        # Se o token for válido, o usuário for policial ativo no sistema, continua...
        return f(*args, **kwargs)
    
    return decorated

