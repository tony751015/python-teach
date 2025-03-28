# 如何本基區網連線開發?

Window: Terminal輸入ipconfig > 查詢 IPv4位址(192.168.1.x)

* 前端檔案修改(.env.lan) VUE_APP_IP4=192.168.1.x
* 前端啟用指令: npm run serve-lan
* Line Develop(https://developers.line.biz/console/channel/2006462026/line-login) 修改 Callback URL (http://192.168.1.x:3000/)
* 後端檔案修改(mackay/user/line_login.py): 修改DEBUG=True > REDIRECT_URL='http://192.168.1.107:3000/'
* 後端Runserver啟用指令: python manage.py runserver 0.0.0.0:8000 --settings=dev
