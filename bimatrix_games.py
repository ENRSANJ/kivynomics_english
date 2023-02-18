import numpy as np
import pygambit as pg
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from main import VentanaLayout, MasInfoVentana, WrappedLabel, WrappedLabel2


# Representaremos 3 decimales en cada output de la aplicación,,,,,,,,,,,,,,,EDITABLE EN OPCIONES?????
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

Builder.load_file('bimatrix_games.kv')

rows = 2
cols = 2


# Mensaje de error por defecto
class MensajeDeError(Popup):
    def __init__(self, mensaje, **kwargs):
        super().__init__(**kwargs)

        self.title = '¡ERROR!'
        self.mensaje = mensaje
        self.size_hint = (.3, .3)

        msg = WrappedLabel(text=mensaje, font_size=self.height * 0.2)
        self.add_widget(msg)


class MensajeDeError2(MensajeDeError):
    def __init__(self, **kwargs):
        a = 'Debe rellenar todas las posiciones de cada matriz de pagos con valores numéricos'
        super().__init__(mensaje=a, **kwargs)


# Popup con los equilibrios de Nash del juego
class PopupNash(DragBehavior, Popup):
    # to allow dragbehavior
    def _align_center(self, *args):
        pass


# Ventana principal de Juegos Bimatriciales
class BimatrixVentana(VentanaLayout):
    altura1 = .75
    espaciado1 = .105

    # Cálculo de los equilibrios de Nash
    def calculanash(self):
        lista1 = []
        lista2 = []

        # Recogemos los datos introducidos por el usuario
        try:
            for hijo in reversed(self.ids.matriz1.children):
                for nieto in reversed(hijo.children):
                    lista1.append(float(nieto.text))

            for hija in reversed(self.ids.matriz2.children):
                for nieta in reversed(hija.children):
                    lista2.append(float(nieta.text))

        # Los almacenamos en matrices de pagos, con el formato adecuado para pygambit
            payoff1 = [pg.Rational(num) for num in lista1]
            pagos1 = np.array(payoff1)
            matrizpagos1 = pagos1.reshape(rows, cols)

            payoff2 = [pg.Rational(num) for num in lista2]
            pagos2 = np.array(payoff2)
            matrizpagos2 = pagos2.reshape(rows, cols)
            juego = pg.Game.from_arrays(matrizpagos1, matrizpagos2)

            # Popup con Scrollview para mostrar el output
            scroll = ScrollView()
            solpopupnash = PopupNash(content=scroll)
            grid = GridLayout(cols=1, size_hint=(1, None), padding='.5dp')
            scroll.add_widget(grid)
            grid.bind(minimum_height=grid.setter('height'))

        # Mostramos como output los equilibrios de Nash, con un formato accesible
            for eq in pg.nash.enummixed_solve(juego, rational=False):
                strats = np.array(eq)
                eq_payoff = np.array2string(np.array([eq.payoff(player) for player in range(2)]), separator=', ')

                a = str('V*[' + np.array2string(strats[:rows], separator=', ').replace('[', '(').replace(']', ')') +
                        ', ' + np.array2string(strats[cols:], separator=', ').replace('[', '(').replace(']', ')') +
                        ']  EP: ' + str(eq_payoff))

                c = WrappedLabel2(text=a, color=(0, 0, 0, 1), font_size=self.height * 0.022, size_hint=(1, None))
                grid.add_widget(c)

            solpopupnash.open()

        except ValueError:
            alertanash = MensajeDeError2()
            alertanash.open()

    def sumanula(self):
        lista = []

        try:
            for hijo in self.ids.matriz1.children:
                for nieto in hijo.children:
                    lista.append(float(nieto.text))
            lista2 = np.array_split(lista, rows)
            for hija, sublista in zip(self.ids.matriz2.children, lista2):
                for nieta, a in zip(hija.children, sublista):
                    nieta.text = str(-a)

        except ValueError:
            alertanash = MensajeDeError2()
            alertanash.open()

    def simetrico(self):
        lista = []
        if rows == cols:
            try:
                for hijo in self.ids.matriz1.children:
                    for nieto in hijo.children:
                        lista.append(float(nieto.text))
                lista2 = np.array(lista).reshape(rows, cols).transpose()
                for hija, sublista in zip(self.ids.matriz2.children, lista2):
                    for nieta, a in zip(hija.children, sublista):
                        nieta.text = str(a)
            except ValueError:
                alertanash = MensajeDeError2()
                alertanash.open()
        else:
            matricesnosimetricas = MensajeDeError('Las matrices de pagos deben ser cuadradas para un juego simétrico')
            matricesnosimetricas.open()

    def aleatorio(self):
        for hijo in self.ids.matriz1.children:
            for nieto in hijo.children:
                nieto.text = str(np.random.randint(-10, 10))

        for hija in self.ids.matriz2.children:
            for nieta in hija.children:
                nieta.text = str(np.random.randint(-10, 10))

    def vaciar(self):
        for hijo in self.ids.matriz1.children:
            for nieto in hijo.children:
                nieto.text = ''

        for hija in self.ids.matriz2.children:
            for nieta in hija.children:
                nieta.text = ''

    def obtenermasinfo(self):
        self.manager.current = 'BimatrixMasInfoScreen'


# BoxLayout para la selección del número de filas y columnas
class SeleccionaRango(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def confirmarango(self):
        global rows, cols
        try:

            if int(self.ids.numrows.text) in range(2, 7) and int(self.ids.numcols.text) in range(2, 7):
                rows = int(self.ids.numrows.text)
                cols = int(self.ids.numcols.text)
                Caja.cambiarango(self.parent.ids.matriz1)
                Caja.cambiarango(self.parent.ids.matriz2)
            else:
                errorrango = MensajeDeError('Introduzca un número de filas y columnas entre [2 y 6]')
                errorrango.open()

        except ValueError:
            errorrango = MensajeDeError('Introduzca un número de filas y columnas entre [1 y 6]')
            errorrango.open()

        self.ids.numrows.text = ''
        self.ids.numcols.text = ''


# Clase para el botón de "Ok" de SeleccionaRango
class OkButton(Button, ThemableBehavior, HoverBehavior):

    def on_enter(self, *args):
        Animation(size_hint=(1, 1), d=0.1).start(self)

    def on_leave(self, *args):
        Animation(size_hint=(1, .9), d=0.1).start(self)


# BoxLayout que contendrá cada una de las matrices en pantalla
class Caja(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.cambiarango()
        self.spacing = '10dp'

    def cambiarango(self):
        self.clear_widgets()
        for x in range(rows):
            a = Fila()
            self.add_widget(a)

        for x in self.children:
            for y in range(cols):
                x.add_widget(Cuadradito())


# Fila de las matrices (contendrá a los "Cuadraditos")
class Fila(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spacing = '20dp'


# TextInput para cada elemento de las matrices
class Cuadradito(TextInput):
    pass


# Textinput para la selección del número de filas y columnas de las matrices de pagos
class SeleccionaInput(TextInput):
    pass


class BimatrixMasInfoScreen(MasInfoVentana):
    pass
