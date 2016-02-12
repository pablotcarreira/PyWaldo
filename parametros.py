# coding=utf-8
#
# Pablo T. Carreira
import inspect
import json


class Params(object):
    is_dirty = True

    def __init__(self, *args, **kwargs):
        """Classe que armazena os parâmetros para a configuração do processamento de qualquer coisa.
        Reinstanciar e definir os parametros disponíveis assim eles ficam disponíveis para a inspeção
        e verificação.

        Um objeto params pode ser criado já configurando seus parametros da seguinte forma:
        # 1- Com um dicionário que vem do cliente ou do banco de dados_OLD.
            params_dict = {'foo': 'bar', 'bacon': 'eggs'}
            params = ParamsSomeModule(params_json)

        # 2- Com argumentos nomeados.
            params = ParamsSomeModule(foo=bar, bacon=eggs)

        # 3- Sem parametros, e depois passando os parametros para o método load,
         que funciona igual as formas anteriores (dicionário ou arqgumentos)
        params = ParamsSomeModule()
        params.load(foo=bar, bacon=eggs)
        """
        self.load(*args, **kwargs)

    def load(self, *args, **kwargs):
        """Carrega parametros neste parametro.
        Ver __init__ para mais detalhes de como  proceder.

        :param dict args: Dicionário de parametros.
        :param dict kwargs:
        """
        if args:
            kwargs = args[0]
        if kwargs:
            for chave in kwargs:
                setattr(self, chave, kwargs[chave])

    def dump(self):
        """Dumps the attributes into a dictionary.
        Atributos iniciado com _ são privados.
        Os atributos precisam ser serializaveis para funcionar.
        """
        params = {}
        for name, value in inspect.getmembers(self, lambda a: not(inspect.isroutine(a))):
            if name[0] != "_":
                # Verifica se é serializável.
                try:
                    json.dumps(value)
                except TypeError:
                    print('PARAMETRO NÃO SERIALIZÁVEL <{}>, UTILIZAR _PARAMETRO PARA EVITAR O ERRO PARAMS LINHA 56'.format(name))
                    continue
                else:
                    params[name] = value
        return params


class ParamsReceita(Params):
    receita = None
    params = []


class ParamsVirtual(Params):
    virtual_components = []
    _virtual_queryset = None
    modulo = None

if __name__ == "__main__":
    class MyParam(Params):
        uma = 1
        duas = 2
    mp = MyParam()
    mp.teste = ['oi', 'oi']

    print mp.dump()
