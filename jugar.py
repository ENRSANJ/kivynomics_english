from kivy.lang import Builder
from main import VentanaLayout


Builder.load_file('jugar.kv')


class JugarVentana(VentanaLayout):

    def obtenermasinfo(self):
        print('adiós')
