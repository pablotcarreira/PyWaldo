# coding=utf-8
#
# Pablo T. Carreira

import sys


# QT ####################################################

from InWaldo.receitas.produtividade import ReceitaProdutividade

# Waldos ################################################
from PyWaldo.waldos.qwaldo import QWaldo

# Prepara o Ambiente ####################################
app = QGuiApplication(sys.argv)


# Cria o componente.
engine = QQmlEngine()
qwaldo_component = QQmlComponent(engine)
qwaldo_component.loadUrl(QUrl('waldo/Waldo.qml'))

# Cria o View
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)
view.setSource(QUrl.fromLocalFile('waldo/stack_space.qml'))
view.show()

#  Exemplo: Instancia um QWaldo e move.
# waldinho = QWaldo(qwaldo_component, view)
# waldinho.qwaldo.mudarPosicao(300)


###############################################################
# Teste para processar produtividade com os waldos e modulos. #
###############################################################
# Uma receita.
receita_produtividade = ReceitaProdutividade()

# Um QWaldo
waldo1 = QWaldo(qwaldo_component, view)
#

# Para a visualização funcionar, colocar o waldo sobre o ultimo modulo.
print receita_produtividade.ultimo_modulo
waldo1.modulo = receita_produtividade.ultimo_modulo

tred = QThread()
waldo1.moveToThread(tred)
tred.started.connect(waldo1.calcular)

tred.start()

# waldo1.calcular_stack()






# Enter Qt main loop
sys.exit(app.exec_())



































