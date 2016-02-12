# coding=utf-8
#
# Pablo T. Carreira

import time

from PyQt5.QtCore import pyqtSignal,  QObject
from PyWaldo.waldos import Waldo


class QWaldo(QObject, Waldo):
    mover_signal = pyqtSignal(float)

    def __init__(self, qwaldo_component, view, **kwargs):
        super(QWaldo, self).__init__(**kwargs)
        # Cria o waldo qml.
        self.qmlwaldo = qwaldo_component.create()
        print self.qmlwaldo
        # Coloca ele na cena.
        self.qmlwaldo.setX(25)
        self.qmlwaldo.setY(525)
        self.qmlwaldo.setParentItem(view.rootObject())
        # Cria referencias para o grid de módulos.
        self.qml_modulos_grid = view.rootObject().findChild(QQuickItem, name="modulos_grid")
        print self.qml_modulos_grid

        # mover_signal - removido, esta aqui apenas para referencia.
        self.mover_signal.connect(self.qmlwaldo.mudarPosicao) #, PyQt5.QtCore.Qt.DirectConnection)

    def get_modulo_under_qmlwaldo(self):
        print self.qmlwaldo.y()
        modulo = self.qml_modulos_grid.childAt(self.qmlwaldo.x() + 10, self.qmlwaldo.y() + 10)
        print self.qmlwaldo.y()
        print modulo.objectName()
        return modulo

    def mover_qmlwaldo(self, resultado, direcao):
        if resultado:
            print("Mover para {}".format(direcao))
            if direcao == 'baixo':
                print "baixo"
                self.mover_signal.emit(+105)
            elif direcao == 'cima':
                self.mover_signal.emit(-105)
        modulo = self.get_modulo_under_qmlwaldo()
        # Delay artificial para que seja possível visualizar as etapas.
        time.sleep(0.5)

    def mover_para_baixo(self):
        resultado = super(QWaldo, self).mover_para_baixo()
        self.mover_qmlwaldo(resultado, 'baixo')
        return resultado

    def mover_para_cima(self):
        resultado = super(QWaldo, self).mover_para_cima()
        self.mover_qmlwaldo(resultado, 'cima')
        return resultado



# class First(object):
#   def __init__(self):
#     super(First, self).__init__()
#     print "first"
#
# class Second(object):
#   def __init__(self):
#     super(Second, self).__init__()
#     print "second"
#
# class Third(First, Second):
#   def __init__(self):
#     super(Third, self).__init__()
#     print "that's it"
#
# a = Third()