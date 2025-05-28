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
        #assert self.saldo >= valor, f'O saldo do usuário {self.name} é insuficiente para o desconto de R${valor}'
        assert valor >= 0, f'Não é possível descontar um valor negativo (R${valor}) ao saldo.'
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
        return '\n'.join(
            [
                f"{op['data']}: {op['operacao']} do ativo {op['ticker']} no valor R${op['valor']}" 
                for op in self.operacoes
            ]
        )

         
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
        provento = lpa*(payout/100)
        self.emissor.descontar_saldo(provento)
        self.detentor.acrescentar_saldo(provento)
        

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
        self.valor_fechado: float = None # Valor pelo qual o negócio foi fechado. Adicionado após os alunos comecarem a atividade


    def fechar_negocio(self, negociante: Usuario, ativo: Ativo, valor_fechado: float):
        '''
        Este método fecha a negociação, fazendo a compra ou venda do ativo de/para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo negociado.
        - valor_fechado (float): valor pelo qual o valor foi fechado.
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
        

    """
    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo, valor_fechado: float):
        '''
        Este método fecha a negociação, fazendo a venda do ativo para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo vendido.
        - valor_fechado (float): valor pelo qual o negócio foi fechado.
        '''
        assert ativo.detentor == self.criador, 'Ativo não pertence ao criador da ordem'
        negociante.descontar_saldo(self.valor)
        self.criador.acrescentar_saldo(self.valor)
        ativo.detentor = negociante
        self.status = 'fechada'
        self.valor_fechado = valor_fechado
    """


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
        
    
    """
    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo, valor_fechado: float):
        '''
        Este método fecha a negociação, fazendo a compra do ativo de outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo comprado
        - valor_fechado (float): valor pelo qual o negócio foi fechado
        '''
        assert ativo.detentor == negociante, 'O ativo não é do negociante'
        self.criador.descontar_saldo(self.valor)
        negociante.acrescentar_saldo(self.valor)
        ativo.detentor = self.criador
        self.status = 'fechada'
        self.valor_fechado = valor_fechado
    """


class BaseSistemaBolsa:
    def __init__(self):
        self.ativos: Dict[str, List[Ativo]] = dict() # dicionário de listas de ativos. Cada chave é um ticker, e cada valor é uma lista de ativos com o respectivo ticker
        self.pessoas_fisicas: List[PessoaFisica] = []
        self.pessoas_juridicas: List[PessoaJuridica] = []


    def listar_tickers(self) -> List[str]:
        """
        Retorna uma lista de tickers de ativos.
        """
        return list(self.ativos.keys())

    
    def cadastrar_pessoa_fisica(self, nome: str, cpf: str, saldo: float) -> PessoaFisica:
        '''
        Cadastra uma pessoa física no sistema.
        Parâmetros:
        - nome (str): nome da pessoa
        - cpf (str): cpf da pessoa
        - saldo (float): saldo da pessoa em conta de investimento, em reais
        Retorna o objeto PessoaFisica criado.
        '''
        pf = PessoaFisica(nome, cpf, saldo)
        self.pessoas_fisicas.append(pf)

    
    def cadastrar_pessoa_juridica(self, nome: str, cnpj: str, saldo: float) -> PessoaJuridica:
        '''
        Cadastrar uma pessoa jurídica (empresa) no sistema.
        Parâmetros:
        - nome (str): razão social da empresa
        - cnpj (str): CNPJ da empresa
        - saldo (float): saldo da empresa em conta de investimento, em reais
        Retorna o objeto PessoaJuridica criado.
        '''
        pj = PessoaJuridica(nome, cnpj, saldo)
        self.pessoas_juridicas.append(pj)


    def obter_pessoa_fisica_por_cpf(self, cpf: str) -> Union[PessoaFisica, None]:
        '''
        Busca uma pessoa física pelo CPF dela e a retorna como um objeto PessoaFisica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cpf (str): CPF da pessoa buscada.
        '''
        for pf in self.pessoas_fisicas:
            if pf.cpf == cpf:
                return pf
        return None


    def obter_pessoa_juridica_por_cnpj(self, cnpj: str) -> Union[PessoaJuridica, None]:
        '''
        Busca uma empresa pelo CNPJ dela e a retorna como um objeto PessoaJuridica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cnpj (str): CNPJ da emrpesa buscada.
        '''
        for pj in self.pessoas_juridicas:
            if pj.cnpj == cnpj:
                return pj
        return None


    def criar_ativo(self, ticker: str, emissor: PessoaJuridica, detentor: Usuario) -> Ativo:
        '''
        Cria um ativo, faz seu registro e retorna-o como um objeto Ativo.
        Parâmetro:
        - ticker (str): ticker do ativo.
        - emissor (PessoaJuridica): empresa que está emitindo o ativo.
        - detentor (Usuario): usuário dono do ativo.
        '''
        ativo = Ativo(ticker, emissor, detentor)
        if ticker in self.ativos.keys():
            self.ativos[ticker].append(ativo)
        else:
            self.ativos[ticker] = [ativo]
        return ativo
    

class Pregao:
    def __init__(self, bolsa: BaseSistemaBolsa, data: date):
        self.bolsa: BaseSistemaBolsa = bolsa
        self.data: date = data
        self.ordens_de_venda: List[OrdemDeVenda] = []
        self.ordens_de_compra: List[OrdemDeCompra] = []


    def obter_ativos_do_usuario(self, usuario: Usuario, ticker: str) -> List[Ativo]:
        # Método adicionado após a atividade
        return [ativo for ativo in self.bolsa.ativos[ticker] if ativo.detentor == usuario]
                

    def fechar_negocio(self, ordem_de_compra: OrdemDeCompra, ordem_de_venda: OrdemDeVenda, ticker: str, valor_fechado: float):
        def obter_ativo_de(detentor: Usuario):
            for ativo in self.bolsa.ativos[ticker]:
                if ativo.detentor == detentor:
                    return ativo
        
        # Obter comprador e vendedor
        vendedor = ordem_de_venda.criador
        comprador = ordem_de_compra.criador
        
        # Obter ativo da carteira do vendedor e transferir para o comprador
        ativo = obter_ativo_de(vendedor)
        ativo.detentor = comprador

        # Transferir valor fechado do comprador para o vendedor
        comprador.descontar_saldo(valor_fechado)
        vendedor.acrescentar_saldo(valor_fechado)
        
        # Definir status das ordems como fechada
        ordem_de_compra.status = 'fechada'
        ordem_de_venda.status = 'fechada'

        # Definir valor fechado das ordens
        ordem_de_compra.valor_fechado = valor_fechado
        ordem_de_venda.valor_fechado = valor_fechado


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
        # Criar ordem de compra
        ordem_de_compra = OrdemDeCompra(ticker, criador, valor, 'pendente')
        
        # Verificar se existe alguma ordem de venda pendente com valor menor ou igual ao do parâmetro
        for ordem_de_venda in self.ordens_de_venda:
            if ordem_de_venda.status == 'pendente' and ordem_de_venda.valor <= valor:
                self.fechar_negocio(ordem_de_compra, ordem_de_venda, ticker, ordem_de_venda.valor)
                return ordem_de_venda.valor

        # Caso não tenha sido possível fechar um negocio imediatamente, a ordem é listada como pendente
        self.ordens_de_compra.append(ordem_de_compra)        


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
        # Criar ordem de venda
        ordem_de_venda = OrdemDeVenda(ticker, emissor, valor, 'pendente')

        # Verificar se há alguma ordem de compra com valor maior ou igual ao do parâmetro
        for ordem_de_compra in self.ordens_de_compra:
            if ordem_de_compra.status == 'pendente' and ordem_de_compra.valor <= valor:
                self.fechar_negocio(ordem_de_compra, ordem_de_venda, ticker, ordem_de_compra.valor)
                return ordem_de_compra.valor

        # Caso não tenha sido possível fechar um negocio imediatamente, a ordem é listada como pendente
        self.ordens_de_venda.append(ordem_de_venda)


    def calcular_cotacao(self, ticker: str) -> float:
        '''
        Deve calcular a cotaçaõ do ativo no dia.
        A cotação é calculada como a média dos valores pelos quais o ativo foi negociado.
        Parâmetros:
        - ticker (str): ticker do ativo
        '''
        valores_fechados = [ordem.valor_fechado for ordem in self.ordens_de_venda if ordem.ticker == ticker]
        media = sum(valores_fechados)/len(valores_fechados)
        return media


    def oferta_publica_inicial(self, emissor: PessoaJuridica, ticker: str, valor: float, quantidade: int):
        '''
        Faz uma oferta pública inicial (IPO).
        Parâmetros:
        - emissor (PessoaJuridica) - empresa que está fazendo o IPO
        - ticker (str) - ticker que a empresa escolhei para o ativo
        - valor (float) - valor pelo qual a empresa está vendendo o ativo
        - quantidade (int) - quantidade de ativos que a empresa está emitindo
        '''
        for i in range(quantidade):
            novo_ativo = self.bolsa.criar_ativo(ticker, emissor, emissor)        
            self.criar_ordem_de_venda(emissor, ticker, valor)


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
        if len(self.pregoes) > 0:
            ultima_data = max(self.pregoes.keys())
            return self.pregoes[ultima_data]
        

    def obter_pregao_da_data(self, data: date) -> Union[Pregao, None]:
        '''
        Retorna o pregão de um dia específico.
        '''
        data_iso = data.isoformat()
        if data_iso in self.pregoes.keys():
            return self.pregoes[data_iso]

    
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
    
