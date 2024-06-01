from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from app.core.settings import settings
from app.routers.user_routers import router as user_router
from app.routers.category_routers import router as category_router
from app.routers.product_routers import router as product_router

# Criando a aplicação FastAPI
app = FastAPI()


# Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurando rotas
app.include_router(user_router, prefix=settings.PREFIX)
app.include_router(category_router, prefix=settings.PREFIX)
app.include_router(product_router, prefix=settings.PREFIX)


# Tratamento de exceções
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# Health Check
@app.get("/", tags=["Health Check"], status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}
