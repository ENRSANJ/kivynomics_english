import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup

from bimatrix_games import MensajeDeError
from main import VentanaLayout, MasInfoVentana

Builder.load_file('jugar.kv')


class NPC:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases


class NPCNash(NPC):
    def __init__(self, img, frases):
        super().__init__(img, frases)

    # Cournot
    def cournot(self, a, b, c):
        return (a - c) / (3 * b)

    # Líder
    def stackelberg1(self, a, b, c):
        return (a - c) / (2 * b)

    # Seguidora
    def stackelberg2(self, a, b, c):
        return (a - c) / (4 * b)

    # Bertrand
    def bertrand(self, a, b, c):
        return a + b + c


npc_Nash = NPCNash('images/johnnash.jpg', ['frase 1', 'frase 999'])

npc_Marx = NPCNash('images/karlmarx.jpeg', ['frase 1', 'frase 999'])

npc_Smith = NPCNash('images/adamsmith.jpg', ['frase 1', 'frase 999'])


class NPCSmith:
    pass


class NPCMarx:
    pass


class SelectPlayer(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.referencia = App.get_running_app().root.ids.jugarid

    def selection1(self):
        self.referencia.player2 = npc_Nash
        self.dismiss()
        self.referencia.inicio_juego()

    def selection2(self):
        self.referencia.player2 = npc_Smith
        self.dismiss()
        self.referencia.inicio_juego()

    def selection3(self):
        self.referencia.player2 = npc_Marx
        self.dismiss()
        self.referencia.inicio_juego()


class JugarVentana(VentanaLayout):
    stage = 0
    player2 = None
    prod2 = 0
    precio = 0
    beneficio1 = 0
    beneficio2 = 0
    cantidad_total = 0
    evento = 0
    historial = {}

    # Asignamos valores aleatorios al inicio del juego
    a = np.random.randint(43, 100)
    b = np.random.randint(2, 10)
    c = np.random.randint(21, 30)

    # Valores a mostrar en pantalla
    modelo = StringProperty('')
    narrativa = StringProperty('')
    demanda_mercado = StringProperty(f'{a} - {b}x')
    costes_totales = StringProperty(f'{c}x')
    imagen = StringProperty('')
    rival = None

    def on_enter(self, *args):
        if self.stage == 0:
            selector = SelectPlayer()
            selector.open()
        else:
            pass

    def obtenermasinfo(self):
        self.manager.current = 'JugarMasInfoScreen'

    def inicio_juego(self):
        self.imagen = str(self.player2.img)

    def evento_aleatorio(self):
        # Selección aleatoria del evento y la cuantía
        self.evento = np.random.randint(1, 6)
        cuantia = np.random.randint(1, 10)

        # Si el evento afecta a la demanda, modificamos la demanda (y viceversa)
        if self.evento == 1:
            self.narrativa = 'Aumento demanda del mercado'
            self.a = self.a + cuantia

        elif self.evento == 2:
            self.narrativa = 'Reducción demanda del mercado'
            self.a = self.a - cuantia

        elif self.evento == 3:
            self.c = self.c + cuantia
            self.narrativa = f'''El Gobierno introdujo un impuesto de {cuantia} u.m. sobre la producción.\
 Los cambios se han introducido en tu función de costes'''

        elif self.evento == 4:
            self.narrativa = 'Reducción de costes totales'
            self.c = self.c - cuantia

        else:
            self.narrativa = 'No sucedió ningún evento'

        self.demanda_mercado = f'{self.a} - {self.b}x'
        self.costes_totales = f'{self.c}x'

    def confirma(self):

        # Comprobamos si el juego se ha acabado
        if self.stage == 3:
            alerta = MensajeDeError('Ha finalizado el juego')
            alerta.open()
            self.historial = {}
            self.stage = 0
            return
        else:
            self.stage += 1

        # Comprobamos si el usuario introdujo un valor admitido
        try:
            respuesta = np.around(float(self.ids.respuesta.text), 3)
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetros válidos')
            alerta.open()
            return

        model = np.random.randint(1, 5)

        # Cournot
        if model == 1:
            self.modelo = 'MODELO DE COURNOT'
            self.prod2 = self.player2.cournot(self.a, self.b, self.c)

        # NPC Stackelberg líder
        elif model == 2:
            self.modelo = 'MODELO DE LÍDER'
            self.prod2 = self.player2.stackelberg1(self.a, self.b, self.c)

        # NPC Stackelberg seguidor
        elif model == 3:
            self.modelo = 'MODELO DE STACKELBERG SEGUIDOR'
            self.prod2 = self.player2.stackelberg2(self.a, self.b, self.c)

        # Bertrand
        else:
            self.modelo = 'MODELO DE BERTRAND'
            self.prod2 = self.player2.bertrand(self.a, self.b, self.c)

        self.prod2 = np.around(self.prod2)
        self.cantidad_total = np.around(respuesta + self.prod2, 3)
        self.precio = np.around(self.a - self.b * self.cantidad_total, 3)
        self.beneficio1 = np.around((self.precio - self.c) * respuesta, 3)
        self.beneficio2 = np.around((self.precio - self.c) * self.prod2, 3)

        # Rellenamos el historial
        self.historial[self.stage] = [[model, self.a, self.b, self.c], [self.precio, self.cantidad_total],
                                      [respuesta, self.beneficio1], [self.prod2, self.beneficio2]]
        print(self.historial)

        self.evento_aleatorio()


class JugarMasInfoScreen(MasInfoVentana):
    pass
