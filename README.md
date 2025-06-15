# Product Review Sentiment Classification for E-commerce Platforms

This project is about the creation of an AI model that enables its users to perform sentiment classification in a wide range of languages on written product reviews without the need for professional-grade or outsourced hardware/computational resources.  This is done by combining two AI models: LibreTranslate and ModernBERT. LibreTranslate is used for identifying the language in which reviews are written, and translating the reviews into English if they're in a different language, and ModernBERT is used for classifying the sentiment of English reviews. Specifically, for classifying how many stars out of five were given to a product.

## Problem Definition
E-commerce platforms face significant challenges in efficiently analyzing multilingual product reviews for sentiment. Existing solutions often demand substantial hardware or outsourcing, limiting accessibility and scalability for businesses seeking to understand customer feedback across diverse linguistic backgrounds and accurately classify multi-star ratings.

## Overview
This project introduces an accessible AI model for multilingual product review sentiment classification, designed to operate without the need for professional-grade computational resources. It integrates LibreTranslate for automatic language detection and translation of reviews into English, and a fine-tuned ModernBERT model for classifying sentiment into 1-5 star ratings based on the translated English text. This combined approach allows for efficient and accurate sentiment analysis across various languages, providing valuable insights into customer opinions.



## Dataset

The dataset we used is called "Amazon Reviews Multi" (https://www.kaggle.com/datasets/mexwell/amazon-reviews-multi). Label-wise, it is a perfectly balanced dataset. It contains 210000 English language product reviews and, alongside the review body, has features: product category, and review title. 

## Model training

The code we used for training and creating the model is in the provided file "sentiment_classifier_model_source_code.ipynb"

We decided to try training the model in three stages, using three disjoint subsets of the part of the training dataset that is in English. The first stage consists of training the model on the first training dataset by concatenating the product categories, review titles, and review bodies of the reviews within it and using those resulting strings for training the model. The second stage consists of training the model on the second training dataset, but this time only concatenating the review titles and review bodies. The third stage consists of only training on review bodies. The idea is to make the model learn the particularities of the reviews of different product categories and, in a way, to put it on training wheels and to slowly make it adjust to only classifying reviews without additional data. We found that different ratios of dataset sizes don't produce drastically different final model accuracies. They all gave accuracies of around 55% when tested on English product reviews.

## Evaluation

The model, when paired with LibreTranslate, performed worse on non-English languages:

German language accuracy: 51.4 %

![german_language_confusion_matrix](https://github.com/user-attachments/assets/109ec26b-236e-4bdb-bd4f-94e39f7e6b52)


Spanish language accuracy: 50.9%

![spanish_language_confusion_matrix](https://github.com/user-attachments/assets/ac275df0-2d9c-4163-9fed-56c140dcd071)


French language accuracy: 49.9%

![french_language_confusion_matrix](https://github.com/user-attachments/assets/97dd568e-90bc-4371-a85e-6ea746188fbc)


Japanese language accuracy: 40.8%

![japanese_language_confusion_matrix](https://github.com/user-attachments/assets/b7d2e4fc-6a52-4788-80f4-35d8d9aaf5e7)


Chinese language accuracy: 39.3%

![chinese_language_confusion_matrix](https://github.com/user-attachments/assets/134aaee0-9078-46ea-8a2b-5d7f8dd60326)


Although, this is for 5-star classification. It achieves higher accuracy on 3-label classification, achieving 76% on English-language 3-label sentiment classification. By "3-label sentiment classification" we mean treating the label 3 as neutral, treating labels greater than 3 as positive, and treating labels less than 3 as negative.

You can find the confusion matrices and model accuracies for different languages on our poster document.

## Conclusion

This project successfully developed an AI model for multilingual product review sentiment classification, demonstrating a practical approach to analyzing customer feedback across diverse languages. By combining LibreTranslate for translation and ModernBERT for sentiment classification, we created a system that can process reviews without requiring specialized hardware. While the model showed promising accuracy on English reviews (around 55% for 5-star classification and 76% for 3-label classification), its performance on non-English languages, when paired with LibreTranslate, varied, with German (51.4%) and Spanish (50.9%) performing better than French (49.9%), Japanese (40.8%), and Chinese (39.3%). These results highlight the inherent challenges of cross-lingual sentiment analysis, where translation quality can significantly impact the final classification accuracy. Despite these variations, the model offers a viable and accessible solution for e-commerce platforms looking to leverage sentiment analysis from a wide array of international customer reviews.

## Future Steps

Several avenues exist to enhance the model's performance and expand its capabilities:

Improving Multilingual Accuracy: Focus on fine-tuning the ModernBERT model with more diverse multilingual datasets. Exploring alternative translation models or incorporating cross-lingual embedding techniques directly into the sentiment classification model could also lead to significant improvements in non-English language accuracy.
Domain-Specific Fine-Tuning: The current model was trained on a general dataset of Amazon reviews. Training on product reviews specific to certain e-commerce categories or industries could further boost accuracy by capturing domain-specific nuances and vocabulary.
Exploring Other Classification Tasks: While the project focused on 5-star and 3-label classification, future work could explore more granular sentiment classification (e.g., aspect-based sentiment analysis) or integrate named entity recognition to identify specific product features being discussed in reviews.
Optimizing Model Size and Inference Speed: Although the current solution aims for accessibility, further optimization of the ModernBERT model's size and inference speed could make it even more practical for resource-constrained environments or real-time applications. Techniques like model quantization or distillation could be explored.
User Interface and Integration: Developing a user-friendly interface or API wrapper would make the model more accessible to non-technical users and facilitate easier integration into existing e-commerce analytics platforms.

## How to use it  


We couldn't upload our trained model to github, as it's too big, but you can find it on this google drive link:  [https://drive.google.com/file/d/1CJJUQt9qoC7Ffyk4jnMsfP4UzctNCAnT/view?usp=drive_link] . Aside from libretranslate, in it is everything needed to install the model. Note: If you don't want to visit the google drive link then we also provide the python script for connecting libretranslate and our model on the github page (multilingual_sentiment_classifier.py); and in that case, the trained ModernBERT model can be generated by the code in "sentiment_classifier_model_source_code.ipynb" file. The python script titled "multilingual_sentiment_classifier.py" can be run by itself for demonstrative purposes, or it can be imported to be used in another script. Just make sure that in whichever folder multilingual_sentiment_classifier.py is, so are all the ModernBERT model files. Or you could edit it to always look for the other files in a specific directory instead of the one it is currently located in. Also, if you decide to run "sample_test_of_multilingual_sentiment_classifier.py" then also make sure it is in the same folder as "multilingual_sentiment_classifier.py".

Note: If you get any errors of the like: "cl.exe not found in PATH". You could run the python file in "Developer command prompt for VS 2022" if you have visual studio installed, as it worked for us when the issue occured.



## **Prerequisites**

Before you can use this classifier, make sure you have the following set up:

1. **Python 3.8+:** This script is written in Python.  
2. **Python Libraries:** You'll need transformers, requests, and torch.  
3. **LibreTranslate:** A local instance of LibreTranslate must be running and accessible.  
4. **ModernBERT Model Files:** Your trained modernBERT model files must be in the correct location.

## **Setup and Installation**

### **1\. Place Model Files**

Ensure your modernBERT model files are in the **same directory** as the multilingual\_sentiment\_classifier.py script. These files are:

* model.safetensors  
* config.json  
* special\_tokens\_map.json  
* tokenizer.json  
* tokenizer\_config.json

The script is designed to automatically load the model from the current working directory.

### **2\. Install Python Dependencies**

Open your terminal or command prompt and run the following command to install the required Python libraries:

pip install transformers requests torch

### **3\. Run LibreTranslate Locally**

You need a running LibreTranslate server. The easiest way to get started is by using Docker:

docker run -ti --rm -p 5000:5000 libretranslate/libretranslate

This command will start LibreTranslate on http://localhost:5000. If you run it on a different port or host, remember to update the libretranslate\_url when initializing the classifier.

Preferably, to save the model and not have to redownload it every time, you can run in the terminal: docker save -o libretranslate.tar libretranslate/libretranslate:latest

## **Usage**

### **1\. Import the Classifier**

In your Python application or script, import the MultilingualSentimentClassifier class:

from multilingual\_sentiment\_classifier import MultilingualSentimentClassifier

### **2\. Initialize the Classifier**

Create an instance of the classifier. By default, it expects LibreTranslate to be running on http://localhost:5000. If your LibreTranslate instance is elsewhere, provide its URL:

\# Default initialization  
classifier \= MultilingualSentimentClassifier()

\# If LibreTranslate is on a different URL/port  
\# classifier \= MultilingualSentimentClassifier(libretranslate\_url="http://your-libretranslate-host:your-port")

Upon initialization, the script will attempt to load your modernBERT model and tokenizer. You'll see a message confirming successful loading or an error if files are missing.

### **3\. Set Translation Mode**

The classifier has an internal state for its translation mode, which determines how it handles non-English reviews. You can control this state using the set\_translation\_mode method.

#### **Automatic Detection Mode ("auto")**

In this mode, the classifier will automatically detect the language of the input review using LibreTranslate. If the detected language is not English, it will translate the review to English before classifying its sentiment. This is the default mode.

classifier.set\_translation\_mode("auto")

review\_spanish \= "Este producto es excelente y lo recomiendo mucho. ¡Cinco estrellas\!"  
result \= classifier.classify\_sentiment(review\_spanish)  
print(result)  
\# Expected output (sentiment might vary based on your model):  
\# {'original\_review': 'Este producto es excelente y lo recomiendo mucho. ¡Cinco estrellas\!',  
\#  'original\_language': 'es',  
\#  'translated\_review': 'This product is excellent and I highly recommend it. Five stars\!',  
\#  'predicted\_label': 'LABEL\_4', 'predicted\_score': 0.99, 'mapped\_stars': 5}

review\_english \= "This product is absolutely fantastic\! Five stars well deserved."  
result \= classifier.classify\_sentiment(review\_english)  
print(result)  
\# Expected output:  
\# {'original\_review': 'This product is absolutely fantastic\! Five stars well deserved.',  
\#  'original\_language': 'en',  
\#  'translated\_review': 'This product is absolutely fantastic\! Five stars well deserved.',  
\#  'predicted\_label': 'LABEL\_4', 'predicted\_score': 0.99, 'mapped\_stars': 5}

#### **Manual Language Mode ("manual")**

In this mode, you explicitly tell the classifier what language to assume the review is in. It will then translate from this assumed language to English if needed. This is useful if you know the source language of a batch of reviews and want to skip language detection for performance or accuracy.

\# Set mode to manual, assuming French reviews  
classifier.set\_translation\_mode("manual", assumed\_lang="fr")

review\_french \= "Ce produit est horrible. Je ne l'achèterais plus jamais."  
result \= classifier.classify\_sentiment(review\_french)  
print(result)  
\# Expected output (sentiment might vary):  
\# {'original\_review': 'Ce produit est horrible. Je ne l\\'achèterais plus jamais.',  
\#  'original\_language': 'fr',  
\#  'translated\_review': 'This product is horrible. I would never buy it again.',  
\#  'predicted\_label': 'LABEL\_0', 'predicted\_score': 0.97, 'mapped\_stars': 1}

\# If you set manual mode without \`assumed\_lang\`, it defaults to "en" (English).  
classifier.set\_translation\_mode("manual") \# Assumed language is now "en" by default

review\_english\_manual \= "Great value, highly recommend."  
result \= classifier.classify\_sentiment(review\_english\_manual)  
print(result)  
\# Expected output:  
\# {'original\_review': 'Great value, highly recommend.',  
\#  'original\_language': 'en',  
\#  'translated\_review': 'Great value, highly recommend.',  
\#  'predicted\_label': 'LABEL\_4', 'predicted\_score': 0.99, 'mapped\_stars': 5}

### **4\. Classify Sentiment**

Use the classify\_sentiment method, passing the review text as a string:

review\_text \= "Das ist ein fantastisches Produkt, sehr empfehlenswert\!"  
sentiment\_result \= classifier.classify\_sentiment(review\_text)  
print(sentiment\_result)

## **Output Structure**

The classify\_sentiment method returns a dictionary containing the following keys:

* original\_review (str): The raw review text provided as input.  
* original\_language (str): The detected or assumed language code of the original review (e.g., "en", "es", "fr").  
* translated\_review (str): The review translated into English (same as original if original\_language was "en").  
* predicted\_label (str): The sentiment label predicted by your modernBERT model (e.g., "LABEL\_0", "LABEL\_1", ..., "LABEL\_4").  
* predicted\_score (float): The confidence score (probability) of the predicted label, rounded to 4 decimal places.  
* mapped\_stars (int or None): An integer representing the 1-5 star rating based on the predicted\_label. This mapping assumes LABEL\_0 is 1-star, LABEL\_1 is 2-stars, and so on. If the label format doesn't match this expectation, it will be None.  
* error (str, optional): This key will be present with an error message if any issues occur during model loading, translation, or classification.

## **Important Notes and Customization**

### **Mapping Labels to Star Ratings**

The script includes a utility to map the model's predicted\_label (e.g., LABEL\_0, LABEL\_1, LABEL\_2, LABEL\_3, LABEL\_4) to a 1-5 star rating. This mapping (LABEL\_X \-\> X+1 stars) is a common convention for 5-star classification tasks.

**If your modernBERT model was trained with a different mapping (e.g., LABEL\_0 means 5 stars, LABEL\_4 means 1 star), you must adjust the mapped\_stars logic within the classify\_sentiment method to correctly interpret your model's output.**

### **LibreTranslate Connection Errors**

If LibreTranslate is not running or is inaccessible at the specified libretranslate\_url, the \_libretranslate\_api\_call method will print an error message to the console, and translation/detection steps will gracefully fail, returning the original text or an error message. Ensure LibreTranslate is always running before using the classifier.

### **Model Loading Errors**

If the model.safetensors, config.json, special\_tokens\_map.json, tokenizer.json, or tokenizer\_config.json files are not found in the same directory as the script, the \_load\_model method will print an error, and sentiment classification will not be possible. Double-check your file placement if you encounter this error.

### **License**

This project is licensed under GNU Affero General Public License.
