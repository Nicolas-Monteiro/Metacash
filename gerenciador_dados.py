import json
from modelos import Usuario

class GerenciadorDeDados:
    """Realiza as operações que precisam de acesso ao arquivo Json"""
    def __init__(self, caminho_arquivo:str = "dados_usuarios.json"):
        self.caminho_arquivo = caminho_arquivo

    def _carregar_dados_usuario(self) -> dict:
        """Carrega os dados do usuario para leitura"""
        try:
            with open(self.caminho_arquivo, "r", encoding= "utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def _salvar_dados_usuario(self, dados:dict) -> bool:
        """Salva os dados em um dicionário Json"""
        try:
            with open(self.caminho_arquivo, "w", encoding= "utf-8") as f:
                json.dump(dados, f, indent= 4)
            return True
        except (IOError, OSError, TypeError) as e:
            print(f"Erro ao salvar dados: {e}")
            return False
        
    def encontrar_usuario(self, nome_usuario: str) -> Usuario | None:
        """Encontra um nome de usuário específico e retorna esse nome"""
        dados = self._carregar_dados_usuario()
        dados_usuario = dados.get(nome_usuario.lower())
        if dados_usuario:
            return Usuario.from_dict(nome_usuario, dados_usuario)
        return None
    
    def salvar_usuario(self, usuario:Usuario):
        """Salva um usuário no arquivo Json"""
        dados = self._carregar_dados_usuario()
        dados[usuario.nome_usuario.lower()] = usuario.to_dict()
        self._salvar_dados_usuario(dados)

    def deletar_usuario(self, nome_usuario: str) -> bool:
        """Deleta um usuário do arquivo Json e salva a alteração."""
        dados = self._carregar_dados_usuario()
        nome_usuario_lower = nome_usuario.lower()
        if nome_usuario_lower in dados:
            del dados[nome_usuario_lower]
            # CORREÇÃO CRÍTICA: Salva o dicionário modificado de volta para o ficheiro JSON.
            return self._salvar_dados_usuario(dados)
        return False

    def email_existe(self, email: str) -> bool:
        """Verifica se o email já existe no arquivo"""
        dados = self._carregar_dados_usuario()
        for dados_usuario in dados.values():
            if dados_usuario.get("email", "").lower() == email.lower():
                return True
        return False
