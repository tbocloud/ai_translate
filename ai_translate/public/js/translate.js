// AI Translation System - No Grid Buttons Version
console.log('AI Translation JavaScript loaded successfully - No Grid Buttons');

// Force execution when form loads
$(document).ready(function() {
    console.log('Document ready - checking for Sales Invoice form');
    
    // Wait for form to be fully loaded
    setTimeout(function() {
        if (cur_frm && cur_frm.doctype === 'Sales Invoice') {
            console.log('Sales Invoice form detected - adding AI buttons');
            add_ai_buttons_force(cur_frm);
            // Removed grid buttons - add_grid_buttons_force(cur_frm);
        }
    }, 1000);
});

frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
        console.log('Sales Invoice onload triggered');
        setTimeout(function() {
            add_ai_buttons_force(frm);
            // Removed grid buttons - add_grid_buttons_force(frm);
        }, 500);
    },
    
    refresh: function(frm) {
        console.log('Sales Invoice refresh triggered');
        add_ai_buttons_force(frm);
        // Removed grid buttons - add_grid_buttons_force(frm);
        
        // Set default values
        if (frm.fields_dict.custom_translation_language && !frm.doc.custom_translation_language) {
            frm.set_value('custom_translation_language', 'Arabic');
        }
        if (frm.fields_dict.custom_ai_provider && !frm.doc.custom_ai_provider) {
            frm.set_value('custom_ai_provider', 'groq');
        }
    },
    
    custom_ai_provider: function(frm) {
        if (frm.doc.custom_ai_provider) {
            frm.save();
        }
    },
    
    custom_translation_language: function(frm) {
        if (frm.doc.custom_translation_language) {
            frm.save();
        }
    }
});

function add_ai_buttons_force(frm) {
    console.log('Adding AI buttons to form');
    
    try {
        // Remove existing buttons first to avoid duplicates
        frm.remove_custom_button('AI Translation');
        
        if (!frm.fields_dict.custom_translation_language) {
            console.log('Custom fields not found - adding setup button');
            frm.add_custom_button('Setup AI Translation', function() {
                setup_fields();
            }, 'AI Translation');
            return;
        }
        
        console.log('Adding AI translation buttons');
        
        frm.add_custom_button('Smart AI Translate', function() {
            show_ai_dialog(frm);
        }, 'AI Translation');
        
        frm.add_custom_button('Quick AI Translate', function() {
            quick_translate(frm);
        }, 'AI Translation');
        
        frm.add_custom_button('Test AI Providers', function() {
            test_providers();
        }, 'AI Translation');
        
        frm.add_custom_button('AI Setup Guide', function() {
            show_setup_guide();
        }, 'AI Translation');
        
        frm.add_custom_button('Translation Stats', function() {
            show_translation_stats();
        }, 'AI Translation');
        
        frm.add_custom_button('Clear All Translations', function() {
            clear_all_translations(frm);
        }, 'AI Translation');
        
        console.log('AI buttons added successfully');
    } catch (e) {
        console.error('Error adding AI buttons:', e);
    }
}

// Removed the add_grid_buttons_force function entirely

function force_show_ai_buttons() {
    if (cur_frm && cur_frm.doctype === 'Sales Invoice') {
        console.log('Force showing AI buttons');
        add_ai_buttons_force(cur_frm);
        // Removed grid buttons
    }
}

window.test_ai_buttons = function() {
    console.log('Testing AI button display');
    force_show_ai_buttons();
    frappe.show_alert({
        message: 'AI buttons should now be visible',
        indicator: 'green'
    });
};

