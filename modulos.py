# coding=utf-8
#
# Pablo T. Carreira
from Waldos.PyWaldo.waldos import Waldo

from parametros import Params, ParamsReceita, ParamsVirtual
from dados import Dado

import sys
import inspect


class Modulo(object):
    waldo_check = True    # Utilizado para verificar se um objeto é um módulo waldo.
    dados = Dado
    params = Params
    disponivel_para_usuario = False
    requisitos = None
    descricao = {
        'nome': None,
        'nomePlural': None,
        'nomeCurto': None}
    use_cache = False
    # persist_params = False  # Salva os parametros no model Django.
    debug = True  # Override the cache for debugging.
    virtual = False
    entity = False


    @classmethod
    def get_description(cls):
        params = cls.params().dump() if cls.params else None
        return {"description": cls.descricao, "params": params}

    def __init__(self, norte=None, nome=None, params=None, cache_path=None, is_dirty=True, model=None):
        """Modulo base. Cria-se uma subclasse deste módulo e reimplementa-se os
        métodos abstratos afim de obter a funcionalidade desejada.

        Os módulos são totalmente independentes do Django mas caso um model Django seja passado
        os parâmetros são salvos novamente no model após o cálculo.

        Quando o módulo está em debug, o erro não é capturado.

         Ideias:
        -------
            release_memory = True/False
            O waldo libera estes dados da memória e abre a partir do cache quando necessário.
            Por exemplo de um dado vai ser usado somente mais para frente no projeto, ele pode ser librado.


        :param cache_path: Caminho para salvar o arquivo do cache.
        :param is_dirty: True - recalcular, False - passa por cima sem calcular pegando o dado que é lazy.
        :param model: Model Django que representa este módulo.
        :param nome: Um nome para a instancia deste módulo.
        :param params: Parametros de configuração para este módulo, pode ser um objeto params ou um dicionário que será carrega no params automaticamente. Ver Params.load() para mais detalhes.
        :param norte: A instância do módulo acima ou None se este for o primeiro módulo.
        :param dados: Um <Dado Class> do tipo do dado produzido por este módulo. O modulo não guarda dados, mas passa para o waldo uma instância do <dado object>.
        :param descricao: Objeto que descreve este módulo para o usuário.
        :param disponivel_para_usuario: Flag que disponibiliza a configuraçao para o usuário.
        :param disable_cache: Override para desligar o cache de modulos que possuem cache.
        """
        # Determina se este módulo já foi calculado no ambiente waldo.
        # Permite que receitas sejam ampliadas e recalculadas sem prejuísos ao desempenho.
        self.calculado = False

        self.ultimo_modulo = True            # Define se é o ultimo módulo do stack.
        self._norte = None                   # Modulo acima.
        self._sul = None                     # Modulo abaixo.
        self.is_dirty = is_dirty            # Marca se o módulo está sujo, precisa ser recalculado.
        self.waldo = None               # Waldo que está sobre este módulo.
        self.django_model = model

        # Prepara as configurações de cache.
        self.cache_path = cache_path

        # Coloca os parametros de configuração.
        self.params = self.__class__.params()
        if isinstance(params, self.params.__class__):
            self.params = params
        elif params:
            self.params.load(params)
        # Coloca os dados.
        self.dados = self.__class__.dados(cache_path=cache_path)

        #: Nome único para este módulo no stack.
        # Se existem dois módulos com o mesmo nome, apenas o primeiro é criado.
        # E seu resultado é reaproveitado.
        self.nome = nome

        # Atalho de conveniência para o nome da classe.
        self.nome_classe = self.__class__.__name__

        # Coloca o módulo norte se foi fornecido.
        if norte:
            self.norte = norte

    @property
    def norte(self):
        return self._norte

    @norte.setter
    def norte(self, modulo_norte):
        """Verifica se o norte conectado está correto, registra no norte deste modulo e
        se registra no sul do módulo norte.
        """
        self._norte = modulo_norte
        modulo_norte.sul = self

    @property
    def sul(self):
        return self._sul

    @sul.setter
    def sul(self, modulo):
        """Registra o modulo sul, não deve ser chamado diretamente, usar sempre o norte.

        :param modulo:
        """
        self.ultimo_modulo = False
        self._sul = modulo

    def calcular(self, waldo):
        """Calcula o módulo. Deve ser reimplementado.

        :param waldo: O Waldo que está chamando esta função.
        :raise NotImplementedError:
        :return: Resultado dos cálculos. A classe principal se encarrega de colocar o
         resultado nos dados_OLD do módulo.
        """
        raise NotImplementedError

    def gerar_nome_cache(self):
        """Nome gerado para cada elemento para salvar no cache,
        Hash atribuída a instância deste modulo, formada pelo nome da classe
        e pelo nome individual da instância. Utilizado para gerar nomes de arquivos.
        """
        return '{}-{}'.format(self.nome_classe, self.nome)

    def salvar_cache(self):
        """Método que salva o cache do resultado.
        A forma como um dado é salvo é responsabilidade do dado,
        assim pode ser reaproveitado para todos os módulos que usam um mesmo tipo.
        """
        if self.use_cache:
            self.dados.read_cache(self.gerar_nome_cache())

    def ler_cache(self):
        """Recupera o cache dos dados_OLD deste modulo.
        Cada tipo de dado tem sua metodologia.
        """
        if self.use_cache:
            self.dados.ler_cache(self.gerar_nome_cache())


