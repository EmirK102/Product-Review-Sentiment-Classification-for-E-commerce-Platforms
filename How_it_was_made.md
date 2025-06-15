This file covers How the model was made. 

To learn how the 5-star sentiment classifier was made, refer to sentiment_classifier_model_source_code.ipynb

Libretranslate is a completely independent program from our model, and is connected with our model via our provided python script.

The provided python script serves to make it convenient to use libretranslate and the classifier model in tandem. The python script can be run by itself for demonstration purposes
or imported for use in another python script. Just make sure that all the classifier model files are in the same directory as our provided python script. Also, It won't work properly if libretranslate isn't also simultaneously running.
