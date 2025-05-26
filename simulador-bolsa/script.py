from typing import *
from datetime import date


class Usuario:
    def __init__(self, nome: str, saldo: float):
        self.nome: str = nome
        self.saldo: float = saldo
        self.operacoes: List[dict] = []


    def obter_dados(self) -> dict:
        return {'nome': self.nome, 'saldo': self.saldo}


    def registrar_compra(self, ticker: str, valor: float, data: date):
        self.operacoes.append({
            'operacao': 'compra',
            'ticker': ticker,
            'valor': valor,
            'data': data.isoformat()
        })


    def registrar_venda(self, ticker: str, valor: float, data: date):
        self.operacoes.append({
            'operacao': 'venda',
            'ticker': ticker,
            'valor': valor,
            'data': data.isoformat()
        })


    def obter_extrato(self) -> str:
        """
        Método que retorna o extrato das operações do usuário.
        Cada linha do extrato deve descrever uma operação no seguinte formato: 
        '{data}: {operacao} do ativo {ticker} no valor R${valor}' 
        """
        raise NotImplementedError()

         
class PessoaJuridica(Usuario):
    def __init__(self, nome: str, cnpj: str, saldo: float):
        super().__init__(nome, saldo)
        self.cnpj: str = cnpj


    def obter_dados(self):
        dados = super().obter_dados()
        dados['cnpj'] = self.cnpj
        return dados


class PessoaFisica(Usuario):
    def __init__(self, nome: str, cpf: str, saldo: float):
        super().__init__(nome, saldo)
        self.cpf: str = cpf


    def obter_dados(self):
        dados = super().obter_dados()
        dados['cpf'] = self.cpf
        return dados


class Ativo:
    def __init__(self, ticker: str, emissor: PessoaJuridica, detentor: Usuario):
        self.ticker: str = ticker
        self.emissor: PessoaJuridica = emissor
        self.detentor: Usuario = detentor


    def pagar_provento(self, lpa: float, payout: float):
        """
        Esse método deve fazer o pagamento dos proventos ao detentor.
        Básicamente, um valor equivalente ao lpa*(payout/100) deve ser incrementado ao saldo do detentor.
        Parâmetros:
        - lpa (float): o valor do lucro por ação do emissor no mês, em R$
        - payout (float): o percentual de payout do emissor (de 0 a 100)
        """
        raise NotImplementedError()


