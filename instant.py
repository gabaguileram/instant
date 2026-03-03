from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# Detecta qué API usar
USE_GROQ = "GROQ_API_KEY" in os.environ

if USE_GROQ:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
else:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

@app.get("/", response_class=HTMLResponse)
def instant():
    message = (
        "¡Estás en un sitio web que acaba de entrar en producción por primera vez!\n"
        "Por favor, responde con un anuncio entusiasta para dar la bienvenida a los visitantes."
    )

    try:
        if USE_GROQ:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": message}]
            )
            reply = response.choices[0].message.content.replace("\n", "<br/>")
        else:
            response = client.responses.create(
                model="gpt-5-nano",
                input=message
            )
            reply = response.output_text.replace("\n", "<br/>")
    except Exception as e:
        reply = f"<b>Error generando respuesta:</b> {e}"

    html = f"""
    <html>
        <head><title>¡En vivo al instante!</title></head>
        <body><p>{reply}</p></body>
    </html>
    """
    return html