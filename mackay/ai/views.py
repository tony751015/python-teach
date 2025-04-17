from google import genai
from google.genai import types
import html
import json
import google.genai
import re

from .models import wound_recognize

from rest_framework.parsers import DataAndFiles, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# 引用客製化的會員
from django.contrib.auth import get_user_model
User = get_user_model()

# 本機開發要驗證身分
# gcloud auth application-default login

# Vertex AI 專案設定
PROJECT_ID = "wdcare"

GEMINI_PRO = {
  "model": "gemini-1.5-pro-002",
  "location": "asia-east1",
}

GEMINI_FLASH = {
  "model": "gemini-2.0-flash-lite-001",
  "location": "us-central1",
}

# 模型回覆安全性設定
SAFETY_SETTINGS = [
  types.SafetySetting(
    category="HARM_CATEGORY_HATE_SPEECH",
    threshold="OFF"
  ),
  types.SafetySetting(
    category="HARM_CATEGORY_DANGEROUS_CONTENT",
    threshold="OFF"
  ),
  types.SafetySetting(
    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
    threshold="OFF"
  ),
  types.SafetySetting(
    category="HARM_CATEGORY_HARASSMENT",
    threshold="OFF"
  )
]

# Vector Search / Groundings設定
tools = [
  # types.Tool(retrieval=types.Retrieval(vertex_rag_store=types.VertexRagStore(rag_resources=[types.VertexRagStoreRagResource(rag_corpus="projects/wdcare/locations/us-central1/ragCorpora/{id}")]))), # RAG Engine

  types.Tool(retrieval=types.Retrieval(vertex_ai_search=types.VertexAISearch(datastore="projects/wdcare/locations/global/collections/default_collection/dataStores/vertex-rag-store_1744872275743"))), # Vertex AI Search

  # types.Tool(google_search_retrieval=types.GoogleSearch()), # Google Grounding
]



# 移除回傳Markdown的Json格式
def clean_json_string(json_string):
  pattern = r'^```json\s*(.*?)\s*```$'
  cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
  # print('clean_json_string', cleaned_string.strip())
  return cleaned_string.strip()



# LLM 生成回覆
def generate_response(drcell_prompt, generate_config, client, models, conversation_history, tools=tools):
  instructions = f"""
    你是由 Wdcare傷口照護平台 開發的 醫療 AI模型，專注於傷口照護處理、皮膚問題分析、健康保健等領域。在 Wdcare 平台上，你提供專業諮詢服務，包括：皮膚傷口範圍照片分析、藥物諮詢、傷口處理諮詢、保健諮詢等。
  """

  print('\033[93m' + f'Gemini Prompt: {drcell_prompt}' + '\033[0m')

  generate_content_config = types.GenerateContentConfig(
    temperature = generate_config['temperature'],
    top_p = generate_config['top_p'],
    max_output_tokens = generate_config['max_output_tokens'],
    response_modalities = ["TEXT"],
    safety_settings = SAFETY_SETTINGS,
    tools = tools,
    # response_mime_type = generate_config['response_mime_type'],
    # response_schema = generate_config['response_schema'],
    system_instruction=[types.Part(text=instructions)],
  )

  contents = []

  for message in conversation_history:
      contents.append(types.Content(role=message["role"], parts=[types.Part(text=message["content"])]))

  responses = client.models.generate_content(
    model = models,
    contents = contents,
    config = generate_content_config,
  )

  # print('\033[93m' + f"""
  #   Gemini Response: {responses.text}
  #   \n
  #   Gemini TokenUsed: {responses.usage_metadata.total_token_count}
  # """ + '\033[0m')

  # 逐行打字效果
  # for chunk in client.models.generate_content_stream(
  #   model = model,
  #   contents = contents,
  #   config = generate_content_config,
  #   ):
  #   if not chunk.candidates or not chunk.candidates[0].content.parts:
  #       continue
  #   print(chunk, end="")

  model_response = responses.text
  token_used = responses.usage_metadata.total_token_count
  conversation_history.append({"role": "model", "content": model_response})

  return model_response, conversation_history, token_used





