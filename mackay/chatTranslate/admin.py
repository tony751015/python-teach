from django.contrib import admin
from .models import TranslationRecord

# Register your models here.

@admin.register(TranslationRecord)
class TranslationRecordAdmin(admin.ModelAdmin):
    """
    翻譯記錄的 Django Admin 配置
    """
    list_display = [
        'id', 
        'original_text_preview', 
        'translated_text_preview', 
        'source_language', 
        'target_language', 
        'translation_model',
        'translation_time',
        'created_at'
    ]
    list_filter = [
        'source_language', 
        'target_language', 
        'translation_model', 
        'created_at'
    ]
    search_fields = [
        'original_text', 
        'translated_text'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at'
    ]
    ordering = ['-created_at']
    
    # 自訂顯示方法
    def original_text_preview(self, obj):
        """顯示原始文字的預覽"""
        return obj.original_text[:100] + '...' if len(obj.original_text) > 100 else obj.original_text
    original_text_preview.short_description = '原始文字預覽'
    
    def translated_text_preview(self, obj):
        """顯示翻譯文字的預覽"""
        if obj.translated_text:
            return obj.translated_text[:100] + '...' if len(obj.translated_text) > 100 else obj.translated_text
        return '無翻譯結果'
    translated_text_preview.short_description = '翻譯結果預覽'
