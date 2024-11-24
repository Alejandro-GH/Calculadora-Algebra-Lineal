# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QGridLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from sympy import symbols, sympify
import re

# Mensajes de depuración para verificar las importaciones
print("SymPy y PyQt5 importados correctamente")

print("Iniciando Metodo_Biseccion.py")
print("SymPy y PyQt5 importados correctamente")

def Metodo_Biseccion(expr_funcion, variable, a, b, tolerancia=1e-6, max_iteraciones=100):
    x = symbols(variable)
    funcion = sympify(expr_funcion)
    procedimiento = []

    encabezado = f"{'a':<12}{'b':<12}{'c':<12}{'f(a)':<12}{'f(b)':<12}{'f(c)':<12}"
    separador = "-" * len(encabezado)
    procedimiento.append(encabezado)
    procedimiento.append(separador)

    iteracion = 0
    while (b - a) / 2 > tolerancia and iteracion < max_iteraciones:
        c = (a + b) / 2
        fa = funcion.subs(x, a)
        fb = funcion.subs(x, b)
        fc = funcion.subs(x, c)
        procedimiento.append(f"{a:<12.6f}{b:<12.6f}{c:<12.6f}{fa:<12.6f}{fb:<12.6f}{fc:<12.6f}")
        if fc == 0:
            return c, procedimiento
        elif fa * fc < 0:
            b = c
        else:
            a = c
        iteracion += 1

    return (a + b) / 2, procedimiento

class AplicacionBiseccion(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print("Inicializando la interfaz de usuario")
        self.setWindowTitle("Método de Bisección")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Inputs y botones
        input_layout = QGridLayout()

        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresar función (e.j., x^2 - 4)")
        input_layout.addWidget(QLabel("Función:"), 0, 0)
        input_layout.addWidget(self.funcion_input, 0, 1)

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Ingrese a (X sub 0)")
        input_layout.addWidget(QLabel("a:"), 1, 0)
        input_layout.addWidget(self.a_input, 1, 1)

        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Ingrese b (X sub 1)")
        input_layout.addWidget(QLabel("b:"), 2, 0)
        input_layout.addWidget(self.b_input, 2, 1)

        self.tolerancia_input = QLineEdit()
        self.tolerancia_input.setPlaceholderText("Tolerancia (e.j., 0.0001)")
        input_layout.addWidget(QLabel("Tolerancia:"), 3, 0)
        input_layout.addWidget(self.tolerancia_input, 3, 1)

        self.iteraciones_input = QLineEdit()
        self.iteraciones_input.setPlaceholderText("Max Iteraciones (e.g., 100)")
        input_layout.addWidget(QLabel("Iteraciones:"), 4, 0)
        input_layout.addWidget(self.iteraciones_input, 4, 1)

        # Botones
        boton_layout = QHBoxLayout()
        calcular_btn = QPushButton("Calcular")
        calcular_btn.clicked.connect(self.calcular_biseccion)
        boton_layout.addWidget(calcular_btn)

        limpiar_btn = QPushButton("Limpiar")
        limpiar_btn.clicked.connect(self.limpiar_campos)
        boton_layout.addWidget(limpiar_btn)

        # Resultados
        self.resultado_label = QLabel("Resultado: ")
        self.resultado_label.setFont(QFont("Arial", 12))
        self.resultado_label.setAlignment(Qt.AlignLeft)

        # Área de procedimiento con scroll
        scroll_area = QScrollArea()
        self.procedimiento_label = QLabel()
        self.procedimiento_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.procedimiento_label.setWordWrap(True)
        scroll_area.setWidget(self.procedimiento_label)
        scroll_area.setWidgetResizable(True)

        # Agregar widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addLayout(boton_layout)
        main_layout.addWidget(self.resultado_label)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def calcular_biseccion(self):
        print("Iniciando cálculo del método de Bisección")
        try:
            funcion_texto = self.funcion_input.text().replace("^", "**")
            funcion_texto = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion_texto)
            expr_funcion = sympify(funcion_texto)
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            tolerancia = float(self.tolerancia_input.text()) if self.tolerancia_input.text() else 1e-6
            iteraciones = int(self.iteraciones_input.text()) if self.iteraciones_input.text() else 100

            raiz, procedimiento = Metodo_Biseccion(expr_funcion, 'x', a, b, tolerancia, iteraciones)
            self.resultado_label.setText(f"Resultado: Raíz aproximada = {raiz}")
            self.procedimiento_label.setText("\n".join(procedimiento))
            print("Cálculo del método de Bisección completado")
        except Exception as e:
            print(f"Error durante el cálculo: {str(e)}")
            self.resultado_label.setText(f"Error: {str(e)}")

    def limpiar_campos(self):
        print("Limpieza de campos iniciada")
        self.funcion_input.clear()
        self.a_input.clear()
        self.b_input.clear()
        self.tolerancia_input.clear()
        self.iteraciones_input.clear()
        self.resultado_label.setText("Resultado: ")
        self.procedimiento_label.setText("")
        print("Limpieza de campos completada")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = AplicacionBiseccion()
    ventana.show()
    print("Aplicación iniciada")
    sys.exit(app.exec_())
