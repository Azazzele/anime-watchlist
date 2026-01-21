from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импортируем главный v1 роутер
from app.api.v1.router import api_router

app = FastAPI(
    title="WordAnimation API",
    description="API для аниме, персонажей, сэйю и т.д.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS — разрешаем фронт (Vue/Vite на 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",      # если вдруг используешь другой порт
        "http://127.0.0.1:3000",
        "*"                           # временно для теста (потом убери)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем все v1 эндпоинты
app.include_router(api_router)

# Проверка, что сервер живой
@app.get("/")
async def root():
    return {"message": "WordAnimation API работает", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "time": "OK"}