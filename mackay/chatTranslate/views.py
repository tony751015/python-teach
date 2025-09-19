from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import requests
import time
from .models import TranslationRecord

# Create your views here.

class LLMTranslationService:
    """
    地端 LLM 翻譯服務類別
    負責與地端部署的 LLM API 進行串接
    """
    
    def __init__(self):
        # LLM API 配置
        self.api_url = "https://e77c18627c0e.ngrok-free.app/api/chat"
        self.model_name = "gemma3:4b"
        self.timeout = 30  # 30秒超時
    
    def translate_text(self, text, source_lang="en", target_lang="zh-tw"):
        """
        翻譯文字
        
        Args:
            text (str): 要翻譯的文字
            source_lang (str): 來源語言代碼
            target_lang (str): 目標語言代碼
            
        Returns:
            dict: 包含翻譯結果和相關資訊的字典
        """
        try:
            start_time = time.time()
            
            # 構建翻譯請求的 prompt - 明確指定翻譯成繁體中文
            if target_lang == "zh-tw":
                prompt = f"請將以下英文翻譯成繁體中文，只需要給出翻譯結果，不要任何解釋或問候語：\n\n{text}"
            elif target_lang == "zh-cn":
                prompt = f"請將以下英文翻譯成簡體中文，只需要給出翻譯結果，不要任何解釋或問候語：\n\n{text}"
            else:
                prompt = f"請翻譯以下文字成{target_lang}，只需要給出翻譯結果：\n\n{text}"
            
            # 構建請求資料
            request_data = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "stream": False
            }
            
            # 發送 HTTP 請求到地端 LLM
            response = requests.post(
                self.api_url,
                json=request_data,
                timeout=self.timeout,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )
            
            # 計算處理時間
            processing_time = time.time() - start_time
            
            # 檢查回應狀態
            if response.status_code == 200:
                response_data = response.json()
                
                # 提取翻譯結果 (根據 LLM API 回應格式調整)
                if 'message' in response_data and 'content' in response_data['message']:
                    translated_text = response_data['message']['content'].strip()
                elif 'choices' in response_data and len(response_data['choices']) > 0:
                    translated_text = response_data['choices'][0]['message']['content'].strip()
                else:
                    translated_text = str(response_data)  # 備用方案
                
                return {
                    'success': True,
                    'translated_text': translated_text,
                    'processing_time': processing_time,
                    'model_used': self.model_name,
                    'original_response': response_data
                }
            else:
                return {
                    'success': False,
                    'error': f"API 請求失敗: HTTP {response.status_code}",
                    'processing_time': processing_time,
                    'response_text': response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "API 請求超時",
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': "無法連接到 LLM API",
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"翻譯處理錯誤: {str(e)}",
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }


