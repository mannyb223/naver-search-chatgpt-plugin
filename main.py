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

# Add CORS middleware for ChatGPT plugin compatibility
app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

# NAVER API credentials
NAVER_CLIENT_ID = "TNnFZOpYxiuA0iJECR_i"
NAVER_CLIENT_SECRET = "78KFaJGKaq"

headers = {
      "X-Naver-Client-Id": NAVER_CLIENT_ID,
      "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

# Serve static files for plugin configuration
try:
      app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
except Exception:
      pass  # Directory might not exist during development

@app.get("/")
async def root():
      return {"message": "NAVER Search ChatGPT Plugin is running"}

@app.get("/news")
async def search_news(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(10, ge=1, le=100, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1000, description="Index of the first result to return"),
      sort: str = Query("sim", regex="^(sim|date)$", description="Sort order of results")
):
      """Search for news articles based on the query."""
      url = "https://openapi.naver.com/v1/search/news.json"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort
      }

    try:
              response = requests.get(url, headers=headers, params=params)
              response.raise_for_status()
              return response.json()
except requests.RequestException as e:
          raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/blog")
async def search_blog(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(10, ge=1, le=100, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1000, description="Index of the first result to return"),
      sort: str = Query("sim", regex="^(sim|date)$", description="Sort order of results")
):
      """Search for blog posts based on the query."""
      url = "https://openapi.naver.com/v1/search/blog.json"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort
      }

    try:
              response = requests.get(url, headers=headers, params=params)
              response.raise_for_status()
              return response.json()
except requests.RequestException as e:
          raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/image")
async def search_image(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(10, ge=1, le=100, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1000, description="Index of the first result to return"),
      sort: str = Query("sim", regex="^(sim|date)$", description="Sort order of results"),
      filter: str = Query("all", regex="^(all|large|medium|small)$", description="Filter by size")
):
      """Search for images based on the query."""
      url = "https://openapi.naver.com/v1/search/image"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort,
          "filter": filter
      }

    try:
              response = requests.get(url, headers=headers, params=params)
              response.raise_for_status()
              return response.json()
except requests.RequestException as e:
          raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/shop")
async def search_shop(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(10, ge=1, le=100, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1000, description="Index of the first result to return"),
      sort: str = Query("sim", regex="^(sim|date|asc|dsc)$", description="Sort order of results"),
      filter: Optional[str] = Query(None, description="Type of products to include"),
      exclude: Optional[str] = Query(None, description="Type of products to exclude")
):
      """Search for products based on the query."""
      url = "https://openapi.naver.com/v1/search/shop.json"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort
      }

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

@app.get("/kin")
async def search_kin(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(10, ge=1, le=100, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1000, description="Index of the first result to return"),
      sort: str = Query("sim", regex="^(sim|date|point)$", description="Sort order of results")
):
      """Search for knowledge content based on the query."""
      url = "https://openapi.naver.com/v1/search/kin.json"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort
      }

    try:
              response = requests.get(url, headers=headers, params=params)
              response.raise_for_status()
              return response.json()
except requests.RequestException as e:
          raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

@app.get("/local")
async def search_local(
      query: str = Query(..., description="Search keywords"),
      display: int = Query(1, ge=1, le=5, description="Number of results to display"),
      start: int = Query(1, ge=1, le=1, description="Index of the first result to return"),
      sort: str = Query("random", regex="^(random|comment)$", description="Sort order of results")
):
      """Search for local business information based on the query."""
      url = "https://openapi.naver.com/v1/search/local.json"
      params = {
          "query": query,
          "display": display,
          "start": start,
          "sort": sort
      }

    try:
              response = requests.get(url, headers=headers, params=params)
              response.raise_for_status()
              return response.json()
except requests.RequestException as e:
          raise HTTPException(status_code=500, detail=f"NAVER API error: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
      return {"status": "healthy", "service": "NAVER Search Plugin"}

if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="0.0.0.0", port=10000)
