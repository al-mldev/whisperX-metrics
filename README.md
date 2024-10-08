

#### :white_check_mark: WhisperX RAG Analytics

This project is designed to evaluate the performance of the speech-to-text process with different models by metrics and a retrieval-augmented generation method to analyze each transcription with an LLM. This module uses faster Whisper models with [WhisperX](https://github.com/m-bain/whisperX) developed by [@m-bain](https://github.com/m-bain/) pipeline that generates transcription and diarization of audio conversations. The objective is to provide a framework for processing audio files in batch loads, generating transcriptions, retrieving diarization objects, and storing them in a non-relational database. The framework will also evaluate the performance metrics of the transcription process within the loaded model. The module metrics can calculate the real-time factor (RTF) for the audio file. If reference data is available, the word error rate (WER) and character error rate (CER) can be calculated and stored in the database. The utils module allows loading Whisper models that can be downloaded from Hugging Face or manually copied into the `models/` directory, and then transformed into the faster Whisper format. It can run transcriptions with multiple models on the same audio and evaluate their individual performance based on the metrics. The retrieval-augmented generation process is implemented to analyze the transcription by an implemented LLM, fed by a vector database containing the transcriptions in a vectorial space, wich recieves a prompt with the transcription text and the instructions like summarize or extract main topics from the conversation. This speech-to-text/RAG process can be implemented in an ETL cycle for a large audio batch, generating new transcriptions, analyze and correct for use as tagged audios to feed training datasets for your models.


#### :white_check_mark: Architecture 

![Pipeline](images/architecture.png)

#### :white_check_mark: Instructions

####  :arrow_right:  Previous settings

#### :small_blue_diamond: Set local environment

This version runs on a standalone Windows local machine, but it could also run in a virtual environment. The needed dependencies are listed in the requirements.txt file. This specific code runs with WhisperX 3.1.2, Python 3.8, CUDA 11.8, and the latest version of FFmpeg.

`pip install -r requirements.txt`

####  :small_blue_diamond: Set mongo db

Install MongoDB and MongoDB Compass, create the database `'whisperx'`, then set the localhost URI, ensuring it matches the one set in the project's connections 

#### :small_blue_diamond: Set huggingface credentials  

In `utils/utils_settings.py` set `HF_TOKEN` with your huggingface token, and `MODEL_NAME` the huggingface uri the pretrained model, the current model set for download is whisper tiny english once selected both, run main.py

#### :small_blue_diamond: LLM Requirements 
The RAG process is running with the LLM `mistral-7b-instruct-v3` implemented locally, it requires minimum of 6GB GPU, but also can run with RAM. 


#### :arrow_right:  Menu

Once you have your local environment, the connection to mongodb, and the hf credentials run main.py and the menu will display 

#### :small_blue_diamond: 1) Create Database Collections 

When the database connection is ready, select option 1 to insert the collections schema into the database. 

![output1](images/option1.png)

#### :small_blue_diamond: 2) Load Models

Select option 2 in the menu to download the Whisper model, then convert it to the Whisper faster format. It can also be loaded manually into the models directory.


#### :small_blue_diamond: 3) Load Audios 

Copy the audios to `local_input_batch/audio_batch/`, making sure to use MP3 format. Then, select option 3 in the menu. The new audio files should appear in the database within the `'audio_files'` collection.

![output3](images/option3.png)

 - Audio object example in mongo db 

![audiodb](images/audioDB.png)


#### :small_blue_diamond: 4) Load References 

This is an optional step. If manually corrected transcriptions are available for the audio, copy the reference files into `local_input_batch/reference_batch/`, making sure to name them `R-<audioname>.txt`. Select option 4 in the menu, provide the `audio_id` generated in the database for the associated MP3 file previously loaded, and the reference should appear in the references collection.


![output4](images/option4.png)

 - Reference object example in mongo db

![audiodb](images/referenceDB.png)

#### :small_blue_diamond: 5) Run Transcriptions

Once all is set up, select option 5 in the menu and then run the transcription. If references are not available, the word error rate (WER) and character error rate (CER) will not be calculated.


#### - Transcription/Diarization Output 
![option5](images/option5.png)

#### - Metrics Output
![metrics](images/metrics.png)


#### :small_blue_diamond: 6) Analyze Transcription with LLM

The generated transcription is stored also in a vector database, to feed the LLM with the document. Select option 6, insert the transcription ID, and the instruction to the LLM. It may take some minutes in generate the output.  

#### - LLM analysis inputs 
![llmInput](images/llmInput.png)

#### - LLM analysis outputs
![llmOutput](images/llmOutput.png)


#### - Raw Transcription

The raw transcription displays the non-aligned text output. If the model generates a consistent transcription, it can be used as a base to create a manual reference. The WER and CER of the generated transcription associated with a specific downloaded model can then be calculated. A reference file example can be found in `local_input_batch/reference_batch/R-audioexample.txt`.

![option6](images/option6.png)



####  :arrow_right: To DO List

- Intergate into a microservices architecture 

- Implement a GUI

