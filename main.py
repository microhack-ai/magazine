import random
import gradio as gr
import re

def extraer_url_youtube(mensaje):
    # Expresión regular para detectar URLs de YouTube
    youtube_regex = r'(https?://www\.youtube\.com/watch\?v=[\w-]+)'
    match = re.search(youtube_regex, mensaje)
    return match.group(0) if match else None

def random_response(message, history):
    extraer_url_youtube(message)
    return extraer_url_youtube(message)

demo = gr.ChatInterface(random_response)

demo.launch()