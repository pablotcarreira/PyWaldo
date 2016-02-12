# coding=utf-8
#
# Pablo T. Carreira

"""Waldo! Módulo principal que contêm o famoso Waldo."""

from multiprocessing import Process
import time
from termcolor import colored
from Waldos.PyWaldo.erros import WaldoBaseException, WErroConfiguracao


class Waldo(Process):
    """Classe principal do Waldo! É um processo e por isto pode rodar de
    forma assíncrona."""
    cores_possivels = ['grey', 'green', 'yellow', 'blue',
                       'magenta', 'cyan', 'white']
    waldo_count = 0
    color_count = 0

    def __init__(self, modulo=None, nome="W", cor=None,
                 comunicativo=True, receita=None):
        """Realiza os cálculos.
        Quando o módulo está em debug, o erro não é capturado.

        Cada stack tem um ou dois waldos.
        Se encarrega de apagar dados sem uso liberando a memória.

        :param list receita: Lista de instâncias de módulos já com os
        parâmetros ou de classes de módulos.
        :param modulo: Um módulo para posicionar o waldo, é passado para
        self.modulo.

        """
        super(Waldo, self).__init__()

        # Determina a cor do waldo e incrementa os contadores.
        # Metodo Classs property
        Waldo.waldo_count += 1
        self._id = Waldo.waldo_count
        self.waldinhos = []
        self._receita = []
        Waldo.color_count += 1
        if Waldo.color_count > 7:
            Waldo.color_count = 0
        # Caracteristicas do Waldo.
        self.nome = nome
        self.cor = cor or self.cores_possivels[self.color_count - 1]
        self.comunicativo = comunicativo
        # Controle da movimentação.
        self.modulo = modulo            # Modulo onde está o Waldo.
        self.indice_modulo = 0          # Posição do módulo na receita.
        # Modulo que solicitou alguma coisa ao Waldo e que ele deve voltar.
        self.modulo_solicitante = None
        # Memória do waldo.
        self.dados = []           # Guarda os dados em uma lista.
        # Registro de tempo para acompanhar a execução de pequenas tarefas.
        self._tempo_parcial = 0
        # Registro de tempo para acompanhar a execução de grandes tarefas.
        self._tempo_global = 0
        # Controla se o waldo deve realizar o override sobre o dirty
        #  do resto dos módulos.
        self.full_dirty = False
        self.falar("Pronto para o trabalho!")

        if receita:
            self._montar_receita(receita)
            self.calcular()

    def run(self):
        """Método chamado quando se dá o start em um processo.
        """
        self.calcular()

    @property
    def receita(self):
        """Getter da receita.

        :returns list: Lista de instâncias de módulos.
        """
        return self._receita

    @receita.setter
    def receita(self, receita):
        """Setter da receita. Notar que é feito o append na receita atual,
        ou seja, a receita não é substituída.

        :param receita:
        """
        self._montar_receita(receita)

    def iniciar_multiprocessamento(self, sincrono_debug=False):
        """Multiprocessa a lista de waldinhos. Nao bloqueia a execuaçao do programa e portanto
        depende de quem for utilizar o waldinho garantir que o calculo tenha terminado. (Chamar o join)"""
        for item in self.waldinhos:
            if not sincrono_debug:
                item.start()
            else:
                item.calcular()

    # noinspection PyMethodMayBeStatic
    def _check_modulo(self, modulo):
        """Verifica se o objeto passado é um módulo waldo.
        Utilizado para verificações de segurança para evitar erros na montagem da receita.

        :param modulo:
        """
        try:
            modulo.waldo_check
        except AttributeError:
            raise TypeError('O objeto passado não é um módulo Waldo, {}.'.format(type(modulo)))

    def _montar_receita(self, instancias):
        """Faz a montagem de uma receita quando recebe uma lista de instâncias.
        Toda vez que este método é chamado é feito o append de novos módulos na receita.
        """
        # Faz as verificações.
        if not isinstance(instancias, (list, tuple)):
            raise TypeError(
                "Apenas listas e tuplas podem ser aceitas como receita. Recebeu: {}".format(type(instancias)))

        # Cria as ligações:
        for indice, instancia in enumerate(instancias):
            self._check_modulo(instancia)
            ultimo_modulo = self.mover_para_ultimo_modulo()
            if not ultimo_modulo:
                self.modulo = instancia
            else:
                instancia.norte = ultimo_modulo
            self._receita.append(instancia)
        self.mover_para_ultimo_modulo()

    #########################
    # Movimentos do Waldo.  #
    #########################
    def mover_para_primeiro_modulo(self):
        """Envia um waldo para o inicio do stack.
        Todos os waldos vão para o primeiro módulo e então vão executando as tarefas
        nos módulos seguintes.

        :rtype : Retorna True quando chegar ao primeiro módulo.
        """
        while self.modulo.norte:
            self.mover_para_cima()
        # self.falar("Estou no primeiro modulo")
        return True

    def mover_para_ultimo_modulo(self):
        """Envia um waldo para o fim do stack.

        Retorna o ultimo modulo.
        """
        if not self.modulo:
            return None
        while self.modulo.sul:
            self.mover_para_baixo()
        # self.falar("Estou no ultimo modulo")
        return self.modulo

    def mover_para_baixo(self):
        """Move o waldo para baixo um módulo.

        :rtype : True quando mover, False quando chegar no topo.
        """
        if not self.modulo.ultimo_modulo:
            # self.falar("vvv descendo")
            self.modulo = self.modulo.sul
            return True
        else:
            self.falar("Oi eu sou o waldo e estou no ultimo modulo")
            return False

    def mover_para_cima(self):
        """Move o waldo para cima um módulo.

        :rtype : True quando mover, False quando chegar no topo.
        """
        if self.modulo.norte:
            # self.falar("^^^ subindo")
            self.modulo = self.modulo.norte
            return True
        else:
            self.falar("Estou no primeiro módulo.")
            return False

    def mover_para_modulo(self, classe):
        """Move o waldo para um módulo de uma classe especifica."""
        # Poderia ter a opção de buscar de cima para baixo e de baixo para cima.
        # self.mover_para_primeiro_modulo()
        self.modulo_solicitante = self.modulo
        while self.mover_para_cima():
            if isinstance(self.modulo, classe):
                return
        raise RuntimeError("Modulo não encontrado.")

    def mover_para_modulo_dado(self, tipo_dado, modulo_atual=False):
        """Move o waldo para o ultimo modulo que tenha um dado específico. Anda para norte.
        Se modulo_atual é True procura também no modulo em que o waldo está.
        """
        self.modulo_solicitante = self.modulo
        while True:
            if modulo_atual:
                # Reseta a tag para que na proxima iteração ele se mova.
                modulo_atual = False
            else:
                self.mover_para_cima()
            if isinstance(self.modulo.dados, tipo_dado):
                self.falar("Dado encontrado - {} - {}".format(tipo_dado.__name__, self.modulo.nome_classe))
                return
            elif not self.modulo.norte:
                raise RuntimeError("Dado não encontrado: {}. \n Solicitante: {}".format(
                    tipo_dado.__name__, self.modulo_solicitante.nome_classe))

    def retornar_ao_solicitante(self):
        """Retorna para o modulo que fez uma solicitação ao Waldo.

        :return: None
        """
        # Verificação para ver se o solicitante foi definido.
        if not self.modulo_solicitante:
            raise RuntimeError("Sem modulo solicitante")
        while True:
            self.mover_para_baixo()
            if self.modulo == self.modulo_solicitante:
                return
            elif self.modulo.ultimo_modulo:
                raise RuntimeError("Não foi possível encontrar o modulo solicitante.")

    #########################
    # Ações do Valdo.       #
    #########################
    def falar(self, mensagem):
        if not self.comunicativo:
            return
        carret = colored("Waldo {}>".format(self.nome), self.cor)
        print "{} {}".format(carret, mensagem)

    def cronometrar_parcial(self):
        if self._tempo_parcial > 0:
            delta_tempo = time.clock() - self._tempo_parcial
            self._tempo_parcial = 0
            return round(delta_tempo, 2)
        else:
            self._tempo_parcial = time.clock()

    def cronometrar_global(self):
        if self._tempo_global > 0:
            delta_tempo = time.clock() - self._tempo_global
            self._tempo_global = 0
            return round(delta_tempo, 2)
        else:
            self._tempo_global = time.clock()

    def gerar_waldinho(self, nome=None):
        """Cria Waldos filhos deste Waldo.
        Os waldinhos herdam os dados do Waldo pai.
        """
        waldinho = Waldo(nome=nome or "Waldinho{}-{}".format(self._id, self.waldinhos), comunicativo=self.comunicativo)
        waldinho.dados = self.dados
        self.waldinhos.append(waldinho)
        return waldinho

    def _save_django_params(self):
        """Salva os parâmetros no módulo django.
        Se não tiver módulo django, apenas passa em silêncio.
        """
        if self.modulo.django_model:
            self.modulo.django_model.is_dirty = self.modulo.params.is_dirty
            self.modulo.django_model.params = self.modulo.params.dump()
            self.modulo.django_model.save()

    #########################
    # Tarefas do Waldo.     #
    #########################
    def calcular(self):
        """Calcula toda a stack, chamando o método calcular dos módulos.
        Dependendo do tipo de módulo o waldo pode tomar decisões diferentes.

        O módulo só é calculado quando está sujo. Quando o Django é usado, a parte Django deve cuidar de
         alterar este parâmetro.
         Se o Django não é utilizado, os modulos são sempre dirty a primeira vez que são calculados.

        Idéias:
        * O waldo poderia limpar sua memória automaticamente apos a tarefa caso ela não fale nada.
        * Caso o cache path exista e is_dirty=Fase, o waldo verifica se o arquivo de cache existe, se não, calcula.
        """
        self.cronometrar_global()
        waldo_ativo = self.mover_para_primeiro_modulo()
        self.indice_modulo = 0
        while waldo_ativo:
            if self.modulo.calculado:
                waldo_ativo = self.mover_para_baixo()
                self.indice_modulo += 1
                continue

            self.cronometrar_parcial()   # Inicia o cronômetro.
            dados = self.modulo.__class__.dados()
            nome_modulo = self.modulo.__class__.__name__
            dados.nome = nome_modulo
            dados.cache_path = self.modulo.cache_path
            # Alertas iniciais.
            self.falar(colored("Iniciando Cálculo {}.".format(nome_modulo), 'blue'))
            if self.modulo.use_cache and not self.modulo.cache_path:
                self.falar(colored('\tATENÇÃO: Modulo usa cache mas não tem cache_path.', 'red'))
            if self.modulo.debug:
                self.falar(colored('\t(DEBUG) Modulo em modo DEBUG, ler cache desativado.', 'red'))
                # Esta linha poderia ser inserida aqui, para forçar o cálculo
                #  dos módulos seguintes em uma situação de debug.
                # self.full_dirty = True

            # Verificações de dirty - Dica: na proxima passada, arrumar a verificação para ela ficar mais clara.
            # (Poderia ser feita uma conta boleana).
            _dirty = self.modulo.is_dirty
            # Override para quando o módulo está em debug.
            if self.modulo.debug:
                _dirty = True

            # Debug: Manualmente torna um determinado módulo dirty para testes:
            # self.falar("Debug: FORCA O RECALCULO - Waldo linha 288.")
            # if self.modulo.nome_classe == "Estilo":
            #     _dirty = True

            if not (self.modulo.use_cache and not _dirty and not self.full_dirty and self.modulo.cache_path and not self.modulo.debug):
                if _dirty:
                    self.full_dirty = True
                # CALCULA EFETIVAMENTE quando não há cache, quando está sujo ou em debug mode.
                self.falar(colored("\tCalculando - UseCache:{}  Dirty:{}  Debug:{}".format(
                    self.modulo.use_cache, self.modulo.params.is_dirty, self.modulo.debug), 'blue'))
                try:
                    resultado = self.modulo.calcular(self)
                    # Tenta usar o resultado.
                    dados.valores = resultado
                except Exception as erro:
                    # Captura o erro e se for um erro propagável, passa para os params.
                    # Se o módulo estiver em debug, escuta o erro original.
                    self.falar("###################################")
                    self.falar("###################################")
                    self.falar("Erro: " + erro.message)
                    self.falar("###################################")
                    self.falar("###################################")
                    if not isinstance(erro, WaldoBaseException):
                        erro = WErroConfiguracao()
                    self.modulo.params.is_dirty = True
                    self.falar("Erro: " + erro.message)
                    self.modulo.params.status = {"erro": True, "menssagem": erro.message, "dica": erro.dica}
                    self._save_django_params()
                    raise erro
                else:
                    self.modulo.params.status = {"erro": False, "menssagem": None, "dica": None}
                    # Salva no cache.
                    if self.modulo.use_cache and self.modulo.cache_path:
                        dados.save_cache(self.modulo.cache_path)
                    self.modulo.params.is_dirty = False
                    # Salva os parametros no model_django quando for o caso.
                    self._save_django_params()
            else:
                self.falar(colored("\t(LAZY) Não calculado - utilizado o cache.", 'magenta'))
            # Coloca os parâmetros nos dados e coloca os dados no Waldo.
            dados.params = self.modulo.params
            self.dados.append(dados)
            # Para o cronômetro.
            tempo = self.cronometrar_parcial()
            self.falar(colored("\tTarefa executada: {}, tempo: {}s".format(nome_modulo, tempo), 'magenta'))
            # Marca o módulo como calculado no ambiente Waldo.
            self.modulo.calculado = True
            waldo_ativo = self.mover_para_baixo()
            self.indice_modulo += 1
        self.falar("Tempo total: {}".format(self.cronometrar_global()))
        return self.dados

    def pegar_dados_modulo_anterior(self):
        """Pega os dados do módulo ao norte.
        """
        self.falar("Pegar dados do módulo anterior")
        self.mover_para_cima()
        dados = self.modulo.dados
        self.mover_para_baixo()
        return dados

    def pegar_dados(self, tipo_dado, allow_null=False):
        """Pega os dado de saída da ultima etapa que gerou dados do tipo solicitado.

        Se desejar incluir o módulo atual na busca, passar 'modulo_atual=True'.
        Caso contrário o waldo anda primeiro para cima antes de buscar o dado.

        :param bool allow_null: Permite não encontrar o dado e retornar NoneType.
        :param tipo_dado: Classe Dado do tipo desejado.
        o nome é igual ao nome do módulo.
        """
        # self.falar("Pegar dados - {}".format(tipo_dado.__name__))
        for dado_object in reversed(self.dados):
            if isinstance(dado_object, tipo_dado):
                return dado_object
        if not allow_null:
            raise RuntimeError(
                "Dado não encontrado: {}. \n Solicitante: {} - {}".format(tipo_dado.__name__, self, self.modulo))
        else:
            return None
