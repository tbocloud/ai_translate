# Migration file: ai_translate/patches/v1_0/0001_create_translation_fields.py

import frappe

def execute():
    """
    Create custom fields for translation functionality
    """
    
    # Create custom field for target language selection in Sales Invoice
    if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "custom_translation_language"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Sales Invoice",
            "label": "Translation Language",
            "fieldname": "custom_translation_language",
            "fieldtype": "Select",
            "options": "\nArabic\nSpanish\nFrench\nGerman\nItalian\nPortuguese\nRussian\nJapanese\nKorean\nChinese (Simplified)\nChinese (Traditional)\nHindi\nUrdu\nTurkish\nDutch\nSwedish\nDanish\nNorwegian\nFinnish",
            "default": "Arabic",
            "insert_after": "language",
            "description": "Select target language for item description translation"
        })
        custom_field.insert(ignore_permissions=True)
        
    # Create custom field for translated description in Sales Invoice Item
    if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice Item", "fieldname": "custom_translated_description"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Sales Invoice Item",
            "label": "Translated Description",
            "fieldname": "custom_translated_description",
            "fieldtype": "Text",
            "insert_after": "description",
            "description": "Auto-translated item description",
            "read_only": 1
        })
        custom_field.insert(ignore_permissions=True)
        
    # Create user preference fields
    if not frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "preferred_translation_provider"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "User",
            "label": "Preferred Translation Provider",
            "fieldname": "preferred_translation_provider",
            "fieldtype": "Select",
            "options": "\ngoogle_free\nmymemory\nlibretranslate",
            "default": "google_free",
            "insert_after": "language"
        })
        custom_field.insert(ignore_permissions=True)
        
    if not frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "auto_translate_descriptions"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "User",
            "label": "Auto Translate Descriptions",
            "fieldname": "auto_translate_descriptions",
            "fieldtype": "Check",
            "default": 0,
            "insert_after": "preferred_translation_provider"
        })
        custom_field.insert(ignore_permissions=True)
        
    frappe.db.commit()
    frappe.clear_cache()