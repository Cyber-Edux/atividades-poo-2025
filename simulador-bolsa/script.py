from typing import *
from datetime import date


class Usuario:
    def __init__(self, nome: str, saldo: float):
        self.nome: str = nome
        self.saldo: float = saldo
        self.operacoes: List[dict] = []

    def obter_dados(self) -> dict:
        return {"nome": self.nome, "saldo": self.saldo}

    def descontar_saldo(self, valor: float):
        assert self.saldo >= valor, (
            f"O saldo do usuário {self.nome} é insuficiente para o desconto de R${valor}"
        )
        self.saldo -= valor

    def acrescentar_saldo(self, valor: float):
        assert valor >= 0, (
            f"Não é possível acrescentar um valor negativo (R${valor}) ao saldo."
        )
        self.saldo += valor

    def registrar_compra(self, ticker: str, valor: float, data: date):
        self.operacoes.append(
            {
                "operacao": "compra",
                "ticker": ticker,
                "valor": valor,
                "data": data.isoformat(),
            }
        )

    def registrar_venda(self, ticker: str, valor: float, data: date):
        self.operacoes.append(
            {
                "operacao": "venda",
                "ticker": ticker,
                "valor": valor,
                "data": data.isoformat(),
            }
        )

    def obter_extrato(self) -> str:
        """
        Método que retorna o extrato das operações do usuário.
        Cada linha do extrato deve descrever uma operação no seguinte formato:
        '{data}: {operacao} do ativo {ticker} no valor R${valor}'
        """
        extrato = ""

        for operacao in self.operacoes:
            extrato += f"{operacao['data']}: {operacao['operacao']} do ativo {operacao['ticker']} no valor R${operacao['valor']}\n"

        return extrato


class PessoaJuridica(Usuario):
    def __init__(self, nome: str, cnpj: str, saldo: float):
        super().__init__(nome, saldo)
        self.cnpj: str = cnpj

    def obter_dados(self):
        dados = super().obter_dados()
        dados["cnpj"] = self.cnpj
        return dados


class PessoaFisica(Usuario):
    def __init__(self, nome: str, cpf: str, saldo: float):
        super().__init__(nome, saldo)
        self.cpf: str = cpf

    def obter_dados(self):
        dados = super().obter_dados()
        dados["cpf"] = self.cpf
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
        proventos = lpa * (payout / 100)
        self.detentor.acrescentar_saldo(proventos)


class Ordem:
    def __init__(
        self,
        ticker: str,
        criador: Usuario,
        valor: float,
        status: Literal["pendente", "fechada", "cancelada"] = "pendente",
    ):
        """
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - criador (Usuário): quem está criando a ordem
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        """
        self.ticker: str = ticker
        self.valor: float = valor
        self.criador: Usuario = criador
        self.status: Literal["pendente", "fechada", "cancelada"] = status

    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        """
        Este método fecha a negociação, fazendo a compra ou venda do ativo de/para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo negociado.
        """
        # Este método não precisa ser implementado
        raise NotImplementedError()

    def cancelar(self):
        """
        Faz o cancelamento da ordem.
        """
        self.status = "cancelada"


class OrdemDeVenda(Ordem):
    def __init__(
        self,
        ticker: str,
        ofertante: Usuario,
        valor: float,
        status: Literal["pendente", "fechada", "cancelada"] = "pendente",
    ):
        """
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - ofertante (Usuário): quem está criando a ordem de venda
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        """
        super().__init__(ticker, ofertante, valor, status)

    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        """
        Este método fecha a negociação, fazendo a venda do ativo para outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo vendido;
        """
        assert ativo.detentor == self.criador, (
            f"O ativo {ativo.ticker} não pertence ao ofertante da ordem"
        )

        negociante.descontar_saldo(self.valor)

        self.criador.acrescentar_saldo(self.valor)

        ativo.detentor = negociante

        from datetime import date

        hoje = date.today()
        self.criador.registrar_venda(ativo.ticker, self.valor, hoje)
        negociante.registrar_compra(ativo.ticker, self.valor, hoje)

        self.status = "fechada"


