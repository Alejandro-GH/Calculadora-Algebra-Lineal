import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont


class MatrizTranspuestaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Transposición de Matrices - PyQt5")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Entrada para la matriz
        self.matriz_input = QLineEdit()
        self.matriz_input.setPlaceholderText("Introduce matriz (filas separadas por ';', elementos por ',')")
        layout_principal.addWidget(self.matriz_input)

        # Botones de acción
        botones_layout = QHBoxLayout()
        calcular_button = QPushButton("Calcular Transpuesta")
        calcular_button.clicked.connect(self.calcular_transpuesta)
        botones_layout.addWidget(calcular_button)

        limpiar_button = QPushButton("Limpiar Todo")
        limpiar_button.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(limpiar_button)

        layout_principal.addLayout(botones_layout)

        # Resultados: Matriz Original y Matriz Transpuesta
        resultados_layout = QHBoxLayout()

        self.label_original = QTextEdit()
        self.label_original.setReadOnly(True)
        self.label_original.setFont(QFont("Courier", 10))
        self.label_original.setPlaceholderText("Matriz Original")
        resultados_layout.addWidget(self.label_original)

        self.label_transpuesta = QTextEdit()
        self.label_transpuesta.setReadOnly(True)
        self.label_transpuesta.setFont(QFont("Courier", 10))
        self.label_transpuesta.setPlaceholderText("Matriz Transpuesta")
        resultados_layout.addWidget(self.label_transpuesta)

        layout_principal.addLayout(resultados_layout)

        self.setLayout(layout_principal)

    def calcular_transpuesta(self):
        try:
            # Leer la matriz desde la entrada y convertirla en una lista de listas
            texto_matriz = self.matriz_input.text()
            if not texto_matriz.strip():
                raise ValueError("La entrada está vacía. Por favor, introduce una matriz.")

            matriz = [fila.split(',') for fila in texto_matriz.split(';')]

            # Verificar que todas las filas tengan el mismo número de columnas
            columnas = len(matriz[0])
            if not all(len(fila) == columnas for fila in matriz):
                raise ValueError("Todas las filas deben tener el mismo número de columnas.")

            # Calcular la transpuesta
            matriz_transpuesta = self.transponer_matriz(matriz)

            # Mostrar la matriz original y su transpuesta
            self.mostrar_resultados(matriz, matriz_transpuesta)

        except ValueError as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(f"Error inesperado: {str(e)}")

    def transponer_matriz(self, matriz):
        """Calcula la transpuesta de la matriz."""
        return [list(fila) for fila in zip(*matriz)]

    def mostrar_resultados(self, matriz_original, matriz_transpuesta):
        """Muestra la matriz original y su transpuesta."""
        original_texto = "\n".join([", ".join(fila) for fila in matriz_original])
        transpuesta_texto = "\n".join([", ".join(fila) for fila in matriz_transpuesta])

        self.label_original.setText(original_texto)
        self.label_transpuesta.setText(transpuesta_texto)

    def limpiar_campos(self):
        """Limpia la entrada y los resultados."""
        self.matriz_input.clear()
        self.label_original.clear()
        self.label_transpuesta.clear()

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en un cuadro de diálogo."""
        QMessageBox.critical(self, "Error", mensaje)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MatrizTranspuestaApp()
    ventana.show()
    sys.exit(app.exec_())
