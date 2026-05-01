from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from contextlib import asynccontextmanager

from config.mongoDB import connectToMongoDB, disconnectFromMongoDB

from limiter.limiter import limiter
from routes.mlLesson01 import mlLesson01Router
from routes.mlLesson02 import mlLesson02Router
from routes.mlLesson03 import mlLesson03Router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting backend...")

    connectToMongoDB()

    print("✅ Backend startup complete")

    yield

    print("🛑 Shutting down backend...")

    disconnectFromMongoDB()

    print("✅ Backend shutdown complete")


app = FastAPI(
    title="ml-lesson02 backend",
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(mlLesson01Router, prefix="/ml-lesson01", tags=["mlLesson01"])
app.include_router(mlLesson02Router, prefix="/ml-lesson02", tags=["mlLesson02"])
app.include_router(mlLesson03Router, prefix="/ml-lesson03", tags=["mlLesson03"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8020)


