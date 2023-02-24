from kivy.lang import Builder
from cournot import CournotVentana


Builder.load_file('stackelberg.kv')


# Heredamos la clase CournotVentana pues los modelos son muy parecidos y solo nos hará falta sobreescribir algún método
class StackelbergVentana(CournotVentana):

    # Sobreescribimos el método obtenermasinfo para abrir una ventana de más info distinta
    def obtenermasinfo(self):
        print('soyStackelberg')

    # Sobreescribimos también el método "calcula" pues el equilibrio hallado es diferente
    def calcula(self):
        print('the notorious')
