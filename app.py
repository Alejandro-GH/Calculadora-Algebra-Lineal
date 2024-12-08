from flask import Flask, render_template, request
from métodos.determinante import calcular_determinante, generar_matriz_inputs
from métodos.falsa_posicion import calcular_falsa_posicion
from métodos.matriz_inversa import calcular_inversa_matriz
from métodos.matriz_por_vector import calcular_matriz_vector
from métodos.met_newton_raphson import newton_raphson
from métodos.metodo_biseccion import biseccion
from métodos.metodo_de_gauss_jordan import eliminacion_gauss_jordan, formatear_matriz
from métodos.metodo_de_matrices_transpuestas import transponer_matriz, formatear_matriz as formatear_matriz_transpuesta
from métodos.multiplicacion_de_matrices import calcular_multiplicacion, formatear_matriz as formatear_matriz_mult
from métodos.propiedad_distributiva import calcular_distributiva
from métodos.regla_de_cramer import calcular_cramer
from métodos.secante import metodo_secante
from sympy import sympify, lambdify, symbols

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/determinante', methods=['GET', 'POST'])
def determinante():
    resultado = None
    propiedades = []
    if request.method == 'POST':
        tamano = request.form.get('tamano')
        matriz_str = request.form.get('matriz')
        if tamano:
            matriz = generar_matriz_inputs(tamano)
        elif matriz_str:
            matriz = [list(map(sympify, row.split())) for row in matriz_str.strip().split('\n')]
            resultado, propiedades = calcular_determinante(matriz)
    else:
        matriz = []
    return render_template('determinante.html', matriz=matriz, resultado=resultado, propiedades=propiedades)

@app.route('/falsa_posicion', methods=['GET', 'POST'])
def falsa_posicion():
    resultado = None
    pasos = []
    if request.method == 'POST':
        funcion = sympify(request.form.get('funcion'))
        a = float(request.form.get('a'))
        b = float(request.form.get('b'))
        tol = float(request.form.get('tolerancia'))
        max_iter = int(request.form.get('iteraciones'))
        resultado, pasos = calcular_falsa_posicion(funcion, a, b, tol, max_iter)
    return render_template('falsa_posicion.html', resultado=resultado, pasos=pasos)

@app.route('/matriz_inversa', methods=['GET', 'POST'])
def matriz_inversa():
    inversa = None
    if request.method == 'POST':
        tamano = int(request.form.get('tamano'))
        matriz_str = request.form.get('matriz')
        matriz = [list(map(float, fila.split(','))) for fila in matriz_str.split(';')]
        inversa = calcular_inversa_matriz(matriz)
    return render_template('inversa.html', inversa=inversa)

@app.route('/matriz_por_vector', methods=['GET', 'POST'])
def matriz_por_vector():
    resultado = None
    if request.method == 'POST':
        matriz_texto = request.form.get('matriz')
        vector_texto = request.form.get('vector')
        resultado = calcular_matriz_vector(matriz_texto, vector_texto)
    return render_template('matriz_por_vector.html', resultado=resultado)

@app.route('/newton_raphson', methods=['GET', 'POST'])
def newton_raphson_route():
    resultado = None
    procedimiento = []
    if request.method == 'POST':
        funcion = sympify(request.form.get('funcion'))
        xi = float(request.form.get('xi'))
        tol = float(request.form.get('tolerancia'))
        max_iter = int(request.form.get('iteraciones'))
        resultado, procedimiento = newton_raphson(funcion, xi, tol, max_iter)
    return render_template('newton_raphson.html', resultado=resultado, procedimiento=procedimiento)

@app.route('/biseccion', methods=['GET', 'POST'])
def biseccion_route():
    resultado = None
    if request.method == 'POST':
        funcion = sympify(request.form.get('funcion'))
        a = float(request.form.get('a'))
        b = float(request.form.get('b'))
        iteraciones = int(request.form.get('iteraciones'))
        resultado = biseccion(funcion, a, b, iteraciones)
    return render_template('biseccion.html', resultado=resultado)

@app.route('/gauss_jordan', methods=['GET', 'POST'])
def gauss_jordan_route():
    resultado = None
    if request.method == 'POST':
        matriz_str = request.form.get('matriz')
        matriz_aumentada = [list(map(float, fila.split(','))) for fila in matriz_str.split(';')]
        a = [fila[:-1] for fila in matriz_aumentada]
        b = [fila[-1] for fila in matriz_aumentada]
        pasos, solucion = eliminacion_gauss_jordan(a, b)
        resultado = f"{pasos}\n\nSolución: {solucion}"
    return render_template('gauss_jordan.html', resultado=resultado)

@app.route('/matrices_transpuestas', methods=['GET', 'POST'])
def matrices_transpuestas_route():
    resultado = None
    if request.method == 'POST':
        matriz_str = request.form.get('matriz')
        matriz = [list(map(float, fila.split(','))) for fila in matriz_str.split(';')]
        original = formatear_matriz_transpuesta(matriz)
        transpuesta = transponer_matriz(matriz)
        resultado = formatear_matriz_transpuesta(transpuesta)
    return render_template('matrices_transpuestas.html', original=original, resultado=resultado)

@app.route('/multiplicacion', methods=['GET', 'POST'])
def multiplicacion_route():
    resultado = None
    matriz_a = None
    matriz_b = None
    if request.method == 'POST':
        matriz_a_str = request.form.get('matriz_a')
        matriz_b_str = request.form.get('matriz_b')
    matriz_a = formatear_matriz_mult(matriz_a_str)
    matriz_b = formatear_matriz_mult(matriz_b_str)
    resultado = formatear_matriz_mult(calcular_multiplicacion(matriz_a, matriz_b))
    return render_template('multiplicacion.html', matriz_a=matriz_a, matriz_b=matriz_b, resultado=resultado)

@app.route('/propiedad_distributiva', methods=['GET', 'POST'])
def propiedad_distributiva_route():
    resultado = None
    if request.method == 'POST':
        matriz_str = request.form.get('matriz')
        vector_u_str = request.form.get('vector_u')
        vector_v_str = request.form.get('vector_v')
        resultado = calcular_distributiva(matriz_str, vector_u_str, vector_v_str)
    return render_template('propiedad_distributiva.html', resultado=resultado)

@app.route('/regla_de_cramer', methods=['GET', 'POST'])
def regla_de_cramer_route():
    resultado = None
    if request.method == 'POST':
        matriz_str = request.form.get('matriz')
        vector_str = request.form.get('vector')
        resultado = calcular_cramer(matriz_str, vector_str)
    return render_template('cramer.html', resultado=resultado)

@app.route('/secante', methods=['GET', 'POST'])
def secante_route():
    resultado = None
    pasos = []
    if request.method == 'POST':
        funcion = sympify(request.form.get('funcion'))
        x0 = float(request.form.get('x0'))
        x1 = float(request.form.get('x1'))
        tol = float(request.form.get('tolerancia'))
        max_iter = int(request.form.get('iteraciones'))
        f = lambdify(symbols('x'), funcion, 'math')
        resultado, pasos = metodo_secante(f, x0, x1, tol, max_iter)
    return render_template('secante.html', resultado=resultado, pasos=pasos)

if __name__ == '__main__':
    app.run(debug=True)
    