class OrdemDeCompra(Ordem):
    def __init__(
        self,
        ticker: str,
        demandante: Usuario,
        valor: float,
        status: Literal["pendente", "fechada", "cancelada"] = "pendente",
    ):
        """
        Parâmetros:
        - ticker (str): ticker do ativo a ser negociado
        - demandante (Usuário): quem está criando a ordem de compra
        - valor (float): valor pelo qual o criador pretende negociar o ativo
        - status (str): status de ordem, que pode ser 'pendente' (caso o negócio não esteja fechado), 'fechada' (caso o negócio já tenha sido fechado) ou 'cancelada' (caso a ordem tenha cido cancelada).
        """
        super().__init__(ticker, demandante, valor, status)

    @override
    def fechar_negocio(self, negociante: Usuario, ativo: Ativo):
        """
        Este método fecha a negociação, fazendo a compra do ativo de outro usuário.
        Parâmetros:
        - negociante (Usuario): usuário com quem o criador da ordem está fechando a negociação.
        - ativo (Ativo): ativo comprado
        """
        assert ativo.detentor == negociante, (
            f"O ativo {ativo.ticker} não pertence ao negociante"
        )

        self.criador.descontar_saldo(self.valor)

        negociante.acrescentar_saldo(self.valor)

        ativo.detentor = self.criador

        from datetime import date

        hoje = date.today()
        self.criador.registrar_compra(ativo.ticker, self.valor, hoje)
        negociante.registrar_venda(ativo.ticker, self.valor, hoje)

        self.status = "fechada"


class BaseSistemaBolsa:
    def __init__(self):
        self.ativos: Dict[str, List[Ativo]] = dict()
        self.pessoas_fisicas: List[PessoaFisica] = []
        self.pessoas_juridicas: List[PessoaJuridica] = []

    def listar_tickers(self) -> List[str]:
        """
        Retorna uma lista de tickers de ativos.
        """
        return list(self.ativos.keys())

    def cadastrar_pessoa_fisica(
        self, nome: str, cpf: str, saldo: float
    ) -> PessoaFisica:
        """
        Cadastra uma pessoa física no sistema.
        Parâmetros:
         - nome (str): nome da pessoa
         - cpf (str): cpf da pessoa
         - saldo (float): saldo da pessoa em conta de investimento, em reais
         Retorna o objeto PessoaFisica criado.
        """
        nova_pessoa = PessoaFisica(nome, cpf, saldo)
        self.pessoas_fisicas.append(nova_pessoa)
        return nova_pessoa

    def cadastrar_pessoa_juridica(
        self, nome: str, cnpj: str, saldo: float
    ) -> PessoaJuridica:
        """
        Cadastrar uma pessoa jurídica (empresa) no sistema.
        Parâmetros:
        - nome (str): razão social da empresa
        - cnpj (str): CNPJ da empresa
        - saldo (float): saldo da empresa em conta de investimento, em reais
        Retorna o objeto PessoaJuridica criado.
        """
        nova_empresa = PessoaJuridica(nome, cnpj, saldo)
        self.pessoas_juridicas.append(nova_empresa)
        return nova_empresa

    def obter_pessoa_fisica_por_cpf(self, cpf: str) -> Union[PessoaFisica, None]:
        """
        Busca uma pessoa física pelo CPF dela e a retorna como um objeto PessoaFisica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cpf (str): CPF da pessoa buscada.
        """
        for pessoa in self.pessoas_fisicas:
            if pessoa.cpf == cpf:
                return pessoa
        return None

    def obter_pessoa_juridica_por_cnpj(self, cnpj: str) -> Union[PessoaJuridica, None]:
        """
        Busca uma empresa pelo CNPJ dela e a retorna como um objeto PessoaJuridica.
        Caso não seja encontrada, retorna None.
        Parâmetros:
        - cnpj (str): CNPJ da emrpesa buscada.
        """
        for empresa in self.pessoas_juridicas:
           if empresa.cnpj == cnpj:
               return empresa
        return None


    def criar_ativo(
        self, ticker: str, emissor: PessoaJuridica, detentor: Usuario
    ) -> Ativo:
        """
        Cria um ativo, faz seu registro e retorna-o como um objeto Ativo.
        Parâmetro:
        - ticker (str): ticker do ativo.
        - emissor (PessoaJuridica): empresa que está emitindo o ativo.
        - detentor (Usuario): usuário dono do ativo.
        """
        novo_ativo = Ativo(ticker, emissor, detentor)
       
        if ticker not in self.ativos:
           self.ativos[ticker] = []
       
        self.ativos[ticker].append(novo_ativo)
        return novo_ativo


