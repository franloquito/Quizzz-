import random
import threading
import time
import sys

# Diccionario con las materias y sus palabras (sin cambios)
palabras_por_materia = {
    "Historia": [
        "revolucion", "imperio", "monarquia", "feudalismo", "colonialismo",
        "democracia", "dictadura", "arqueologia", "civilizacion", "guerra",
        "tratado", "independencia", "progreso", "antiguedad", "moderna",
        "prehistoria", "renacimiento", "paz", "reforma", "invasion"
    ],
    "Literatura": [
        "poesia", "novela", "autor", "metafora", "rima", "protagonista",
        "verso", "narrador", "cuento", "drama", "ficcion", "clasico",
        "epopeya", "dialogo", "ensayo", "literario", "tragedia", "romance",
        "fabula", "comedia"
    ],
    "Geografía": [
        "montaña", "río", "océano", "planeta", "globo", "cordillera",
        "clima", "territorio", "latitud", "longitud", "valle", "volcán",
        "continente", "desierto", "bosque", "mapa", "isla", "región",
        "costa", "ecosistema"
    ],
    "Matemática": [
        "suma", "resta", "multiplicacion", "division", "ecuacion", "fraccion",
        "numero", "geometria", "porcentaje", "raiz", "potencia", "angulo",
        "paralelo", "variable", "algebra", "estadistica", "recta", "funcion",
        "logaritmo", "simetria"
    ],
    "Biología": [
        "celula", "adn", "evolucion", "ecosistema", "reproduccion", "genetica",
        "fotosintesis", "organismo", "bacteria", "virus", "tejido", "nervioso",
        "musculo", "respiracion", "plantas", "animales", "especie", "bioma",
        "mitosis", "sangre"
    ]
}

# Variables globales
respuesta_jugador = None
tiempo_expirado = False

def temporizador(segundos):
    """
    Muestra un contador regresivo.
    SOLUCIÓN 2: Este hilo ahora maneja la línea de input
    y marca si se acaba el tiempo.
    """
    global tiempo_expirado, respuesta_jugador
    
    for i in range(segundos, 0, -1):
        # Si el jugador ya respondió (en el hilo principal), esta variable tendrá valor.
        if respuesta_jugador is not None:
            sys.stdout.write("\n") # Limpiamos la línea antes de salir
            sys.stdout.flush()
            return # El jugador respondió a tiempo, este hilo termina.

        # SOLUCIÓN 2 (Visual):
        # Escribimos el timer Y el prompt en la misma línea.
        # \r (carriage return) vuelve al inicio de la línea para sobrescribir.
        sys.stdout.write(f"\r⏳ Tiempo restante: {i:2d} segundos | Respuesta >>> ")
        sys.stdout.flush()
        time.sleep(1)

    # Si el bucle termina, el tiempo se acabó.
    # Volvemos a chequear por si el jugador respondió en el último microsegundo.
    if respuesta_jugador is not None:
        return

    # Ahora sí, el tiempo expiró.
    tiempo_expirado = True
    
    # Limpiamos la línea del prompt (sobrescribimos con espacios)
    sys.stdout.write("\r" + " " * 70 + "\r") 
    sys.stdout.write("\n⌛ ¡Se acabó el tiempo!\n")
    sys.stdout.flush()
    
    # Nota: El input() principal sigue activo y bloqueando.
    # El usuario tendrá que presionar Enter para que el juego continúe.

def quiz():
    global respuesta_jugador, tiempo_expirado

    # Reseteamos las variables globales por si se juega varias veces
    respuesta_jugador = None
    tiempo_expirado = False

    print("=== 🧠 BIENVENIDO AL QUIZ ESCOLAR ===\n")
    print("Elige una materia:")
    materias = list(palabras_por_materia.keys())
    
    for i, materia in enumerate(materias, start=1):
        print(f"{i}. {materia}")

    while True:
        try:
            opcion = int(input("\nIngresa el número de la materia: "))
            if 1 <= opcion <= len(materias):
                materia_elegida = materias[opcion - 1]
                break
            else:
                print("Por favor, elige un número válido.")
        except ValueError:
            print("Debes ingresar un número válido.")

    palabra = random.choice(palabras_por_materia[materia_elegida])
    letras = list(palabra)
    random.shuffle(letras)
    palabra_desordenada = ''.join(letras)

    print(f"\nHas elegido: {materia_elegida}")
    print(f"🔤 Adivina la palabra: {palabra_desordenada}")
    print("Tienes 20 segundos para responder. \n")

    # Inicia el temporizador
    hilo_tiempo = threading.Thread(target=temporizador, args=(20,))
    hilo_tiempo.start()

    try:
        # SOLUCIÓN 2 (Input):
        # El prompt se muestra desde el hilo del temporizador.
        # Aquí solo capturamos la entrada, sin mostrar prompt.
        respuesta_jugador = input("").strip().lower()
    except Exception:
        respuesta_jugador = None # Por si ocurre un error

    # Espera a que el hilo termine (ya sea por tiempo o por respuesta)
    hilo_tiempo.join()

    # === LÓGICA DE EVALUACIÓN CORREGIDA ===

    # SOLUCIÓN 1 (Lógica):
    # 1. Chequeamos PRIMERO si el tiempo se agotó.
    # Si es así, el jugador pierde sin importar lo que escribió.
    if tiempo_expirado:
        # El temporizador ya imprimió "¡Se acabó el tiempo!"
        print(f"❌ La palabra correcta era '{palabra}'.")
        
    # 2. Si el tiempo NO se agotó, chequeamos la respuesta.
    elif respuesta_jugador == palabra.lower():
        # El \n es necesario para separar de la línea de input
        print("\n🎉 ¡Felicidades! ¡Has acertado la palabra!")
        
    # 3. Si el tiempo NO se agotó y la respuesta es incorrecta.
    else:
        print(f"\n❌ ¡Has perdido! La palabra correcta era '{palabra}'.")

if __name__ == "__main__":
    quiz()
