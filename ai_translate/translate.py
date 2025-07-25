import frappe
import requests
import json
import logging
import os
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@frappe.whitelist()
def ai_translate_text(text, target_language="ar", source_language="en", ai_provider="groq"):
    """
    Natural AI translation with robust error handling
    """
    
    if not text or not text.strip():
        return {
            "success": False,
            "error": "No text provided for translation",
            "translated_text": "",
            "ai_provider": ai_provider
        }
    
    try:
        start_time = datetime.now()
        result = None
        
        # Clean input text
        text = text.strip()
        if len(text) > 5000:  # Limit text length
            text = text[:5000] + "..."
        
        # Try the specified provider first
        if ai_provider == "groq":
            result = translate_with_groq_natural(text, target_language, source_language)
        elif ai_provider == "openai":
            result = translate_with_openai_natural(text, target_language, source_language)
        elif ai_provider == "claude":
            result = translate_with_claude_natural(text, target_language, source_language)
        elif ai_provider == "perplexity":
            result = translate_with_perplexity_natural(text, target_language, source_language)
        elif ai_provider == "deepseek":
            result = translate_with_deepseek_natural(text, target_language, source_language)
        else:
            # Auto-select best available provider
            result = translate_with_auto_provider(text, target_language, source_language)
        
        if result and result.get('translated_text'):
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "translated_text": result['translated_text'],
                "source_language": source_language,
                "target_language": target_language,
                "ai_provider": result.get('provider', ai_provider),
                "model_used": result.get('model', 'unknown'),
                "confidence_score": result.get('confidence', 0.95),
                "processing_time": processing_time,
                "context_aware": True,
                "ai_enhanced": True
            }
        else:
            return {
                "success": False,
                "error": "AI translation failed - no result returned",
                "translated_text": "",
                "ai_provider": ai_provider
            }
            
    except Exception as e:
        logger.error(f"AI Translation error with {ai_provider}: {str(e)}")
        
        # Try fallback providers
        fallback_providers = ['groq', 'deepseek', 'openai']
        if ai_provider in fallback_providers:
            fallback_providers.remove(ai_provider)
        
        for fallback in fallback_providers:
            try:
                if has_api_key_configured(fallback):
                    logger.info(f"Trying fallback provider: {fallback}")
                    if fallback == 'groq':
                        fallback_result = translate_with_groq_natural(text, target_language, source_language)
                    elif fallback == 'deepseek':
                        fallback_result = translate_with_deepseek_natural(text, target_language, source_language)
                    elif fallback == 'openai':
                        fallback_result = translate_with_openai_natural(text, target_language, source_language)
                    
                    if fallback_result and fallback_result.get('translated_text'):
                        return {
                            "success": True,
                            "translated_text": fallback_result['translated_text'],
                            "source_language": source_language,
                            "target_language": target_language,
                            "ai_provider": f"{ai_provider} (fallback: {fallback})",
                            "model_used": fallback_result.get('model', 'unknown'),
                            "warning": f"Primary provider {ai_provider} failed, used {fallback}",
                            "ai_enhanced": True
                        }
            except Exception as fallback_error:
                logger.warning(f"Fallback provider {fallback} also failed: {str(fallback_error)}")
                continue
            
        return {
            "success": False,
            "error": f"All AI providers failed. Primary error: {str(e)}",
            "translated_text": "",
            "ai_provider": ai_provider,
            "debug_info": f"Tried providers: {[ai_provider] + fallback_providers}"
        }

