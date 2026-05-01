from fastapi import APIRouter

mlLesson03Router = APIRouter()


@mlLesson03Router.get("/")
async def ml_lesson03_root():
    return {"lesson": "03"}