class Pregao:
    def __init__(self, bolsa: BaseSistemaBolsa, data: date):
        self.bolsa: BaseSistemaBolsa = bolsa
        self.data: date = data
        self.ordens_de_venda: List[OrdemDeVenda] = []
        self.ordens_de_compra: List[OrdemDeCompra] = []

    def criar_ordem_de_compra(
        self, criador: Usuario, ticker: str, valor: Optional[float] = None
    ) -> Union[float, None]:
        """
        Deve fazer a compra de um ativo por até o valor especificado.
        Caso não seja possível comprar um ativo imediatamente, uma ordem de compra deve ser registrada.
        Parâmetros:
        - criador (Usuario): quem está fazendo a ordem de compra
        - ticker (str): ticker do ativo negociado
        - valor (float, opcional): valor máximo pelo qual o ativo deve ser comprado. Caso seja None, não tem valor máximo.
        Retorna (float ou None): o valor pelo qual o ativo foi comprado, ou None caso a compra não tenha sido feita de imediato.
        """
        # 1. Verifica se o criador tem saldo suficiente para a compra
        if valor is not None and criador.saldo < valor:
            raise ValueError(f'Saldo insuficiente para a compra. Saldo atual: R${criador.saldo}')
        
        # 2. Procura por uma ordem de venda compatível (valor menor ou igual ao oferecido)
        ordem_compativel = None
        for ordem_venda in self.ordens_de_venda:
            if ordem_venda.status == 'pendente' and ordem_venda.ticker == ticker:
                if valor is None or ordem_venda.valor <= valor:
                    ordem_compativel = ordem_venda
                    break
                   
        # 2.1 Se encontrou uma ordem compatível, executar a negociação imediatamente
        if ordem_compativel:
            ativo_negociado = None
            if ticker in self.bolsa.ativos:
                for ativo in self.bolsa.ativos[ticker]:
                    if ativo.detentor == ordem_compativel.criador:
                        ativo_negociado = ativo
                        break
                       
            if ativo_negociado:
                ordem_compativel.fechar_negocio(criador, ativo_negociado)
                
                ordem_compra = OrdemDeCompra(ticker, criador, ordem_compativel.valor, 'fechada')
                self.ordens_de_compra.append(ordem_compra)
                
                return ordem_compativel.valor
        
        # 2.2 Se não encontrou ordem compatível, criar ordem de compra pendente
        if valor is not None:
            ordem_compra = OrdemDeCompra(ticker, criador, valor, 'pendente')
            self.ordens_de_compra.append(ordem_compra)
        
        return None

    def criar_ordem_de_venda(
        self, emissor: Usuario, ticker: str, valor: Optional[float] = None
    ) -> Union[float, None]:
        """
        Deve fazer a venda de um ativo por até o valor mínimo especificado.
        Caso não seja possível comprar um ativo imediatamente, uma oferta pendente deve ser registrada.
        Parâmetros:
        - criador (Usuario): quem está fazendo a ordem de venda
        - ticker (str): ticker do ativo negociado
        - valor (float, opcional): valor mínimo pelo qual o ativo deve ser vendido. Caso seja None, não tem valor mínimo.
        Retorna (float ou None): o valor pelo qual ativo foi vendido, ou None caso a venda não tenha sido feita de imediato.
        """
       # 1. Verifica se o emissor possui um ativo com o ticker especificado
       ativo_para_venda = None
       if ticker in self.bolsa.ativos:
           for ativo in self.bolsa.ativos[ticker]:
               if ativo.detentor == emissor:
                   ativo_para_venda = ativo
                   break
       
       if not ativo_para_venda:
           raise ValueError(f'O usuário não possui ativo com ticker {ticker}')
       
       # 2. Procura por uma ordem de compra compatível (valor maior ou igual ao mínimo)
       ordem_compativel = None
       for ordem_compra in self.ordens_de_compra:
           if ordem_compra.status == 'pendente' and ordem_compra.ticker == ticker:
               if valor is None or ordem_compra.valor >= valor:
                   ordem_compativel = ordem_compra
                   break
       
       # 2.1 Se encontrou uma ordem compatível, executa a negociação imediatamente
       if ordem_compativel:
           ordem_compativel.fechar_negocio(emissor, ativo_para_venda)
           
           ordem_venda = OrdemDeVenda(ticker, emissor, ordem_compativel.valor, 'fechada')
           # 3. Insire a ordem criada na lista ordens_de_venda
           self.ordens_de_venda.append(ordem_venda)
           
           return ordem_compativel.valor
       
       # 2.2 Se não encontrou ordem compatível, cria ordem de venda pendente
       if valor is not None:
           ordem_venda = OrdemDeVenda(ticker, emissor, valor, 'pendente')
           # 3. Insire a ordem criada na lista ordens_de_venda
           self.ordens_de_venda.append(ordem_venda)
       
       return None

    def calcular_cotacao(self, ticker: str) -> float:
        """
        Deve calcular a cotaçaõ do ativo no dia.
        A cotação é calculada como a média dos valores pelos quais o ativo foi negociado.
        Parâmetros:
        - ticker (str): ticker do ativo
        """
        # Calcule a média de todas as ordens fechadas do ativo
        raise NotImplementedError()

    def oferta_publica_inicial(
        self, emissor: PessoaJuridica, ticker: str, valor: float, quantidade: int
    ):
        """
        Faz uma oferta pública inicial (IPO).
        Parâmetros:
        - emissor (PessoaJuridica) - empresa que está fazendo o IPO
        - ticker (str) - ticker que a empresa escolhei para o ativo
        - valor (float) - valor pelo qual a empresa está vendendo o ativo
        - quantidade (int) - quantidade de ativos que a empresa está emitindo
        """
        raise NotImplementedError()


