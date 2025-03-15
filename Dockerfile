# 使用官方 Python 映像檔作為基底
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製所有專案檔案到容器內
COPY . /app

# 安裝專案的 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Flask 伺服器的預設埠
EXPOSE 5000

# 啟動程式
CMD ["python", "main.py"]
