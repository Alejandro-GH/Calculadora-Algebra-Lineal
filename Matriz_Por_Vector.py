import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont

class AplicacionMatriz(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Multiplicación Matriz-Vector y Gráficas - PyQt5")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(self.matriz_input)

        # Entrada para el vector
        self.vector_input = QLineEdit()
        self.vector_input.setPlaceholderText("Introduce vector (elementos separados por comas)")
        layout_principal.addWidget(self.vector_input)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular Resultado")
        calcular_button.clicked.connect(self.calcular_matriz)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar Todo")
        limpiar_button.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(limpiar_button)

        graficar_button = QPushButton("Mostrar Gráfica")
        graficar_button.clicked.connect(self.mostrar_grafica)
        botones_layout.addWidget(graficar_button)

        layout_principal.addLayout(botones_layout)

        # Área de resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier", 10))
        layout_principal.addWidget(self.resultado_text)

        self.setLayout(layout_principal)

    def calcular_matriz(self):
        try:
            # Leer y convertir la matriz y el vector
            texto_matriz = self.matriz_input.text()
            texto_vector = self.vector_input.text()

            if not texto_matriz.strip() or not texto_vector.strip():
                raise ValueError("La matriz y el vector no pueden estar vacíos.")

            matriz = [list(map(float, fila.split(','))) for fila in texto_matriz.split(';')]
            vector = list(map(float, texto_vector.split(',')))

            if len(matriz[0]) != len(vector):
                raise ValueError("El número de columnas de la matriz debe coincidir con el tamaño del vector.")

            # Multiplicar la matriz por el vector
            resultado = self.multiplicar_matriz_vector(matriz, vector)
            self.resultado_text.setText(f"Resultado: {resultado}")

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def multiplicar_matriz_vector(self, matriz, vector):
        resultado_final = [0] * len(matriz)
        for col in range(len(vector)):
            coeficiente = vector[col]
            columna_matriz = [fila[col] for fila in matriz]
            for fila in range(len(columna_matriz)):
                resultado_final[fila] += coeficiente * columna_matriz[fila]
        return resultado_final

    def mostrar_grafica(self):
        try:
            # Obtener el resultado del área de texto
            texto_resultado = self.resultado_text.toPlainText()
            if not texto_resultado.startswith("Resultado:"):
                raise ValueError("No hay resultado para graficar.")

            resultado_texto = texto_resultado.replace("Resultado: ", "").strip("[]")
            resultado = list(map(float, resultado_texto.split(',')))

            if len(resultado) == 2:
                self.plot_vector_2d(resultado)
            elif len(resultado) == 3:
                self.plot_vector_3d(resultado)
            else:
                raise ValueError(f"No se puede graficar un vector de {len(resultado)} dimensiones.")

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def plot_vector_2d(self, resultado):
        fig, ax = plt.subplots()
        ax.quiver(0, 0, resultado[0], resultado[1], angles='xy', scale_units='xy', scale=1, color='b')

        ax.set_xlim([0, resultado[0] + 1])
        ax.set_ylim([0, resultado[1] + 1])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Gráfica 2D del Resultado")
        ax.grid()
        plt.show()

    def plot_vector_3d(self, resultado):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = [0, resultado[0]]
        y = [0, resultado[1]]
        z = [0, resultado[2]]

        ax.quiver(0, 0, 0, resultado[0], resultado[1], resultado[2], color='b')
        ax.set_xlim([0, resultado[0] + 1])
        ax.set_ylim([0, resultado[1] + 1])
        ax.set_zlim([0, resultado[2] + 1])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Gráfica 3D del Resultado")
        plt.show()

    def limpiar_campos(self):
        self.matriz_input.clear()
        self.vector_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = AplicacionMatriz()
    ventana.show()
    sys.exit(app.exec_())
