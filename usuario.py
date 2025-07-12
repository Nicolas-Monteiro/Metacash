class Usuario():
    """Representa um usuário e suas credenciais e estado temporário de autenticação"""
    def __init__ (self, nome_usuario: str, senha:str, email:str, salario: float = 0.0):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
        self.salario = float(salario)
        self.gastos_fixos = 0.0
        self.preferencias_gastos = {'alimentacao': 3, 'lazer': 3, 'transporte': 3}
        self.meta = Meta()
        self.codigo_2fa = None 
        self.codigo_2fa_expiracao = None

    def verificar_senha(self, senha_fornecida: str) -> bool:
        """Faz a verificação da senha, retorna True se ela for válida e False se ela estiver inválida"""
        return self.senha == senha_fornecida
    
    def to_dict(self) -> dict:
        """Converte os dados que precisam ser armazenados em um dicionário"""
        return {
            "nome_usuario": self.nome_usuario,
            "senha": self.senha,
            "email": self.email,
            "salario": self.salario,
            "gastos_fixos": self.gastos_fixos,
            "preferencias_gastos": self.preferencias_gastos,
            "meta": {
                "valor_total": self.meta.valor_total,
                "prazo_dias": self.meta.prazo_dias,
                "progresso_atual": self.meta.progresso_atual,
            }
        }
    
    @staticmethod
    def from_dict(nome_usuario: str, data: dict):
        """Cria uma instância de Usuário a partir de um dicionário"""
        usuario = Usuario(
            nome_usuario=nome_usuario,
            senha=data['senha'],
            email=data['email'],
            salario=data.get('salario', 0.0)
        )
        usuario.gastos_fixos = data.get('gastos_fixos', 0.0)
        usuario.preferencias_gastos = data.get('preferencias_gastos', {'alimentacao': 3, 'lazer': 3, 'transporte': 3})
        
        meta_data = data.get('meta', {})
        usuario.meta = Meta(
            meta_data.get('valor_total', 0.0),
            meta_data.get('prazo_dias', 0),
            meta_data.get('progresso_atual', 0.0)
        )
        return usuario
    
    def __repr__(self):
        return f"Usuario(nome_usuario= '{self.nome_usuario}', email='{self.email}')"
    
class Meta:
    """Representa uma meta financeira com seu valor, prazo e progresso"""
    def __init__ (self, valor_total: float = 0.0, prazo_dias: int = 0, progresso_atual: float = 0.0):
        self.valor_total = float(valor_total)
        self.prazo_dias = int(prazo_dias)
        self.progresso_atual = float(progresso_atual)

    def registrar_progresso(self, valor: float = 0.0):
        if valor > 0:
            self.progresso_atual += valor
            if self.prazo_dias > 0:
                self.prazo_dias -= 1

    def calculo_valor_restante(self) -> float:
        return max(0, self.valor_total - self.progresso_atual)
    
    def calcular_porcentagem(self) -> float:
        if self.valor_total == 0:
            return 0.0
        return min(100.0, (self.progresso_atual / self.valor_total) * 100)
    
    def __repr__(self) -> str:
        return f"Meta(R${self.valor_total:2f} em {self.prazo_dias} dias - Progresso: {self.calcular_porcentagem():.1f}%)"

