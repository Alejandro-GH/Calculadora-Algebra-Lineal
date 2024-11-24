import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from subprocess import Popen, PIPE

# Mensajes de depuración para verificar las importaciones
print("Entorno virtual activado")
print("Numpy importado correctamente")
print("Matplotlib importado correctamente")
print("PyQt5 importado correctamente")

class MenuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print("Inicializando la interfaz de usuario")
        self.setWindowTitle("Calculadora")
        self.setGeometry(100, 100, 600, 800)

        layout_principal = QVBoxLayout()

        # Etiqueta de bienvenida
        label_bienvenida = QLabel("Calculadora\nOpciones:")
        label_bienvenida.setStyleSheet("font-size: 18px; font-weight: bold;")
        label_bienvenida.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(label_bienvenida)

        # Botones de las opciones
        botones = [
            ("Determinantes", self.llama_archivo1),
            ("Inversa de Matriz", self.llama_archivo2),
            ("Multiplicación Matriz - Vector", self.llama_archivo3),
            ("Newton-Raphson", self.llama_archivo4),
            ("Bisección", self.llama_archivo5),
            ("Gauss-Jordan", self.llama_archivo6),
            ("Transposición de Matriz", self.llama_archivo7),
            ("Multiplicación de Matrices", self.llama_archivo8),
            ("Propiedad Distributiva", self.llama_archivo9),
            ("Regla de Cramer", self.llama_archivo10),
            ("Salir", self.salir),
        ]

        for texto, metodo in botones:
            boton = QPushButton(texto)
            boton.clicked.connect(metodo)
            layout_principal.addWidget(boton)

        self.setLayout(layout_principal)

    def llama_archivo(self, script_name):
        # Obtener el directorio actual
        print(f"Obteniendo el directorio actual para {script_name}")
        script_dir = os.path.dirname(os.path.realpath(__file__))
        script_path = os.path.join(script_dir, script_name)

        # Verificar si el archivo existe
        if os.path.isfile(script_path):
            try:
                # Ejecutar el script en el entorno virtual
                print(f"Ejecutando {script_name}")
                venv_python = os.path.join(script_dir, 'entorno_algebra', 'Scripts', 'python.exe')
                process = Popen([venv_python, script_path], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    raise Exception(f"Error al ejecutar {script_name}: {stderr.decode()}")
                print(stdout.decode())
            except Exception as e:
                print(f"Error al ejecutar {script_name}: {str(e)}")
                QMessageBox.critical(self, "Error", f"Error al ejecutar {script_name}: {str(e)}")
        else:
            print(f"El archivo {script_name} no se encontró.")
            QMessageBox.critical(self, "Error", f"El archivo {script_name} no se encontró.")

    # Métodos para llamar archivos específicos
    def llama_archivo1(self):
        print("Llamando a Determinantes.py")
        self.llama_archivo("Determinantes.py")

    def llama_archivo2(self):
        print("Llamando a Matriz_Inversa.py")
        self.llama_archivo("Matriz_Inversa.py")

    def llama_archivo3(self):
        print("Llamando a Matriz_Por_Vector.py")
        self.llama_archivo("Matriz_Por_Vector.py")

    def llama_archivo4(self):
        print("Llamando a Met_Newton-Raphson.py")
        self.llama_archivo("Met_Newton-Raphson.py")

    def llama_archivo5(self):
        print("Llamando a Metodo_Biseccion.py")
        self.llama_archivo("Metodo_Biseccion.py")

    def llama_archivo6(self):
        print("Llamando a Metodo_De_Gauss-Jordan.py")
        self.llama_archivo("Metodo_De_Gauss-Jordan.py")

    def llama_archivo7(self):
        print("Llamando a Metodo_De_Matrices_Transpuestas.py")
        self.llama_archivo("Metodo_De_Matrices_Transpuestas.py")

    def llama_archivo8(self):
        print("Llamando a Multiplicacion_De_Matrices.py")
        self.llama_archivo("Multiplicacion_De_Matrices.py")

    def llama_archivo9(self):
        print("Llamando a Propiedad_Distributiva.py")
        self.llama_archivo("Propiedad_Distributiva.py")

    def llama_archivo10(self):
        print("Llamando a Regla_De_Cramer.py")
        self.llama_archivo("Regla_De_Cramer.py")

    def salir(self):
        print("Saliendo de la aplicación")
        self.close()

if __name__ == "__main__":
    print("Iniciando la aplicación")
    app = QApplication(sys.argv)
    ventana = MenuApp()
    ventana.show()
    print("Aplicación iniciada")
    sys.exit(app.exec_())
