# 部署指南

## 架构概览

```
用户浏览器
  ↓
Cloudflare Pages（前端静态文件）
  ↓ API 请求
Railway（FastAPI 后端）
  ↓
Supabase（PostgreSQL + Auth）
```

---

## 1️⃣ Supabase 配置

### 创建项目
1. 访问 [supabase.com](https://supabase.com) 创建新项目
2. 在 **Settings → API** 记录：
   - `SUPABASE_URL`: `https://xxxxx.supabase.co`
   - `SUPABASE_ANON_KEY`（anon / publishable key）
   - `SUPABASE_SERVICE_ROLE_KEY`（service_role / secret key，仅后端使用）

### 创建数据表
在 SQL Editor 中执行 `database/schema.sql`

---

## 2️⃣ Railway 部署后端

### 创建服务
1. 访问 [railway.app](https://railway.app) 并连接 GitHub 仓库
2. **New Project → Deploy from GitHub**
3. 选中本仓库，在 Service 设置中指定：
   - **Root Directory**: `backend`
   - **Start Command**（若未自动识别）: `python run_prod.py`

Railway 会通过 `backend/railway.toml` 使用 `/health` 做健康检查；启动时会自动探测 Supabase REST + Auth 是否可达，失败则部署不会通过。

### 环境变量（必填 3 项）

认证由 Supabase Auth 处理，后端无需 `SECRET_KEY`、`JWT_SECRET` 或 `bcrypt` 相关依赖。

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

可选：

```
PORT=8000
HOST=0.0.0.0
WORKERS=1
```

> Railway 会自动注入 `PORT`，一般无需手动设置。免费套餐建议 `WORKERS=1`。

### 获取后端 URL
部署成功后，在 Railway → Service → **Settings → Networking** 生成域名，例如：

`https://baby-production-xxxx.up.railway.app`

### 验证 Supabase 连接

```bash
curl https://你的服务.up.railway.app/health
```

成功示例：

```json
{
  "status": "ok",
  "supabase": {
    "ok": true,
    "rest": true,
    "auth": true,
    "checked_at": "2026-05-17T12:00:00+00:00",
    "errors": []
  }
}
```

若 `status` 为 `degraded` 或 HTTP 503，检查 Railway 环境变量是否与 Supabase 控制台一致，并确认 Supabase 项目未暂停。

---

## 3️⃣ Cloudflare Pages 部署前端

### 创建项目
1. 访问 [pages.cloudflare.com](https://pages.cloudflare.com)
2. 连接 GitHub 并选择本仓库
3. 配置：
   - **生产分支**: `main`
   - **根目录 / 构建目录**: `frontend`
   - **构建命令**: `npm install && npm run build`
   - **输出目录**: `dist`

### 环境变量
```
VITE_API_URL=https://你的服务.up.railway.app/api
```

### 获取前端 URL
例如：`https://baby-growth-tracker.pages.dev`

---

## 4️⃣ CORS（可选）

当前 `backend/app/main.py` 中 `allow_origins=["*"]`，开发联调最省事。上线后若需只允许 Cloudflare 域名，把该列表改成你的 Pages 地址即可。

---

## 5️⃣ 测试部署

1. `curl https://你的服务.up.railway.app/health` → Supabase 连接正常
2. 访问前端 URL，注册账号
3. 添加倒计时、写信

---

## 安全检查清单

- [ ] `.env` 已加入 `.gitignore`，未提交密钥
- [ ] `SUPABASE_SERVICE_ROLE_KEY` 仅在 Railway 后端配置
- [ ] 前端只配置 `VITE_API_URL`
- [ ] 生产环境按需收紧 CORS

---

## 常见问题

### Railway 部署失败 / 容器反复重启
- 查看 Deploy Logs：若出现 `Supabase connection check failed`，说明启动自检未通过
- 核对三个 `SUPABASE_*` 变量无多余空格、与 Supabase 控制台一致

### 前端无法连接后端
- `VITE_API_URL` 须为 `https://xxx.up.railway.app/api`（带 `/api`）
- Railway 域名需已公开（Generate Domain）

### 登录失败
- Supabase → Authentication：开发环境可关闭邮箱验证
- 确认项目未休眠（免费版长期不用会暂停）

### `/health` 返回 503
- Supabase 项目是否暂停
- `SUPABASE_URL` 是否含 `https://` 且末尾无多余斜杠问题（代码会自动 trim）
