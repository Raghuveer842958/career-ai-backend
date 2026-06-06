# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.routes.job_routes import router as job_router
# from app.routes.chat_routes import router as chat_router
# from app.routes.interview_routes import router as interview_router
# from app.routes.voice_routes import router as voice_router

# from fastapi.staticfiles import (
#     StaticFiles
# )

# app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount(
#     "/audio",
#     StaticFiles(
#         directory="app/voice/generated_audio"
#     ),
#     name="audio"
# )

# app.mount(
#     "/user-audio",
#     StaticFiles(
#         directory=
#         "app/voice/user_audio"
#     ),
#     name="user-audio"
# )

# # app.include_router(user_router)

# app.include_router(
#     job_router,
#     prefix='/jobs'
# )

# app.include_router(
#     chat_router,
#     prefix='/chat'
# )

# app.include_router(
#     interview_router,
#     prefix="/interview",
# )

# app.include_router(
#     voice_router,
#     prefix="/voice",
# )






from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routes.job_routes import router as job_router
from app.routes.chat_routes import router as chat_router
from app.routes.interview_routes import router as interview_router
from app.routes.voice_routes import router as voice_router

from app.database import connect_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    print("✅ Database connected")

    yield

    print("👋 App shutting down")


app = FastAPI(lifespan=lifespan)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files
app.mount(
    "/audio",
    StaticFiles(directory="app/voice/generated_audio"),
    name="audio",
)

app.mount(
    "/user-audio",
    StaticFiles(directory="app/voice/user_audio"),
    name="user-audio",
)


# Routes
app.include_router(job_router, prefix="/jobs")
app.include_router(chat_router, prefix="/chat")
app.include_router(interview_router, prefix="/interview")
app.include_router(voice_router, prefix="/voice")