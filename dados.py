# coding=utf-8
#
# Pablo T. Carreira
import numpy as np
import os
import warnings


class Dado(object):
    nome = None

    def __init__(self, valores=None, cache_path=None):
        """Define um dado que que é gerado por um módulo.
         Deve ser reinstanciado para definir tipos de dados_OLD personalizados para cada tipo de módulo.

        :param valores: Valores para serem adicionados na criação.
        :param cache_path: Caminho do cache.
        """
        self._valores = None
        self.cache_path = cache_path
        if valores is not None:
            self.valores = valores

    def save_cache(self, cache_path):
        """Escreve os dados para um determinado cache. Fazer o override para cada tipo.
        Ou transformar em mixin.
        """
        raise NotImplementedError

    def load_cache(self, cache_path):
        """Lê os dados de um determinado cache. Fazer o override para cada tipo.
        Ou transformar em mixin.
        """
        raise NotImplementedError

    def delete_cache(self, cache_path):
        """Apaga a matriz do disco."""
        os.remove(cache_path)

    @property
    def valores(self):
        """Retorna os dados armazenados na propriedade valores."""
        if self._valores is None and not self.cache_path:
            raise ValueError("Dado {} sem valores.".format(self))
        elif self._valores is None and self.cache_path:
            self.load_cache(self.cache_path)
        return self._valores

    @valores.setter
    def valores(self, valores):
        """Armazena os dados na propriedade 'valores'.

        :param valores:
        :raise ValueError:
        """
        try:
            self.verificar(valores)
        except AssertionError:
            raise AssertionError('Modulo {} não produz dados do tipo correto.'.format(self.nome))
        else:
            self._valores = valores

    def verificar(self, valores):
        """Verifica se o dado salvo em valores é do tipo correto.
        Pode ser um classmethod pois a verificação pode ser utilizada em outros pontos além dos módulos.
        """
        warnings.warn("Não é recomendado utilizar a classe {} sem verificação.".format(self.__class__.__name__))
        if valores is None:
            raise ValueError('Valores não pode receber um NoneType')


class NumpyArrayDict(Dado):
    """Dicionario contendo arrays de dados."""
    def load_cache(self, cache_path):
        self._valores = np.load(cache_path)

    def save_cache(self, cache_path):
        np.savez_compressed(cache_path, self.valores)
        #Apaga a extenssão do arquivo.
        os.rename(cache_path + '.npz', cache_path)

    def verificar(self, valores):
        assert isinstance(valores, dict)
        for chave, matriz in valores.iteritems():
            assert isinstance(matriz, (np.ndarray, dict))