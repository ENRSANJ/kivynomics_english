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


# Función que resuelve el modelo de Bertrand dados 4 parámetros (f.demanda y costes marginales)
def solve_bertrand(a, b, c, e):

    # Comprobamos si los parámetros son compatibles con una solución razonable del modelo
    if a <= c and a <= e:
        raise ValueError('Introduce parámetros válidos')

    if c < e:
        # La empresa 1 se lleva toda la demanda
        if (c + a) / 2 >= e:
            # Si no puede establecer precio de monopolio, establece
            # un precio marginalmente inferior al Coste Marginal de la empresa 2
            p = e - .001

        else:
            p = (c + a) / 2

        x1_sol = (a - p) / b
        x2_sol = 0

    elif c > e:
        # La empresa 2 se lleva toda la demanda
        if (e + a) / 2 >= c:
            # Si no puede establecer precio de monopolio, establece
            # un precio marginalmente inferior al Coste Marginal de la empresa 2
            p = c - .001

        else:
            p = (e + a) / 2

        x1_sol = 0
        x2_sol = (a - p) / b

    else:
        # Distribuimos la demanda a partes iguales
        p = c
        x1_sol = (a - c) / (2 * b)
        x2_sol = (a - c) / (2 * b)

    x_total = x1_sol + x2_sol
    beneficio1 = (p - c) * x1_sol
    beneficio2 = (p - e) * x2_sol

    return {'p': p, 'q': x_total, 'q1': x1_sol, 'q2': x2_sol, 'profit1': beneficio1, 'profit2': beneficio2}


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

        # Obtenemos los resultados, redondeados
        try:
            solucion = {key: np.around(value, 3) for key, value in solve_bertrand(a, b, c, e).items()}
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetro válidos')
            alerta.open()
            return

        self.precio = 'Precio en el mercado: ' + str(solucion['p'])
        self.empresa1 = 'EMPRESA 1'
        self.empresa2 = 'EMPRESA 2'
        self.prod_1 = 'Producción óptima: ' + str(solucion['q1'])
        self.prod_2 = 'Producción óptima: ' + str(solucion['q2'])
        self.beneficio1 = 'Beneficio: ' + str(solucion['profit1'])
        self.beneficio2 = 'Beneficio: ' + str(solucion['profit2'])

        x1_sol = solucion['q1']
        x2_sol = solucion['q2']
        x_total = solucion['q']
        p = solucion['p']

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
                  plt.plot([], [], 'r--', label='Costes marginales')[0]])

        # Cambiamos el grosor de los bordes
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_linewidth(2)

        # Creamos el widget FigureCanvasKivyAgg (vaciamos "graficournot" para eliminar el gráfico anterior)
        canvas = FigureCanvasKivyAgg(figure=fig)
        plt.close("all")
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
    a = '''Joseph Louis François Bertrand (1822-1900), matemático y economista francés del si-glo XIX, revisó el modelo\
 de duopolio de Cournot, indicando que en una situación de duopolio las empresas acabarían compitiendo en precios,\
 dando forma al conocido como modelo de Bertrand.
    
 El modelo de Bertrand es un modelo de competencia entre dos o más empresas en el que, a diferencia de\
 en los modelos anteriores, la variable de decisión es el precio. Esto es, las empresas deciden a qué precio\
 venderán su producto y la cantidad será la determinada por la demanda del mercado para dicho precio.
 
Partiendo de costes marginales iguales, solo existe un equilibrio de Nash en el modelo: precio_1 = precio_2 =\
 Coste Marginal ya que siempre que el precio sea superior al coste marginal, existen incentivos para desviarse de la\
 situación.
 
Cuando las empresas presentan costes marginales distintos, la que menores costes tenga se podrá hacer con\
 toda la demanda del mercado y tendrá que decidir entre establecer su precio de monopolio (si puede hacerlo dejando\
 fuera a la empresa rival) o un precio marginalmente inferior al coste marginal de la otra empresa. '''
