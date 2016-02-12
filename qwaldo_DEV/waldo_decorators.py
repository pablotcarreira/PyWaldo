# coding=utf-8
#
# Pablo T. Carreira
import time



class WaldoSignal(object):
    """Classe que reporta o que o waldo está fazendo."""
    qml_waldo_slot = None
    sinal = QtCore.Signal(float)



    def enviar_sinal(self, tipo):
        if tipo == "mover_para_baixo":
            valor = 100
        elif tipo == "mover_para_cima":
            valor = -100
        else:
            valor = 0
        self.sinal.emit(valor)


class WaldoReport(WaldoSignal): # if USE_QT_WALDO else object):  #TODO: Ajustar a opção de não usar o Qt.
    def __init__(self):
        """Decorator que faz o waldo emitir sinais sobre suas atividades.

        Aqui podem vir os parametros do decorator.
        """
        super(WaldoReport, self).__init__()
        self.sinal.connect(self.qml_waldo_slot)

    def __call__(self, funcao):
        def wrapped_func(*fnargs, **fnkwargs):
            self.waldo = fnargs[0]
            self.falar("{} - {}".format(self.waldo.modulo.nome_classe, funcao.__name__))
            time.sleep(1)
            self.enviar_sinal(funcao.__name__)
            time.sleep(1)
            resultado = funcao(*fnargs, **fnkwargs)
            return resultado
        return wrapped_func

    def falar(self, mensagem):
        """Waldo fala."""
        #obs. Existem módulos mais práticos para colorir as coisas.
        print "{}Waldo {}>{} {}".format(self.waldo.cor, self.waldo.nome, '\033[0m', mensagem)

