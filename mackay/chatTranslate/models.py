from django.db import models
from django.utils import timezone

# Create your models here.

class TranslationRecord(models.Model):
    """
    翻譯記錄模型 - 用於儲存翻譯請求和結果
    """
    original_text = models.TextField(
        verbose_name="原始文字",
        help_text="需要翻譯的原始文字內容"
    )
    translated_text = models.TextField(
        verbose_name="翻譯結果",
        help_text="翻譯後的文字內容",
        blank=True,
        null=True
    )
    source_language = models.CharField(
        max_length=10,
        verbose_name="來源語言",
        help_text="原始文字的語言代碼",
        default="en"
    )
    target_language = models.CharField(
        max_length=10,
        verbose_name="目標語言", 
        help_text="翻譯目標語言代碼",
        default="zh-tw"
    )
    translation_model = models.CharField(
        max_length=50,
        verbose_name="翻譯模型",
        help_text="使用的翻譯模型名稱",
        default="gemma3:4b"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新時間"
    )
    translation_time = models.FloatField(
        verbose_name="翻譯耗時",
        help_text="翻譯處理時間(秒)",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "翻譯記錄"
        verbose_name_plural = "翻譯記錄"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"翻譯記錄 #{self.id} - {self.original_text[:50]}..."
