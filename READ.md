# Ollama 安裝與使用指南

## Windows 安裝
從官網 https://ollama.com/ 下載安裝程式
或使用 winget
winget install ollama
命令行指令

### 啟動 Ollama 服務
ollama start

### 查看當前運行的模型

ollama ps

### 拉取 Llama3 模型

ollama pull llama3

### 運行 Llama3 模型

ollama run llama3

### 列出所有可用模型

ollama list

### 刪除模型

ollama rm llama3

## macOS 安裝
使用 Homebrew
brew install ollama

### 啟動服務

brew services start ollama
## Linux 安裝

使用官方一鍵安裝腳本
curl https://ollama.ai/install.sh | sh

## 或使用 Docker

docker pull ollama/ollama
docker run -d -p 11434:11434 ollama/ollama

# Python 後端環境設置

## 建立虛擬環境
python -m venv venv
source venv/bin/activate # Windows 用 venv\Scripts\activate

## 安裝必要套件

pip install fastapi uvicorn httpx pandas scikit-learn pydantic
推薦的 requirements.txt
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.26.0
pandas==2.2.0
scikit-learn==1.2.2
pydantic==2.6.0

# Vue 前端環境設置
環境準備
##  安裝 Vue CLI
npm install -g @vue/cli

## 建立新專案

vue create mindwave-ai

## 進入專案目錄

cd mindwave-ai

## 安裝必要依賴

npm install axios vue-router marked highlight.js
npm install @vitejs/plugin-vue # 如果使用 Vite

## 推薦的 package.json
jsonCopy{
"dependencies": {
"axios": "^1.6.0",
"vue-router": "^4.2.5",
"marked": "^9.1.2",
"highlight.js": "^11.9.0"
},
"devDependencies": {
"@vitejs/plugin-vue": "^4.5.0",
"vite": "^5.0.0"
}
}
# Docker 容器化部署
Dockerfile for Python Backend
dockerfileCopy# backend/Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Dockerfile for Vue Frontend
dockerfileCopy# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package\*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```
## docker-compose.yml

```yml
yamlCopyversion: '3.8'
services:
backend:
build: ./backend
ports: - "8000:8000"
environment: - OLLAMA_URL=http://ollama:11434

frontend:
build: ./frontend
ports: - "3000:3000"
depends_on: - backend

ollama:
image: ollama/ollama
ports: - "11434:11434"
``` 
# 專案啟動流程

## 啟動 Ollama

ollama start
ollama pull llama3

## 啟動後端

cd backend
uvicorn main:app --reload

## 啟動前端

npm install
npm run dev
常見問題排查
端口占用
bashCopy# Windows 查看端口
netstat -ano | findstr :<port>

# 強制關閉佔用進程

taskkill /PID <PID> /F
Ollama 連接問題

確保 Ollama 服務正在運行
檢查防火牆設置
驗證 http://localhost:11434 是否可訪問

# 安全性建議

使用環境變數管理敏感信息
在生產環境啟用 HTTPS
實施適當的跨域資源共享 (CORS) 策略
定期更新依賴包

