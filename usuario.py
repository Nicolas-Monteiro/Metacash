from datetime import datetime

class Usuario():
    """Representa um usuário, suas credenciais e dados financeiros."""
    def __init__(self, nome_usuario: str, senha: str, email: str, salario: float = 0.0):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
        self.salario = float(salario)
        self.gastos_fixos = 0.0
        self.gastos_alimentacao = 0.0
        self.gastos_transporte = 0.0
        self.gastos_lazer = 0.0
        self.preferencias_gastos = {'alimentacao': 3, 'lazer': 3, 'transporte': 3}
        self.meta = Meta()
        self.codigo_2fa = None
        self.codigo_2fa_expiracao = None
        self.verificado = False

    def verificar_senha(self, senha_fornecida: str) -> bool:
        return self.senha == senha_fornecida

    def to_dict(self) -> dict:
        """Converte os dados que precisam ser armazenados em um dicionário."""
        return {
            "nome_usuario": self.nome_usuario,
            "senha": self.senha,
            "email": self.email,
            "salario": self.salario,
            "gastos_fixos": self.gastos_fixos,
            "gastos_alimentacao": self.gastos_alimentacao,
            "gastos_transporte": self.gastos_transporte,
            "gastos_lazer": self.gastos_lazer,
            "preferencias_gastos": self.preferencias_gastos,
            "verificado": self.verificado,
            "meta": self.meta.to_dict()
        }

    @staticmethod
    def from_dict(nome_usuario: str, data: dict):
        """Cria uma instância de Usuário a partir de um dicionário."""
        usuario = Usuario(
            nome_usuario=nome_usuario,
            senha=data['senha'],
            email=data['email'],
            salario=data.get('salario', 0.0)
        )
        usuario.gastos_fixos = data.get('gastos_fixos', 0.0)
        usuario.gastos_alimentacao = data.get('gastos_alimentacao', 0.0)
        usuario.gastos_transporte = data.get('gastos_transporte', 0.0)
        usuario.gastos_lazer = data.get('gastos_lazer', 0.0)
        usuario.preferencias_gastos = data.get('preferencias_gastos', {'alimentacao': 3, 'lazer': 3, 'transporte': 3})
        usuario.verificado = data.get('verificado', False)
        
        meta_data = data.get('meta', {})
        usuario.meta = Meta.from_dict(meta_data)
        return usuario

    def __repr__(self):
        return f"Usuario(nome_usuario='{self.nome_usuario}', email='{self.email}')"

class Meta:
    """Representa uma meta financeira com detalhes, progresso e histórico."""
    def __init__(self, nome: str = "", valor_total: float = 0.0, prazo_dias: int = 0, progresso_atual: float = 0.0, data_inicio: str = None, historico: list = None, marcos_atingidos: list = None):
        self.nome = nome
        self.valor_total = float(valor_total)
        self.prazo_dias = int(prazo_dias)
        self.progresso_atual = float(progresso_atual)
        self.data_inicio = data_inicio
        self.historico = historico if historico is not None else []
        self.marcos_atingidos = marcos_atingidos if marcos_atingidos is not None else []

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "valor_total": self.valor_total,
            "prazo_dias": self.prazo_dias,
            "progresso_atual": self.progresso_atual,
            "data_inicio": self.data_inicio,
            "historico": self.historico,
            "marcos_atingidos": self.marcos_atingidos
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Meta(
            nome=data.get("nome", ""),
            valor_total=data.get("valor_total", 0.0),
            prazo_dias=data.get("prazo_dias", 0),
            progresso_atual=data.get("progresso_atual", 0.0),
            data_inicio=data.get("data_inicio"),
            historico=data.get("historico", []),
            marcos_atingidos=data.get("marcos_atingidos", [])
        )

    def calcular_porcentagem(self) -> float:
        if self.valor_total == 0:
            return 0.0
        return min(100.0, (self.progresso_atual / self.valor_total) * 100)

    def __repr__(self) -> str:
        return f"Meta('{self.nome}' - R${self.valor_total:.2f} em {self.prazo_dias} dias - Progresso: {self.calcular_porcentagem():.1f}%)"