from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from .routes import auth, posts, categories, tags, comments, likes, admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
bearer_scheme = HTTPBearer(auto_error=False)

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "oauth2RedirectUrl": "/docs/oauth2-redirect",
        "supportedSubmitMethods": ["get", "put", "post", "delete", "patch"],
    },
    security=[
        {"Bearer": []},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(likes.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API"}

def main():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
