# my_app.py
from multilingual_sentiment_classifier import MultilingualSentimentClassifier

# Initialize the classifier
# Make sure LibreTranslate is running at this URL
classifier = MultilingualSentimentClassifier(libretranslate_url="http://localhost:5000")

# --- Use in Automatic Translation Mode (Default) ---
print("\n--- Automatic Mode ---")
classifier.set_translation_mode("auto")

review1 = "Este producto es excelente y me encanta. Cinco estrellas!"
sentiment1 = classifier.classify_sentiment(review1)
print(f"Sentiment for '{review1}': {sentiment1}")

review2 = "This is a truly awful product, very disappointing."
sentiment2 = classifier.classify_sentiment(review2)
print(f"Sentiment for '{review2}': {sentiment2}")

# --- Use in Manual Translation Mode (e.g., assuming German) ---
print("\n--- Manual Mode (Assuming German) ---")
classifier.set_translation_mode("manual", assumed_lang="de")

review3 = "Ich bin sehr zufrieden mit diesem Kauf, tolles Produkt!" # "I am very satisfied with this purchase, great product!"
sentiment3 = classifier.classify_sentiment(review3)
print(f"Sentiment for '{review3}': {sentiment3}")

review4 = "Absolut enttäuschend, nicht zu empfehlen." # "Absolutely disappointing, not recommended."
sentiment4 = classifier.classify_sentiment(review4)
print(f"Sentiment for '{review4}': {sentiment4}")

# You can also override the assumed_lang for a single call in manual mode
print("\n--- Manual Mode (Overriding for one French review) ---")
review5 = "C'est un produit médiocre, je suis déçu." # "It's a mediocre product, I'm disappointed."
# Even if mode is manual-de, this will be translated from French for this call
sentiment5 = classifier.classify_sentiment(review5) # No need to pass assumed_lang here, it will use the instance state.
print(f"Sentiment for '{review5}': {sentiment5}")