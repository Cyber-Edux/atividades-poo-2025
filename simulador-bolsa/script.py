from typing import *
from datetime import date


class Usuario:
    def __init__(self, nome: str, saldo: float):
        self.nome: str = nome
        self.saldo: float = saldo
        self.operacoes: List[dict] = []


    def obter_dados(self) -> dict:
        return {'nome': self.nome, 'saldo': self.saldo}


    def descontar_saldo(self, valor: float):
        assert self.saldo >= valor, f'O saldo do usuário {self.name} é insuficiente para o desconto de R${valor}'
        self.saldo -= valor


    def acrescentar_saldo(self, valor: float):
        assert valor >= 0, f'Não é possível acrescentar um valor negativo (R${valor}) ao saldo.'
        self.saldo += valor
        

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
        # Para cada operação, crie uma linha no formato '{data}: {operacao} do ativo {ticker} no valor R${valor}'
        # Junte todas as linhas criadas em uma única string, separando-as por '\n'
        # Sugestão: utilize o método join das strings para juntar as linhas
        raise NotImplementedError() # Remova esta linha depois de implementar o método

         
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
        # Calcule o valor do provento como lpa*(payout/100)
        # Incremente o provento ao saldo do emissor do ativo
        raise NotImplementedError() # Remova após fazer a implementação


