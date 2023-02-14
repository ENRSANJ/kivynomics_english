from kivy.lang import Builder
from main import VentanaLayout


Builder.load_file('bertrand.kv')


class BertrandVentana(VentanaLayout):

    def obtenermasinfo(self):
        print('soyBertrand')
