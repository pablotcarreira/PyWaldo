# coding=utf-8


from __future__ import unicode_literals
import traceback
import sys


class WaldoBaseException(Exception):
    visible = True  # Esta flag determina se a excessão pode ser propagada para o cliente.
    message = u"{}"
    dica = u"Verifique os parâmetros de configuração. Se o problema não for solucionado, contate o suporte."

    def __init__(self, menssagem=None):
        self.message = self.message.format(menssagem)

    def __str__(self):
        return self.message


class WErroConfiguracao(WaldoBaseException):
    """Erro de configuração de um processamento ou recomendação."""
    message = u"Erro de configuracao: {}"

class WErroNaoCapturado(WaldoBaseException):
    """Erro levantado pelo Waldo quando um cálculo falha.
    Só deve ser usado pelo Waldo. Nunca usar em um módulo.
    """
    message = "Erro não capturado ao calcular {}."
    pass

