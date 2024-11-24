# -*- coding: utf-8 -*-
import sys
import math
import re
import random
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)

# Mensajes de depuración para verificar las importaciones
print("NumPy importado correctamente")
print("Matplotlib importado correctamente")
print("PyQt5 importado correctamente")

# Método de Newton-Raphson
def newton_raphson(func, xi, tol, max_iter):
    h = 1e-5  # Incremento para la derivada numérica
    procedimiento = []

    encabezado = "{:<12}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
        "Iteración", "xi", "xi+1", "Ea (%)", "f(xi)", "f'(xi)"
    )
    procedimiento.append(encabezado)
    procedimiento.append("-" * len(encabezado))

    for i in range(1, max_iter + 1):
        try:
            func = preprocesar_funcion(func)
            fx = eval(func, {"x": xi, "math": math})
            derivada = (eval(func, {"x": xi + h, "math": math}) - fx) / h

            if derivada == 0:
                procedimiento.append(f"Derivada nula en iteración {i}. Proceso terminado.")
                return None, procedimiento

            xi1 = xi - fx / derivada
            ea = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')

            procedimiento.append(
                "{:<12}{:<15.6f}{:<15.6f}{:<15.6f}{:<15.6f}{:<15.6f}".format(
                    i, xi, xi1, ea, fx, derivada
                )
            )

            if ea < tol:
                procedimiento.append(f"Convergencia alcanzada en iteración {i}: xi ≈ {xi1}")
                return xi1, procedimiento

            xi = xi1
        except Exception as e:
            procedimiento.append(f"Error en iteración {i}: {str(e)}")
            return None, procedimiento

    procedimiento.append("No se alcanzó convergencia en el número máximo de iteraciones.")
    return None, procedimiento

# Preprocesar funciones matemáticas
def preprocesar_funcion(func):
    func = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", func)  # Ej: 2x -> 2*x
    func = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", func)  # Ej: x2 -> x*2
    func = func.replace("^", "**")  # Reemplazar ^ por **
    return func

# Graficar función
def graficar_funcion(func):
    func = preprocesar_funcion(func).replace("sin", "np.sin").replace("cos", "np.cos")
    func = func.replace("tan", "np.tan").replace("log", "np.log").replace("sqrt", "np.sqrt")

    x = np.linspace(-10, 10, 500)
    try:
        y = eval(func, {"x": x, "np": np})
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, label=f"f(x) = {func}")
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.title("Gráfica de la función")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Error al graficar la función: {e}")

class NewtonRaphsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Newton-Raphson - PyQt5")
        self.setGeometry(100, 100, 800, 600)

        layout_principal = QVBoxLayout()

        # Entradas
        layout_entradas = QGridLayout()

        layout_entradas.addWidget(QLabel("Función f(x):"), 0, 0)
        self.funcion_input = QLineEdit()
        layout_entradas.addWidget(self.funcion_input, 0, 1)

        layout_entradas.addWidget(QLabel("x0 (Valor inicial):"), 1, 0)
        self.x0_input = QLineEdit()
        layout_entradas.addWidget(self.x0_input, 1, 1)

        layout_entradas.addWidget(QLabel("Tolerancia:"), 2, 0)
        self.tolerancia_input = QLineEdit()
        layout_entradas.addWidget(self.tolerancia_input, 2, 1)

        layout_entradas.addWidget(QLabel("Máx Iteraciones:"), 3, 0)
        self.iteraciones_input = QLineEdit()
        layout_entradas.addWidget(self.iteraciones_input, 3, 1)

        layout_principal.addLayout(layout_entradas)

        # Botones
        botones_layout = QHBoxLayout()

        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(self.calcular)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.clicked.connect(self.limpiar)
        botones_layout.addWidget(limpiar_button)

        grafica_button = QPushButton("Graficar")
        grafica_button.clicked.connect(self.mostrar_grafica)
        botones_layout.addWidget(grafica_button)

        problema_button = QPushButton("Problema Aleatorio")
        problema_button.clicked.connect(self.generar_problema_aleatorio)
        botones_layout.addWidget(problema_button)

        layout_principal.addLayout(botones_layout)

        # Resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        layout_principal.addWidget(self.resultado_text)

        self.setLayout(layout_principal)

    def calcular(self):
        try:
            print("Inicio del cálculo del método de Newton-Raphson")
            func = self.funcion_input.text()
            xi = float(self.x0_input.text())
            tol = float(self.tolerancia_input.text())
            max_iter = int(self.iteraciones_input.text())

            resultado, procedimiento = newton_raphson(func, xi, tol, max_iter)
            if resultado is not None:
                self.resultado_text.setText(f"Raíz: {resultado}\n\n" + "\n".join(procedimiento))
            else:
                self.resultado_text.setText("No se encontró una raíz.\n\n" + "\n".join(procedimiento))
            print("Fin del cálculo del método de Newton-Raphson")
        except Exception as e:
            print(f"Error durante el cálculo: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error en el cálculo: {str(e)}")

    def limpiar(self):
        print("Limpieza de campos iniciada")
        self.funcion_input.clear()
        self.x0_input.clear()
        self.tolerancia_input.clear()
        self.iteraciones_input.clear()
        self.resultado_text.clear()
        print("Limpieza de campos completada")

    def mostrar_grafica(self):
        func = self.funcion_input.text()
        if not func.strip():
            QMessageBox.critical(self, "Error", "Ingrese una función para graficar.")
            return
        print("Mostrando la gráfica de la función")
        graficar_funcion(func)

    def generar_problema_aleatorio(self):
        funciones = [
            "x^2 - 4", "sin(x) + x", "cos(x) - x", "tan(x) + 1",
            "x^3 - x", "sqrt(x) - 2", "exp(x) - 5", "log(x) - 1"
        ]
        self.funcion_input.setText(random.choice(funciones))
        self.x0_input.setText(str(random.uniform(-10, 10)))
        self.tolerancia_input.setText("0.001")
        self.iteraciones_input.setText("50")
        print("Problema aleatorio generado")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = NewtonRaphsonApp()
    ventana.show()
    print("Aplicación iniciada")
    sys.exit(app.exec_())
