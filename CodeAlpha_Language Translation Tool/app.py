from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator 

app = Flask(__name__)
CORS(app) 


translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text_api():
    
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_lang')
    source_language = data.get('source_lang')

    
    if not text or not target_language:
        return jsonify({"error": "Text aur target language zaroori hain."}), 400
    
    
    final_source_lang = source_language if source_language and source_language != '' else 'auto'


    try:
        translation = translator.translate(
            text, 
            src=final_source_lang, 
            dest=target_language
        )
        
        translated_text = translation.text
        
        return jsonify({
            "translated_text": translated_text,
            "success": True
        })

    except Exception as e:
        
        return jsonify({
            "error": f"Google Translate Service error: {e}",
            "detail": str(e)
        }), 500

if __name__ == '__main__':
    print("Flask Server running at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
