from kivy.animation import Animation
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
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)))


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
    # b: size_hint de los botones "ajustes" e "información",,,solo height,,, cambiar????
    size1 = (1, .27)


# Ventana principal de la aplicación
class MenuPrincipal(Screen):
    pass


# La clase VentanaLayout contendrá las características generales para todas las ventanas de la aplicación
class VentanaLayout(Screen):
    pass


# La clase VentanaLayout contendrá las características generales para las ventanas secundarias
class VentanaLayout2(Screen):
    pass


# Inicio de las clases de las ventanas que luego iniciaremos en otro lado por guardar un orden
class InformacionVentana(VentanaLayout2):
    pass


class AjustesVentana(VentanaLayout2):
    pass


class MasInfoVentana(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def volver(self):
        self.manager.transition = FadeTransition()
        self.manager.current = self.manager.previous()
        self.manager.transition = SlideTransition()


class tfgApp(MDApp):
    color1 = (0, 0, 0.1961, 1)
    color2 = ()

    def build(self):
        # REVISAR WINDOW.SIZE,,,,¿no se puede hacer relativo?,,,,en móvil da igual
        Window.size = (1000, 600)
        minwinsize = ('1000dp', '600dp')
        Window.clearcolor = (0, .4, .6, 1)
        Window.minimum_width, Window.minimum_height = minwinsize
        return Manager()

    # funciones que describen el comportamiento al pasar el ratón por encima de cada botón del menú principal
    def descambiar(self):
        self.root.ids.imagencita.source = ''
        self.root.ids.etiqueta.text = 'Seleccione un ítem'

    def cambiar1(self):
        self.root.ids.imagencita.source = 'images/bimatricillo.jpg'
        self.root.ids.etiqueta.text = 'Halla todos los equilibrios de Nash de un juego dadas las matrices de pagos de los 2 jugadores.'

    def cambiar2(self):
        self.root.ids.imagencita.source = 'images/cournotillo.jpg'
        self.root.ids.etiqueta.text = 'Modelo de Cournot'

    def cambiar3(self):
        self.root.ids.imagencita.source = 'images/stackillo.jpg'
        self.root.ids.etiqueta.text = 'Modelo de Stackelberg'

    def cambiar4(self):
        self.root.ids.imagencita.source = 'images/bertranillo.png'
        self.root.ids.etiqueta.text = 'Modelo de Bertrand'

    def cambiar5(self):
        self.root.ids.imagencita.source = 'images/npcillo.jpg'
        self.root.ids.etiqueta.text = 'Jugar contra el ordenador'


if __name__ == '__main__':
    tfgApp().run()
