import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CramerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Regla de Cramer - PyQt5")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para la entrada de matriz y vector
        input_layout = QGridLayout()
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz (filas separadas por ';', elementos por ',')")
        input_layout.addWidget(QLabel("Matriz:"), 0, 0)
        input_layout.addWidget(self.matriz_input, 0, 1)

        self.vector_input = QLineEdit()
        self.vector_input.setPlaceholderText("Introduce vector (separado por comas)")
        input_layout.addWidget(QLabel("Vector:"), 1, 0)
        input_layout.addWidget(self.vector_input, 1, 1)

        main_layout.addLayout(input_layout)

        # Botón para calcular
        button_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(self.calcular_cramer)
        button_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar")
        limpiar_button.clicked.connect(self.limpiar_campos)
        button_layout.addWidget(limpiar_button)

        main_layout.addLayout(button_layout)

        # Resultado
        self.resultado_label = QLabel("Resultado:")
        self.resultado_label.setFont(QFont("Arial", 12))
        self.resultado_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.resultado_label)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.resultado_text)

        self.setLayout(main_layout)

    def calcular_cramer(self):
        try:
            # Convertir entradas en matriz y vector
            matriz_texto = self.matriz_input.text()
            vector_texto = self.vector_input.text()

            matriz = [list(map(float, fila.split(','))) for fila in matriz_texto.split(';')]
            vector = list(map(float, vector_texto.split(',')))

            if len(matriz) != len(vector):
                self.resultado_label.setText("Error: Dimensiones no coinciden")
                return

            # Calcular soluciones con la Regla de Cramer
            soluciones = self.cramer_rule(matriz, vector)
            self.resultado_label.setText("Resultado:")
            self.resultado_text.setText("\n".join([f"x{i+1} = {sol}" for i, sol in enumerate(soluciones)]))

        except ValueError:
            self.resultado_label.setText("Error: Formato de entrada inválido.")
        except Exception as e:
            self.resultado_label.setText(f"Error inesperado: {str(e)}")
            
    def limpiar_campos(self):
        self.matriz_input.clear()
        self.vector_input.clear()
        self.resultado_label.setText("Resultado:")
        self.resultado_text.clear()

    def cramer_rule(self, matrix, vector):
        det_A = self.determinant(matrix)

        if det_A == 0:
            return ["La matriz tiene múltiples soluciones o es singular"]

        solutions = []
        for i in range(len(matrix)):
            matrix_i = [row[:] for row in matrix]
            for j in range(len(vector)):
                matrix_i[j][i] = vector[j]
            det_Ai = self.determinant(matrix_i)
            solution = det_Ai / det_A
            solutions.append(solution)

        return solutions
    
    def determinant(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for c in range(len(matrix)):
            sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += ((-1)**c) * matrix[0][c] * self.determinant(sub_matrix)
        return det
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = CramerApp()
    ventana.show()
    sys.exit(app.exec_())
