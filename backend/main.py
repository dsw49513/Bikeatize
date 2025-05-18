from fastapi import FastAPI
from backend.routes import router
from backend.auth import router as auth_router  # Importujemy router autoryzacji

app = FastAPI()
app.include_router(router)

# Rejestrujemy wszystkie routery
app.include_router(router)  # Główne endpointy
app.include_router(auth_router)  # Endpointy związane z autoryzacją

@app.get("/")
async def root():
    return {"message": "API is running!"}
