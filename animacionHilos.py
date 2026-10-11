import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import threading
import queue
import time



# CONFIGURACIÓN


ANCHO = 1000
ALTO = 600

VELOCIDAD_CABALLERO = 0.35
VELOCIDAD_GATO = 0.45

TAM_CABALLERO = (230, 230)
TAM_GATO = (250, 250)



# RUTAS


CARPETA_PROYECTO = Path(__file__).resolve().parent

RECURSOS = CARPETA_PROYECTO / "resources"



# COLA PARA LOS HILOS


cola = queue.Queue()

detener = threading.Event()



# CREAR VENTANA


ventana = tk.Tk()

ventana.title("Animación con Hilos")

ventana.geometry(f"{ANCHO}x{ALTO}")

ventana.resizable(False, False)



# CREAR CANVAS


canvas = tk.Canvas(
    ventana,
    width=ANCHO,
    height=ALTO,
    highlightthickness=0
)

canvas.pack()



# CARGAR FONDO


ruta_fondo = RECURSOS / "FONDOVALLE.png"

imagen_fondo = Image.open(ruta_fondo).convert("RGB")

# Ajustar el fondo al tamaño de la ventana
imagen_fondo = imagen_fondo.resize(
    (ANCHO, ALTO),
    Image.Resampling.NEAREST
)

fondo = ImageTk.PhotoImage(imagen_fondo)


# Mostrar fondo
canvas.create_image(
    0,
    0,
    image=fondo,
    anchor="nw"
)



# FUNCIÓN PARA CARGAR SPRITES


def cargar_imagen(nombre, tamano):

    ruta = RECURSOS / nombre

    imagen = Image.open(ruta).convert("RGBA")

    imagen.thumbnail(
        tamano,
        Image.Resampling.NEAREST
    )

    return ImageTk.PhotoImage(imagen)



# CARGAR CABALLERO


caballero = [

    cargar_imagen(
        "CABALLERO P1.png",
        TAM_CABALLERO
    ),

    cargar_imagen(
        "CABALLERO P2.png",
        TAM_CABALLERO
    )

]



# CARGAR GATO


gato = [

    cargar_imagen(
        "GATO P1.png",
        TAM_GATO
    ),

    cargar_imagen(
        "GATO P2.png",
        TAM_GATO
    )

]



# CREAR CABALLERO


sprite_caballero = canvas.create_image(
    250,
    555,
    image=caballero[0],
    anchor="s"
)



# CREAR GATO


sprite_gato = canvas.create_image(
    750,
    555,
    image=gato[0],
    anchor="s"
)



# CRONÓMETRO


# Pequeña sombra para que se vea bien sobre el fondo

sombra_cronometro = canvas.create_text(
    ANCHO // 2 + 2,
    52,
    text="00:00.0",
    font=("Arial", 30, "bold"),
    fill="black"
)


texto_cronometro = canvas.create_text(
    ANCHO // 2,
    50,
    text="00:00.0",
    font=("Arial", 30, "bold"),
    fill="white"
)



# HILO 1 - CABALLERO


def animar_caballero():

    frame = 0

    while not detener.is_set():

        frame = 1 - frame

        cola.put(
            ("caballero", frame)
        )

        time.sleep(
            VELOCIDAD_CABALLERO
        )



# HILO 2 - GATO


def animar_gato():

    frame = 0

    while not detener.is_set():

        frame = 1 - frame

        cola.put(
            ("gato", frame)
        )

        time.sleep(
            VELOCIDAD_GATO
        )



# HILO 3 - CRONÓMETRO


def cronometro():

    inicio = time.perf_counter()

    while not detener.is_set():

        tiempo = time.perf_counter() - inicio

        minutos = int(
            tiempo // 60
        )

        segundos = int(
            tiempo % 60
        )

        decimas = int(
            (tiempo * 10) % 10
        )

        texto = (
            f"{minutos:02}:"
            f"{segundos:02}."
            f"{decimas}"
        )

        cola.put(
            ("tiempo", texto)
        )

        time.sleep(0.1)



# ACTUALIZAR INTERFAZ


def actualizar():

    try:

        while True:

            mensaje = cola.get_nowait()

            tipo = mensaje[0]

            valor = mensaje[1]



            # CABALLERO


            if tipo == "caballero":

                canvas.itemconfig(
                    sprite_caballero,
                    image=caballero[valor]
                )



            # GATO


            elif tipo == "gato":

                canvas.itemconfig(
                    sprite_gato,
                    image=gato[valor]
                )



            # CRONÓMETRO


            elif tipo == "tiempo":

                canvas.itemconfig(
                    texto_cronometro,
                    text=valor
                )

                canvas.itemconfig(
                    sombra_cronometro,
                    text=valor
                )


    except queue.Empty:

        pass


    ventana.after(
        16,
        actualizar
    )



# CERRAR PROGRAMA


def cerrar_programa():

    detener.set()

    ventana.destroy()


ventana.protocol(
    "WM_DELETE_WINDOW",
    cerrar_programa
)


#------------------------------------------------------------------------------
# CREAR HILOS


hilo_caballero = threading.Thread(
    target=animar_caballero,
    daemon=True
)


hilo_gato = threading.Thread(
    target=animar_gato,
    daemon=True
)


hilo_cronometro = threading.Thread(
    target=cronometro,
    daemon=True
)



# INICIAR HILOS


hilo_caballero.start()

hilo_gato.start()

hilo_cronometro.start()

#------------------------------------------------------------------------------

# INICIAR ACTUALIZACIÓN


actualizar()



# EJECUTAR


ventana.mainloop()
