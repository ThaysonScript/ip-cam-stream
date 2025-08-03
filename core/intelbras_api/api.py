import hashlib
import logging
import random
import re
import sys

import requests


class Api:
    def __init__(self):
        pass
    
    
    def enable_debug(self):
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger('pyintelbras')
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)
    
    
    def __extract_digest_info(self, www_authenticate):
        """Extrai realm, nonce, opaque, qop do header WWW-Authenticate"""
        fields = {}
        for key in ['realm', 'nonce', 'opaque', 'qop']:
            match = re.search(rf'{key}="([^"]+)"', www_authenticate)
            if match:
                fields[key] = match.group(1)
        return fields
    
    
    def __compute_digest_auth(self, method, uri, username, password, digest_info, nc='00000001'):
        """Calcula cabeçalho Digest Authorization manualmente"""
        cnonce = ''.join(random.choices('abcdef0123456789', k=16))

        ha1_str = f"{username}:{digest_info['realm']}:{password}"
        ha1 = hashlib.md5(ha1_str.encode()).hexdigest()

        ha2_str = f"{method}:{uri}"
        ha2 = hashlib.md5(ha2_str.encode()).hexdigest()

        response_str = f"{ha1}:{digest_info['nonce']}:{nc}:{cnonce}:{digest_info['qop']}:{ha2}"
        response_hash = hashlib.md5(response_str.encode()).hexdigest()

        # Monta o cabeçalho Authorization
        auth_header = (
            f'Digest username="{username}", realm="{digest_info["realm"]}", '
            f'nonce="{digest_info["nonce"]}", uri="{uri}", '
            f'response="{response_hash}", opaque="{digest_info["opaque"]}", '
            f'qop={digest_info["qop"]}, nc={nc}, cnonce="{cnonce}"'
        )
        return auth_header
    
    
    def get_with_digest(self, url, username, password):
        """Executa GET com autenticação Digest para uma URL"""
        method = "GET"
        parsed_uri = requests.utils.urlparse(url).path + ('?' + requests.utils.urlparse(url).query if requests.utils.urlparse(url).query else '')

        # Etapa 1: requisição inicial para obter nonce etc.
        r1 = requests.get(url)
        if 'WWW-Authenticate' not in r1.headers:
            print("Servidor não respondeu com Digest.")
            return r1

        digest_info = self.__extract_digest_info(r1.headers['WWW-Authenticate'])

        # Etapa 2: monta e envia cabeçalho Authorization
        headers = {
            "Authorization": self.__compute_digest_auth(method, parsed_uri, username, password, digest_info),
            "User-Agent": "PythonManualDigest/1.0"
        }
        r2 = requests.get(url, headers=headers)
        return r2