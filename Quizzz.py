import random
import time
import sys
import os

# Intentamos importar librerías específicas del sistema operativo para leer teclas
# sin bloquear el programa (detectar pulsaciones al instante).
try:
    import msvcrt  # Para Windows
    OS_TYPE = 'windows'
except ImportError:
    import select  # Para Linux/Mac
    import tty
    import termios
    OS_TYPE = 'unix'

# --- CONFIGURACIÓN DEL JUEGO ---
palabras_por_materia = {
    "Historia": ["revolucion", "imperio", "monarquia", "feudalismo", "colonialismo", "independencia", "dictadura", "guerra","tratado","genocidio"],
    "Literatura": ["poesia", "novela", "metafora", "protagonista", "narrador", "ensayo","fabula","autor","antagonista","prosa"],
    "Geografía": ["cordillera", "continente", "atmosfera", "meridiano", "ecuador", "archipielago","longitud","latitud","oceanos","paises"],
    "Matemática": ["ecuacion", "hipotenusa", "logaritmo", "estadistica", "derivada", "poligono","geometria","angulo","radicacion","potenciacion"],
    "Biología": ["fotosintesis", "mitocondria", "ecosistema", "cromosoma", "metabolismo", "biodiversidad","inerte","bacteria","esternocleidomastoideo","evolucion"]
}

# --- FUNCIONES DE SISTEMA (Lectura de teclas) ---

def get_char():
    """Lee un solo carácter del teclado sin esperar Enter (Cross-platform)."""
    if OS_TYPE == 'windows':
        # msvcrt.kbhit() verifica si hay una tecla presionada
        if msvcrt.kbhit():
            ch = msvcrt.getwch() # getwch lee el caracter (incluyendo tildes)
            return ch
        return None
    else:
        # Versión para Linux/Mac
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            # select verifica si hay datos listos para leer en stdin
            rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
            if rlist:
                return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

def input_con_temporizador(prompt, segundos):
    """
    Maneja el input del usuario y el reloj al mismo tiempo.
    Devuelve:
        - La cadena escrita por el usuario si presiona Enter.
        - None si el tiempo se agota.
    """
    inicio = time.time()
    texto_actual = []
    
    # Limpiamos buffers previos
    if OS_TYPE == 'windows':
        while msvcrt.kbhit(): msvcrt.getwch()

    while True:
        tiempo_transcurrido = time.time() - inicio
        tiempo_restante = int(segundos - tiempo_transcurrido)

        if tiempo_restante <= 0:
            sys.stdout.write(f"\r⌛ ¡Tiempo agotado! {' ' * 40}\n")
            return None

        # Construimos la barra visual: Reloj + Prompt + Texto escrito
        # \r nos devuelve al inicio de la línea para sobrescribir
        barra_estado = f"\r⏳ Tiempo: {tiempo_restante}s | {prompt} {''.join(texto_actual)}"
        
        # Rellenamos con espacios al final para borrar caracteres viejos si borramos texto
        sys.stdout.write(barra_estado + "   ") 
        sys.stdout.flush()

        # Leemos tecla (sin bloquear)
        char = get_char()

        if char:
            # Si es Enter (\r o \n), terminamos
            if char in ('\r', '\n'):
                sys.stdout.write("\n") # Salto de línea final
                return ''.join(texto_actual)
            
            # Si es Backspace (borrar) -> \x08 es código ASCII de backspace, \x7f es DEL
            elif char in ('\x08', '\x7f'):
                if len(texto_actual) > 0:
                    texto_actual.pop()
            
            # Si es un caracter imprimible normal
            elif char.isprintable():
                texto_actual.append(char)
        
        # Pequeña pausa para no quemar el CPU
        time.sleep(0.05)

# --- LÓGICA DEL QUIZ ---

def quiz():
    print("=== 🧠 BIENVENIDO AL QUIZ DINÁMICO ===\n")
    
    materias = list(palabras_por_materia.keys())
    for i, materia in enumerate(materias, start=1):
        print(f"{i}. {materia}")

    while True:
        try:
            opcion = int(input("\nIngresa el número de la materia: "))
            if 1 <= opcion <= len(materias):
                materia_elegida = materias[opcion - 1]
                break
            print("Número inválido.")
        except ValueError:
            print("Debes ingresar un número.")

    palabra = random.choice(palabras_por_materia[materia_elegida])
    letras = list(palabra)
    random.shuffle(letras)
    palabra_desordenada = ''.join(letras)

    print(f"\nHas elegido: {materia_elegida}")
    print(f"🔤 Adivina la palabra: {palabra_desordenada}")
    print("------------------------------------------------")

    # USAMOS LA NUEVA FUNCIÓN DE INPUT
    respuesta = input_con_temporizador("Tu respuesta >>> ", 20)

    # Evaluación
    if respuesta is None:
        print(f"❌ La palabra correcta era '{palabra}'.")
    elif respuesta.lower().strip() == palabra.lower():
        print(f"🎉 ¡Correcto! Has adivinado '{palabra}'.")
    else:
        print(f"❌ Incorrecto. Dijiste '{respuesta}', pero era '{palabra}'.")

if __name__ == "__main__":
    quiz()