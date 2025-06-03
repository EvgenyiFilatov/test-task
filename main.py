import asyncio
import hashlib

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()
fake_db = {}  # Простая "база данных" в виде словаря


def generate_short_id(url: str) -> str:
    """Генерирует короткий идентификатор для переданного URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:8]


@app.post("/")
async def shorten_url(request: Request):
    """Принимает URL в теле запроса и возвращает сокращённую ссылку."""
    body = await request.body()
    url = body.decode().strip()
    if not url.startswith('http'):
        raise HTTPException(status_code=400, detail="Invalid URL")
    short_id = generate_short_id(url)
    fake_db[short_id] = url
    return JSONResponse(
        status_code=201,
        content={"shortened": f"http://127.0.0.1:8080/{short_id}"}
    )


@app.get("/async-data")
async def get_async_data():
    """Асинхронно возвращает всю "базу данных" со всеми сокращениями."""
    # Имитация асинхронной работы (например, задержки обращения к БД)
    await asyncio.sleep(1)
    return fake_db  # Возвращаем всю "базу данных"


@app.get("/{shorten_url_id}")
async def redirect_to_original(shorten_url_id: str):
    """По короткому идентификатору возвращает исходный URL."""
    url = fake_db.get(shorten_url_id)
    if url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return JSONResponse(
        status_code=307,
        content={"Location": url}
    )  # Возвращаем JSON с полем Location (имитируя временный редирект)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