class Coletor(Modulo):
    """Módulo que abre uma nova árvore de receitas.
    """
    def __init__(self):
        super(Coletor, self).__init__()
        self.receitas = None

    def calcular(self, waldo):
        """Coleta informações de várias receitas.
        O coletor monta a árvore de receitas, colocando os
        roteadores e junta os dados_OLD obtidos de cada receita.
        """
        self.waldo = waldo
        # Monta a árvore de receitas.
        # self.construir_arvore() DEPRECATED
        resultado = self.calcular_coletor()
        self.dados.valores = resultado

    def calcular_coletor(self, assincrono=False):
        """Modifica o comportamento do Waldo, fazendo ele calcular outras receitas.
        """
        self.waldo.falar('Coletor tomando o controle, ramificando cálculos com waldinhos.')

        # Cria um waldo para cada receita e manda ele fazer o trabalho.
        waldinhos = []
        for receita in self.receitas:
            waldinho = self.waldo.gerar_waldinho()
            waldinho.modulo = receita.ultimo_modulo
            waldinhos.append(waldinho)
            if assincrono:
                waldinho.start()
            else:
                waldinho.calcular()
        resultados = []
        for waldinho in waldinhos:
            if assincrono:
                waldinho.join()  # Espera todos os waldinhos terminarem.
            resultados.append(waldinho.modulo.dados)
        self.waldo.falar("Todos os Waldinhos retornaram, dados_OLD Coletados :)")
        return resultados


class Virtual(Modulo):
    """Dá origem aos virtual components. É especial que representa um
    conjunto de componentes virtuais.

    Os dados de uma módulo virtual provem da combinação de dados de outros
     módulos.

    Os outros módulos devem ser passados para os params e o método clacular
    se encarrega de agir e fazer as tranformações para gerar os dados necessários.
    """
    virtual = True
    params = ParamsVirtual
    disponivel_para_usuario = True
    use_cache = False


class Receita(Modulo):
    """
    Uma receita é um conjunto de módulos em ordem para serem calculados.
        * A receita não participa nos cálculos.
        * As receitas só são montadas quando necessário.
        * Monta apenas receitas verticais.

        :param receita: Classes dos módulos em ordem de cima para baixo.
        :param params: Lista ou dicionário de parâmetros para serem passados para os módulos no momento
        da montagem da receita.
    """
    entity = True
    params = ParamsReceita
    dados = Dado
    disponivel_para_usuario = True
    receita = []

    def calcular(self, waldo=None):
        """O calcular da receita é bem especial e pode ser feito o override
        para interceptar o resultado.

        :param waldo:
        :return:
        """
        receita_preparada = self.preparar_receita()
        # Se recebe um waldo usa ele.
        if waldo:
            # Gurarda as informações do waldo.
            waldo_indice_modulo = waldo.indice_modulo
            # Troca as informações e o módulo.
            waldo.indice_modulo = 0
            waldo.modulo = receita_preparada[-1]  # Ultimo módulo da receita.
            resultado = waldo.calcular()
            # Devolve as informações anteriores.
            waldo.indice_modulo = waldo_indice_modulo
            waldo.modulo = self
        # Se não tem waldo, cria um.
        else:
            waldo = Waldo(receita=receita_preparada)
            resultado = waldo.dados
        return resultado

    def preparar_receita(self):
        """Cria as instâncias e faz as ligações entre os módulos."""
        instancias = []
        receita = self.receita

        # Verifica se é classe e coloca os parametros em cada ítem.
        for item in receita:
            if inspect.isclass(item):
                nome = item.__name__
                try:
                    params_item = getattr(self.params, nome)
                except AttributeError:
                    instancia_item = item()
                else:
                    instancia_item = item(params=params_item)
                instancias.append(instancia_item)

        # Cria as ligações:
        if len(instancias) == 1:
            return instancias

        for indice, instancia in enumerate(instancias):
            try:
                modulo_sul = instancias[indice + 1]
            except IndexError:
                continue
            else:
                modulo_sul.norte = instancia
        return instancias