from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .router.router_user import router_user
from .router.router_exercise import router_exercise
from .router.router_level import router_level
from .router.router_level_quiz import router_level_quiz
from .router.router_user_level import router_user_level
from .router.router_user_exercise import router_user_exercise

load_dotenv(find_dotenv())

app = FastAPI(title="TuturKata API", description="API for TuturKata application", version="0.1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint with redirect to docs
@app.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')

# Include routers
app.include_router(router_user)
app.include_router(router_user_level)
app.include_router(router_user_exercise)

