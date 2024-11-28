from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import json

app = Flask(__name__)

def translate_text(text, target_lang):
    """
    Translate text to target language using deep_translator
    
    :param text: Text to translate
    :param target_lang: Target language code
    :return: Translated text
    """
    try:
        # Initialize translator with auto-detect source language
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Translate text
        translated_text = translator.translate(text)
        
        return translated_text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Predefined language dictionary
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'ru': 'Russian',
    'zh-cn': 'Chinese (Simplified)',
    'pt': 'Portuguese',
    'ko': 'Korean',
    'nl': 'Dutch'
}

@app.route('/')
def index():
    """
    Render the main translation page
    """
    # Prepare a list of languages for the dropdown
    language_list = sorted([(code, name) for code, name in LANGUAGES.items()])
    
    return render_template('index.html', languages=language_list)

@app.route('/translate', methods=['POST'])
def translate():
    """
    Handle translation requests
    """
    # Get input from the form
    text = request.form.get('text', '')
    target_lang = request.form.get('language', 'fr')
    
    # Check if text is empty
    if not text or not text.strip():
        return jsonify({
            'error': 'Please enter text to translate',
            'original': '',
            'translated': ''
        }), 400
    
    # Perform translation
    translated_text = translate_text(text, target_lang)
    
    # Return translation result
    return jsonify({
        'original': text,
        'translated': translated_text,
        'target_language': LANGUAGES.get(target_lang, 'Unknown'),
        'target_code': target_lang
    })

@app.route('/languages')
def get_languages():
    """
    Endpoint to get all supported languages
    """
    return jsonify(LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True)