@api_view(['POST'])
def translate_chat_message(request):
    """
    翻譯聊天訊息的 API 端點
    
    POST /api/translate/
    Body: {
        "text": "要翻譯的文字",
        "source_lang": "en",
        "target_lang": "zh-tw"
    }
    """
    try:
        # 解析請求資料
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data
        
        # 驗證必要參數
        if 'text' not in data or not data['text'].strip():
            return Response({
                'success': False,
                'error': '請提供要翻譯的文字'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        text_to_translate = data['text'].strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'zh-tw')
        
        # 建立翻譯服務實例
        translator = LLMTranslationService()
        
        # 執行翻譯
        translation_result = translator.translate_text(
            text=text_to_translate,
            source_lang=source_lang,
            target_lang=target_lang
        )
        
        # 儲存翻譯記錄到資料庫
        translation_record = TranslationRecord.objects.create(
            original_text=text_to_translate,
            translated_text=translation_result.get('translated_text', ''),
            source_language=source_lang,
            target_language=target_lang,
            translation_model=translation_result.get('model_used', 'gemma3:4b'),
            translation_time=translation_result.get('processing_time', 0)
        )
        
        # 準備回應資料
        response_data = {
            'success': translation_result['success'],
            'record_id': translation_record.id,
            'original_text': text_to_translate,
            'translated_text': translation_result.get('translated_text', ''),
            'source_language': source_lang,
            'target_language': target_lang,
            'processing_time': translation_result.get('processing_time', 0),
            'model_used': translation_result.get('model_used', 'gemma3:4b')
        }
        
        # 如果翻譯失敗，加入錯誤資訊
        if not translation_result['success']:
            response_data['error'] = translation_result.get('error', '未知錯誤')
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'處理請求時發生錯誤: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_translation_records(request):
    """
    取得翻譯記錄列表
    
    GET /api/translate/records/
    """
    try:
        # 取得最近的翻譯記錄 (限制50筆)
        records = TranslationRecord.objects.all()[:50]
        
        records_data = []
        for record in records:
            records_data.append({
                'id': record.id,
                'original_text': record.original_text,
                'translated_text': record.translated_text,
                'source_language': record.source_language,
                'target_language': record.target_language,
                'translation_model': record.translation_model,
                'created_at': record.created_at.isoformat(),
                'processing_time': record.translation_time
            })
        
        return Response({
            'success': True,
            'records': records_data,
            'total_count': len(records_data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'取得翻譯記錄時發生錯誤: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def test_translation_view(request):
    """
    測試翻譯功能的簡單頁面
    """
    context = {
        'test_result': None,
        'test_text': '',
        'error_message': None
    }
    
    if request.method == 'POST':
        # 處理測試翻譯請求
        test_text = request.POST.get('test_text', 'how do you do').strip()
        context['test_text'] = test_text
        
        if test_text:
            try:
                # 建立翻譯服務實例並測試
                translator = LLMTranslationService()
                result = translator.translate_text(test_text)
                
                # 印出結果到控制台
                print("=== 翻譯測試結果 ===")
                print(f"原始文字: {test_text}")
                print(f"翻譯成功: {result['success']}")
                if result['success']:
                    print(f"翻譯結果: {result['translated_text']}")
                    print(f"處理時間: {result['processing_time']:.2f} 秒")
                else:
                    print(f"錯誤訊息: {result['error']}")
                print("==================")
                
                context['test_result'] = result
                
            except Exception as e:
                context['error_message'] = f"測試過程發生錯誤: {str(e)}"
                print(f"測試錯誤: {e}")
        else:
            context['error_message'] = "請輸入要翻譯的文字"
    
    # 先生成結果 HTML
    result_html = _generate_result_html(context)
    test_text_value = context.get('test_text', 'how do you do')
    
    # 生成 HTML 內容
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>翻譯功能測試</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .form-group {{ margin: 20px 0; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #333; }}
            input, textarea {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }}
            button {{ background-color: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background-color: #005a87; }}
            .result {{ margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 4px; border-left: 4px solid #007cba; }}
            .success {{ background-color: #d4edda; border-left-color: #28a745; }}
            .error {{ background-color: #f8d7da; border-left-color: #dc3545; }}
            .info {{ background-color: #e2f3ff; border-left-color: #007cba; }}
            .translation-result {{ margin-top: 15px; padding: 15px; background-color: #fff; border: 1px solid #ddd; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 ChatTranslate 翻譯功能測試</h1>
            
            <form method="post">
                <div class="form-group">
                    <label for="test_text">要翻譯的英文文字:</label>
                    <textarea id="test_text" name="test_text" rows="4" placeholder="輸入要翻譯的英文文字...">{test_text_value}</textarea>
                </div>
                <button type="submit">🚀 開始翻譯</button>
            </form>
            
            {result_html}
            
            <div class="result info">
                <h3>📋 系統資訊</h3>
                <ul>
                    <li><strong>API 端點:</strong> /chatTranslate/api/translate/</li>
                    <li><strong>記錄查詢:</strong> /chatTranslate/api/translate/records/</li>
                    <li><strong>使用模型:</strong> gemma3:4b</li>
                    <li><strong>LLM API:</strong> https://e77c18627c0e.ngrok-free.app/api/chat</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    from django.http import HttpResponse
    return HttpResponse(html_content)

def _generate_result_html(context):
    """生成結果 HTML"""
    if context.get('error_message'):
        return f"""
        <div class="result error">
            <h3>❌ 錯誤</h3>
            <p>{context['error_message']}</p>
        </div>
        """
    
    if context.get('test_result'):
        result = context['test_result']
        if result['success']:
            return f"""
            <div class="result success">
                <h3>✅ 翻譯成功!</h3>
                <div class="translation-result">
                    <p><strong>🔤 原始文字:</strong> {context['test_text']}</p>
                    <p><strong>🈯 翻譯結果:</strong> {result['translated_text']}</p>
                    <p><strong>⏱️ 處理時間:</strong> {result['processing_time']:.2f} 秒</p>
                    <p><strong>🤖 使用模型:</strong> {result.get('model_used', 'gemma3:4b')}</p>
                </div>
            </div>
            """
        else:
            return f"""
            <div class="result error">
                <h3>❌ 翻譯失敗</h3>
                <p><strong>錯誤原因:</strong> {result.get('error', '未知錯誤')}</p>
                <p><strong>處理時間:</strong> {result.get('processing_time', 0):.2f} 秒</p>
            </div>
            """
    
    return ""
