from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class Movie(BaseModel):
    title: str
    originalTitle: str
    link: str
    rating: float
    description: str
    event: str
    key: str


class MovieEntry(BaseModel):
    id: int
    date: str
    month: str
    day: str
    lunar: str
    week: str
    movie: Movie


app = FastAPI(
    title="电影API服务",
    description="从movies_2025.json获取电影数据的API服务",
    version="1.0.0"
)


def load_movies_data() -> List[Dict[Any, Any]]:
    """加载电影数据"""
    try:
        with open("movies_2025.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="电影数据文件未找到")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="电影数据格式错误")


@app.get("/", summary="根路径", description="返回API基本信息")
async def root():
    """根路径返回API信息"""
    return {
        "message": "欢迎使用电影API服务",
        "description": "这是一个从movies_2025.json获取电影数据的API服务",
        "endpoints": {
            "/movies": "获取所有电影数据",
            "/movies/{movie_id}": "根据ID获取特定电影",
            "/movies/date/{date}": "根据日期获取电影",
            "/movies/random": "随机获取一部电影"
        }
    }


@app.get("/movies", response_model=List[MovieEntry], summary="获取所有电影", description="返回所有电影数据")
async def get_all_movies():
    """获取所有电影数据"""
    movies_data = load_movies_data()
    return movies_data


@app.get("/movies/random", response_model=MovieEntry, summary="随机获取电影", description="随机返回一部电影")
async def get_random_movie():
    """随机获取一部电影"""
    import random
    
    movies_data = load_movies_data()
    
    if not movies_data:
        raise HTTPException(status_code=404, detail="没有可用的电影数据")
    
    random_movie = random.choice(movies_data)
    return random_movie


@app.get("/movies/search", response_model=List[MovieEntry], summary="搜索电影", description="根据电影标题搜索电影")
async def search_movies(title: Optional[str] = None, rating_min: Optional[float] = None):
    """搜索电影"""
    movies_data = load_movies_data()
    
    filtered_movies = movies_data
    
    # 根据标题筛选
    if title:
        filtered_movies = [
            movie for movie in filtered_movies 
            if movie.get("movie") and (
                title.lower() in movie["movie"]["title"].lower() or 
                title.lower() in movie["movie"]["originalTitle"].lower()
            )
        ]
    
    # 根据最低评分筛选
    if rating_min is not None:
        filtered_movies = [
            movie for movie in filtered_movies 
            if movie.get("movie") and movie["movie"]["rating"] >= rating_min
        ]
    
    return filtered_movies


@app.get("/movies/{movie_id}", response_model=MovieEntry, summary="根据ID获取电影", description="根据电影ID获取特定电影数据")
async def get_movie_by_id(movie_id: int):
    """根据ID获取特定电影"""
    movies_data = load_movies_data()
    
    for movie in movies_data:
        if movie["id"] == movie_id:
            return movie
    
    raise HTTPException(status_code=404, detail=f"未找到ID为{movie_id}的电影")


@app.get("/movies/date/{date}", response_model=MovieEntry, summary="根据日期获取电影", description="根据日期(YYYY-MM-DD格式)获取电影数据")
async def get_movie_by_date(date: str):
    """根据日期获取电影"""
    # 验证日期格式
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
    
    movies_data = load_movies_data()
    
    for movie in movies_data:
        if movie["date"] == date:
            return movie
    
    raise HTTPException(status_code=404, detail=f"未找到日期为{date}的电影")


@app.get("/health", summary="健康检查", description="检查服务状态")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "message": "电影API服务运行正常",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50001) 