@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def gemini_request(request):
  serializer = JSONParser().parse(request)
  input_content = serializer['input_content']

  models = GEMINI_PRO['model']
  client = genai.Client(vertexai=True, project=PROJECT_ID, location = GEMINI_PRO['location'])

  userReport = {
    'birthday': '1990-01-01',
    'gender': '男',
    'cancer_type': '乳癌',
    'cancer_period': '二期',
    'subdivide': 'HER2陽性',
    'medicine': '泰莫西芬',
    'disease': '高血壓',
    'allergy': '無',
  }
  
  # 主要的prompt + 帶入參數組合上下文本
  drcell_prompt = """
    你將收到 [我的問題]，該問題是一個文字字串的輸入。你的任務是根據以下規則處理此文字並返回 JSON 回應。

    [我的問題]: %s

    <執行任務的步驟>
    1. 文字理解和驗證：
      - 請先判斷是否能夠完全理解 [我的問題] 所描述的內容、語意。

    2. 直接返回JSON 回應（如果無法完全理解 [我的問題] 所描述的內容、語意）：
      - 如果無法完全理解[我的問題]所描述的內容、語意，務必直接返回以下 JSON 回應：`{"response": "很抱歉，我似乎無法完全理解您的問題。請您更具體地描述您的問題，我會盡力根據您提供的資訊，給予您更適切的建議。您也可以 **(點擊右下角【請醫師補充】按鈕)** ，由醫護本人做進階說明。", "tags": []}`。
      - 返回 JSON 回應後，停止執行後續所有任務。

    3. 提供治療建議與解決方案（如果能夠完全理解 [我的問題] 所描述的內容、語意）：
      - 你是癌症醫療專家，能夠理解和處理文字，擅長診斷和治療所有癌症，並能提供專業治療計畫與治療建議。根據以下病理報告和症狀提供專業意見，請專注於診斷、治療建議及其他相關專業意見：
        - 出生日期：%s
        - 性別：%s
        - 癌症類型：%s (%s期) %s
        - 治療藥物：%s
        - 其他病史：%s
        - 過敏反應：%s

      - 根據現有的知識生成回答，只使用繁體中文回覆。
      - 盡可能針對 [我的問題] 作回答，確保經過現有的知識查證，提供安全、可信賴的回答內容。
      - 簡短回答，開頭直接回覆不用重複問題、病歷資料、症狀等資訊。
      - 字數不超過2000字。

    4. 重要： 請將你的回覆格式化為 純文字。
        - 嚴禁使用任何 Markdown 語法。**  這包括但不限於：
          *   加粗/斜體 (例如：`**文字**`, `_文字_`)
          *   標題 (例如：`# 標題`)
          *   清單 (例如：`* 項目`)
          *   程式碼區塊 (例如：`` `程式碼` ``)
          *   引用 (例如: `> 引用文字`)
        - 確保你的回覆不包含任何會被解讀為 Markdown 的特殊字元。

    5.最後確保不提供其他註釋，並使用以下 JSON 格式：{"response": "你回覆的內容"}。
  """ % (
    input_content,
    userReport['birthday'],
    userReport['gender'],
    userReport['cancer_type'],
    userReport['cancer_period'],
    userReport['subdivide'],
    userReport['medicine'],
    userReport['disease'],
    userReport['allergy'] if userReport['allergy'] else '無',
  )
  
  # LLM輸出設定
  generate_config = {
    "max_output_tokens": 8192, # 單次輸出上限的token
    "temperature": 1, # 生成輸出隨機性 0.1 ~ 2
    "top_p": 0.95, # 生成輸出與任務需求的相符合性 0.1-0.95
    "response_mime_type": "application/json", # 回應輸出的結構? 預設markdown、這裡指定給json
    "response_schema": None, # 如果給json，json的schema格式
  }

  conversation_history = [
    { "role": "user", "content": drcell_prompt },
  ]

  # 開始生成輸出
  drcellGenerateMessage, conversation_history, tokenUsed = generate_response(drcell_prompt, generate_config, client, models, conversation_history, tools)
  
  # 移除多餘符號
  drcellGenerateMessage = clean_json_string(drcellGenerateMessage)
  # 將字串的json內容轉成json數據
  jsonGenerateMessage = json.loads(drcellGenerateMessage)

  print('\033[93m' + f'Gemini的回覆: {drcellGenerateMessage}' + '\033[0m')
  print('\033[93m' + f'Gemini的Token使用: {tokenUsed}' + '\033[0m')
  
  # API回傳結果
  return Response(drcellGenerateMessage, status=200)
  