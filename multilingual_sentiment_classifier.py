import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

class MultilingualSentimentClassifier:
    """
    A class to perform multilingual product review sentiment classification.
    It integrates a local modernBERT model with a local LibreTranslate instance
    to handle various input languages.
    """

    def __init__(self, libretranslate_url: str = "http://localhost:5000"):
        """
        Initializes the sentiment classifier with a LibreTranslate endpoint.

        Args:
            libretranslate_url (str): The URL of the locally running LibreTranslate instance.
        """
        self.libretranslate_url = libretranslate_url
        self.tokenizer = None
        self.model = None
        # Internal variable to track the translation state: "auto" or "manual"
        self._translation_mode: str = "auto"
        # The language to assume if _translation_mode is "manual"
        self._assumed_language: str = "en"

        self._load_model()

    def _load_model(self):
        """
        Loads the modernBERT sentiment classification model and tokenizer
        from the current directory.
        """
        try:
            # Assume model files are in the same directory as this script.
            # Using "./" tells transformers to look in the current directory.
            self.tokenizer = AutoTokenizer.from_pretrained("./")
            self.model = AutoModelForSequenceClassification.from_pretrained("./")
            self.model.eval() # Set the model to evaluation mode
            print("modernBERT model and tokenizer loaded successfully from current directory.")
        except Exception as e:
            print(f"Error loading modernBERT model or tokenizer. Please ensure all files "
                  f"(model.safetensors, config.json, special_tokens_map.json, "
                  f"tokenizer.json, tokenizer_config.json) are in '{os.getcwd()}'."
                  f"\nError details: {e}")
            self.tokenizer = None
            self.model = None

    def set_translation_mode(self, mode: str, assumed_lang: str = None):
        """
        Sets the translation mode for incoming reviews.

        Args:
            mode (str):
                "auto": Automatically detect the review language using LibreTranslate
                        and translate to English if needed.
                "manual": Assume the review is in `assumed_lang` and translate to English.
            assumed_lang (str, optional):
                The language code (e.g., "es", "fr", "de") to assume if `mode` is "manual".
                If `mode` is "manual" and `assumed_lang` is not provided, it defaults to "en".
                This value is ignored if `mode` is "auto".
        Raises:
            ValueError: If an invalid mode is provided.
        """
        if mode not in ["auto", "manual"]:
            raise ValueError("Invalid mode. Must be 'auto' or 'manual'.")

        self._translation_mode = mode
        if mode == "manual":
            self._assumed_language = assumed_lang if assumed_lang is not None else "en"
            print(f"Translation mode set to: '{self._translation_mode}'. "
                  f"Reviews will be assumed to be in '{self._assumed_language}'.")
        else:
            print(f"Translation mode set to: '{self._translation_mode}'. "
                  f"Review language will be automatically detected.")

    def _libretranslate_api_call(self, endpoint: str, data: dict):
        """
        Makes a POST request to the LibreTranslate API.

        Args:
            endpoint (str): The specific API endpoint (e.g., "detect", "translate").
            data (dict): The payload for the POST request.

        Returns:
            dict or None: The JSON response from LibreTranslate, or None if an error occurs.
        """
        try:
            response = requests.post(f"{self.libretranslate_url}/{endpoint}", json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to LibreTranslate at {self.libretranslate_url}. "
                  f"Please ensure LibreTranslate is running and accessible.")
            return None
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred during LibreTranslate API call ({endpoint}): {err} - {response.text}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during LibreTranslate API call ({endpoint}): {e}")
            return None

    def _detect_language(self, text: str) -> str:
        """
        Detects the language of the given text using LibreTranslate.

        Args:
            text (str): The text whose language needs to be detected.

        Returns:
            str: The detected language code (e.g., "en", "es"), defaults to "en" if detection fails.
        """
        data = {"q": text}
        result = self._libretranslate_api_call("detect", data)
        if result and isinstance(result, list) and result and result[0].get("language"):
            detected_lang = result[0]["language"]
            print(f"LibreTranslate detected language: '{detected_lang}' for review.")
            return detected_lang
        print("Language detection failed, defaulting to 'en'.")
        return "en" # Default to English if detection fails

    def _translate_text(self, text: str, source_lang: str, target_lang: str = "en") -> str:
        """
        Translates the given text from `source_lang` to `target_lang` using LibreTranslate.

        Args:
            text (str): The text to be translated.
            source_lang (str): The language code of the source text.
            target_lang (str): The language code for the translated text (default is "en").

        Returns:
            str: The translated text, or the original text if translation fails.
        """
        data = {"q": text, "source": source_lang, "target": target_lang}
        result = self._libretranslate_api_call("translate", data)
        if result and result.get("translatedText"):
            translated_text = result["translatedText"]
            print(f"LibreTranslate translated from '{source_lang}' to '{target_lang}'.")
            return translated_text
        print(f"Translation from '{source_lang}' to '{target_lang}' failed, returning original text.")
        return text # Return original text if translation fails

    def classify_sentiment(self, review_text: str) -> dict:
        """
        Classifies the sentiment of a product review. The review is translated to English
        based on the current translation mode before being fed to the modernBERT model.

        Args:
            review_text (str): The text of the product review.

        Returns:
            dict: A dictionary containing the predicted label, score, and potentially
                  a mapped star rating (if applicable), or an error message.
                  Example: {"label": "LABEL_4", "score": 0.95, "mapped_stars": 5}
        """
        if self.tokenizer is None or self.model is None:
            return {"error": "Sentiment model not loaded. Cannot classify sentiment."}

        translated_text = review_text
        original_lang = "N/A" # Will be updated if language is detected or assumed

        if self._translation_mode == "auto":
            original_lang = self._detect_language(review_text)
            if original_lang != "en":
                translated_text = self._translate_text(review_text, original_lang, "en")
        elif self._translation_mode == "manual":
            original_lang = self._assumed_language
            if original_lang != "en":
                translated_text = self._translate_text(review_text, original_lang, "en")

        if not translated_text:
            return {"error": "Translation step failed. Cannot classify sentiment."}

        try:
            # Tokenize the translated text
            inputs = self.tokenizer(
                translated_text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            # Perform inference
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get logits and probabilities
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            
            # Get the predicted class ID and its confidence score
            predicted_class_id = torch.argmax(probabilities, dim=1).item()
            predicted_score = probabilities[0][predicted_class_id].item()

            # Map the predicted class ID to its label (e.g., LABEL_0, LABEL_1, ..., LABEL_4)
            predicted_label = self.model.config.id2label[predicted_class_id]

            # --- IMPORTANT: Mapping Labels to Stars ---
            # The exact mapping (e.g., LABEL_0 is 1-star, LABEL_4 is 5-star)
            # depends entirely on how your 'modernBERT' model was trained and
            # what its classification head outputs.
            # This is a common assumption for 5-star classification:
            # LABEL_0 -> 1 star
            # LABEL_1 -> 2 stars
            # LABEL_2 -> 3 stars
            # LABEL_3 -> 4 stars
            # LABEL_4 -> 5 stars
            # Adjust this mapping if your model uses a different convention.
            mapped_stars = None
            try:
                # Attempt to map LABEL_X to X+1 stars
                # Example: "LABEL_0" -> 1, "LABEL_1" -> 2, etc.
                numeric_part = int(predicted_label.split('_')[-1])
                mapped_stars = numeric_part + 1
            except (ValueError, IndexError):
                print(f"Warning: Could not automatically map label '{predicted_label}' to stars. "
                      f"Check your model's id2label configuration if star mapping is crucial.")

            result = {
                "original_review": review_text,
                "original_language": original_lang,
                "translated_review": translated_text,
                "predicted_label": predicted_label,
                "predicted_score": round(predicted_score, 4),
                "mapped_stars": mapped_stars
            }
            print(f"\n--- Classification Result ---")
            print(f"Original: '{review_text}' (Lang: {original_lang})")
            if original_lang != "en":
                print(f"Translated: '{translated_text}'")
            print(f"Sentiment: {predicted_label} (Score: {predicted_score:.4f}, Stars: {mapped_stars})")
            print(f"-----------------------------")

            return result

        except Exception as e:
            return {"error": f"Error during sentiment classification: {e}"}

# Example of how you might use this module (this part is for demonstration and testing,
# and would typically go into another Python file that imports this one):
if __name__ == "__main__":
    # Initialize the classifier. Ensure LibreTranslate is running on this URL.
    classifier = MultilingualSentimentClassifier(libretranslate_url="http://localhost:5000")

    print("\n--- Testing in Automatic Translation Mode ---")
    classifier.set_translation_mode("auto")
    
    # Test with an English review
    print("\nClassifying English review:")
    result_en = classifier.classify_sentiment("This product is absolutely fantastic! Five stars well deserved.")
    print(f"Result (English): {result_en}")

    # Test with a Spanish review
    print("\nClassifying Spanish review:")
    result_es = classifier.classify_sentiment("Este producto es excelente y lo recomiendo mucho. ¡Cinco estrellas!")
    print(f"Result (Spanish): {result_es}")

    # Test with a German review
    print("\nClassifying German review:")
    result_de = classifier.classify_sentiment("Das Produkt ist schrecklich und ich bin sehr enttäuscht. Eine Katastrophe.")
    print(f"Result (German): {result_de}")
    
    # Test with a review that LibreTranslate might struggle with (or non-text)
    print("\nClassifying a challenging review:")
    result_challenge = classifier.classify_sentiment("🚀💫🌌 Awesome product! ✨👍")
    print(f"Result (Challenge): {result_challenge}")

    print("\n--- Testing in Manual Translation Mode (assuming French) ---")
    classifier.set_translation_mode("manual", assumed_lang="fr")

    # Test with a French review
    print("\nClassifying French review (manually assuming French):")
    result_fr_manual = classifier.classify_sentiment("Ce produit est horrible. Je ne l'achèterais plus jamais.")
    print(f"Result (French Manual): {result_fr_manual}")

    # Test with an English review (still assuming French, so it will try to translate from French)
    print("\nClassifying English review (manually assuming French - will be incorrect):")
    result_en_misclassified = classifier.classify_sentiment("This is a great item!")
    print(f"Result (English Misclassified): {result_en_misclassified}")

    print("\n--- Testing in Manual Translation Mode (assuming no specific language, defaults to English) ---")
    classifier.set_translation_mode("manual") # Assumed language defaults to "en"
    print("\nClassifying English review (manual, default assumed_lang 'en'):")
    result_manual_default_en = classifier.classify_sentiment("Fantastic value, highly recommend.")
    print(f"Result (Manual Default EN): {result_manual_default_en}")

    # Simulate an error (e.g., LibreTranslate not running)
    # To test this, you would stop your LibreTranslate server before running this part.
    # print("\n--- Testing LibreTranslate connection error ---")
    # error_classifier = MultilingualSentimentClassifier(libretranslate_url="http://localhost:9999") # Incorrect port
    # error_result = error_classifier.classify_sentiment("This should fail.")
    # print(f"Result (Error Test): {error_result}")