function show_ai_dialog(frm) {
    console.log('Opening AI dialog');
    
    frappe.call({
        method: 'ai_translate.translate.get_available_ai_providers',
        callback: function(response) {
            var providers = response.message || {};
            var available = [];
            
            for (var key in providers) {
                if (providers[key].configured) {
                    available.push(key);
                }
            }
            
            if (available.length === 0) {
                frappe.msgprint({
                    title: 'No AI Providers Configured',
                    message: 'Please configure at least one AI provider. Click AI Setup Guide for instructions.',
                    indicator: 'orange'
                });
                return;
            }
            
            var d = new frappe.ui.Dialog({
                title: 'Smart AI Translation Settings',
                fields: [
                    {
                        label: 'AI Provider',
                        fieldname: 'ai_provider',
                        fieldtype: 'Select',
                        options: available.join('\n'),  // ← real newlines
                        default: frm.doc.custom_ai_provider || available[0],
                        reqd: 1,
                        description: 'Choose your preferred AI provider for translation'
                    },       
                    {
                        label: 'Target Language',
                        fieldname: 'target_language',
                        fieldtype: 'Select',
                        options: [
                        'Arabic',
                        'Spanish',
                        'French',
                        'German',
                        'Italian',
                        'Portuguese',
                        'Russian',
                        'Japanese',
                        'Korean',
                        'Chinese (Simplified)',
                        'Chinese (Traditional)',
                        'Hindi',
                        'Urdu',
                        'Turkish',
                        'Dutch',
                        'Swedish',
                        'Danish',
                        'Norwegian',
                        'Finnish'
                        ].join('\n'),
                        default: get_default_language(frm),
                        reqd: 1,
                        description: 'Select the target language for translation'
                    },   
                    {
                        label: 'Translation Options',
                        fieldname: 'section_break',
                        fieldtype: 'Section Break'
                    },
                    {
                        label: 'Overwrite Existing Translations',
                        fieldname: 'overwrite_existing',
                        fieldtype: 'Check',
                        default: 0,
                        description: 'Check to replace existing translations'
                    },
                    {
                        label: 'Skip Empty Descriptions',
                        fieldname: 'skip_empty',
                        fieldtype: 'Check',
                        default: 1,
                        description: 'Skip items without descriptions'
                    }
                ],
                primary_action_label: 'Start AI Translation',
                primary_action: function(values) {
                    d.hide();
                    perform_bulk_translation(frm, values);
                },
                secondary_action_label: 'Test Provider First',
                secondary_action: function(values) {
                    test_single_provider(values.ai_provider);
                }
            });
            
            d.show();
        }
    });
}

// Removed translate_single function since grid buttons are removed
// Removed translate_multiple function since grid buttons are removed

function quick_translate(frm) {
    var items_to_translate = [];
    for (var i = 0; i < frm.doc.items.length; i++) {
        var item = frm.doc.items[i];
        if (item.description && item.description.trim()) {
            items_to_translate.push(item);
        }
    }
    
    if (items_to_translate.length === 0) {
        frappe.msgprint({
            title: 'No Items to Translate',
            message: 'No items with descriptions found in this invoice.',
            indicator: 'orange'
        });
        return;
    }
    
    var ai_provider = frm.doc.custom_ai_provider || 'groq';
    var target_language = get_default_language(frm);
    
    frappe.confirm(
        'Quick AI Translation will use ' + ai_provider.toUpperCase() + ' to translate all ' + 
        items_to_translate.length + ' items to ' + target_language + '. Continue?',
        function() {
            perform_bulk_ai_translation(frm, items_to_translate);
        }
    );
}

function perform_bulk_ai_translation(frm, items) {
    var target_language = get_default_language(frm);
    var language_code = get_language_code(target_language);
    var ai_provider = frm.doc.custom_ai_provider || 'groq';
    
    frappe.show_progress('AI Bulk Translation', 0, 100, 'Preparing bulk translation request...');
    
    var items_data = [];
    for (var i = 0; i < items.length; i++) {
        items_data.push({
            item_code: items[i].item_code,
            description: items[i].description
        });
    }
    
    frappe.call({
        method: 'ai_translate.translate.bulk_ai_translate_items',
        args: {
            items_data: JSON.stringify(items_data),
            target_language: language_code,
            ai_provider: ai_provider
        },
        callback: function(response) {
            frappe.hide_progress();
            
            if (response.message && response.message.results) {
                var results = response.message.results;
                var summary = response.message.summary;
                
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    if (result.success && result.translated_text) {
                        var item = items[i];
                        frappe.model.set_value(item.doctype, item.name, 'custom_translated_description', 
                            result.translated_text);
                    }
                }
                
                show_bulk_results(summary);
                frm.refresh_fields();
            } else {
                frappe.msgprint({
                    title: 'Translation Failed',
                    message: 'AI bulk translation failed. Please check your provider configuration and try again.',
                    indicator: 'red'
                });
            }
        }
    });
}

