import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from fractions import Fraction

def matriz_identidad(n):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]

def determinante(matriz):
    n = len(matriz)
    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    def menor(matriz, fila, col):
        return [row[:col] + row[col+1:] for row in (matriz[:fila] + matriz[fila+1:])]
    
    det = 0
    for j in range(n):
        det += (-1 if j % 2 else 1) * matriz[0][j] * determinante(menor(matriz, 0, j))
    return det

def gauss_jordan(matriz):
    n = len(matriz)
    identidad = matriz_identidad(n)
    for i in range(n):
        if matriz[i][i] == 0:
            raise ValueError("La matriz es singular y no tiene inversa.")
        
        pivote = matriz[i][i]
        for j in range(n):
            matriz[i][j] /= pivote
            identidad[i][j] /= pivote
        
        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(n):
                    matriz[k][j] -= factor * matriz[i][j]
                    identidad[k][j] -= factor * identidad[i][j]
    return identidad

class InversaMatrizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cálculo de la Inversa de una Matriz - PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(self.matriz_input)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular Inversa")
        calcular_button.clicked.connect(self.calcular_inversa)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(limpiar_button)

        layout_principal.addLayout(botones_layout)

        # Área de resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier", 10))
        layout_principal.addWidget(self.resultado_text)

        self.setLayout(layout_principal)

    def calcular_inversa(self):
        try:
            # Leer y validar la matriz de entrada
            texto_matriz = self.matriz_input.text()
            if not texto_matriz.strip():
                raise ValueError("La entrada está vacía. Por favor, introduce una matriz.")
            
            matriz = [list(map(Fraction, fila.split(','))) for fila in texto_matriz.split(';')]
            n = len(matriz)
            if not all(len(fila) == n for fila in matriz):
                raise ValueError("La matriz debe ser cuadrada (n x n).")

            # Verificar si la matriz tiene inversa
            det = determinante(matriz)
            if det == 0:
                raise ValueError("La matriz es singular (determinante = 0) y no tiene inversa.")

            # Calcular la inversa utilizando Gauss-Jordan
            inversa = gauss_jordan(matriz)

            # Mostrar el proceso y los resultados
            self.resultado_text.append(f"Matriz original:\n{self.formatear_matriz(matriz)}")
            self.resultado_text.append(f"Determinante: {det}")
            self.resultado_text.append(f"Inversa de la matriz:\n{self.formatear_matriz(inversa)}")

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def limpiar_campos(self):
        """Limpia la entrada y los resultados."""
        self.matriz_input.clear()
        self.resultado_text.clear()

    def formatear_matriz(self, matriz):
        """Convierte una matriz en una cadena formateada para mostrarla."""
        return "\n".join(["\t".join(map(str, fila)) for fila in matriz])

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en un cuadro de diálogo."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = InversaMatrizApp()
    ventana.show()
    sys.exit(app.exec_())