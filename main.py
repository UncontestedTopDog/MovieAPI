from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os

app = FastAPI(title="电影数据 API", description="基于 FastAPI 的电影数据查询服务", version="1.0.0")

# 数据模型
class Movie(BaseModel):
    id: int
    title: str
    originalTitle: str
    link: str
    rating: float
    date: str
    description: str
    event: str
    key: str

# 根路径
@app.get("/")
async def read_root():
    return {"message": "欢迎使用 FastAPI 电影 API！", "status": "运行中", "description": "电影数据 API 服务"}

# 读取电影数据的辅助函数
def load_movies() -> List[Movie]:
    """从 movies_2025.json 文件读取电影数据"""
    try:
        with open("movies_2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Movie(**movie) for movie in data]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="电影数据文件未找到")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="电影数据文件格式错误")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取电影数据时发生错误: {str(e)}")

# 根据ID获取电影信息
@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: int):
    """根据电影ID获取电影详细信息"""
    movies = load_movies()
    
    for movie in movies:
        if movie.id == movie_id:
            return movie
    
    raise HTTPException(status_code=404, detail=f"未找到ID为 {movie_id} 的电影")

# 获取所有电影列表
@app.get("/movies/", response_model=List[Movie])
async def get_all_movies(skip: int = 0, limit: int = 100):
    """获取所有电影列表，支持分页"""
    movies = load_movies()
    
    if skip < 0:
        skip = 0
    if limit <= 0:
        limit = 100
    
    total_movies = len(movies)
    paginated_movies = movies[skip:skip + limit]
    
    return paginated_movies

# 搜索电影
@app.get("/movies/search/", response_model=List[Movie])
async def search_movies(q: str, limit: int = 20):
    """根据电影标题搜索电影"""
    if not q or len(q.strip()) == 0:
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    movies = load_movies()
    search_term = q.lower().strip()
    
    # 在标题和原标题中搜索
    matched_movies = []
    for movie in movies:
        if (search_term in movie.title.lower() or 
            search_term in movie.originalTitle.lower()):
            matched_movies.append(movie)
    
    # 限制返回结果数量
    return matched_movies[:limit]

# 根据评分范围获取电影
@app.get("/movies/rating/", response_model=List[Movie])
async def get_movies_by_rating(min_rating: float = 0.0, max_rating: float = 10.0, limit: int = 50):
    """根据评分范围获取电影"""
    if min_rating < 0 or max_rating > 10 or min_rating > max_rating:
        raise HTTPException(status_code=400, detail="评分范围无效，应在0-10之间且最小值不能大于最大值")
    
    movies = load_movies()
    
    filtered_movies = [
        movie for movie in movies 
        if min_rating <= movie.rating <= max_rating
    ]
    
    return filtered_movies[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 