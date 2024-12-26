FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y     ffmpeg     gcc     python3-dev     && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir     moviepy==1.0.3     numpy==1.21.2     pydub==0.25.1     openai-whisper

# 启动命令
CMD ["python", "api/index.py"]
