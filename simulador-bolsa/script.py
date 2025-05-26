from typing import *
from datetime import date

class Usuario:
    def __init__(self, nome: str, saldo: float):
        self.nome: str = nome
        self.saldo: str = saldo
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

    def pagar_provento(self, lucro: float, payout: float):
        """
        Esse método deve fazer o pagamento dos proventos ao detentor.
        Básicamente, um valor equivalente ao lucro*(payout/100) deve ser incrementado ao saldo do detentor.
        Parâmetros:
        - lucro (float): o valor do lucro do emissor no mês, em R$
        - payout (float): o percentual de payout do emissor (de 0 a 100)
        """
        raise NotImplementedError()

class Oferta:
    def __init__(self, ativo: Ativo, ofertante: Usuario, valor: float):
        self.ativo: Ativo = ativo
        self.ofertante: Usuario = ofertante
        self.valor: float = valor
        self.finalizada: bool = False

    def comprar(self, comprador: Usuario):
        """
        Este método deve fazer a compra do ativo ofertado pelo comprador.
        Para isso, o valor do ativo deve ser descontado do saldo do comprador, o detentor do ativo deve ser alterado, e o atributo 'finalizado' deve ser alterado para True.
        Parâmetros:
        - comprador (Usuario): Pessoa física ou jurídica que comprou o ativo
        """
        raise NotImplementedError()

class Cadastros:
    def __init__(self):
        self.ativos: List[Ativo] = []
        self.pessoas_fisicas: List[PessoaFisica] = []
        self.pessoas_juridicas: List[PessoaJuridica] = []

    def listar_tickers(self) -> List[str]:
        """
        Retorna uma lista de tickers de ativos.
        """
        raise NotImplementedError()


class Pregao:
    def __init__(self, cadastros: Cadastros, data: date):
        self.cadastros: Cadastros = cadastros
        self.data = date
        self.ofertas: List[Oferta] = []

    def comprar_ativo(self, emissor: Usuario, ticker: str, valor_max: Optional[float] = None) -> Union[float, None]:
        '''
        Deve fazer a compra de um ativo para o emissor por até o valor máximo especificado.
        Parâmetros:
        - emissor (Usuario): quem está fazendo a compra
        - ticker (str): ticker do ativo negociado
        - valor_max (float, opcional): valor máximo pelo qual o ativo deve ser comprado. Caso seja None, não tem valor máximo.
        Retorna (float ou None): o valor pelo qual ativo foi comprado, ou None caso a compra não seja feita.
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



        