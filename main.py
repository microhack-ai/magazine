import random
import gradio as gr
import re
import subprocess
import glob

def extraer_url_youtube(mensaje):
    # Expresión regular para detectar URLs de YouTube
    youtube_regex = r'(https?://www\.youtube\.com/watch\?v=[\w-]+)'
    match = re.search(youtube_regex, mensaje)
    return match.group(0) if match else None

def nombre_primer_subtitulo_youtube(url):
    # Comando para listar subtítulos disponibles
    comando_listar = ["youtube-dl", "--list-subs", url]
    
    # Ejecuta el comando y captura la salida
    resultado = subprocess.run(comando_listar, capture_output=True, text=True)
    salida = resultado.stdout
    
    # Buscar el primer idioma de subtítulo disponible
    match = re.search(r'Language formats\n([a-zA-Z-]+)', salida)
    if not match:
        print("No se encontraron subtítulos para el video.")
        return None
    
    idioma = match.group(1)
    
    # Comando para obtener el nombre del archivo sin descargar
    comando_nombre = ["youtube-dl", "--get-filename", "-o", "%(title)s", url]
    resultado_nombre = subprocess.run(comando_nombre, capture_output=True, text=True)
    nombre_base = resultado_nombre.stdout.strip()
    
    # Añadir la extensión y el código de idioma al nombre del archivo
    nombre_archivo = f"{nombre_base}-{idioma}.vtt"
    
    # Comando para descargar el subtítulo del idioma encontrado
    comando_descargar = ["youtube-dl", "--write-sub", "--sub-lang", idioma, "--skip-download", url]
    
    try:
        # Ejecutar el comando y esperar a que finalice
        subprocess.run(comando_descargar, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return None
    
    return nombre_archivo

def descargar_primer_subtitulo_youtube(url):
    # Extraer el ID del video de la URL
    video_id = re.search(r"v=([\w-]+)", url).group(1)
    
    # Comando para obtener el título del video
    comando_nombre = ["youtube-dl", "--get-filename", "-o", "%(title)s", url]
    resultado_nombre = subprocess.run(comando_nombre, capture_output=True, text=True)
    nombre_base = resultado_nombre.stdout.strip()
    
    # Construir el nombre del archivo de subtítulos
    nombre_archivo = f"{nombre_base}-{video_id}.en.vtt"
    
    # Comando para descargar el subtítulo automático
    comando_descargar = ["youtube-dl", "--write-auto-sub", "--sub-format", "vtt", "--skip-download", url]
    
    try:
        # Ejecutar el comando y esperar a que finalice
        subprocess.run(comando_descargar, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return None
    
    return nombre_archivo



def obtener_primeros_2500_del_subtitulo(url):
    # Descargar el subtítulo
    nombre_archivo = descargar_primer_subtitulo_youtube(url)
    print("nombre archivo")
    print(nombre_archivo)
    
    # Si no se pudo obtener el nombre del archivo, retornar None
    if not nombre_archivo:
        return None

    # Intentar leer el archivo
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read(2500)
        return contenido
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo {nombre_archivo}")
        return None

def random_response(message, history):
    url = extraer_url_youtube(message)
    contenido = obtener_primeros_2500_del_subtitulo(url)
    print(contenido)
    return contenido

demo = gr.ChatInterface(random_response)

demo.launch()