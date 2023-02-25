import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.lang import Builder
import sympy as sp
from kivy.uix.scrollview import ScrollView
from matplotlib import pyplot as plt
from bimatrix_games import MensajeDeError
from cournot import CournotVentana
from main import MasInfoVentana

Builder.load_file('stackelberg.kv')


# Heredamos la clase CournotVentana pues los modelos son muy parecidos y solo nos hará falta sobreescribir algún método
class StackelbergVentana(CournotVentana):

    # Sobreescribimos el método obtenermasinfo para abrir una ventana de más info distinta
    def obtenermasinfo(self):
        self.manager.current = 'StackelbergMasInfoScreen'

    # Sobreescribimos también el método "calcula" pues el equilibrio hallado es diferente
    def calcula(self):
        if not self.todo_en_orden():
            return

        # Almacenamos en variables el input del usuario
        a = float(self.ids.a.text)
        b = float(self.ids.b.text)
        c = float(self.ids.c.text)
        e = float(self.ids.e.text)

        # Definimos las variables del problema (cantidad producida por la empresa líder, la 1)
        x = sp.symbols('x')

        # Obtenemos la función de reacción de la empresa 2
        f2 = ((a - e)/(2 * b)) - (x/2)

        # Obtenemos la producción óptima de cada empresa y pasamos el valor a la StringProperty a mostrar
        x1_sol = (a + e - 2*c)/(2*b)
        x2_sol = (a - 3*e + 2*c)/(4*b)
        self.prod_1 = 'Producción óptima: ' + str(np.around(x1_sol, 3))
        self.prod_2 = 'Producción óptima: ' + str(np.around(x2_sol, 3))

        if (x1_sol < 0) or (x2_sol < 0):
            alerta = MensajeDeError('CANTIDAD ÓPTIMA NEGATIVA, modifique los parámetros')
            alerta.open()

        # Calculamos el beneficio de cada empresa y el precio final
        p = a - b * (x1_sol + x2_sol)
        self.beneficio1 = 'Beneficio: ' + str(np.around((p-c)*x1_sol, 3))
        self.beneficio2 = 'Beneficio: ' + str(np.around((p-e)*x2_sol, 3))
        self.precio = 'Precio en el mercado: ' + str(np.around(p, 3))
        self.empresa1 = 'EMPRESA LÍDER'
        self.empresa2 = 'EMPRESA SEGUIDORA'

        # GRÁFICO
        # Convert the sympy equation to a lambda function
        fl2 = sp.lambdify(x, f2)

        # Calculamos el mayor valor que pueden tomar x e y
        x1_max_f2 = (a - e)/b
        x2_max_f2 = (a - e)/(2*b)

        # escogemos un entero un 10% superior al máximo para graficarlo bien
        x1_max = int(np.ceil(1.1*x1_max_f2 + 1))
        x2_max = int(np.ceil(1.1*x2_max_f2 + 1))

        # Generamos los valores de x
        x_vals = np.linspace(0, x1_max, x1_max)

        # Calculamos los valores y asociados a cada valor de x mediante las funciones de reacción
        y2 = fl2(x_vals)

        # Dibujamos el gráfico
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Dibujamos las ecuaciones
        ax.plot(x_vals, y2, label='f2', color="orange")

        # Dibujamos el punto de equilibrio
        ax.plot(x1_sol, x2_sol, marker='o', markersize=5, c='black', alpha=1)
        ax.annotate(f'Eq ({x1_sol:.3f}, {x2_sol:.3f})', xy=(x1_sol, x2_sol),
                    xycoords='data', xytext=(5, 5), textcoords='offset points')

        # Editamos las características del gráfico
        plt.title('Funciones de reacción')
        plt.xlabel('x$_{1}$')
        plt.ylabel('x$_{2}$')

        ax.set_xlim(0, x1_max)
        ax.set_ylim(0, x2_max)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend()

        # Líneas de puntos entre los ejes y el punto de equilibrio
        ax.plot([x1_sol, x1_sol], [0, x2_sol], ':', c='black')
        ax.plot([0, x1_sol], [x2_sol, x2_sol], ':', c='black')

        # Cambiamos el grosor de los bordes
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_linewidth(2)

        # Creamos el widget FigureCanvasKivyAgg (vaciamos "graficournot" para eliminar el gráfico anterior)
        canvas = FigureCanvasKivyAgg(figure=fig)
        self.ids.graficournot.clear_widgets()
        self.ids.graficournot.add_widget(canvas)


class StackelbergMasInfoScreen(MasInfoVentana):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()

        self.add_widget(scroll)
