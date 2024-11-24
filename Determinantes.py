import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QFont


def calcular_determinante(matriz):
    n = len(matriz)

    # Caso base para matriz 1x1
    if n == 1:
        return matriz[0][0], [f"Paso: Matriz 1x1, determinante = {matriz[0][0]}"]
    
    # Caso base para matriz 2x2
    if n == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        pasos = [
            f"Paso: Determinante 2x2 = ({matriz[0][0]} * {matriz[1][1]}) - ({matriz[0][1]} * {matriz[1][0]}) = {det}"
        ]
        return det, pasos
    
    # Inicializar el determinante
    det = 0
    pasos = []

    # Calculando el determinante para matrices mayores
    for c in range(n):
        # Crear submatriz excluyendo la primera fila y la columna c
        submatriz = [fila[:c] + fila[c+1:] for fila in matriz[1:]]
        
        # Calcular el determinante de la submatriz
        sub_det, sub_pasos = calcular_determinante(submatriz)
        
        # Alternar signo y sumar el determinante de la submatriz
        signo = (-1) ** c
        contribucion = signo * matriz[0][c] * sub_det
        det += contribucion
        
        # Guardar el paso en formato legible
        pasos.append(f"Paso: {signo} * {matriz[0][c]} * det({submatriz}) = {contribucion}")
        pasos.extend(sub_pasos)

    return det, pasos


class DeterminanteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cálculo del Determinante - PyQt5")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para el tamaño de la matriz
        layout_tamano = QHBoxLayout()
        layout_tamano.addWidget(QLabel("Tamaño de la matriz (n x n):"))
        self.tamano_input = QLineEdit()
        self.tamano_input.setPlaceholderText("Ingrese n")
        layout_tamano.addWidget(self.tamano_input)
        layout_principal.addLayout(layout_tamano)

        # Entrada para los elementos de la matriz
        self.matriz_layout = QGridLayout()
        layout_principal.addLayout(self.matriz_layout)

        self.generar_matriz_button = QPushButton("Generar matriz")
        self.generar_matriz_button.clicked.connect(self.generar_matriz_inputs)
        layout_principal.addWidget(self.generar_matriz_button)

        # Botón para calcular el determinante
        self.calcular_button = QPushButton("Calcular Determinante")
        self.calcular_button.clicked.connect(self.calcular_determinante_gui)
        layout_principal.addWidget(self.calcular_button)

        # Área de resultados
        self.resultado_label = QLabel("Resultado: ")
        self.resultado_label.setFont(QFont("Arial", 12))
        layout_principal.addWidget(self.resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        layout_principal.addWidget(self.resultado_text)

        self.setLayout(layout_principal)

    def generar_matriz_inputs(self):
        # Obtener el tamaño ingresado
        try:
            n = int(self.tamano_input.text())
            if n <= 0:
                raise ValueError("El tamaño debe ser mayor a 0.")
        except ValueError:
            self.mostrar_error("Error: Ingrese un número entero positivo para el tamaño de la matriz.")
            return

        # Limpiar el layout de matriz
        for i in reversed(range(self.matriz_layout.count())):
            widget = self.matriz_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Generar inputs para la matriz
        self.matriz_inputs = []
        for i in range(n):
            fila_inputs = []
            for j in range(n):
                input_field = QLineEdit()
                input_field.setPlaceholderText(f"({i+1}, {j+1})")
                fila_inputs.append(input_field)
                self.matriz_layout.addWidget(input_field, i, j)
            self.matriz_inputs.append(fila_inputs)

    def calcular_determinante_gui(self):
        try:
            # Construir la matriz desde los inputs
            matriz = []
            for fila_inputs in self.matriz_inputs:
                fila = []
                for input_field in fila_inputs:
                    valor = input_field.text()
                    if not valor:
                        raise ValueError("Complete todos los campos de la matriz.")
                    fila.append(float(valor))
                matriz.append(fila)

            # Calcular el determinante y mostrar los pasos
            det, pasos = calcular_determinante(matriz)
            self.resultado_label.setText(f"Resultado: Determinante = {det}")
            self.resultado_text.setText("\n".join(pasos))

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = DeterminanteApp()
    ventana.show()
    sys.exit(app.exec_())