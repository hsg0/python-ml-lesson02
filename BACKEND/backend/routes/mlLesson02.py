from fastapi import APIRouter

mlLesson02Router = APIRouter()


@mlLesson02Router.get("/")
async def ml_lesson02_root():
    return {"lesson": "02"}
