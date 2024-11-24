import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont


class GaussJordanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Método de Gauss-Jordan - PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz aumentada
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz aumentada (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(QLabel("Matriz Aumentada:"))
        layout_principal.addWidget(self.matriz_input)

        # Botón para calcular
        calcular_button = QPushButton("Calcular Gauss-Jordan")
        calcular_button.clicked.connect(self.calcular_gauss_jordan)
        layout_principal.addWidget(calcular_button)

        # Área de resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier", 10))
        layout_principal.addWidget(self.resultado_text)

        self.setLayout(layout_principal)

    def calcular_gauss_jordan(self):
        try:
            # Leer la matriz aumentada
            matriz_aumentada = self.matriz_input.text()
            if not matriz_aumentada.strip():
                raise ValueError("La matriz aumentada no puede estar vacía.")

            matriz_aumentada = [list(map(float, fila.split(','))) for fila in matriz_aumentada.split(';')]

            # Separar la matriz de coeficientes (A) y el vector independiente (b)
            a = [fila[:-1] for fila in matriz_aumentada]
            b = [fila[-1] for fila in matriz_aumentada]

            # Resolver usando Gauss-Jordan
            pasos, solucion = self.eliminacion_gauss_jordan(a, b)

            # Mostrar los pasos y la solución
            resultado = f"{pasos}\n\nSolución: {solucion}"
            self.resultado_text.setText(resultado)

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, asegúrate de ingresar números válidos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def eliminacion_gauss_jordan(self, a, b):
        n = len(b)
        pasos = ""

        for i in range(n):
            pasos += f"Paso {i + 1}:\n"
            # Seleccionar el pivote
            fila_max = i + max(range(n - i), key=lambda k: abs(a[i + k][i]))
            if fila_max != i:
                pasos += f"Intercambiando fila {i + 1} con fila {fila_max + 1}\n"
                a[i], a[fila_max] = a[fila_max], a[i]
                b[i], b[fila_max] = b[fila_max], b[i]

            # Normalizar la fila del pivote
            pivote = a[i][i]
            if pivote != 1:
                pasos += f"Dividiendo fila {i + 1} por el pivote ({pivote:.2f})\n"
                for j in range(len(a[i])):
                    a[i][j] /= pivote
                b[i] /= pivote

            # Eliminar el elemento en las demás filas
            for k in range(n):
                if k != i:
                    factor = a[k][i]
                    if factor != 0:
                        pasos += f"F{k + 1} --> F{k + 1} - ({factor:.2f}) * F{i + 1}\n"
                        for j in range(len(a[i])):
                            a[k][j] -= factor * a[i][j]
                        b[k] -= factor * b[i]

        pasos += "\nMatriz final:\n"
        pasos += self.formatear_matriz(a, b)

        return pasos, b

    def formatear_matriz(self, a, b):
        n = len(b)
        filas = []
        for i in range(n):
            fila = ["{:.2f}".format(a[i][j]) for j in range(len(a[i]))]
            filas.append(" | ".join(fila) + " | " + "{:.2f}".format(b[i]))
        return "\n".join(filas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = GaussJordanApp()
    ventana.show()
    sys.exit(app.exec_())