def translate_with_groq_natural(text, target_lang, source_lang):
    """
    Natural translation using Groq with updated models
    """
    lang_names = get_language_names()
    target_name = lang_names.get(target_lang, target_lang)
    source_name = lang_names.get(source_lang, 'English')
    
    api_key = get_groq_api_key()
    if not api_key:
        raise Exception("Groq API key not configured")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Natural, context-aware prompt
    prompt = f"""You are a professional translator specializing in natural, fluent translations.

Translate this {source_name} text to {target_name}:
"{text}"

Requirements:
- Make it sound completely natural in {target_name}
- Preserve the original meaning and tone
- Use appropriate business terminology
- Don't add explanations or notes
- Return ONLY the translation

Translation:"""

    # Updated to use current available models
    payload = {
        "model": "llama3-70b-8192",  # Updated model name
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert translator. Translate text naturally to {target_name}, preserving meaning and business context."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
        "top_p": 0.9
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result['choices'][0]['message']['content'].strip()
        
        # Clean up the response
        translated_text = clean_translation_response(translated_text)
        
        if translated_text and len(translated_text) > 0:
            return {
                'translated_text': translated_text,
                'confidence': 0.95,
                'model': 'llama3-70b-8192',
                'provider': 'groq'
            }
        else:
            raise Exception("Groq returned empty translation")
    else:
        error_msg = f"Groq API error: HTTP {response.status_code}"
        if response.text:
            error_msg += f" - {response.text}"
        raise Exception(error_msg)

def translate_with_openai_natural(text, target_lang, source_lang):
    """
    Natural translation using OpenAI
    """
    lang_names = get_language_names()
    target_name = lang_names.get(target_lang, target_lang)
    source_name = lang_names.get(source_lang, 'English')
    
    api_key = get_openai_api_key()
    if not api_key:
        raise Exception("OpenAI API key not configured")
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Translate this {source_name} business text to natural, fluent {target_name}:

"{text}"

Make it sound native and professional. Return only the translation."""

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"You are a professional translator. Translate to natural {target_name}."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result['choices'][0]['message']['content'].strip()
        translated_text = clean_translation_response(translated_text)
        
        if translated_text:
            return {
                'translated_text': translated_text,
                'confidence': 0.96,
                'model': 'gpt-3.5-turbo',
                'provider': 'openai'
            }
        else:
            raise Exception("OpenAI returned empty translation")
    else:
        raise Exception(f"OpenAI API error: HTTP {response.status_code}")

def translate_with_claude_natural(text, target_lang, source_lang):
    """
    Natural translation using Claude
    """
    lang_names = get_language_names()
    target_name = lang_names.get(target_lang, target_lang)
    
    api_key = get_claude_api_key()
    if not api_key:
        raise Exception("Claude API key not configured")
    
    url = "https://api.anthropic.com/v1/messages"
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    prompt = f"""Translate to natural {target_name}:

"{text}"

Make it sound fluent and professional. Return only the translation."""

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result['content'][0]['text'].strip()
        translated_text = clean_translation_response(translated_text)
        
        if translated_text:
            return {
                'translated_text': translated_text,
                'confidence': 0.97,
                'model': 'claude-3-haiku',
                'provider': 'claude'
            }
        else:
            raise Exception("Claude returned empty translation")
    else:
        raise Exception(f"Claude API error: HTTP {response.status_code}")

def translate_with_deepseek_natural(text, target_lang, source_lang):
    """
    Natural translation using DeepSeek
    """
    lang_names = get_language_names()
    target_name = lang_names.get(target_lang, target_lang)
    
    api_key = get_deepseek_api_key()
    if not api_key:
        raise Exception("DeepSeek API key not configured")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Translate to natural {target_name}:

"{text}"

Make it sound fluent and professional."""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result['choices'][0]['message']['content'].strip()
        translated_text = clean_translation_response(translated_text)
        
        if translated_text:
            return {
                'translated_text': translated_text,
                'confidence': 0.90,
                'model': 'deepseek-chat',
                'provider': 'deepseek'
            }
        else:
            raise Exception("DeepSeek returned empty translation")
    else:
        raise Exception(f"DeepSeek API error: HTTP {response.status_code}")

def translate_with_perplexity_natural(text, target_lang, source_lang):
    """
    Natural translation using Perplexity
    """
    lang_names = get_language_names()
    target_name = lang_names.get(target_lang, target_lang)
    
    api_key = get_perplexity_api_key()
    if not api_key:
        raise Exception("Perplexity API key not configured")
    
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Translate to natural {target_name}:

"{text}"

Make it sound fluent and professional."""

    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result['choices'][0]['message']['content'].strip()
        translated_text = clean_translation_response(translated_text)
        
        if translated_text:
            return {
                'translated_text': translated_text,
                'confidence': 0.92,
                'model': 'llama-3.1-sonar-large',
                'provider': 'perplexity'
            }
        else:
            raise Exception("Perplexity returned empty translation")
    else:
        raise Exception(f"Perplexity API error: HTTP {response.status_code}")

def translate_with_auto_provider(text, target_lang, source_lang):
    """
    Try providers in order of preference
    """
    providers = [
        ('groq', translate_with_groq_natural),
        ('deepseek', translate_with_deepseek_natural),
        ('openai', translate_with_openai_natural),
        ('claude', translate_with_claude_natural),
        ('perplexity', translate_with_perplexity_natural)
    ]
    
    for provider_name, translate_func in providers:
        if has_api_key_configured(provider_name):
            try:
                result = translate_func(text, target_lang, source_lang)
                if result and result.get('translated_text'):
                    return result
            except Exception as e:
                logger.warning(f"Provider {provider_name} failed: {str(e)}")
                continue
    
    raise Exception("All available AI providers failed")

def clean_translation_response(text):
    """
    Clean up AI translation responses to get natural text
    """
    if not text:
        return ""
    
    text = text.strip()
    
    # Remove common AI response patterns
    patterns_to_remove = [
        r'^translation:\s*',
        r'^here is the translation:\s*',
        r'^the translation is:\s*',
        r'^translated text:\s*',
        r'^result:\s*',
        r'^output:\s*',
        r'^answer:\s*',
        r'^\w+:\s*',  # Remove "Arabic:" or similar prefixes
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove quotes if the entire text is wrapped
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1]
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_language_names():
    """
    Get full language names for better AI prompting
    """
    return {
        "ar": "Arabic",
        "es": "Spanish", 
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "zh-tw": "Traditional Chinese",
        "hi": "Hindi",
        "ur": "Urdu",
        "tr": "Turkish",
        "nl": "Dutch",
        "sv": "Swedish",
        "da": "Danish",
        "no": "Norwegian",
        "fi": "Finnish",
        "en": "English"
    }

# API Key management functions
def get_openai_api_key():
    return frappe.conf.get('openai_api_key') or os.getenv('OPENAI_API_KEY', '')

def get_claude_api_key():
    return frappe.conf.get('claude_api_key') or os.getenv('CLAUDE_API_KEY', '')

def get_groq_api_key():
    return frappe.conf.get('groq_api_key') or os.getenv('GROQ_API_KEY', '')

def get_perplexity_api_key():
    return frappe.conf.get('perplexity_api_key') or os.getenv('PERPLEXITY_API_KEY', '')

def get_deepseek_api_key():
    return frappe.conf.get('deepseek_api_key') or os.getenv('DEEPSEEK_API_KEY', '')

def has_api_key_configured(provider):
    key_getters = {
        'openai': get_openai_api_key,
        'claude': get_claude_api_key,
        'groq': get_groq_api_key,
        'perplexity': get_perplexity_api_key,
        'deepseek': get_deepseek_api_key
    }
    
    getter = key_getters.get(provider)
    if getter:
        key = getter()
        return bool(key and len(key.strip()) > 0)
    return False

@frappe.whitelist()
def test_ai_translation():
    """
    Test AI translation with detailed debugging
    """
    test_text = "High-quality professional business solution"
    target_lang = "ar"
    
    # Test all configured providers
    providers = ['groq', 'openai', 'claude', 'deepseek', 'perplexity']
    results = {}
    
    for provider in providers:
        if has_api_key_configured(provider):
            try:
                result = ai_translate_text(test_text, target_lang, "en", provider)
                results[provider] = result
            except Exception as e:
                results[provider] = {
                    "success": False,
                    "error": str(e),
                    "ai_provider": provider
                }
        else:
            results[provider] = {
                "success": False,
                "error": "API key not configured",
                "ai_provider": provider
            }
    
    return {
        "test_text": test_text,
        "target_language": target_lang,
        "results": results,
        "configured_providers": [p for p in providers if has_api_key_configured(p)]
    }

@frappe.whitelist()
def test_ai_providers():
    """
    Test all AI providers with a sample translation
    """
    test_text = "High-quality professional business solution"
    target_lang = "ar"
    
    # Test all providers
    providers = ['groq', 'openai', 'claude', 'deepseek', 'perplexity']
    results = {}
    
    for provider in providers:
        if has_api_key_configured(provider):
            try:
                start_time = datetime.now()
                result = ai_translate_text(test_text, target_lang, "en", provider)
                processing_time = (datetime.now() - start_time).total_seconds()
                
                if result.get('success'):
                    results[provider] = {
                        "status": "success",
                        "translated_text": result.get('translated_text', ''),
                        "model": result.get('model_used', 'unknown'),
                        "processing_time": processing_time,
                        "confidence": result.get('confidence_score', 0)
                    }
                else:
                    results[provider] = {
                        "status": "failed",
                        "error": result.get('error', 'Unknown error'),
                        "translated_text": "",
                        "processing_time": processing_time
                    }
                    
            except Exception as e:
                results[provider] = {
                    "status": "failed",
                    "error": str(e),
                    "translated_text": "",
                    "processing_time": 0
                }
        else:
            results[provider] = {
                "status": "not_configured",
                "error": "API key not configured",
                "translated_text": "",
                "processing_time": 0
            }
    
    return results

@frappe.whitelist()
def get_ai_setup_guide():
    """
    Get setup instructions for AI providers
    """
    return {
        'groq': {
            'name': 'Groq (Recommended - Fast & Free)',
            'free_tier': 'Yes - 6,000 requests/minute',
            'signup_url': 'https://console.groq.com',
            'api_key_url': 'https://console.groq.com/keys',
            'config_key': 'groq_api_key',
            'model': 'llama3-70b-8192',
            'speed': 'Ultra Fast',
            'quality': 'Very Good'
        },
        'openai': {
            'name': 'OpenAI GPT-3.5',
            'free_tier': 'No - $0.002/1K tokens',
            'signup_url': 'https://platform.openai.com/signup',
            'api_key_url': 'https://platform.openai.com/api-keys',
            'config_key': 'openai_api_key',
            'model': 'gpt-3.5-turbo',
            'speed': 'Fast',
            'quality': 'Excellent'
        },
        'claude': {
            'name': 'Anthropic Claude',
            'free_tier': 'Limited free tier',
            'signup_url': 'https://console.anthropic.com',
            'api_key_url': 'https://console.anthropic.com/settings/keys',
            'config_key': 'claude_api_key',
            'model': 'claude-3-haiku',
            'speed': 'Fast',
            'quality': 'Excellent'
        },
        'deepseek': {
            'name': 'DeepSeek',
            'free_tier': 'Yes - Good free tier',
            'signup_url': 'https://platform.deepseek.com',
            'api_key_url': 'https://platform.deepseek.com/api_keys',
            'config_key': 'deepseek_api_key',
            'model': 'deepseek-chat',
            'speed': 'Fast',
            'quality': 'Good'
        },
        'perplexity': {
            'name': 'Perplexity AI',
            'free_tier': 'Limited free tier',
            'signup_url': 'https://www.perplexity.ai',
            'api_key_url': 'https://www.perplexity.ai/settings/api',
            'config_key': 'perplexity_api_key',
            'model': 'llama-3.1-sonar-large',
            'speed': 'Fast',
            'quality': 'Very Good'
        }
    }

@frappe.whitelist()
def get_available_ai_providers():
    """
    Get list of available AI providers with their status
    """
    providers = {
        'groq': {
            'name': 'Groq (Llama3)',
            'configured': has_api_key_configured('groq'),
            'speed': 'Ultra Fast',
            'quality': 'Very Good',
            'cost': 'Free'
        },
        'openai': {
            'name': 'OpenAI (GPT-3.5)',
            'configured': has_api_key_configured('openai'),
            'speed': 'Fast',
            'quality': 'Excellent',
            'cost': 'Low'
        },
        'claude': {
            'name': 'Claude (Haiku)',
            'configured': has_api_key_configured('claude'),
            'speed': 'Fast',
            'quality': 'Excellent',
            'cost': 'Low'
        },
        'deepseek': {
            'name': 'DeepSeek',
            'configured': has_api_key_configured('deepseek'),
            'speed': 'Fast',
            'quality': 'Good',
            'cost': 'Very Low'
        },
        'perplexity': {
            'name': 'Perplexity AI',
            'configured': has_api_key_configured('perplexity'),
            'speed': 'Fast',
            'quality': 'Very Good',
            'cost': 'Low'
        }
    }
    
    return providers

@frappe.whitelist()
def bulk_ai_translate_items(items_data, target_language="ar", ai_provider="groq"):
    """
    Robust bulk translation with better error handling
    """
    
    if isinstance(items_data, str):
        items_data = json.loads(items_data)
    
    if not has_api_key_configured(ai_provider):
        return {
            'results': [],
            'summary': {
                'total_items': len(items_data),
                'successful_translations': 0,
                'failed_translations': len(items_data),
                'error': f'AI provider {ai_provider} is not configured'
            }
        }
    
    results = []
    successful_translations = 0
    failed_translations = 0
    total_processing_time = 0
    
    for item in items_data:
        try:
            item_code = item.get('item_code', '')
            description = item.get('description', '')
            
            if not description or not description.strip():
                results.append({
                    'item_code': item_code,
                    'success': False,
                    'error': 'No description to translate',
                    'translated_text': '',
                    'ai_enhanced': False
                })
                failed_translations += 1
                continue
            
            translation_result = ai_translate_text(
                description.strip(), 
                target_language, 
                "en", 
                ai_provider
            )
            
            results.append({
                'item_code': item_code,
                'success': translation_result['success'],
                'translated_text': translation_result.get('translated_text', ''),
                'error': translation_result.get('error', ''),
                'ai_enhanced': translation_result.get('ai_enhanced', False),
                'processing_time': translation_result.get('processing_time', 0),
                'confidence_score': translation_result.get('confidence_score', 0),
                'model_used': translation_result.get('model_used', ''),
                'ai_provider': translation_result.get('ai_provider', ai_provider)
            })
            
            if translation_result['success']:
                successful_translations += 1
                total_processing_time += translation_result.get('processing_time', 0)
            else:
                failed_translations += 1
                
        except Exception as e:
            results.append({
                'item_code': item.get('item_code', ''),
                'success': False,
                'error': f"Translation error: {str(e)}",
                'translated_text': '',
                'ai_enhanced': False
            })
            failed_translations += 1
    
    return {
        'results': results,
        'summary': {
            'total_items': len(items_data),
            'successful_translations': successful_translations,
            'failed_translations': failed_translations,
            'ai_enhanced_count': successful_translations,
            'average_processing_time': total_processing_time / max(successful_translations, 1),
            'ai_provider': ai_provider,
            'total_processing_time': total_processing_time
        }
    }

# Backward compatibility
@frappe.whitelist()
def translate_text(text, target_language="ar", source_language="en", api_provider="groq"):
    return ai_translate_text(text, target_language, source_language, api_provider)

@frappe.whitelist()
def bulk_translate_items(items_data, target_language="ar", api_provider="groq"):
    return bulk_ai_translate_items(items_data, target_language, api_provider)

@frappe.whitelist()
def create_translation_custom_fields():
    """Create custom fields for AI translation functionality"""
    try:
        if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_translation_language"}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Sales Invoice",
                "label": "Translation Language",
                "fieldname": "custom_translation_language",
                "fieldtype": "Select",
                "options": "\nArabic\nSpanish\nFrench\nGerman\nItalian\nPortuguese\nRussian\nJapanese\nKorean\nChinese (Simplified)\nChinese (Traditional)\nHindi\nUrdu\nTurkish\nDutch\nSwedish\nDanish\nNorwegian\nFinnish",
                "default": "Arabic",
                "insert_after": "language"
            })
            custom_field.insert(ignore_permissions=True)
        
        if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice Item", "fieldname": "custom_translated_description"}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Sales Invoice Item",
                "label": "AI Translated Description",
                "fieldname": "custom_translated_description",
                "fieldtype": "Text",
                "insert_after": "description",
                "read_only": 1
            })
            custom_field.insert(ignore_permissions=True)
        
        if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_ai_provider"}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Sales Invoice",
                "label": "AI Provider",
                "fieldname": "custom_ai_provider",
                "fieldtype": "Select",
                "options": "\ngroq\nopenai\nclaude\nperplexity\ndeepseek",
                "default": "groq",
                "insert_after": "custom_translation_language"
            })
            custom_field.insert(ignore_permissions=True)
            
        frappe.db.commit()
        frappe.clear_cache()
        
        return {"success": True, "message": "Custom fields created successfully"}
        
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "error": str(e)}

# Additional utility functions
def validate_translation_fields(doc, method):
    """
    Validate translation fields on Sales Invoice
    """
    pass  # Add validation logic if needed

def on_sales_invoice_update(doc, method):
    """
    Handle Sales Invoice updates for translation tracking
    """
    pass  # Add update logic if needed

@frappe.whitelist()
def get_translation_stats():
    """
    Get translation statistics for dashboard
    """
    try:
        # Count total translations
        total_translations = frappe.db.count('Sales Invoice Item', 
            filters={'custom_translated_description': ['!=', '']})
        
        # Count by provider (simplified)
        provider_stats = {
            'groq': 0,
            'openai': 0, 
            'claude': 0,
            'deepseek': 0,
            'perplexity': 0
        }
        
        # Get recent translation activity
        recent_activity = frappe.db.sql("""
            SELECT DATE(modified) as date, COUNT(*) as count
            FROM `tabSales Invoice Item`
            WHERE custom_translated_description IS NOT NULL
            AND custom_translated_description != ''
            AND modified >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY DATE(modified)
            ORDER BY date DESC
            LIMIT 30
        """, as_dict=True)
        
        return {
            'total_translations': total_translations,
            'provider_stats': provider_stats,
            'recent_activity': recent_activity,
            'configured_providers': [p for p in ['groq', 'openai', 'claude', 'deepseek', 'perplexity'] 
                                   if has_api_key_configured(p)]
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'total_translations': 0,
            'provider_stats': {},
            'recent_activity': [],
            'configured_providers': []
        }

@frappe.whitelist()
def validate_api_key(provider, api_key):
    """
    Validate an API key for a specific provider
    """
    try:
        test_text = "Hello world"
        
        if provider == 'groq':
            result = test_groq_key(api_key, test_text)
        elif provider == 'openai':
            result = test_openai_key(api_key, test_text)
        elif provider == 'claude':
            result = test_claude_key(api_key, test_text)
        elif provider == 'deepseek':
            result = test_deepseek_key(api_key, test_text)
        elif provider == 'perplexity':
            result = test_perplexity_key(api_key, test_text)
        else:
            return {'valid': False, 'error': 'Unknown provider'}
            
        return {'valid': True, 'test_result': result}
        
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def test_groq_key(api_key, text):
    """Test Groq API key with updated model"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",  # Updated model
        "messages": [{"role": "user", "content": f"Translate to Arabic: {text}"}],
        "max_tokens": 50
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.status_code == 200

def test_openai_key(api_key, text):
    """Test OpenAI API key"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Translate to Arabic: {text}"}],
        "max_tokens": 50
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.status_code == 200

def test_claude_key(api_key, text):
    """Test Claude API key"""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 50,
        "messages": [{"role": "user", "content": f"Translate to Arabic: {text}"}]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.status_code == 200

def test_deepseek_key(api_key, text):
    """Test DeepSeek API key"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"Translate to Arabic: {text}"}],
        "max_tokens": 50
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.status_code == 200

def test_perplexity_key(api_key, text):
    """Test Perplexity API key"""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [{"role": "user", "content": f"Translate to Arabic: {text}"}],
        "max_tokens": 50
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.status_code == 200

@frappe.whitelist()
def clear_all_translations():
    """
    Clear all translations (for testing purposes)
    """
    try:
        frappe.db.sql("""
            UPDATE `tabSales Invoice Item` 
            SET custom_translated_description = NULL 
            WHERE custom_translated_description IS NOT NULL
        """)
        frappe.db.commit()
        return {'success': True, 'message': 'All translations cleared'}
    except Exception as e:
        frappe.db.rollback()
        return {'success': False, 'error': str(e)}

@frappe.whitelist()
def export_translations():
    """
    Export all translations for backup/analysis
    """
    try:
        translations = frappe.db.sql("""
            SELECT 
                sii.parent as invoice_name,
                sii.item_code,
                sii.description as original_text,
                sii.custom_translated_description as translated_text,
                si.custom_translation_language as target_language,
                si.custom_ai_provider as ai_provider,
                sii.modified
            FROM `tabSales Invoice Item` sii
            JOIN `tabSales Invoice` si ON sii.parent = si.name
            WHERE sii.custom_translated_description IS NOT NULL
            AND sii.custom_translated_description != ''
            ORDER BY sii.modified DESC
        """, as_dict=True)
        
        return {
            'success': True,
            'data': translations,
            'count': len(translations)
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Scheduled tasks (referenced in hooks.py)
def cleanup_translation_logs():
    """
    Clean up old translation logs (if you implement logging)
    """
    try:
        # Clean up logs older than 30 days
        thirty_days_ago = frappe.utils.add_days(frappe.utils.nowdate(), -30)
        
        # If you implement a Translation Log doctype, clean it up here
        # frappe.db.delete('Translation Log', {'creation': ['<', thirty_days_ago]})
        
        logger.info("Translation logs cleanup completed")
        
    except Exception as e:
        logger.error(f"Translation logs cleanup failed: {str(e)}")

@frappe.whitelist()
def get_supported_languages():
    """
    Get list of supported languages with their codes
    """
    lang_names = get_language_names()
    return [
        {
            'code': code,
            'name': name,
            'native_name': get_native_language_name(code)
        }
        for code, name in lang_names.items()
    ]

def get_native_language_name(code):
    """
    Get native language names for better UX
    """
    native_names = {
        'ar': 'العربية',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch',
        'it': 'Italiano',
        'pt': 'Português',
        'ru': 'Русский',
        'ja': '日本語',
        'ko': '한국어',
        'zh': '中文',
        'zh-tw': '中文(繁體)',
        'hi': 'हिन्दी',
        'ur': 'اردو',
        'tr': 'Türkçe',
        'nl': 'Nederlands',
        'sv': 'Svenska',
        'da': 'Dansk',
        'no': 'Norsk',
        'fi': 'Suomi',
        'en': 'English'
    }
    return native_names.get(code, code)