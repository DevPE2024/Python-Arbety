class Cores:
    def __init__(self):
        self.padroes_red = {
            ('green', 'red', 'green'): 'red',
            ('green', 'red', 'red', 'green'): 'red',
            ('red', 'red'): 'red',
            ('red', 'green','green', 'red'): 'red',
            ('red', 'white'): 'red',
            ('green', 'white'): 'red',
        }
        self.padroes_green = {
            ('red', 'green', 'red'): 'green',
            ('red', 'green', 'green', 'red'): 'green',
            ('green', 'green',): 'green',
            ('green', 'white', 'green'): 'green',
            ('green', 'white',): 'green',
            ('red', 'white',): 'green',
        }

    def get_padrao(self, lista_cores):
        # Conta a ocorrência de cada cor na lista
        contagem_cores = {'red': 0, 'green': 0, 'white': 0}
        for cor in lista_cores:
            contagem_cores[cor] += 1
        
        total = sum(contagem_cores.values())
        
        # Calcula as porcentagens
        porcentagem_red = (contagem_cores['red'] / total) * 100
        porcentagem_green = (contagem_cores['green'] / total) * 100
        
        # Escolhe o padrão com base na porcentagem
        if porcentagem_green >= porcentagem_red:
            return self.padroes_green
        else:
            return self.padroes_red
