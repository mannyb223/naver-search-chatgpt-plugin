from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from typing import Optional

app = FastAPI(
    title="NAVER Search ChatGPT Plugin",
    description="A plugin that enhances ChatGPT with the capability to perform searches on NAVER for various content types including news and blogs.",
    version="v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "TNnFZOpYxiuA0iJECR_i")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "78KFaJGKaq")

headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

try:
    app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
except Exception:
    pass

@app.get("/")
async def root():
    return {"message": "NAVER Search ChatGPT Plugin is running"}

@app.get("/search/news")
async def search_news(
    query: str = Query(...),
    display: int = Query(10, ge=1, le=100),
    start: int = Query(1, ge=1, le=1000),
    sort: str = Query("sim", regex="^(sim|date)$")
):
    url = "https://openapi.naver.com/v1/search/news.json"
    params = {"query": query, "display": display, "start": start, "sort": sort}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/search/blog")
async def search_blog(
    query: str = Query(...),
    display: int = Query(10, ge=1, le=100),
    start: int = Query(1, ge=1, le=1000),
    sort: str = Query("sim", regex="^(sim|date)$")
):
    url = "https://openapi.naver.com/v1/search/blog.json"
    params = {"query": query, "display": display, "start": start, "sort": sort}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/search/image")
async def search_image(
    query: str = Query(...),
    display: int = Query(10, ge=1, le=100),
    start: int = Query(1, ge=1, le=1000),
    sort: str = Query("sim", regex="^(sim|date)$"),
    filter: str = Query("all", regex="^(all|large|medium|small)$")
):
    url = "https://openapi.naver.com/v1/search/image"
    params = {"query": query, "display": display, "start": start, "sort": sort, "filter": filter}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/search/shop")
async def search_shop(
    query: str = Query(...),
    display: int = Query(10, ge=1, le=100),
    start: int = Query(1, ge=1, le=1000),
    sort: str = Query("sim", regex="^(sim|date|asc|dsc)$"),
    filter: Optional[str] = Query(None),
    exclude: Optional[str] = Query(None)
):
    url = "https://openapi.naver.com/v1/search/shop.json"
    params = {"query": query, "display": display, "start": start, "sort": sort}
    if filter:
        params["filter"] = filter
    if exclude:
        params["exclude"] = exclude
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/search/kin")
async def search_kin(
    query: str = Query(...),
    display: int = Query(10, ge=1, le=100),
    start: int = Query(1, ge=1, le=1000),
    sort: str = Query("sim", regex="^(sim|date|point)$")
):
    url = "https://openapi.naver.com/v1/search/kin.json"
    params = {"query": query, "display": display, "start": start, "sort": sort}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/search/local")
async def search_local(
    query: str = Query(...),
    display: int = Query(1, ge=1, le=5),
    start: int = Query(1, ge=1, le=1),
    sort: str = Query("random", regex="^(random|comment)$")
):
    url = "https://openapi.naver.com/v1/search/local.json"
    params = {"query": query, "display": display, "start": start, "sort": sort}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NAVER Search Plugin"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