function perform_bulk_translation(frm, settings) {
    var items_to_translate = [];
    for (var i = 0; i < frm.doc.items.length; i++) {
        var item = frm.doc.items[i];
        if (!item.description || !item.description.trim()) {
            continue;
        }
        if (!settings.overwrite_existing && item.custom_translated_description) continue;
        items_to_translate.push(item);
    }
    
    if (items_to_translate.length === 0) {
        frappe.msgprint({
            title: 'No Items to Translate',
            message: 'No items found to translate with current settings.',
            indicator: 'orange'
        });
        return;
    }
    
    var language_code = get_language_code(settings.target_language);
    
    frappe.show_progress('Smart AI Translation', 0, 100, 'Preparing smart translation...');
    
    var items_data = [];
    for (var i = 0; i < items_to_translate.length; i++) {
        items_data.push({
            item_code: items_to_translate[i].item_code,
            description: items_to_translate[i].description
        });
    }
    
    frappe.call({
        method: 'ai_translate.translate.bulk_ai_translate_items',
        args: {
            items_data: JSON.stringify(items_data),
            target_language: language_code,
            ai_provider: settings.ai_provider
        },
        callback: function(response) {
            frappe.hide_progress();
            
            if (response.message && response.message.results) {
                var results = response.message.results;
                var summary = response.message.summary;
                
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    if (result.success && result.translated_text) {
                        var item = items_to_translate[i];
                        frappe.model.set_value(item.doctype, item.name, 'custom_translated_description', 
                            result.translated_text);
                    }
                }
                
                show_bulk_results(summary);
                frm.refresh_fields();
            } else {
                frappe.msgprint({
                    title: 'Smart Translation Failed',
                    message: 'Smart AI translation failed. Please try again.',
                    indicator: 'red'
                });
            }
        }
    });
}

function show_bulk_results(summary) {
    var success_rate = ((summary.successful_translations / summary.total_items) * 100).toFixed(1);
    var cost_estimate = ((summary.total_items || 0) * 0.001).toFixed(3);
    
    frappe.msgprint({
        title: 'AI Translation Results',
        message: '<div style="padding: 20px; background: #f8f9fa; border-radius: 10px;">' +
            '<h3 style="text-align: center; margin-bottom: 20px; color: #28a745;">AI Translation Complete!</h3>' +
            '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 20px 0;">' +
            '<div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid #dee2e6;">' +
            '<div style="font-size: 24px; font-weight: bold; color: #28a745;">' + summary.successful_translations + '</div>' +
            '<div style="font-size: 12px; color: #666;">Successful</div>' +
            '</div>' +
            '<div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid #dee2e6;">' +
            '<div style="font-size: 24px; font-weight: bold; color: #007bff;">' + success_rate + '%</div>' +
            '<div style="font-size: 12px; color: #666;">Success Rate</div>' +
            '</div>' +
            '<div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid #dee2e6;">' +
            '<div style="font-size: 24px; font-weight: bold; color: #6f42c1;">' + (summary.average_processing_time || 0).toFixed(1) + 's</div>' +
            '<div style="font-size: 12px; color: #666;">Avg Speed</div>' +
            '</div>' +
            '</div>' +
            '<div style="background: white; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px solid #dee2e6;">' +
            '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">' +
            '<div><strong>AI Provider:</strong> ' + (summary.ai_provider || 'Auto').toUpperCase() + '</div>' +
            '<div><strong>Est. Cost:</strong> ~$' + cost_estimate + '</div>' +
            '</div>' +
            (summary.failed_translations > 0 ? 
                '<div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 5px; border: 1px solid #ffeaa7;">' +
                '<strong>Note:</strong> ' + summary.failed_translations + ' items failed to translate' +
                '</div>' : '') +
            '</div>' +
            '</div>',
        indicator: summary.failed_translations > 0 ? 'orange' : 'green'
    });
}

function test_providers() {
    frappe.show_alert({
        message: 'Testing all AI providers...',
        indicator: 'blue'
    });
    
    frappe.call({
        method: 'ai_translate.translate.test_ai_providers',
        callback: function(response) {
            if (response.message) {
                show_test_results(response.message);
            } else {
                frappe.msgprint({
                    title: 'Test Failed',
                    message: 'Failed to test AI providers. Please check your configuration.',
                    indicator: 'red'
                });
            }
        }
    });
}

