from fastapi import FastAPI, WebSocket
import google.generativeai as genai
from dotenv import dotenv_values

config = dotenv_values(".env")

app = FastAPI()

# Asumiendo que has configurado las credenciales de GCP adecuadamente
client = genai.configure(api_key=config["GEMINI_API_KEY"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        prompt = data
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Finge ser Jarvis, de la pelicula de Iron Man, debes actuar con mucha inteligencia y responder textos de manera corta, sin nada representado en markdown, solo texto plano con signos de puntuacion y esto es lo que debes hacer: {prompt}")
        generated_text = response.text  

        await websocket.send_text(generated_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)