class SistemaBolsa(BaseSistemaBolsa):
    def __init__(self):
        super().__init__()
        self.pregoes: Dict[str, Pregao] = (
            dict()
        )  # Dicionário no formato {'YYYY-MM-DD': <pregao>}.

    def criar_pregao(self, data: date) -> Pregao:
        """
        Cria e retorna pregão de uma data específica.
        """
        assert data.isoformat() not in self.pregoes.keys(), (
            "Já existe um pregão na data especificada"
        )
        pregao = Pregao(self, data)
        self.pregoes[data.isoformat()] = pregao
        return pregao

    def obter_ultimo_pregao(self) -> Union[Pregao, None]:
        """
        Retorna o ultimo pregão realizado ou None.
        """
        # Verifique se há pregões no dicionário. Caso não haja, retorne None
        # Caso contrário, obtenha a data mais recente com max(self.pregoes.keys())
        # Obtenha o pregão da data mais recente e retorne-o
        raise NotImplementedError()  # Remova ao implementar

    def obter_pregao_da_data(self, data: date) -> Union[Pregao, None]:
        """
        Retorna o pregão de um dia específico.
        """
        # Verifique se há um pregão na data especificada. Caso não haja, retorne None
        # Caso haja, retorne-o
        raise NotImplementedError()  # Remova ao implementar
