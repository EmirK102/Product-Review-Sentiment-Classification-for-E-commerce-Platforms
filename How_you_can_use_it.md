The first step is installing and running libretranslate. There are a number of ways to do it and it shouldn't matter which one is used
, as libretranslate always uses the same api. 

The way we managed to get it running is with docker. Firstly, install docker. Then open a terminal and type: docker run -ti --rm -p 5000:5000 libretranslate/libretranslate
and hit enter. This should download and run libretranslate

Preferably, to save the model and not have to redownload it every time, you can run in the terminal: docker save -o libretranslate.tar libretranslate/libretranslate:latest

Next step is to download the folder in the repository titled "project_model". In it is the rest of everything needed. The python script
titled sentiment_analyzer_app.py can be run by itself for demonstrative purposes or can be imported to be used in another script. Just
make sure that in whichever folder sentiment_analyzer_app.py is, so are the other model files, or you could edit sentiment_analyzer_app.py to always look for the other files
in a specific directory instead of the one it is currently located in.

Note: If you get any errors of the like: "cl.exe not found in PATH". You could run the python file in "Developer command prompt for VS 2022" if you have visual studio installed, as it worked for us when the issue occured.

(AI generated) How to use it when imported into another script:

Method Manual: SentimentAnalyzer and LibreTranslateClient
This manual provides a detailed description of the methods available in the SentimentAnalyzer class and its internal LibreTranslateClient class, as defined in sentiment_analyzer_app.py.

1. SentimentAnalyzer Class Methods
This is the main class you will interact with to perform sentiment analysis.

__init__(self, model_path: str, libretranslate_url: str)
Description: Initializes the SentimentAnalyzer object. It loads your BERT-based sentiment model and tokenizer, sets up the connection to the LibreTranslate server, and defines the default translation mode.

Parameters:

model_path (str): The file path to the directory containing your sentiment model files (e.g., ./my_sentiment_model).

libretranslate_url (str): The base URL of your running LibreTranslate API (e.g., http://localhost:5000).

Returns: None.

Notes: This method is called automatically when you create an instance of SentimentAnalyzer. It will print messages indicating model loading status and the device (CPU/GPU) being used. Raises RuntimeError if the model cannot be loaded.

set_translation_mode(self, mode: TranslationMode)
Description: Sets the translation mode that the analyzer will use for subsequent review processing. This determines how the input language is handled before sentiment analysis.

Parameters:

mode (TranslationMode enum): The desired translation mode. You must use one of the TranslationMode enum values:

TranslationMode.AUTO_DETECT_AND_TRANSLATE

TranslationMode.MANUAL_SOURCE_TRANSLATE_TO_EN

TranslationMode.NO_TRANSLATION

Returns: None.

Raises: TypeError if mode is not a TranslationMode enum instance.

get_predicted_rating(self, review_text: str, source_lang: Optional[str] = None) -> Dict
Description: The primary method to get the predicted 5-star rating for a given product review. It handles language determination (auto-detect, manual, or no translation) and translation (to English) based on the current mode or an explicit override.

Parameters:

review_text (str): The product review string you want to analyze.

source_lang (str, optional): An optional explicit 2-letter language code (e.g., 'es', 'fr') for this specific review. If provided, this will override the current_translation_mode's source determination for this call.

Important for MANUAL_SOURCE_TRANSLATE_TO_EN mode: If current_translation_mode is MANUAL_SOURCE_TRANSLATE_TO_EN, you should provide source_lang when calling this method (as is handled in the example if __name__ == "__main__": block). If not provided, it will assume English as a fallback.

Returns: Dict containing the following keys:

'original_review' (str): The input review text.

'determined_source_language' (str): The language code determined as the source for translation (e.g., 'en', 'es', or 'N/A' if no text).

'translated_text' (str): The review text after translation to English (if any). If no translation occurred, this will be the same as original_review.

'predicted_star_rating' (int): The 5-star rating (1-5). Returns 0 for empty input.

'probabilities' (list): A list of 5 floats representing the probability for each star rating (1-star to 5-star).

'status' (str): A string indicating the success or failure reason.

2. LibreTranslateClient Class Methods (self.lt within SentimentAnalyzer)
This class handles direct communication with your LibreTranslate server. You typically interact with this indirectly via SentimentAnalyzer.get_predicted_rating(), but you can also call its methods directly if you have an instance of SentimentAnalyzer (e.g., analyzer.lt.detect_language(...)).

__init__(self, base_url: str)
Description: Initializes the LibreTranslate client.

Parameters:

base_url (str): The base URL of your running LibreTranslate API (e.g., http://localhost:5000).

Returns: None.

detect_language(self, text: str) -> Optional[str]
Description: Sends a request to the LibreTranslate /detect endpoint to identify the language of the provided text.

Parameters:

text (str): The text string for which to detect the language.

Returns: str representing the 2-letter language code (e.g., 'en', 'fr', 'es') if successful, or None if detection fails or an error occurs.

Notes: Prints console messages about the detected language and confidence.

translate_text(self, text: str, source_lang: str, target_lang: str) -> Optional[str]
Description: Sends a request to the LibreTranslate /translate endpoint to translate text from a source language to a target language.

Parameters:

text (str): The text string to be translated.

source_lang (str): The 2-letter language code of the input text (e.g., 'es').

target_lang (str): The 2-letter language code for the desired output translation (e.g., 'en').

Returns: str containing the translated text if successful, or None if translation fails or an error occurs.

Notes: Prints console messages about the translation process. If source_lang and target_lang are the same, it skips the API call and returns the original text.

This method manual should help you understand the functionality and usage of each component within the sentiment_analyzer_app.py file.
