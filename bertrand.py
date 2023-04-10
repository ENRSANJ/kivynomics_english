import numpy as np
from kivy.lang import Builder
from bimatrix_games import MensajeDeError
from cournot import CournotVentana
from main import MasInfoVentana
from docx import Document
from docx.shared import Inches
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import sympy as sp

Builder.load_file('bertrand.kv')


class BertrandVentana(CournotVentana):

    def obtenermasinfo(self):
        self.manager.current = 'BertrandMasInfoScreen'

    def aleatorio(self):
        self.ids.a.text = str(np.random.randint(11, 30))
        self.ids.b.text = str(np.random.randint(1, 10))
        self.ids.c.text = str(np.random.randint(1, 10))
        self.ids.e.text = str(np.random.randint(1, 10))

    def calcula(self):
        if not self.todo_en_orden():
            return

        # Almacenamos en variables el input del usuario
        a = float(self.ids.a.text)
        b = float(self.ids.b.text)
        c = float(self.ids.c.text)
        e = float(self.ids.e.text)

        # Comprobamos si los parámetros son compatibles con una solución razonable del modelo
        if a <= c and a <= e:
            alerta = MensajeDeError('Introduzca parámetro válidos')
            alerta.open()
            return

        if c < e:
            # La empresa 1 se lleva toda la demanda
            if (c + a) / 2 > e:
                # Si no puede establecer precio de monopolio, establece
                # un precio marginalmente inferior al Coste Marginal de la empresa 2
                p = e - .001

            else:
                p = (c + a) / 2

            x1_sol = (a - p) / b
            x2_sol = 0
            self.prod_1 = 'Producción óptima: ' + str(np.around(x1_sol, 3))
            self.prod_2 = 'Producción óptima: 0'

            self.beneficio1 = 'Beneficio: ' + str(np.around((p - c) * x1_sol, 3))
            self.beneficio2 = 'Beneficio: 0'

        elif c > e:
            # La empresa 2 se lleva toda la demanda
            if (e + a) / 2 > c:
                # Si no puede establecer precio de monopolio, establece
                # un precio marginalmente inferior al Coste Marginal de la empresa 2
                p = c - .001

            else:
                p = (e + a) / 2

            x1_sol = 0
            x2_sol = (a - p) / b
            self.prod_1 = 'Producción óptima: 0'
            self.prod_2 = 'Producción óptima: ' + str(np.around(x2_sol, 3))

            self.beneficio1 = 'Beneficio: 0'
            self.beneficio2 = 'Beneficio: ' + str(np.around((p - e) * x2_sol, 3))

        else:
            # Distribuimos la demanda a partes iguales
            p = c
            x1_sol = (a - c) / (2 * b)
            x2_sol = (a - c) / (2 * b)
            self.prod_1 = 'Producción óptima: ' + str(np.around(x1_sol, 3))
            self.prod_2 = 'Producción óptima: ' + str(np.around(x2_sol, 3))

            self.beneficio1 = 'Beneficio: 0'
            self.beneficio2 = 'Beneficio: 0'

        self.precio = 'Precio en el mercado: ' + str(np.around(p, 3))
        self.empresa1 = 'EMPRESA 1'
        self.empresa2 = 'EMPRESA 2'

        # Gráfico
        # Generamos los valores de x

        demanda_max = int(np.ceil((a/b)*1.1))
        x_vals = np.linspace(0, demanda_max)

        # Creamos la función de demanda
        x = sp.symbols('x')
        fl1 = sp.lambdify(x, (a-b*x))

        # Calculamos los valores de p asociados a cada valor de x mediante la función de demanda
        y1 = fl1(x_vals)

        # Dibujamos el gráfico
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Dibujamos la ecuación
        ax.plot(x_vals, y1, color='b')

        # Dibujamos los costes marginales
        plt.axhline(y=c, color='r', linestyle='--')
        plt.axhline(y=e, color='r', linestyle='--')

        # Dibujamos la producción
        x_total = x1_sol+x2_sol
        ax.plot(x_total, p, marker='o', markersize=5, c='black', alpha=1)
        ax.annotate(f'Eq ({x_total:.3f}, {p:.3f})', xy=(x_total, p),
                    xycoords='data', xytext=(5, 5), textcoords='offset points')

        # Líneas de puntos entre los ejes y la producción de cada empresa
        ax.plot([x1_sol, x1_sol], [0, p], ':', c='black')
        ax.plot([x2_sol, x2_sol], [0, p], ':', c='black')

        # Editamos las características del gráfico
        plt.title('Modelo de Bertrand')
        plt.xlabel('x, x$_{1}$, x$_{2}$')
        plt.ylabel('p')

        ax.set_xlim(0, demanda_max)
        ax.set_ylim(0, int(np.ceil(a*1.1)))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(handles=[plt.plot([], [], 'b-', label='Función de demanda')[0],
                  plt.plot([], [], 'r--', label='Costes Marginales')[0]])

        # Cambiamos el grosor de los bordes
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_linewidth(2)

        # Creamos el widget FigureCanvasKivyAgg (vaciamos "graficournot" para eliminar el gráfico anterior)
        canvas = FigureCanvasKivyAgg(figure=fig)
        self.ids.graficournot.clear_widgets()
        self.ids.graficournot.add_widget(canvas)

        # Generamos el output en Word si el usuario lo requiere
        try:
            if self.ids.a_word.active:
                fdemanda = f'p(X) = {a} - {b}X ,    X = x\u2081 + x\u2082'
                ct1 = f'CT(x\u2081) = {c}x\u2081'
                ct2 = f'CT(x\u2082) = {e}x\u2082'

                fig.savefig('bertrand_graph.png')
                crear_bertrand_word(fdemanda, ct1, ct2, self.precio, self.prod_1,
                                    self.beneficio1, self.prod_2, self.beneficio2)
                alerta = MensajeDeError("Se ha creado el documento de Word 'bertrand_output.docx' exitosamente")
                alerta.title = ''
                alerta.open()
        except PermissionError:
            alerta = MensajeDeError("Cierra los archivos con nombre 'bertrand_output.docx' o 'bertrand_graph.png'")
            alerta.open()


# Método para exportar los resultados a Word
def crear_bertrand_word(fdemanda, ct1, ct2, precio, prod1, beneficio1, prod2, beneficio2):
    # Create a new Word document
    document = Document()

    # Añadimos nuestros datos al documento
    document.add_paragraph('MODELO DE BERTRAND')
    document.add_paragraph('Función de demanda del mercado: ' + fdemanda)
    document.add_paragraph('Costes totales de la empresa 1: ' + ct1)
    document.add_paragraph('Costes totales de la empresa 2: ' + ct2)
    document.add_paragraph()
    document.add_picture('bertrand_graph.png', width=Inches(6))
    document.add_paragraph('Resultados: ')
    document.add_paragraph(precio)
    document.add_paragraph()
    document.add_paragraph('EMPRESA 1: ')
    document.add_paragraph(prod1)
    document.add_paragraph(beneficio1)
    document.add_paragraph()
    document.add_paragraph('EMPRESA 2: ')
    document.add_paragraph(prod2)
    document.add_paragraph(beneficio2)

    # Save the Word document
    document.save('bertrand_output.docx')


class BertrandMasInfoScreen(MasInfoVentana):
    a = '''El duopolio de Stackelberg, al igual que el modelo de Cournot, es también un modelo económico en el que dos\
 empresas compiten decidiendo sobre su producción.'''
