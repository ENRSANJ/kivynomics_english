import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup

from bimatrix_games import MensajeDeError
from main import VentanaLayout, MasInfoVentana

Builder.load_file('jugar.kv')


class NPC:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases


class NPCNash:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases

    # Cournot
    @staticmethod
    def cournot(a, b, c):
        return (a - c) / (3 * b)

    # Líder
    @staticmethod
    def stackelberg1(a, b, c):
        return (a - c) / (2 * b)

    # Seguidora
    @staticmethod
    def stackelberg2(a, b, c):
        return (a - c) / (4 * b)

    # Bertrand
    @staticmethod
    def bertrand(c):
        return c


npc_Nash = NPCNash('images/johnnash.jpg', ['Buen día, prepárese para reportar las pérdidas más cuantiosas de su vida',
                                           'Llevo esperando este momento desde la salida de mi último libro'])

npc_Marx = NPCNash('images/karlmarx.jpeg', ['''Espero trates bien a tus trabajadores, no te quiero ver extrayendo\
 plusvalía''', 'frase 999'])

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


class ResetGame(Popup):
    pass


class JugarVentana(VentanaLayout):

    player2 = None
    prod1 = 0
    prod2 = 0
    precio = 0
    beneficio1 = 0
    beneficio2 = 0
    cantidad_total = 0
    evento = 0
    historial = {}
    model = 0
    precio2 = 0

    # Asignamos valores aleatorios al inicio del juego
    a = 0
    b = 0
    c = 0

    # Valores a mostrar en pantalla
    comentario = StringProperty('')
    modelo = StringProperty('')
    narrativa = StringProperty('')
    demanda_mercado = StringProperty(f'{a} - {b}x')
    costes_totales = StringProperty(f'{c}x')
    imagen = StringProperty('')
    rival = None
    stage = NumericProperty(1)
    stage1 = StringProperty('')
    stage2 = StringProperty('')
    stage3 = StringProperty('')

    def on_enter(self, *args):
        if self.stage == 1:
            selector = SelectPlayer()
            selector.open()
        else:
            pass

    def inicio_juego(self):
        # Asignamos valores aleatorios al inicio del juego
        self.a = np.random.randint(70, 150)
        self.b = np.random.randint(2, 15)
        self.c = np.random.randint(21, 40)

        self.imagen = str(self.player2.img)
        self.comentario = self.player2.frases[np.random.randint(0, 2)]
        self.update_screen()
        self.selecciona_modelo()

    def update_screen(self):
        self.demanda_mercado = f'{self.a} - {self.b}x'
        self.costes_totales = f'{self.c}x'

    def selecciona_modelo(self):
        self.model = np.random.randint(1, 5)

        # Cournot
        if self.model == 1:
            self.modelo = 'MODELO DE COURNOT'
            self.prod2 = np.around(self.player2.cournot(self.a, self.b, self.c), 3)

        # NPC Stackelberg líder
        elif self.model == 2:
            self.modelo = 'MODELO DE NPC = LÍDER'
            self.prod2 = np.around(self.player2.stackelberg1(self.a, self.b, self.c), 3)

        # NPC Stackelberg seguidor
        elif self.model == 3:
            self.modelo = 'MODELO DE STACKELBERG NPC = SEGUIDOR'
            self.prod2 = np.around(self.player2.stackelberg2(self.a, self.b, self.c), 3)

        # Bertrand
        else:
            self.modelo = 'MODELO DE BERTRAND'
            self.precio2 = self.player2.bertrand(self.c)

    def fin_juego(self):
        self.historial = {}
        self.stage = 1
        self.ids.respuesta.text = ''
        reseteo = ResetGame()
        reseteo.open()

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

        self.update_screen()

    def confirma(self):

        # Comprobamos si el juego se ha acabado
        if self.stage > 3:
            self.fin_juego()
            return

        # Comprobamos si el usuario introdujo un valor admitido
        try:
            respuesta = np.around(float(self.ids.respuesta.text), 3)
            if respuesta == 0:
                raise ValueError
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetros válidos')
            alerta.open()
            return

        # Si es modelo de Bertrand, la variable de decisión cambia
        if self.model == 4:
            self.precio2 = self.precio2

            if self.precio2 > respuesta:
                self.precio = respuesta
                self.prod1 = np.around((self.a - self.precio)/self.b, 3)
                self.prod2 = 0

            elif self.precio2 < respuesta:
                self.precio = self.precio2
                self.prod1 = 0
                self.prod2 = np.around((self.a - self.precio) / self.b, 3)

            # Por defecto, a igual precio suponemos los clientes se distribuyen equitativamente
            else:
                self.precio = respuesta
                self.prod1 = np.around((self.a - self.precio) / (2*self.b), 3)
                self.prod2 = np.around((self.a - self.precio) / (2*self.b), 3)

        else:
            self.prod1 = respuesta
            self.precio = np.around(self.a - (self.b * (self.prod1 + self.prod2)), 3)

        self.cantidad_total = np.around(self.prod1 + self.prod2, 3)
        self.beneficio1 = np.around((self.precio - self.c) * self.prod1, 3)
        self.beneficio2 = np.around((self.precio - self.c) * self.prod2, 3)

        # Rellenamos el historial
        self.historial[self.stage] = [[self.model, self.a, self.b, self.c], [self.precio, self.cantidad_total],
                                      [self.prod1, self.beneficio1], [self.prod2, self.beneficio2]]

        stage_dict = {1: 'stage1', 2: 'stage2', 3: 'stage3'}
        stage_key = stage_dict.get(self.stage)
        setattr(self, stage_key, f'Beneficio: {self.beneficio1}')

        print(self.historial)

        # Pasamos de etapa
        self.stage += 1

        self.selecciona_modelo()

    def obtenermasinfo(self):
        self.manager.current = 'JugarMasInfoScreen'


class JugarMasInfoScreen(MasInfoVentana):
    pass
