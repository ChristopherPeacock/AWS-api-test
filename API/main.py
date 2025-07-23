
from fastapi import FastAPI,

app = FastAPI(
    title="OptiCultivate API",
    version="1.0.0",
    description="Private API for targeted service discovery in the UK.",
)

@app.get("/")
def test():
    return {"API Running": True}

