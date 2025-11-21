from flask import jsonify
import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'static', 'json', 'estados.json')

def validar_estado(estado):
    if not estado:
        return False
    
    try:
        with open(JSON_PATH, encoding='utf-8') as f:
            data = json.load(f)
        estados = [item['sigla'] for item in data.get('estados', [])]
        return estado in estados
    except Exception as e:
        return False


def validar_cidade(estado, cidade):
    if not estado or not cidade:
        return False
    
    try:
        with open(JSON_PATH, encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data['estados']:
            if item['sigla'] == estado:
                cidades = item.get('cidades', [])
                return cidade in cidades
        return False
    except Exception as e:
        return False

def validar_senha(senha):
    if not senha:
        return False
        
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Z]', senha):
        return False
    if not re.search(r'[a-z]', senha):
        return False
    if not re.search(r'\d', senha):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    return True


def validar_numero_celular(num_celular):
    if not num_celular or not num_celular.strip():
        return False
        
    num_celular = re.sub(r'[^\d]', '', num_celular)

    if len(num_celular) != 11:
        return False

    try:
        ddd = int(num_celular[:2])
        if ddd < 11 or ddd > 99:
            return False
    except ValueError:
        return False

    if num_celular[2] != '9':
        return False
    return True

def validar_numero_fixo(num_fixo):
    if not num_fixo or not num_fixo.strip():
        return False
        
    num_fixo = re.sub(r'[^\d]', '', num_fixo)

    if len(num_fixo) != 10:
        return False

    # Validar DDD (deve estar entre 11 e 99)
    try:
        ddd = int(num_fixo[:2])
        if ddd < 11 or ddd > 99:
            return False
    except ValueError:
        return False
        
    return True

def validar_email(email):
    if not email or not email.strip():
        return False
        
    email = email.strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False
    return True

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True
    
def validar_tipo_sanguineo(tipo):
    tipos_validos = {' ', '', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}
    return tipo in tipos_validos
    
def validar_apenas_letras(campo):
    if not campo:
        return False
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', campo):
        return False
    return True

def validar_apenas_numeros(campo):
    if not campo:
        return False
    if not re.match(r'^[0-9]+$', campo):
        return False
    return True

def validar_cep(cep):
    if not cep or not cep.strip():
        return False
    # Remove hífen e espaços
    cep_limpo = re.sub(r'[^\d]', '', cep)
    # CEP deve ter exatamente 8 dígitos
    if len(cep_limpo) != 8:
        return False
    return True

def validar_data_nascimento(data_nascimento):
    if not data_nascimento or not data_nascimento.strip():
        return False
    try:
        data_obj = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        data_atual = datetime.now().date()
        
        if data_obj > data_atual:
            return False
        
        return True
    except ValueError:
        return False
        
    