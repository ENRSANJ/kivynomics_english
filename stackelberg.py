from kivy.lang import Builder
from main import VentanaLayout


Builder.load_file('stackelberg.kv')


class StackelbergVentana(VentanaLayout):

    def obtenermasinfo(self):
        print('soyStackelberg')
