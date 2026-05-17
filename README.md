# 宝宝成长记录系统

一个基于 Cloudflare + Supabase + FastAPI + Vue.js 的宝宝成长记录系统，包含倒计时、信件、孕妇餐记录等功能。

## 🌟 功能特性

- ✅ **倒计时时钟**：显示距离预产期等重要日期的倒计时
- ✅ **给宝宝的信**：写信、看信、定时解锁功能
- ✅ **用户认证**：邮箱+密码登录注册
- ✅ **保活系统**：Cloudflare Workers 自动保活 Supabase
- ✅ **响应式设计**：支持 PC 和移动端

## 📦 技术栈

### 前端
- Vue 3 + Vite
- Tailwind CSS
- Pinia (状态管理)
- Vue Router
- Axios

### 后端
- Python FastAPI
- Supabase (PostgreSQL + Auth，经 REST / Auth HTTP API 访问)

### 部署
- Cloudflare Pages (前端)
- Railway (后端)
- Cloudflare Workers (Supabase 保活，可选)
- Supabase (数据库和认证)

## 🚀 快速开始

### 1. 创建 Supabase 项目

1. 访问 [Supabase](https://supabase.com) 创建账号
2. 创建新项目
3. 在 SQL Editor 中运行 `database/schema.sql` 创建数据表
4. 获取项目 URL 和 API Keys

### 2. 配置后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量文件
copy .env.example .env

# 编辑 .env 文件，填入 Supabase 配置
```

### 3. 启动后端

```bash
# 启动开发服务器
uvicorn app.main:app --reload --port 8000

# 访问 API 文档
# http://localhost:8000/docs

# 检查 Supabase 连接
# http://localhost:8000/health
```

生产部署见 [DEPLOYMENT.md](./DEPLOYMENT.md)（Railway + Cloudflare Pages + Supabase）。

### 4. 配置前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问前端
# http://localhost:3000
```

### 5. 部署 Cloudflare Workers 保活

```bash
# 进入 Cloudflare Worker 目录
cd cloudflare-worker

# 安装 Wrangler
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 设置环境变量
wrangler secret put SUPABASE_ANON_KEY
# 输入你的 Supabase Anon Key

# 部署
wrangler deploy
```

## 📁 项目结构

```
Baby/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── models/         # 数据模型
│   │   ├── routers/        # API 路由
│   │   ├── utils/          # 工具函数
│   │   ├── config.py       # 配置文件
│   │   ├── database.py     # 数据库连接
│   │   └── main.py         # 应用入口
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/               # Vue.js 前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API 服务
│   │   ├── router/        # 路由配置
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── package.json
│   └── vite.config.js
│
├── cloudflare-worker/      # 保活脚本
│   ├── worker.js
│   └── wrangler.toml
│
└── database/              # 数据库
    └── schema.sql         # 表结构
```

## 🔧 环境变量

### 后端 (.env)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

登录与 JWT 由 Supabase Auth 负责，后端通过 HTTP 调用 Supabase，不依赖 `python-jose` / `bcrypt`。

### Cloudflare Workers

```toml
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

## 📱 功能演示

### 倒计时时钟
- 显示距离预产期、生日等重要日期的倒计时
- 支持多个倒计时事件
- 动画效果和渐变背景

### 信件系统
- 写信：富文本编辑，支持图片
- 看信：时间轴视图，仪式感设计
- 定时解锁：设置未来某个日期解锁
- 邮件提醒：每年特定日子提醒写信

### 用户认证
- 邮箱+密码注册登录
- JWT Token 认证
- 路由守卫保护

## 🎨 设计特色

- 🌈 渐变背景和玻璃态效果
- ✨ 流畅的动画和过渡
- 📱 完全响应式设计
- 🎯 极简主义风格
- 💝 仪式感设计元素

## 📝 开发计划

- [ ] 孕妇餐记录功能
- [ ] 准爸爸技术指南
- [ ] 图片上传功能
- [ ] 邮件提醒功能
- [ ] 导出信件为 PDF
- [ ] 多语言支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 💡 致谢

感谢以下开源项目：
- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase](https://supabase.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Cloudflare Workers](https://workers.cloudflare.com/)
