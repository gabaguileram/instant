from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def instant():
    return "Primer despliegue CPD 2026!"
