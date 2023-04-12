import numpy as np
from kivy.lang import Builder
from kivy.properties import StringProperty

from bimatrix_games import MensajeDeError
from main import VentanaLayout

Builder.load_file('jugar.kv')


class NPC:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases


class NPCNash(NPC):
    def __init__(self, img, frases):
        super().__init__(img, frases)

    def cournot(self, a, b, c):
        return (a - c) / (3 * b)

    # Líder
    def stackelberg1(self, a, b, c):
        return (a - c) / (2 * b)

    # Seguidora
    def stackelberg2(self, a, b, c):
        return (a - c) / (4 * b)

    def bertrand(self, a, b, c):
        return a + b + c


npc_Nash = NPCNash('images/johnnash.jpg', ['frase 1', 'frase 999'])


class NPCSmith:
    pass


class NPCMarx:
    pass


class JugarVentana(VentanaLayout):
    player2 = None
    # Asignamos valores aleatorios al inicio del juego
    a = np.random.randint(43, 100)
    b = np.random.randint(2, 10)
    c = np.random.randint(21, 30)

    # Valores a mostrar en pantalla
    narrativa = StringProperty('')
    demanda_mercado = StringProperty(f'{a} - {b}x')
    costes_totales = StringProperty(f'{c}x')
    imagen = StringProperty('')

    def obtenermasinfo(self):
        print('adiós')

    def select_player(self):
        self.player2 = npc_Nash
        self.imagen = str(self.player2.img)

    def evento_aleatorio(self):
        # Selección aleatoria del evento y la cuantía
        evento = np.random.randint(1, 6)
        cuantia = np.random.randint(1, 10)

        # Si el evento afecta a la demanda, modificamos la demanda (y viceversa)
        if evento == 1:
            self.narrativa = 'Aumento demanda del mercado'
            self.a = self.a + cuantia

        elif evento == 2:
            self.narrativa = 'Reducción demanda del mercado'
            self.a = self.a - cuantia

        elif evento == 3:
            self.narrativa = f'El Gobierno introdujo un impuesto de {cuantia} u.m. sobre la producción'
            self.c = self.c + cuantia

        elif evento == 4:
            self.narrativa = 'Reducción de costes totales'
            self.c = self.c - cuantia

        else:
            self.narrativa = 'No sucedió ningún evento'

        self.demanda_mercado = f'{self.a} - {self.b}x'
        self.costes_totales = f'{self.c}x'

    def confirma(self):
        self.select_player()
        # Comprobamos si el usuario introdujo un valor admitido
        try:
            respuesta = np.around(float(self.ids.respuesta.text), 3)
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetros válidos')
            alerta.open()
            return

        stage = np.random.randint(1, 5)

        # Cournot
        if stage == 1:
            self.prod2 = self.player2.cournot(self.a, self.b, self.c)

        # NPC Stackelberg líder
        elif stage == 2:
            self.prod2 = self.player2.stackelberg1(self.a, self.b, self.c)

        # NPC Stackelberg seguidor
        elif stage == 3:
            self.prod2 = self.player2.stackelberg2(self.a, self.b, self.c)

        # Bertrand
        else:
            self.prod2 = self.player2.bertrand(self.a, self.b, self.c)

        self.precio = self.a - self.b * (respuesta + self.prod2)
        self.beneficio1 = (self.precio - self.c) * respuesta
        self.beneficio2 = (self.precio - self.c) * self.prod2

        print(self.prod2)
        print(stage)