function test_single_provider(provider) {
    frappe.show_alert({
        message: 'Testing ' + provider.toUpperCase() + ' provider...',
        indicator: 'blue'
    });
    
    frappe.call({
        method: 'ai_translate.translate.ai_translate_text',
        args: {
            text: 'High-quality professional business solution',
            target_language: 'ar',
            source_language: 'en',
            ai_provider: provider
        },
        callback: function(response) {
            if (response.message && response.message.success) {
                frappe.show_alert({
                    message: provider.toUpperCase() + ' is working correctly!',
                    indicator: 'green'
                });
            } else {
                frappe.show_alert({
                    message: provider.toUpperCase() + ' test failed: ' + (response.message ? response.message.error : 'Unknown error'),
                    indicator: 'red'
                });
            }
        }
    });
}

function show_test_results(results) {
    var html = '<div style="padding: 20px;">';
    html += '<h3>AI Provider Test Results</h3>';
    
    var working_count = 0;
    var total_count = 0;
    
    for (var provider in results) {
        total_count++;
        var result = results[provider];
        var status_icon = result.status === 'success' ? '✅' : 
                         result.status === 'not_configured' ? '⚙️' : '❌';
        var status_text = result.status === 'success' ? 'Working' :
                         result.status === 'not_configured' ? 'Not Configured' : 'Failed';
        
        if (result.status === 'success') working_count++;
        
        html += '<div style="margin: 15px 0; padding: 15px; border: 1px solid #dee2e6; border-radius: 8px;">';
        html += '<h4>' + status_icon + ' ' + provider.toUpperCase() + '</h4>';
        html += '<div><strong>Status:</strong> ' + status_text + '</div>';
        
        if (result.status === 'success') {
            html += '<div><strong>Model:</strong> ' + (result.model || 'Unknown') + '</div>';
            html += '<div><strong>Response Time:</strong> ' + (result.processing_time || 0).toFixed(2) + 's</div>';
            html += '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; font-style: italic;">';
            html += '"' + (result.translated_text || 'No translation returned') + '"</div>';
        }
        
        if (result.error) {
            html += '<div style="color: #dc3545; margin-top: 10px;"><strong>Error:</strong> ' + result.error + '</div>';
        }
        
        html += '</div>';
    }
    
    html += '<div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center;">';
    html += '<h4>Summary</h4>';
    html += '<div><strong>' + working_count + ' of ' + total_count + '</strong> providers working</div>';
    html += '</div>';
    
    html += '</div>';
    
    frappe.msgprint({
        title: 'AI Provider Test Results',
        message: html,
        indicator: working_count > 0 ? 'green' : 'orange'
    });
}

function show_setup_guide() {
    frappe.call({
        method: 'ai_translate.translate.get_ai_setup_guide',
        callback: function(response) {
            var guide = response.message || {};
            
            var html = '<div style="padding: 20px;">';
            html += '<h2>AI Translation Setup Guide</h2>';
            html += '<p>Configure one or more AI providers to start translating:</p>';
            
            for (var provider in guide) {
                var info = guide[provider];
                
                html += '<div style="margin: 20px 0; padding: 20px; border: 1px solid #dee2e6; border-radius: 8px;">';
                html += '<h3>' + info.name + '</h3>';
                html += '<div><strong>Free Tier:</strong> ' + info.free_tier + '</div>';
                html += '<div><strong>Sign Up:</strong> <a href="' + info.signup_url + '" target="_blank">' + info.signup_url + '</a></div>';
                html += '<div><strong>API Keys:</strong> <a href="' + info.api_key_url + '" target="_blank">' + info.api_key_url + '</a></div>';
                html += '<div style="margin-top: 15px; background: #f8f9fa; padding: 15px; border-radius: 5px;">';
                html += '<strong>site_config.json:</strong><br>';
                html += '<code>"' + info.config_key + '": "your_api_key_here"</code>';
                html += '</div>';
                html += '</div>';
            }
            
            html += '<div style="background: #d4edda; padding: 15px; border-radius: 5px; margin-top: 20px;">';
            html += '<strong>Quick Start:</strong> Get Groq (free) at console.groq.com';
            html += '</div>';
            html += '</div>';
            
            frappe.msgprint({
                title: 'AI Setup Guide',
                message: html,
                indicator: 'blue'
            });
        }
    });
}