class Ordem:
    def __init__(self, ticker: str, criador: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        '''
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - criador (Usuário): quem está criando a ordem
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        '''
        self.ticker: str = ticker
        self.valor: float = valor
        self.criador: Usuario = criador
        self.status: Literal['pendente', 'fechada', 'cancelada'] = status


    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        '''
        Este método fecha a negociação, fazendo a compra ou venda do ativo de/para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo negociado.
        '''
        # Este método não precisa ser implementado
        raise NotImplementedError()


    def cancelar(self):
        '''
        Faz o cancelamento da ordem.
        '''
        self.status = 'cancelada'
        

class OrdemDeVenda(Ordem):
    def __init__(self, ticker: str, ofertante: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        '''
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - ofertante (Usuário): quem está criando a ordem de venda
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        '''
        super().__init__(ticker, ofertante, valor, status)
        

    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        '''
        Este método fecha a negociação, fazendo a venda do ativo para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo vendido;
        '''
        # Verifique se o ativo é realmente do criador da ordem (ofertante)
        # No saldo do negociante, desconte o valor da ordem
        # Em seguida, defina o detentor do ativo negociado como o negociante
        # Mude o status para 'fechada'
        raise NotImplementedError() # Remova após fazer a implementação


class OrdemDeCompra(Ordem):
    def __init__(self, ticker: str, demandante: Usuario, valor: float, status: Literal['pendente', 'fechada', 'cancelada'] = 'pendente'):
        '''
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - demandante (Usuário): quem está criando a ordem de compra
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        '''
        super().__init__(ticker, demandante, valor, status)
        
        
    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        '''
        Este método fecha a negociação, fazendo a compra do ativo de outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo comprado
        '''
        # Verifique se o ativo é realmente do negociante
        # No saldo do criador da ordem (demandante), desconte o valor do ativo
        # Em seguida, defina o detentor do ativo como o criador da ordem
        # Mude o status para 'fechada'
        raise NotImplementedError() # Remova ao implementar


class BaseSistemaBolsa:
    def __init__(self):
        self.ativos: Dict[str, List[Ativo]] = dict() # dicionário de listas de ativos. Cada chave é um ticker, e cada valor é uma lista de ativos com o respectivo ticker
        self.pessoas_fisicas: List[PessoaFisica] = []
        self.pessoas_juridicas: List[PessoaJuridica] = []


    def listar_tickers(self) -> List[str]:
        """
        Retorna uma lista de tickers de ativos.
        """
        # Lembre-se que as chaves do dicionário de ativos são os tickers.
        # Você pode obter uma lista com as chaves de um dicionário usando o conversor list() e o método keys
        raise NotImplementedError() # Remova ao implementar

    
    def cadastrar_pessoa_fisica(self, nome: str, cpf: str, saldo: float) -> PessoaFisica:
        '''
        Cadastra uma pessoa física no sistema.
        Parâmetros:
        - nome (str): nome da pessoa
        - cpf (str): cpf da pessoa
        - saldo (float): saldo da pessoa em conta de investimento, em reais
        Retorna o objeto PessoaFisica criado.
        '''
        # Crie um objeto PessoaFisica e insira na lista pessoas_fisicas
        raise NotImplementedError() # Remova ao implementar

    
    def cadastrar_pessoa_juridica(self, nome: str, cnpj: str, saldo: float) -> PessoaJuridica:
        '''
        Cadastrar uma pessoa jurídica (empresa) no sistema.
        Parâmetros:
        - nome (str): razão social da empresa
        - cnpj (str): CNPJ da empresa
        - saldo (float): saldo da empresa em conta de investimento, em reais
        Retorna o objeto PessoaJuridica criado.
        '''
        # Crie um objeto PessoaJuridica e insira na lista pessoas_juridicas
        raise NotImplementedError() # Remova ao implementar


    def obter_pessoa_fisica_por_cpf(self, cpf: str) -> Union[PessoaFisica, None]:
        '''
        Busca uma pessoa física pelo CPF dela e a retorna como um objeto PessoaFisica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cpf (str): CPF da pessoa buscada.
        '''
        # Faça um laço for na lista pessoas_fisicas verificando se o CPF da pessoa física atual é igual ao do parâmetro
        # Ao encontrar o objeto PessoaFisica com o CPF igual ao parâmetro, retorne-o
        raise NotImplementedError()


    def obter_pessoa_juridica_por_cnpj(self, cnpj: str) -> Union[PessoaJuridica, None]:
        '''
        Busca uma empresa pelo CNPJ dela e a retorna como um objeto PessoaJuridica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cnpj (str): CNPJ da emrpesa buscada.
        '''
        # Faça um laço for na lista pessoas_juridicas verificando se o CNPJ da pessoa juridica atual é igual ao do parâmetro
        # Ao encontrar o objeto PessoaJuridica com o CNPJ igual ao parâmetro, retorne-o
        raise NotImplementedError()


    def criar_ativo(self, ticker: str, emissor: PessoaJuridica, detentor: Usuario) -> Ativo:
        '''
        Cria um ativo, faz seu registro e retorna-o como um objeto Ativo.
        Parâmetro:
        - ticker (str): ticker do ativo.
        - emissor (PessoaJuridica): empresa que está emitindo o ativo.
        - detentor (Usuario): usuário dono do ativo.
        '''
        # Crie um objeto Ativo
        # Insira o objeto no dicionário ativos
        # Retorne o objeto criado
        raise NotImplementedError() # Remova ao implementar
    

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
        # 1. Verifique se o criador da ordem tem saldo o suficiente para a compra
        # 2. Verifique se existe alguma ordem de venda pendente com valor menor ou igual ao do parâmetro
        #   2.1 Caso encontre a ordem de venda pendente, feche-a e crie uma ordem de compra já fechada
        #   2.2 Caso não encontre uma ordem de venda pendente que dê 'match' com a demanda atual, crie uma ordem de compra pendente
        # 3. Insira a ordem criada na lista ordens_de_compra
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
        # 1. Verifique se o emissor possui um ativo com o ticker especificado
        # 2. Verifique se existe uma ordem de compra pendente com valor maior ou igual ao do parâmetro:
        #   2.1 Caso encontre a ordem de compra, feche-a e crie uma ordem de venda já fechada
        #   2.2 Caso não encontrar uma ordem de compra pendente que dê 'match' com a oferta, crie uma ordem de venda pendente
        # 3. Insire a ordem criada na lista ordens_de_venda
        raise NotImplementedError()


    def calcular_cotacao(self, ticker: str) -> float:
        '''
        Deve calcular a cotaçaõ do ativo no dia.
        A cotação é calculada como a média dos valores pelos quais o ativo foi negociado.
        Parâmetros:
        - ticker (str): ticker do ativo
        '''
        # Calcule a média de todas as ordens fechadas do ativo
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
        # Verifique se há pregões no dicionário. Caso não haja, retorne None
        # Caso contrário, obtenha a data mais recente com max(self.pregoes.keys())
        # Obtenha o pregão da data mais recente e retorne-o
        raise NotImplementedError() # Remova ao implementar


    def obter_pregao_da_data(self, data: date) -> Union[Pregao, None]:
        '''
        Retorna o pregão de um dia específico.
        '''
        # Verifique se há um pregão na data especificada. Caso não haja, retorne None
        # Caso haja, retorne-o
        raise NotImplementedError() # Remova ao implementar

    
if __name__ == '__main__':
    # --- TESTE ---
    bolsa = SistemaBolsa()
    pregao = bolsa.criar_pregao(date(2025, 5, 27))
    assert isinstance(pregao, Pregao)
    assert bolsa.obter_ultimo_pregao() == pregao
    assert bolsa.obter_pregao_da_data(date(2025, 5, 27)) == pregao
    weg = bolsa.cadastrar_pessoa_juridica(
        nome='WEG EQUIPAMENTOS ELÉTRICOS S/A',
        cnpj='84.429.695/0001-11',
        saldo=21280000000 # R$ 21,28 bi
    )
    assert isinstance(weg, PessoaJuridica)
    fulano = bolsa.cadastrar_pessoa_fisica(
        nome='Fulano da Silva',
        cpf='123.456.789-10',
        saldo=10000
    )
    assert isinstance(fulano, PessoaFisica)
    pregao.oferta_publica_inicial(weg, 'WEGE3', 20, 100)
    assert 'WEGE3' in bolsa.ativos.keys()
    assert len(bolsa.ativos['WEGE3']) == 100
    assert all([isinstance(acao, Ativo) for acao in bolsa.ativos['WEGE3']])
    
