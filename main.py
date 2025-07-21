from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from typing import Optional

app = FastAPI(
    title="NAVER Search ChatGPT Plugin",
    description="Search NAVER for news, blogs, images, shopping, local info, and knowledge.",
    version="v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com","https://chatgpt.com"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

NAVER_CLIENT_ID     = os.getenv("NAVER_CLIENT_ID", "TNnFZOpYxiuA0iJECR_i")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "78KFaJGKaq")
HEADERS = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

# serve .well-known for plugin manifest
try:
    app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
except:
    pass

@app.get("/")
async def root():
    return {"message": "Plugin is running"}

def naver_get(path: str, params: dict):
    url = f"https://openapi.naver.com/v1/search/{path}.json"
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

@app.get("/search/news")
async def search_news(query: str = Query(...), display: int = Query(10, ge=1, le=100), start: int = Query(1, ge=1, le=1000), sort: str = Query("sim", regex="^(sim|date)$")):
    return naver_get("news", {"query": query, "display": display, "start": start, "sort": sort})

@app.get("/search/blog")
async def search_blog(query: str = Query(...), display: int = Query(10, ge=1, le=100), start: int = Query(1, ge=1, le=1000), sort: str = Query("sim", regex="^(sim|date)$")):
    return naver_get("blog", {"query": query, "display": display, "start": start, "sort": sort})

@app.get("/search/image")
async def search_image(query: str = Query(...), display: int = Query(10, ge=1, le=100), start: int = Query(1, ge=1, le=1000), sort: str = Query("sim", regex="^(sim|date)$"), filter: str = Query("all", regex="^(all|large|medium|small)$")):
    return naver_get("image", {"query": query, "display": display, "start": start, "sort": sort, "filter": filter})

@app.get("/search/shop")
async def search_shop(query: str = Query(...), display: int = Query(10, ge=1, le=100), start: int = Query(1, ge=1, le=1000), sort: str = Query("sim", regex="^(sim|date|asc|dsc)$"), filter: Optional[str] = Query(None), exclude: Optional[str] = Query(None)):
    params = {"query": query, "display": display, "start": start, "sort": sort}
    if filter:  params["filter"] = filter
    if exclude: params["exclude"] = exclude
    return naver_get("shop", params)

@app.get("/search/kin")
async def search_kin(query: str = Query(...), display: int = Query(10, ge=1, le=100), start: int = Query(1, ge=1, le=1000), sort: str = Query("sim", regex="^(sim|date|point)$")):
    return naver_get("kin", {"query": query, "display": display, "start": start, "sort": sort})

@app.get("/search/local")
async def search_local(query: str = Query(...), display: int = Query(1, ge=1, le=5), start: int = Query(1, ge=1, le=1), sort: str = Query("random", regex="^(random|comment)$")):
    return naver_get("local", {"query": query, "display": display, "start": start, "sort": sort})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
