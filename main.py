from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import os

app = FastAPI(title="电影数据 API", description="基于 FastAPI 的电影数据查询服务", version="1.0.0")

# 数据模型
class MovieInfo(BaseModel):
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
    movie: Optional[MovieInfo] = None

class Movie(BaseModel):
    """为了保持API兼容性的简化电影模型"""
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
def load_movie_entries() -> List[MovieEntry]:
    """从 movies_2025.json 文件读取原始电影数据"""
    try:
        with open("movies_2025.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return [MovieEntry(**entry) for entry in data]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="电影数据文件未找到")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="电影数据文件格式错误")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取电影数据时发生错误: {str(e)}")

def load_movies() -> List[Movie]:
    """转换为简化的Movie对象列表，过滤掉movie为null的记录"""
    entries = load_movie_entries()
    movies = []
    
    for entry in entries:
        if entry.movie is not None:  # 只处理有电影信息的记录
            movie = Movie(
                id=entry.id,
                title=entry.movie.title,
                originalTitle=entry.movie.originalTitle,
                link=entry.movie.link,
                rating=entry.movie.rating,
                date=entry.date,
                description=entry.movie.description,
                event=entry.movie.event,
                key=entry.movie.key
            )
            movies.append(movie)
    
    return movies

# 获取完整的电影条目（包含日期信息）
@app.get("/entries/", response_model=List[MovieEntry])
async def get_all_entries(skip: int = 0, limit: int = 100):
    """获取所有电影条目（包含完整的日期信息），支持分页"""
    entries = load_movie_entries()
    
    if skip < 0:
        skip = 0
    if limit <= 0:
        limit = 100
    
    paginated_entries = entries[skip:skip + limit]
    return paginated_entries

# 根据日期获取电影条目
@app.get("/entries/date/{date}", response_model=MovieEntry)
async def get_entry_by_date(date: str):
    """根据日期获取电影条目信息"""
    entries = load_movie_entries()
    
    for entry in entries:
        if entry.date == date:
            return entry
    
    raise HTTPException(status_code=404, detail=f"未找到日期为 {date} 的电影条目")

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

# 根据月份获取电影条目
@app.get("/entries/month/{month}", response_model=List[MovieEntry])
async def get_entries_by_month(month: str, limit: int = 50):
    """根据月份获取电影条目"""
    entries = load_movie_entries()
    
    matched_entries = [
        entry for entry in entries 
        if entry.month.startswith(month) or month in entry.month
    ]
    
    return matched_entries[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
