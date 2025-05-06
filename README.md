# Line Bot 專案

這是一個使用 Django 框架開發的 Line Bot 專案。

## 環境設置

1. 創建虛擬環境：
```bash
python -m venv venv
```

2. 啟動虛擬環境：
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 設置環境變數：
創建 .env 文件並填入以下內容：
```
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_CHANNEL_SECRET=your_channel_secret
DJANGO_SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=.ngrok.io,localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key
```

5. 運行遷移：
```bash
python manage.py migrate
```

6. 啟動服務器：
```bash
python manage.py runserver
```

## 功能

- 接收用戶訊息
- 回覆相同的訊息

## 注意事項

- 請確保已經在 Line Developers Console 中設置了正確的 Webhook URL
- 使用 ngrok 等工具來測試本地開發的 webhook