class Ordem:
    def __init__(self, ativo: Ativo, criador: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        '''
        Parâmetros:
        - ativo (Ativo): ativo a ser negociado (compra ou venda)
        - criador (Usuário): quem está criando a ordem
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        '''
        self.ativo: Ativo = ativo
        self.valor: float = valor
        self.criador: Usuario = criador
        self.status: Literal['pendente', 'fechada', 'cancelada'] = status


    def fechar_negocio(self, negociante: Usuario):
        '''
        Este método fecha a negociação, fazendo a compra ou venda do ativo de/para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        '''
        raise NotImplementedError()
        

class OrdemDeVenda(Ordem):
    def __init__(self, ativo: Ativo, ofertante: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        super().__init__(ativo, ofertante, valor, status)


    @override
    def fechar_negocio(self, negociante: Usuario):
        '''
        Este método fecha a negociação, fazendo a venda do ativo para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        '''
        raise NotImplementedError()


class OrdemDeCompra:
    def __init__(self, ativo: Ativo, demandante: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        super().__init__(ativo, demandante, valor, status)

        
    @override
    def fechar_negocio(self, negociante: Usuario):
        '''
        Este método fecha a negociação, fazendo a compra do ativo de outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        '''
        raise NotImplementedError()


class BaseSistemaBolsa:
    def __init__(self):
        self.ativos: List[Ativo] = []
        self.pessoas_fisicas: List[PessoaFisica] = []
        self.pessoas_juridicas: List[PessoaJuridica] = []


    def listar_tickers(self) -> List[str]:
        """
        Retorna uma lista de tickers de ativos.
        """
        raise NotImplementedError()

    
    def cadastrar_pessoa_fisica(self, nome: str, cpf: str, saldo: float) -> PessoaFisica:
        '''
        Cadastra uma pessoa física no sistema.
        Parâmetros:
        - nome (str): nome da pessoa
        - cpf (str): cpf da pessoa
        - saldo (float): saldo da pessoa em conta de investimento, em reais
        Retorna o objeto PessoaFisica criado.
        '''
        raise NotImplementedError()

    
    def cadastrar_pessoa_juridica(self, nome: str, cnpj: str, saldo: float) -> PessoaJuridica:
        '''
        Cadastrar uma pessoa jurídica (empresa) no sistema.
        Parâmetros:
        - nome (str): razão social da empresa
        - cnpj (str): CNPJ da empresa
        - saldo (float): saldo da empresa em conta de investimento, em reais
        Retorna o objeto PessoaJuridica criado.
        '''
        raise NotImplementedError()


    def obter_pessoa_fisica_por_cpf(self, cpf: str) -> Union[PessoaFisica, None]:
        '''
        Busca uma pessoa física pelo CPF dela e a retorna como um objeto PessoaFisica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cpf (str): CPF da pessoa buscada.
        '''
        raise NotImplementedError()


    def obter_pessoa_juridica_por_cnpj(self, cnpj: str) -> Union[PessoaJuridica, None]:
        '''
        Busca uma empresa pelo CNPJ dela e a retorna como um objeto PessoaJuridica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cnpj (str): CNPJ da emrpesa buscada.
        '''
        raise NotImplementedError()
    

class Pregao:
    def __init__(self, bolsa: BaseSistemaBolsa, data: date):
        self.bolsa: BaseSistemaBolsa = bolsa
        self.data: date = data
        self.ordens_de_venda: List[OrdemDeVenda] = []
        self.ordens_de_compra: List[OrdemDeCompra] = []


    def criar_ordem_de_compra(self, criador: Usuario, ticker: str, valor: Optional[float] = None) -> Union[float, None]:
        '''
        Deve fazer a compra de um ativo por até o valor especificado.
        Caso não seja possível comprar um ativo imediatamente, uma ordem de compra deve ser registrada.
        Parâmetros:
        - criador (Usuario): quem está fazendo a ordem de compra
        - ticker (str): ticker do ativo negociado
        - valor (float, opcional): valor máximo pelo qual o ativo deve ser comprado. Caso seja None, não tem valor máximo.
        Retorna (float ou None): o valor pelo qual o ativo foi comprado, ou None caso a compra não tenha sido feita de imediato.
        '''
        raise NotImplementedError()


    def criar_ordem_de_venda(self, emissor: Usuario, ticker: str, valor: Optional[float] = None) -> Union[float, None]:
        '''
        Deve fazer a venda de um ativo por até o valor mínimo especificado.
        Caso não seja possível comprar um ativo imediatamente, uma oferta pendente deve ser registrada.
        Parâmetros:
        - criador (Usuario): quem está fazendo a ordem de venda
        - ticker (str): ticker do ativo negociado
        - valor (float, opcional): valor mínimo pelo qual o ativo deve ser vendido. Caso seja None, não tem valor mínimo.
        Retorna (float ou None): o valor pelo qual ativo foi vendido, ou None caso a venda não tenha sido feita de imediato.
        '''
        raise NotImplementedError()


    def calcular_cotacao(self, ativo: Ativo) -> float:
        '''
        Deve calcular a cotaçaõ do ativo no dia.
        A cotação é calculada como a média dos valores pelos quais o ativo foi negociado.
        '''
        raise NotImplementedError()


    def oferta_publica_inicial(self, emissor: PessoaJuridica, ticker: str, valor: float, quantidade: int):
        '''
        Faz uma oferta pública inicial (IPO).
        Parâmetros:
        - emissor (PessoaJuridica) - empresa que está fazendo o IPO
        - ticker (str) - ticker que a empresa escolhei para o ativo
        - valor (float) - valor pelo qual a empresa está vendendo o ativo
        - quantidade (int) - quantidade de ativos que a empresa está emitindo
        '''
        raise NotImplementedError()
    

class SistemaBolsa(BaseSistemaBolsa):
    def __init__(self):
        super().__init__()
        self.pregoes: Dict[str, Pregao] = dict() # Dicionário no formato {'YYYY-MM-DD': <pregao>}.


    def criar_pregao(self, data: date) -> Pregao:
        '''
        Cria e retorna pregão de uma data específica.
        '''
        assert data.isoformat() not in self.pregoes.keys(), 'Já existe um pregão na data especificada'
        pregao = Pregao(self, data)
        self.pregoes[data.isoformat()] = pregao
        return pregao
    

    def obter_ultimo_pregao(self) -> Union[Pregao, None]:
        '''
        Retorna o ultimo pregão realizado ou None.
        '''
        raise NotImplementedError()


    def obter_pregao_da_data(self, data: date) -> Union[Pregao, None]:
        '''
        Retorna o pregão de um dia específico.
        '''
        raise NotImplementedError()

    
    