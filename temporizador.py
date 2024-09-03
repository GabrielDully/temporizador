import pandas as pd
import time

# Módulo para armazenar instantes e calcular durações de procedimentos.
class temporizador(object):

    def __init__(self):
        self.instantes = {}
        self.origem = time.time()


    def get_instantes(self):
        return self.instantes


    def get_origem(self):
        return self.origem


    def iniciar(self, rotulo):

        self.instantes[rotulo] = {
            'inicio': time.time() - self.origem,
            'termino': None
        }


    def finalizar(self, rotulo):

        try:
            self.instantes[rotulo]['termino'] = time.time() - self.origem

            print(f"(período)   Duração de '{rotulo}': {temporizador.formatar_seg(self.instantes[rotulo]['termino'] - self.instantes[rotulo]['inicio'])}\n")

        except KeyError:

            raise KeyError(f"O rótulo '{rotulo}' foi finalizado sem ter sido inicializado.")


    def total(self):
        print(f'Tempo total de execução: {temporizador.formatar_seg(time.time() - self.origem)}')


    def exportar_periodos(self, mypath, nome=''):

        path_file_time = f'{mypath}tempos/{nome}.txt'

        with open(path_file_time, 'w') as arquivo:

            for rotulo, instantes in self.instantes.items():

                linha = f"{rotulo}: {instantes['termino'] - instantes['inicio']}"
                arquivo.write(f'{linha}\n')


    def exportar_instantes(self):

        lista = []

        i = 0
        for key, valor in self.instantes.items():

            lista.append([])

            lista[i].append('inicio: ' + key)
            lista[i].append(valor['inicio'])

            if valor['termino']:
                i += 1
                lista.append([])
                lista[i].append('termino: ' + key)
                lista[i].append(valor['termino'])

            i += 1

        lista_ordenada = sorted(lista, key=lambda x: x[1])
        df_tempo = pd.DataFrame(index=range(1), columns=[x[0] for x in lista_ordenada])

        for elemento in lista_ordenada:
            df_tempo[elemento[0]] = elemento[1]


        df_tempo.to_excel('historico_de_instantes.xlsx', index=False)


    @staticmethod
    def formatar_seg(segundos: float):

        horas, segundos = divmod(segundos, 3600)
        minutos, segundos = divmod(segundos, 60)

        str_aux = ''
        if horas:
            str_aux += f'{int(horas)}h '
        if minutos:
            str_aux += f'{int(minutos)}m '
        str_aux += f'{segundos:.4f}s'

        return str_aux
