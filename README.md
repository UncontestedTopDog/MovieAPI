# FastAPI 电影数据 API

这是一个基于 FastAPI 的电影数据查询服务。

## 功能特性

- ✅ 电影数据 RESTful API 接口
- ✅ 自动生成 API 文档
- ✅ 数据验证和类型检查
- ✅ 异步处理支持
- ✅ 多种查询方式（按 ID、搜索、评分筛选）
- ✅ 分页支持

## 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

## 运行应用

### 方法一：直接运行 Python 文件
```bash
python3 main.py
```

### 方法二：使用 uvicorn 命令
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 访问应用

启动后，您可以访问以下链接：

- **应用主页**: http://127.0.0.1:8000
- **交互式 API 文档 (Swagger UI)**: http://127.0.0.1:8000/docs
- **备用 API 文档 (ReDoc)**: http://127.0.0.1:8000/redoc

## API 端点

### 基础端点
- `GET /` - 根路径，返回欢迎信息

### 电影 API 端点 🎬
- `GET /movies/{movie_id}` - 根据电影ID获取电影详细信息
- `GET /movies/` - 获取所有电影列表（支持分页）
- `GET /movies/search/` - 根据电影标题搜索电影
- `GET /movies/rating/` - 根据评分范围获取电影

## API 使用示例 🎬

#### 根据 ID 获取电影信息
```bash
curl "http://127.0.0.1:8000/movies/1"
```

#### 获取电影列表（分页）
```bash
# 获取前10部电影
curl "http://127.0.0.1:8000/movies/?limit=10"

# 跳过前20部，获取接下来的15部电影
curl "http://127.0.0.1:8000/movies/?skip=20&limit=15"
```

#### 搜索电影
```bash
# 搜索标题包含"机器人"的电影
curl "http://127.0.0.1:8000/movies/search/?q=机器人&limit=5"

# 搜索标题包含"爱情"的电影
curl "http://127.0.0.1:8000/movies/search/?q=爱情"
```

#### 根据评分范围获取电影
```bash
# 获取评分在9.0-10.0之间的电影
curl "http://127.0.0.1:8000/movies/rating/?min_rating=9.0&max_rating=10.0&limit=10"

# 获取评分8.5以上的电影
curl "http://127.0.0.1:8000/movies/rating/?min_rating=8.5&limit=20"
```

## 开发说明

- 使用 `--reload` 参数运行时，代码修改会自动重启服务器
- 所有的 API 接口都有自动的数据验证
- 访问 `/docs` 可以在浏览器中测试 API 接口

## 项目结构

```
FastAPI/
├── main.py              # 电影 API 主应用文件
├── movies_2025.json     # 电影数据文件（3600+ 部电影）
├── calendar_2025.json   # 日历数据文件
├── requirements.txt     # 项目依赖列表
└── README.md           # API 说明文档
```

## 数据说明

- `movies_2025.json`: 包含2025年的电影数据，每部电影包含以下信息：
  - `id`: 电影唯一标识
  - `title`: 中文标题
  - `originalTitle`: 原标题
  - `link`: 豆瓣链接
  - `rating`: 评分（0-10）
  - `date`: 相关日期
  - `description`: 电影描述
  - `event`: 相关事件说明 
  - `key`: 图片资源的 key

  source venv/bin/activate && python main.py