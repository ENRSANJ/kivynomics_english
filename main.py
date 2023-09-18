from kivy import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '1000')
Config.set('graphics', 'minimum_height', '600')

from kivy.animation import Animation
from kivy.uix.label import Label
from kivymd.app import MDApp
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

    a = '''This application is the result of a bachelor's degree thesis in economics focused on game theory. \
The application implements fundamental game theory models in their most basic versions, aiming to provide an accessible \
and understandable approach to the subject. For more information about the models and their specific implementation, \
you can access the full text of the bachelor's degree thesis by clicking on the corresponding button.\



You can access the complete source code of the application on Github. Additionally, there is an Android version of the \
application that replicates the "Play vs NPC" section. The complete code for the Android app is also available in its \
respective Github repository along with the packaged apk. For any issues, questions, suggestions, or contributions, you \
can contact me through Github.'''

    def volver(self):
        self.manager.current = 'Main Menu'
        self.manager.transition.direction = 'right'


class AjustesVentana(MasInfoVentana):
    def volver(self):
        self.manager.current = 'Main Menu'
        self.manager.transition.direction = 'right'


class kivynomicsApp(MDApp):
    color1 = (0, 0, 0.1961, 1)
    color2 = ()

    def build(self):
        return Manager()

    # funciones que describen el comportamiento al pasar el ratón por encima de cada botón del menú principal
    def descambiar(self):
        self.root.ids.imagencita.source = ''
        self.root.ids.etiqueta.text = 'Seleccione un ítem'

    def cambiar1(self):
        self.root.ids.imagencita.source = 'images/bimatricillo.jpg'
        self.root.ids.etiqueta.text = '''Find all Nash's extreme equilibria of a game given the payment matrices of two
players'''

    def cambiar2(self):
        self.root.ids.imagencita.source = 'images/cournotillo.jpg'
        self.root.ids.etiqueta.text = '''Given the market demand function and the cost functions of two companies,
calculate Cournot's equilibrium'''

    def cambiar3(self):
        self.root.ids.imagencita.source = 'images/stackillo.jpg'
        self.root.ids.etiqueta.text = '''Given the market demand function and the cost functions of two companies,
calculate Stackelberg's equilibrium'''

    def cambiar4(self):
        self.root.ids.imagencita.source = 'images/bertranillo.jpg'
        self.root.ids.etiqueta.text = '''Given the market demand function and the cost functions of two companies,
calculate Bertrand's equilibrium'''

    def cambiar5(self):
        self.root.ids.imagencita.source = 'images/npcillo.jpg'
        self.root.ids.etiqueta.text = '''Face the computer in several stages where you will have to decide an optimal
strategy to respond to the models developed in the application'''


if __name__ == '__main__':
    kivynomicsApp().run()