function show_translation_stats() {
    frappe.call({
        method: 'ai_translate.translate.get_translation_stats',
        callback: function(response) {
            var stats = response.message || {};
            
            var html = '<div style="padding: 20px;">';
            html += '<h3>Translation Statistics</h3>';
            html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">';
            html += '<div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">';
            html += '<div style="font-size: 24px; font-weight: bold; color: #007bff;">' + (stats.total_translations || 0) + '</div>';
            html += '<div>Total Translations</div>';
            html += '</div>';
            html += '<div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">';
            html += '<div style="font-size: 24px; font-weight: bold; color: #28a745;">' + (stats.configured_providers ? stats.configured_providers.length : 0) + '</div>';
            html += '<div>Configured Providers</div>';
            html += '</div>';
            html += '</div>';
            
            if (stats.configured_providers && stats.configured_providers.length > 0) {
                html += '<div style="margin-top: 20px;">';
                html += '<h4>Active Providers:</h4>';
                html += '<div style="display: flex; flex-wrap: wrap; gap: 10px;">';
                for (var i = 0; i < stats.configured_providers.length; i++) {
                    html += '<span style="background: #007bff; color: white; padding: 5px 12px; border-radius: 15px; font-size: 12px;">' + 
                            stats.configured_providers[i].toUpperCase() + '</span>';
                }
                html += '</div>';
                html += '</div>';
            }
            
            html += '</div>';
            
            frappe.msgprint({
                title: 'Translation Statistics',
                message: html,
                indicator: 'blue'
            });
        }
    });
}

function clear_all_translations(frm) {
    frappe.confirm(
        'Clear all translations in this invoice?<br><br>This will remove all AI translated descriptions from the current invoice items.',
        function() {
            for (var i = 0; i < frm.doc.items.length; i++) {
                var item = frm.doc.items[i];
                frappe.model.set_value(item.doctype, item.name, 'custom_translated_description', '');
            }
            
            frappe.show_alert({
                message: 'All translations cleared successfully',
                indicator: 'green'
            });
            
            frm.refresh_field('items');
        }
    );
}

function get_default_language(frm) {
    return frm.doc.custom_translation_language || 'Arabic';
}

function get_language_code(language_name) {
    var codes = {
        'Arabic': 'ar', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
        'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Japanese': 'ja',
        'Korean': 'ko', 'Chinese (Simplified)': 'zh', 'Chinese (Traditional)': 'zh-tw',
        'Hindi': 'hi', 'Urdu': 'ur', 'Turkish': 'tr', 'Dutch': 'nl',
        'Swedish': 'sv', 'Danish': 'da', 'Norwegian': 'no', 'Finnish': 'fi'
    };
    return codes[language_name] || 'ar';
}

function setup_fields() {
    frappe.confirm(
        'This will create the required custom fields for AI translation. Continue?',
        function() {
            frappe.call({
                method: 'ai_translate.translate.create_translation_custom_fields',
                callback: function(response) {
                    if (response.message && response.message.success) {
                        frappe.show_alert({
                            message: 'AI translation fields created successfully. Please refresh the page.',
                            indicator: 'green'
                        });
                        setTimeout(function() {
                            location.reload();
                        }, 2000);
                    } else {
                        frappe.msgprint({
                            title: 'Setup Error',
                            message: response.message ? response.message.error : 'Failed to create custom fields. Please check permissions.',
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    );
}

// Manual trigger for testing in browser console
console.log('AI Translation System loaded successfully! Type test_ai_buttons() in console to force show buttons.');

// Global helper functions for debugging
window.ai_translation_debug = {
    force_buttons: force_show_ai_buttons,
    test_buttons: function() { 
        force_show_ai_buttons();
        frappe.show_alert({message: 'AI buttons forced to show', indicator: 'blue'});
    },
    check_form: function() {
        console.log('Current form:', cur_frm);
        console.log('Doctype:', cur_frm ? cur_frm.doctype : 'No form');
        console.log('Custom fields:', cur_frm ? {
            language: !!cur_frm.fields_dict.custom_translation_language,
            provider: !!cur_frm.fields_dict.custom_ai_provider,
            translated: !!cur_frm.fields_dict.items
        } : 'No form');
    }
};