# AI Translation System for ERPNext
## Complete Documentation

![AI Translation Banner](https://img.shields.io/badge/AI%20Translation-ERPNext-blue?style=for-the-badge&logo=artificial-intelligence)

### 📚 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)
9. [Performance & Costs](#performance--costs)
10. [Contributing](#contributing)

---

## 🌟 Overview

The **AI Translation System** is a powerful ERPNext app that provides automatic translation of Sales Invoice item descriptions using multiple AI providers. It seamlessly integrates with your ERPNext workflow to deliver natural, context-aware translations in 19+ languages.

### 🎯 Key Benefits
- **Multi-Provider Support**: 5 AI providers with automatic fallback
- **Bulk Translation**: Translate hundreds of items in seconds
- **Natural Quality**: Business-focused, context-aware translations
- **Cost-Effective**: Free options available (Groq)
- **Zero Configuration**: Works out-of-the-box with API keys

---

## ✨ Features

### 🤖 AI Providers
| Provider | Model | Speed | Quality | Cost | Free Tier |
|----------|-------|-------|---------|------|-----------|
| **Groq** ⭐ | Llama 3 70B | Ultra Fast | Very Good | Free | 6,000 req/min |
| **OpenAI** | GPT-3.5 Turbo | Fast | Excellent | Low | No |
| **Claude** | Haiku | Fast | Excellent | Low | Limited |
| **DeepSeek** | DeepSeek Chat | Fast | Good | Very Low | Yes |
| **Perplexity** | Llama 3.1 Sonar | Fast | Very Good | Low | Limited |

### 🌍 Supported Languages
- **Arabic** (ar) - العربية
- **Spanish** (es) - Español  
- **French** (fr) - Français
- **German** (de) - Deutsch
- **Italian** (it) - Italiano
- **Portuguese** (pt) - Português
- **Russian** (ru) - Русский
- **Japanese** (ja) - 日本語
- **Korean** (ko) - 한국어
- **Chinese Simplified** (zh) - 中文
- **Chinese Traditional** (zh-tw) - 中文(繁體)
- **Hindi** (hi) - हिन्दी
- **Urdu** (ur) - اردو
- **Turkish** (tr) - Türkçe
- **Dutch** (nl) - Nederlands
- **Swedish** (sv) - Svenska
- **Danish** (da) - Dansk
- **Norwegian** (no) - Norsk
- **Finnish** (fi) - Suomi

### 🛠️ Core Features
- ✅ **Smart AI Translate** - Advanced translation with options
- ⚡ **Quick AI Translate** - One-click bulk translation
- 🔬 **Provider Testing** - Real-time provider validation
- 📊 **Translation Statistics** - Usage analytics
- 🧹 **Clear Translations** - Reset translated content
- ⚙️ **Setup Guide** - Step-by-step configuration
- 🔄 **Auto-Fallback** - Automatic provider switching on failure

---

## 📦 Installation

### Prerequisites
- ERPNext v15 or Frappe v15
- Python 3.8+
- Internet connection for AI APIs

### Step 1: Install the App

```bash
# Navigate to your Frappe bench
cd /path/to/frappe-bench

# Option A: Install from repository (if published)
bench get-app [https://github.com/your-repo/ai_translate.git](https://github.com/tbocloud/ai_translate.git)

# Install to your site
bench --site your-site-name install-app ai_translate
```

### Step 2: File Structure

Create the following files in your app:

```
ai_translate/
├── ai_translate/
│   ├── __init__.py
│   ├── hooks.py                    # App configuration
│   ├── translate.py                # Backend translation logic
│   └── public/
│       └── js/
│           └── translate.js        # Frontend interface
├── ai_translate/
│   └── fixtures/
│       └── sales_invoice_item.json # Custom field definition
├── setup.py
└── README.md
```

### Step 3: Copy Code Files

Copy the provided code into these files:

1. **Backend** (`ai_translate/translate.py`): [Full Python Code](#python-backend)
2. **Frontend** (`ai_translate/public/js/translate.js`): [Full JavaScript Code](#javascript-frontend)
3. **Configuration** (`ai_translate/hooks.py`): [Hooks Configuration](#hooks-configuration)
4. **Custom Fields** (`sales_invoice_item.json`): [Field Definition](#custom-fields)

---

## ⚙️ Configuration

### Step 1: API Keys Setup

Choose and configure one or more AI providers by adding their API keys to your `site_config.json`:

```json
{
  "groq_api_key": "gsk_your_groq_api_key_here",
  "openai_api_key": "sk-your_openai_api_key_here",
  "claude_api_key": "sk-ant-your_claude_api_key_here",
  "deepseek_api_key": "sk-your_deepseek_api_key_here",
  "perplexity_api_key": "pplx-your_perplexity_api_key_here"
}
```

### Step 2: Get API Keys

#### 🏆 Recommended: Groq (Free & Fast)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with your email
3. Navigate to [API Keys](https://console.groq.com/keys)
4. Create a new key
5. Copy the key (starts with `gsk_`)

#### Other Providers
| Provider | Sign Up | API Keys | Key Format |
|----------|---------|----------|------------|
| **OpenAI** | [platform.openai.com](https://platform.openai.com) | [API Keys](https://platform.openai.com/api-keys) | `sk-proj-...` |
| **Claude** | [console.anthropic.com](https://console.anthropic.com) | [Settings](https://console.anthropic.com/settings/keys) | `sk-ant-...` |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com) | [API Keys](https://platform.deepseek.com/api_keys) | `sk-...` |
| **Perplexity** | [perplexity.ai](https://www.perplexity.ai) | [Settings](https://www.perplexity.ai/settings/api) | `pplx-...` |

### Step 3: Restart Your Site

```bash
bench --site your-site-name restart
bench --site your-site-name clear-cache
```

### Step 4: Create Custom Fields

Open any Sales Invoice and click **"Setup AI Translation"** if custom fields don't exist, or run:

```bash
bench --site your-site-name console
```

```python
from ai_translate.translate import create_translation_custom_fields
create_translation_custom_fields()
```

---

## 🚀 Usage

### Quick Start

1. **Open a Sales Invoice** with items that have descriptions
2. **Set Translation Settings**:
   - **Translation Language**: Choose target language (e.g., Arabic)
   - **AI Provider**: Select your preferred provider (e.g., groq)
3. **Click "⚡ Quick AI Translate"** to translate all items instantly

### Detailed Workflow

#### 1. Smart AI Translation
For advanced control:

1. Click **"🧠 Smart AI Translate"**
2. Configure options:
   - **AI Provider**: Choose specific provider
   - **Target Language**: Select language
   - **Overwrite Existing**: Replace existing translations
   - **Skip Empty Descriptions**: Ignore items without descriptions
3. Click **"Start AI Translation"**

#### 2. Provider Testing
Before translating:

1. Click **"🔬 Test AI Providers"**
2. Review test results:
   - ✅ **Working**: Provider is configured and functional
   - ⚙️ **Not Configured**: API key not set
   - ❌ **Failed**: Provider error (check API key)

#### 3. Translation Management
- **View Stats**: Click **"📊 Translation Stats"** for usage analytics
- **Clear All**: Click **"🧹 Clear All Translations"** to reset
- **Setup Guide**: Click **"⚙️ AI Setup Guide"** for configuration help

### Translation Results

After translation, you'll see:
- **Success Rate**: Percentage of successful translations
- **Processing Time**: Average time per translation
- **Cost Estimate**: Approximate API costs
- **Provider Used**: Which AI service was used

---

## 🔧 API Reference

### Core Functions

#### `ai_translate_text(text, target_language, source_language, ai_provider)`
Translate a single text string.

**Parameters:**
- `text` (str): Text to translate
- `target_language` (str): Target language code (e.g., 'ar')
- `source_language` (str): Source language code (default: 'en')
- `ai_provider` (str): AI provider ('groq', 'openai', 'claude', etc.)

**Returns:**
```python
{
    "success": True,
    "translated_text": "النص المترجم",
    "ai_provider": "groq",
    "model_used": "llama3-70b-8192",
    "processing_time": 1.2,
    "confidence_score": 0.95
}
```

#### `bulk_ai_translate_items(items_data, target_language, ai_provider)`
Translate multiple items in bulk.

**Parameters:**
- `items_data` (list): List of items with `item_code` and `description`
- `target_language` (str): Target language code
- `ai_provider` (str): AI provider

**Returns:**
```python
{
    "results": [...],
    "summary": {
        "total_items": 10,
        "successful_translations": 9,
        "failed_translations": 1,
        "average_processing_time": 1.5
    }
}
```

#### `test_ai_providers()`
Test all configured AI providers.

**Returns:**
```python
{
    "groq": {
        "status": "success",
        "translated_text": "مرحبا بالعالم",
        "processing_time": 0.8
    },
    "openai": {
        "status": "not_configured",
        "error": "API key not configured"
    }
}
```

### Utility Functions

#### `get_available_ai_providers()`
Get list of available providers and their configuration status.

#### `get_translation_stats()`
Get translation usage statistics.

#### `create_translation_custom_fields()`
Create required custom fields for translation functionality.

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No AI Providers Configured"
**Problem**: No API keys are set up.

**Solution:**
```bash
# Check current configuration
bench --site your-site-name console
```

```python
import frappe
print("Groq key:", bool(frappe.conf.get('groq_api_key')))
print("OpenAI key:", bool(frappe.conf.get('openai_api_key')))
```

Add keys to `site_config.json` and restart.

#### 2. "Invalid API Key" or HTTP 401 Errors
**Problem**: API key is incorrect or expired.

**Solution:**
1. Verify the key format matches the provider
2. Check if the key is active in the provider's dashboard
3. Regenerate the API key if needed

#### 3. "AI Translation Buttons Not Showing"
**Problem**: JavaScript not loading or custom fields missing.

**Solution:**
```javascript
// In browser console
test_ai_buttons()

// Check if functions exist
console.log(typeof force_show_ai_buttons)
```

If functions are missing, clear cache:
```bash
bench --site your-site-name clear-cache
```

#### 4. "Custom Fields Not Found"
**Problem**: Translation fields haven't been created.

**Solution:**
Click **"🔧 Setup AI Translation"** or run manually:
```python
from ai_translate.translate import create_translation_custom_fields
create_translation_custom_fields()
```

#### 5. "Translation Failed" Errors
**Problem**: Provider-specific issues.

**Diagnostic Steps:**
```python
# Test specific provider
from ai_translate.translate import ai_translate_text
result = ai_translate_text("test", "ar", "en", "groq")
print(result)
```

### Debug Commands

#### Python Console (Frappe)
```python
# Full diagnostic
from ai_translate.translate import *

# Check configuration
providers = ['groq', 'openai', 'claude', 'deepseek']
for p in providers:
    print(f"{p}: {has_api_key_configured(p)}")

# Test translation
result = ai_translate_text("Hello world", "ar", "en", "groq")
print(result)
```

#### Browser Console
```javascript
// Check if loaded
console.log('AI functions:', typeof test_ai_buttons)

// Force show buttons
test_ai_buttons()

// Test provider
frappe.call({
    method: 'ai_translate.translate.test_ai_providers',
    callback: r => console.log(r.message)
});
```

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `HTTP 401` | Invalid API key | Check/regenerate API key |
| `HTTP 429` | Rate limit exceeded | Wait or upgrade plan |
| `HTTP 500` | Server error | Check provider status |
| `Timeout` | Request timed out | Check internet connection |
| `Empty translation` | No text returned | Try different provider |

---

## 🔧 Advanced Configuration

### Custom Language Support

Add new languages by modifying the `get_language_names()` function:

```python
def get_language_names():
    return {
        "ar": "Arabic",
        "es": "Spanish",
        "your_code": "Your Language",
        # Add more languages here
    }
```

### Environment Variables

Alternative to `site_config.json`:

```bash
export GROQ_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
```

### Custom Field Configuration

Modify field properties in `create_translation_custom_fields()`:

```python
{
    "doctype": "Custom Field",
    "dt": "Sales Invoice Item",
    "fieldname": "custom_translated_description",
    "fieldtype": "Text Editor",  # or "Text", "Long Text"
    "read_only": 0,  # Set to 1 for read-only
    # Add more properties
}
```

### Provider Priorities

Modify provider order in `translate_with_auto_provider()`:

```python
providers = [
    ('your_preferred_provider', translate_with_provider_function),
    ('groq', translate_with_groq_natural),
    # Reorder as needed
]
```

### Rate Limiting

Add delays between requests in bulk operations:

```javascript
// In translate_multiple function
setTimeout(function() {
    // translation code
}, index * 2000); // 2 second delay
```

---

## 📊 Performance & Costs

### Performance Metrics

| Provider | Avg Speed | Concurrent Requests | Rate Limit |
|----------|-----------|-------------------|------------|
| **Groq** | 0.5-1.0s | High | 6,000/min |
| **OpenAI** | 1.0-2.0s | Medium | 3,500/min |
| **Claude** | 1.0-2.0s | Medium | 1,000/min |
| **DeepSeek** | 1.5-2.5s | Medium | 300/min |
| **Perplexity** | 1.0-2.0s | Medium | 200/min |

### Cost Analysis

#### Free Options
- **Groq**: Completely free, 6,000 requests/minute
- **DeepSeek**: Good free tier, 300 requests/minute

#### Paid Options (per 1K tokens)
- **OpenAI GPT-3.5**: ~$0.002
- **Claude Haiku**: ~$0.0025
- **Perplexity**: ~$0.001

#### Cost Estimation
- **100 items**: ~$0.10-0.25
- **1,000 items**: ~$1.00-2.50
- **10,000 items**: ~$10.00-25.00

### Optimization Tips

1. **Use Groq for bulk operations** (free and fast)
2. **Use premium providers for important documents**
3. **Batch translations during off-peak hours**
4. **Cache translations to avoid re-processing**
5. **Set up rate limiting for large batches**

---

## 📁 Code Reference

### Python Backend
```python
# ai_translate/translate.py
import frappe
import requests
import json
import logging
import os
from datetime import datetime
import re

# [Full code from translate.py artifact]
```

### JavaScript Frontend
```javascript
// ai_translate/public/js/translate.js
console.log('AI Translation JavaScript loaded successfully');

// [Full code from translate.js artifact]
```

### Hooks Configuration
```python
# ai_translate/hooks.py
app_name = "ai_translate"
app_title = "AI Translate"
app_publisher = "Your Name"
app_description = "AI-powered translation system for ERPNext"

# [Full code from hooks.py artifact]
```

### Custom Fields
```json
{
  "custom_fields": [
    {
      "dt": "Sales Invoice Item",
      "fieldname": "custom_translated_description",
      "fieldtype": "Text Editor",
      "label": "AI Translated Description",
      "insert_after": "description"
    }
  ]
}
```

---

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Clone your fork**
3. **Install in development mode**
4. **Make changes**
5. **Test thoroughly**
6. **Submit pull request**

### Code Standards

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features
- **Documentation**: Update docs for new features
- **Testing**: Add tests for new functionality

### Reporting Issues

Include:
- ERPNext version
- Python version
- Error messages
- Steps to reproduce
- Browser console logs

---

## 📄 License

MIT License - feel free to use in commercial projects.

---

## 🙏 Acknowledgments

- **ERPNext Community** for the amazing framework
- **AI Providers** for their excellent APIs
- **Contributors** who help improve this project

---

## 🔗 Links

- **ERPNext**: [erpnext.com](https://erpnext.com)
- **Frappe Framework**: [frappeframework.com](https://frappeframework.com)
- **Support**: Create an issue on GitHub

---

**Made with ❤️ for the ERPNext community**

*Last updated: July 2025*
