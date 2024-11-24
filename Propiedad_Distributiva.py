import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont


class PropiedadDistributivaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Propiedad Distributiva - PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce Matriz A (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(QLabel("Matriz A:"))
        layout_principal.addWidget(self.matriz_input)

        # Entrada para el vector u
        self.vector_u_input = QLineEdit()
        self.vector_u_input.setPlaceholderText("Introduce Vector u (elementos separados por comas)")
        layout_principal.addWidget(QLabel("Vector u:"))
        layout_principal.addWidget(self.vector_u_input)

        # Entrada para el vector v
        self.vector_v_input = QLineEdit()
        self.vector_v_input.setPlaceholderText("Introduce Vector v (elementos separados por comas)")
        layout_principal.addWidget(QLabel("Vector v:"))
        layout_principal.addWidget(self.vector_v_input)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(self.calcular_distributiva)
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

    def calcular_distributiva(self):
        try:
            # Leer las entradas
            matriz_str = self.matriz_input.text()
            vector_u_str = self.vector_u_input.text()
            vector_v_str = self.vector_v_input.text()

            if not matriz_str.strip() or not vector_u_str.strip() or not vector_v_str.strip():
                raise ValueError("Todos los campos deben estar completos.")

            # Convertir las entradas a listas de números
            matriz = [[float(num) for num in fila.split(',')] for fila in matriz_str.split(';')]
            u = [float(num) for num in vector_u_str.split(',')]
            v = [float(num) for num in vector_v_str.split(',')]

            if len(matriz[0]) != len(u) or len(u) != len(v):
                raise ValueError("El número de columnas de la matriz debe coincidir con el tamaño de los vectores.")

            # Calcular A(u + v)
            suma_uv = self.sumar_vectores(u, v)
            resultado_a_uv = self.multiplicar_matriz_vector(matriz, suma_uv)

            # Calcular Au + Av
            resultado_au = self.multiplicar_matriz_vector(matriz, u)
            resultado_av = self.multiplicar_matriz_vector(matriz, v)
            resultado_au_av = self.sumar_vectores(resultado_au, resultado_av)

            # Verificar la propiedad distributiva
            es_distributivo = self.comparar_vectores(resultado_a_uv, resultado_au_av)

            # Mostrar resultados
            resultados = (
                f"A(u + v): {resultado_a_uv}\n"
                f"Au + Av: {resultado_au_av}\n\n"
                f"Propiedad distributiva: {'Cumple' if es_distributivo else 'No cumple'}"
            )
            self.resultado_text.setText(resultados)

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def multiplicar_matriz_vector(self, matriz, vector):
        resultado = [0] * len(matriz)
        for i in range(len(matriz)):
            for j in range(len(vector)):
                resultado[i] += matriz[i][j] * vector[j]
        return resultado

    def sumar_vectores(self, u, v):
        return [u[i] + v[i] for i in range(len(u))]

    def comparar_vectores(self, vec1, vec2):
        return all(abs(a - b) < 1e-9 for a, b in zip(vec1, vec2))

    def limpiar_campos(self):
        self.matriz_input.clear()
        self.vector_u_input.clear()
        self.vector_v_input.clear()
        self.resultado_text.clear()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = PropiedadDistributivaApp()
    ventana.show()
    sys.exit(app.exec_())
