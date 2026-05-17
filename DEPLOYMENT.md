# 部署指南

## 架构概览

```
用户浏览器
  ↓
Cloudflare Pages（前端静态文件）
  ↓ API 请求
Render/Railway（FastAPI 后端）
  ↓
Supabase（PostgreSQL 数据库）
```

---

## 1️⃣ Supabase 配置

### 创建项目
1. 访问 [supabase.com](https://supabase.com) 创建新项目
2. 记录以下信息：
   - `SUPABASE_URL`: `https://xxxxx.supabase.co`
   - `SUPABASE_ANON_KEY`: `eyJ...`
   - `SUPABASE_SERVICE_ROLE_KEY`: `eyJ...`
   - `DATABASE_URL`: `postgresql://postgres:xxx@db.xxxxx.supabase.co:5432/postgres`

### 获取 JWT Secret
1. 进入项目 Settings → API → JWT Settings
2. 复制 `JWT Secret`

### 创建数据表
在 SQL Editor 中执行 `database/schema.sql`

---

## 2️⃣ Render 部署后端

### 创建 Web Service
1. 访问 [render.com](https://render.com) 并连接 GitHub
2. 选择 `baby-growth-tracker` 仓库
3. 配置：
   - **Name**: `baby-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_prod.py`

### 环境变量
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_JWT_SECRET=xxx
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=postgresql://postgres:xxx@db.xxxxx.supabase.co:5432/postgres
ALLOWED_ORIGINS=https://your-frontend.pages.dev
PORT=8000
HOST=0.0.0.0
WORKERS=2
```

### 获取后端 URL
部署完成后，Render 会给你一个 URL，如：`https://baby-backend.onrender.com`

---

## 3️⃣ Cloudflare Pages 部署前端

### 创建项目
1. 访问 [pages.cloudflare.com](https://pages.cloudflare.com)
2. 连接 GitHub 并选择 `baby-growth-tracker` 仓库
3. 配置：
   - **项目名称**: `baby-growth-tracker`
   - **生产分支**: `main`
   - **构建目录**: `frontend`
   - **构建命令**: `npm install && npm run build`
   - **输出目录**: `dist`

### 环境变量
```
VITE_API_URL=https://baby-backend.onrender.com/api
```

### 获取前端 URL
部署完成后，Cloudflare 会给你一个 URL，如：`https://baby-growth-tracker.pages.dev`

---

## 4️⃣ 更新 CORS 配置

在 Render 后端环境变量中更新：
```
ALLOWED_ORIGINS=https://baby-growth-tracker.pages.dev
```

---

## 5️⃣ 测试部署

1. 访问前端 URL：`https://baby-growth-tracker.pages.dev`
2. 注册新账号
3. 添加倒计时事件
4. 写一封信给宝宝

---

## 安全检查清单

- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] `SUPABASE_SERVICE_ROLE_KEY` 仅在后端使用
- [ ] `SUPABASE_JWT_SECRET` 仅在后端使用
- [ ] 前端只使用 `VITE_API_URL` 环境变量
- [ ] CORS 配置只允许你的前端域名

---

## 常见问题

### 前端无法连接后端
检查 `VITE_API_URL` 是否正确设置为后端 API 地址

### 登录失败
检查 Supabase 的邮箱确认设置，开发环境可关闭邮箱验证

### 数据库连接失败
检查 `DATABASE_URL` 格式是否正确，确保 Supabase 项目未暂停
