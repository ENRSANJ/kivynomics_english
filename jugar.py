import numpy as np
from kivy.lang import Builder
from kivy.properties import StringProperty

from bimatrix_games import MensajeDeError
from main import VentanaLayout


Builder.load_file('jugar.kv')


class JugarVentana(VentanaLayout):

    # Asignamos valores aleatorios al inicio del juego
    a = np.random.randint(21, 100)
    b = np.random.randint(2, 10)
    c = np.random.randint(2, 10)

    narrativa = '''El Estado introdujo un impuesto sobre la producción\
 de 5 € por unidad'''

    demanda_mercado = StringProperty(f'{a} - {b}x')
    costes_totales = f'{c}x'
    imagen = 'images/johnnash.jpg'

    def obtenermasinfo(self):
        print('adiós')

    def evento_aleatorio(self):
        pass

    def confirma(self):
        # Comprobamos si el usuario introdujo un valor admitido
        try:
            respuesta = np.around(float(self.ids.respuesta.text), 3)
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetros válidos')
            alerta.open()
            return

        # Cournot
        if cournot:
            self.prod2 = (self.a-self.c)/(3*self.b)

        # NPC líder
        elif stackelberg1:
            self.prod2 = (self.a-self.c)/(2*self.b)

        # NPC seguidor
        elif stackelberg2:
            self.prod2 = (self.a-self.c)/(4*self.b)

        # Bertrand
        else:
            self.prod2 =

        self.precio = self.a - self.b*(respuesta+self.prod2)

        self.beneficio1 = (self.precio-self.c)*respuesta
        self.beneficio2 = (self.precio-self.c)*self.prod2
