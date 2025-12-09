document.addEventListener('DOMContentLoaded', () => {
    
    const INPUT_TEXT = document.getElementById('input-text');
    const OUTPUT_TEXT_DISPLAY = document.getElementById('output-text');
    const TRANSLATE_BTN = document.getElementById('translate-btn');
    const COPY_BTN = document.getElementById('copy-btn');
    const SOURCE_LANG = document.getElementById('source-lang');
    const TARGET_LANG = document.getElementById('target-lang');
    const SWAP_ICON = document.querySelector('.swap-icon');

    
    const FLASK_API_URL = 'http://127.0.0.1:5000/translate';



    TRANSLATE_BTN.addEventListener('click', async () => {
        const textToTranslate = INPUT_TEXT.value.trim();
        const sourceLangCode = SOURCE_LANG.value;
        const targetLangCode = TARGET_LANG.value;

        if (textToTranslate === "") {
            alert("Please enter text to translate.");
            return;
        }

    
        OUTPUT_TEXT_DISPLAY.innerHTML = `<p class="loading-message">...Translating via Backend...</p>`;

        try {
            
            const response = await fetch(FLASK_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: textToTranslate,
                    source_lang: sourceLangCode,
                    target_lang: targetLangCode
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                
                OUTPUT_TEXT_DISPLAY.innerHTML = `<p>${result.translated_text}</p>`;
            } else {
                
                OUTPUT_TEXT_DISPLAY.innerHTML = `<p class="error-message">Error: ${result.error || 'Translation failed.'}</p>`;
            }

        } catch (error) {
            
            console.error('Fetch error:', error);
            OUTPUT_TEXT_DISPLAY.innerHTML = `<p class="error-message">Could not connect to the Python backend server (Is app.py running?).</p>`;
        }
    });



    SWAP_ICON.addEventListener('click', () => {
        const currentSource = SOURCE_LANG.value;
        const currentTarget = TARGET_LANG.value;

        
        SOURCE_LANG.value = currentTarget;
        TARGET_LANG.value = currentSource;

    
        if (INPUT_TEXT.value.trim() !== "") {
             TRANSLATE_BTN.click();
        }
    });


    COPY_BTN.addEventListener('click', () => {
        const translatedContent = OUTPUT_TEXT_DISPLAY.textContent.trim();

        if (translatedContent === "Translated text will appear here." || translatedContent.startsWith("...Translating") || translatedContent.startsWith("Error:")) {
            alert("No valid translated text to copy.");
            return;
        }

        
        navigator.clipboard.writeText(translatedContent).then(() => {
            alert('Translated text copied to clipboard!');
        }).catch(err => {
            console.error('Could not copy text: ', err);
            alert('Failed to copy text. Please try manually.');
        });
    });
});