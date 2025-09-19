#!/usr/bin/env python
"""
測試網頁端點是否正常運作
"""

import requests
import time

def test_web_endpoint():
    print("=== 測試網頁端點 ===")
    
    # 等待伺服器啟動
    time.sleep(2)
    
    try:
        # 測試 GET 請求
        print("🔄 測試 GET 請求...")
        response = requests.get('http://localhost:8000/chatTranslate/test/', timeout=10)
        print(f"📊 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ GET 請求成功！")
            print(f"📄 內容長度: {len(response.text)} 字元")
            if "ChatTranslate" in response.text:
                print("✅ 頁面內容正確包含 ChatTranslate")
            else:
                print("⚠️ 頁面內容可能有問題")
        else:
            print(f"❌ GET 請求失敗: {response.status_code}")
            print(f"錯誤內容: {response.text}")
        
        # 測試 POST 請求
        print("\n🔄 測試 POST 請求...")
        data = {
            'test_text': 'Hello World'
        }
        response = requests.post('http://localhost:8000/chatTranslate/test/', data=data, timeout=30)
        print(f"📊 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ POST 請求成功！")
            if "Hello World" in response.text:
                print("✅ 表單資料正確處理")
        else:
            print(f"❌ POST 請求失敗: {response.status_code}")
            print(f"錯誤內容: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到伺服器，請確認 Django 開發伺服器是否運行")
    except requests.exceptions.Timeout:
        print("❌ 請求超時")
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")
    
    print("\n=== 測試完成 ===")

if __name__ == "__main__":
    test_web_endpoint()
