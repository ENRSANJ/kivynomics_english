from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.button import Button


class RoundedButton(Button):
    pass


# Clase para las etiquetas de texto ajustadas a su tamaño (wrapped)
class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = 'center'
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))


# Sólo ajustado el ancho, para el output de Bimatrix Games
class WrappedLabel2(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = 'center'
        self.bind(
            width=lambda *x: self.setter('text_size')(self, (self.width, None)))


# Botones de selección de ventana del menú principal
class HoverButton(RoundedButton, ThemableBehavior, HoverBehavior):

    def on_enter(self, *args):
        Animation(size_hint=(1.2, 1.2), d=0.1).start(self)

    def on_leave(self, *args):
        Animation(size_hint=(1, 1), d=0.1).start(self)


# Botones de información y ajustes
class HoverButton2(RoundedButton, ThemableBehavior, HoverBehavior):

    def on_enter(self, *args):
        Animation(size_hint=(1.1, .3), d=0.1).start(self)

    def on_leave(self, *args):
        Animation(size_hint=(1, .25), d=0.1).start(self)


# Botón de regreso al menú principal de cada ventana
class HoverButton3(RoundedButton, ThemableBehavior, HoverBehavior):

    def on_enter(self, *args):
        Animation(size_hint=(1.1, 1.1), d=0.05).start(self)

    def on_leave(self, *args):
        Animation(size_hint=(1, 1), d=0.05).start(self)


# Botón calcula de bimatrixventana
class HoverButton4(RoundedButton, ThemableBehavior, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        Animation(size_hint=(.1, .1), d=0.05).start(self)

    def on_leave(self, *args):
        Animation(size_hint=(.09, .09), d=0.05).start(self)

# Root de la aplicación
class Manager(ScreenManager):
    # size_hint de los botones "ajustes" e "información"
    size1 = (1, .27)
    clicked1bool = True
    clicked2bool = True

    # Método para vaciar el output de Cournot si es la primera vez que entramos
    def clicked1(self):
        if self.clicked1bool:
            self.ids.cournotid.ids.fr1.text = ''
            self.ids.cournotid.ids.fr2.text = ''
            self.clicked1bool = False
        else:
            pass

    # Método para vaciar el output de Stackelberg si es la primera vez que entramos
    def clicked2(self):
        if self.clicked2bool:
            self.ids.stackelbergid.ids.fr2.text = ''
            self.clicked2bool = False
        else:
            pass


# Ventana principal de la aplicación
class MenuPrincipal(Screen):
    pass


# La clase VentanaLayout contendrá las características generales para todas las ventanas de la aplicación
class VentanaLayout(Screen):
    pass


# Clase para las ventanas de más información de cada apartado de la aplicación
class MasInfoVentana(Screen):

    def volver(self):
        self.manager.transition = FadeTransition()
        self.manager.current = self.manager.previous()
        self.manager.transition = SlideTransition()


# Ventanas de información y ajustes del menú principal
class InformacionVentana(MasInfoVentana):

    a = '''Esta aplicación es el resultado de un trabajo de fin de grado en economía centrado\
 en la teoría de juegos. La aplicación implementa los modelos de teoría de juegos fundamentales\
 en sus versiones más básicas, con el fin de ofrecer una aproximación accesible y comprensible\
 a la materia. Para más información sobre los modelos y su implementación concreta, puedes\
 acceder al texto completo del TFG haciendo click sobre el botón correspondiente.\


Puedes acceder al código fuente completo de la aplicación en Github. Asimismo, existe una versión de la aplicación\
 para Android, que contiene el apartado "Jugar vs NPC". El código completo de la app de Android también está\
 disponible en su correspondiente repositorio de Github junto con el apk ya empaquetado. Para cualquier\
 problema, pregunta, sugerencia o aporte puedes contactarme a través de Github'''

    def volver(self):
        self.manager.current = 'MenuPrincipal'
        self.manager.transition.direction = 'right'


class AjustesVentana(MasInfoVentana):
    def volver(self):
        self.manager.current = 'MenuPrincipal'
        self.manager.transition.direction = 'right'


class kivynomicsApp(MDApp):
    color1 = (0, 0, 0.1961, 1)
    color2 = ()

    def build(self):
        # REVISAR WINDOW.SIZE,,,,¿no se puede hacer relativo?,,,,en móvil da igual
        Window.size = (dp(1000), dp(600))
        minwinsize = ('1000dp', '600dp')
        Window.minimum_width, Window.minimum_height = minwinsize
        return Manager()

    # funciones que describen el comportamiento al pasar el ratón por encima de cada botón del menú principal
    def descambiar(self):
        self.root.ids.imagencita.source = ''
        self.root.ids.etiqueta.text = 'Seleccione un ítem'

    def cambiar1(self):
        self.root.ids.imagencita.source = 'images/bimatricillo.jpg'
        self.root.ids.etiqueta.text = '''Halla todos los equilibrios extremos de Nash de un juego dadas \
las matrices de pagos de los dos jugadores.'''

    def cambiar2(self):
        self.root.ids.imagencita.source = 'images/cournotillo.jpg'
        self.root.ids.etiqueta.text = '''Dadas la función de demanda del mercado y las funciones de costes de dos\
 empresas, calcula el equilibrio de Cournot-Nash.'''

    def cambiar3(self):
        self.root.ids.imagencita.source = 'images/stackillo.jpg'
        self.root.ids.etiqueta.text = '''Dadas la función de demanda del mercado y las funciones de costes de dos\
 empresas, calcula el equilibrio de Stackelberg-Nash.'''

    def cambiar4(self):
        self.root.ids.imagencita.source = 'images/bertranillo.jpg'
        self.root.ids.etiqueta.text = '''Dadas la función de demanda del mercado y las funciones de costes de dos\
 empresas, calcula el equilibrio de Bertrand.'''

    def cambiar5(self):
        self.root.ids.imagencita.source = 'images/npcillo.jpg'
        self.root.ids.etiqueta.text = '''Enfréntate al ordenador en varias etapas donde tendrás decidir una estrategia\
 óptima para dar respuesta a los modelos desarrollados en la aplicación.'''


if __name__ == '__main__':
    kivynomicsApp().run()
