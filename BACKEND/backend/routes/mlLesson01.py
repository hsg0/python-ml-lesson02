from fastapi import APIRouter

mlLesson01Router = APIRouter()


@mlLesson01Router.get("/")
async def ml_lesson01_root():
    return {"lesson": "01"}
