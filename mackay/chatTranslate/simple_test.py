#!/usr/bin/env python
"""
chatTranslate 簡單測試腳本
執行這個檔案即可測試翻譯功能
"""

import os
import sys
import django

# 設定 Django 環境 (需要往上一層找到 mackay 專案根目錄)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mackay.settings')
django.setup()

from chatTranslate.views import LLMTranslationService

def main():
    print("=== chatTranslate 翻譯功能測試 ===")
    print()
    
    # 建立翻譯服務
    translator = LLMTranslationService()
    
    # 預設測試文字 (你可以修改這裡)
    test_text = "LUKE I AM YOUR FATHER"
    
    print(f"🔧 API 網址: {translator.api_url}")
    print(f"🤖 使用模型: {translator.model_name}")
    print(f"📝 測試文字: {test_text}")
    print()
    print("開始翻譯...")
    
    # 執行翻譯
    result = translator.translate_text(test_text)
    
    # 顯示結果
    print("=" * 50)
    if result['success']:
        print("✅ 翻譯成功！")
        print(f"🔤 原始文字: {test_text}")
        print(f"🈯 翻譯結果: {result['translated_text']}")
        print(f"⏱️  處理時間: {result['processing_time']:.2f} 秒")
        print(f"🤖 使用模型: {result['model_used']}")
    else:
        print("❌ 翻譯失敗！")
        print(f"🚫 錯誤原因: {result['error']}")
        print(f"⏱️  處理時間: {result['processing_time']:.2f} 秒")
    
    print("=" * 50)
    print("測試完成！")

if __name__ == "__main__":
    main()
