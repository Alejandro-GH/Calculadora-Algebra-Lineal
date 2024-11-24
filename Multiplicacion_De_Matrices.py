import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont


class MatrizMultiplicacionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Multiplicación de Matrices - PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz A
        self.matriz_a_input = QLineEdit()
        self.matriz_a_input.setPlaceholderText("Introduce Matriz A (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(QLabel("Matriz A:"))
        layout_principal.addWidget(self.matriz_a_input)

        # Entrada para la matriz B
        self.matriz_b_input = QLineEdit()
        self.matriz_b_input.setPlaceholderText("Introduce Matriz B (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(QLabel("Matriz B:"))
        layout_principal.addWidget(self.matriz_b_input)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(self.calcular_matriz)
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

    def calcular_matriz(self):
        try:
            # Leer las matrices desde las entradas
            matriz_a_str = self.matriz_a_input.text()
            matriz_b_str = self.matriz_b_input.text()

            if not matriz_a_str.strip() or not matriz_b_str.strip():
                raise ValueError("Ambas matrices deben ser ingresadas.")

            # Convertir las matrices de texto a listas de listas
            matriz_a = [[int(num) for num in fila.split(',')] for fila in matriz_a_str.split(';')]
            matriz_b = [[int(num) for num in fila.split(',')] for fila in matriz_b_str.split(';')]

            # Verificar compatibilidad de dimensiones para A*B
            if len(matriz_a[0]) != len(matriz_b):
                raise ValueError("Las dimensiones de las matrices no permiten la multiplicación (columnas de A deben ser iguales a filas de B).")

            # Multiplicar A*B y almacenar los pasos
            resultado_ab, pasos_ab = self.multiplicar_matrices(matriz_a, matriz_b)

            # Verificar si B*A es posible
            conmutatividad = "No se puede verificar la conmutatividad, B*A no es posible."
            if len(matriz_b[0]) == len(matriz_a):
                resultado_ba, _ = self.multiplicar_matrices(matriz_b, matriz_a)
                if resultado_ab == resultado_ba:
                    conmutatividad = "Las matrices son conmutativas (A*B = B*A)."
                else:
                    conmutatividad = "Las matrices no son conmutativas (A*B ≠ B*A)."

            # Mostrar el procedimiento y el resultado
            resultado_texto = f"Procedimiento A*B:\n{pasos_ab}\n\nResultado A*B:\n{resultado_ab}\n\n{conmutatividad}"
            self.resultado_text.setText(resultado_texto)

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def multiplicar_matrices(self, A, B):
        filas_a = len(A)
        columnas_b = len(B[0])
        columnas_a = len(A[0])

        resultado = [[0 for _ in range(columnas_b)] for _ in range(filas_a)]
        pasos = ""

        for i in range(filas_a):
            for j in range(columnas_b):
                suma = 0
                paso = f"Fila {i+1} por Columna {j+1}: "
                for k in range(columnas_a):
                    multiplicacion = A[i][k] * B[k][j]
                    suma += multiplicacion
                    paso += f"{A[i][k]}*{B[k][j]}"
                    if k < columnas_a - 1:
                        paso += " + "
                resultado[i][j] = suma
                pasos += f"{paso} = {suma}\n"

        resultado_str = "\n".join(["\t".join(map(str, fila)) for fila in resultado])
        return resultado_str, pasos

    def limpiar_campos(self):
        self.matriz_a_input.clear()
        self.matriz_b_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MatrizMultiplicacionApp()
    ventana.show()
    sys.exit(app.exec_())
