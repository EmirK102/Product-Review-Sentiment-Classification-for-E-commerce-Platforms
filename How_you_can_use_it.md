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

