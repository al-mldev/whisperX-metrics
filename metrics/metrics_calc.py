from evaluate import load
from db_utils.db_settings import CLIENT_URL, DATABASE_NAME
from jiwer import cer
from pymongo import MongoClient
from utils.load_lists import load_transcription_text, load_reference_text
import gridfs
import os
import librosa
import tempfile

def whisperx_metrics_rtf(audio_id, file_name, last_end):
  last_end = float(last_end)
  client = MongoClient(CLIENT_URL)  
  db = client[DATABASE_NAME] 
  fs = gridfs.GridFS(db)   
  collection = db['audio_files']
  file_name = collection.find_one({'audio_id': audio_id})
  file_id = file_name['file_id']
  mp3_data = fs.get(file_id).read() 
  with tempfile.TemporaryDirectory() as temp_dir:
    output_path = os.path.join(temp_dir, file_name['filename'])
    output_path = output_path.replace("\\", "/")
    with open(output_path, 'wb') as f:
      f.write(mp3_data)
    audio_duration = librosa.get_duration(filename=output_path)
    rtf_score = last_end/audio_duration
  return rtf_score
  
def whisperx_metrics_wer(file_name, document_id):
  file_name=file_name.replace('.mp3', '.txt')
  print("-------------------------------------------------------------------\n",
        "------------------------WER Calculation----------------------------\n",
        "-------------------------------------------------------------------")
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------\n"
          "Error: No data to calculate WER metrics")
  else:
    ref_str = str(reference_list)
    tr_str = str(transcription_list)
    wer = load("wer")
    wer_score = wer.compute(predictions=[tr_str], references=[ref_str])
    return wer_score

def whisperx_metrics_cer(file_name, document_id):
  print("-------------------------------------------------------------------\n",
        "------------------------CER Calculation----------------------------\n",
        "-------------------------------------------------------------------")
  file_name=file_name.replace('.mp3', '.txt')
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------")
    print('Error: No data to calculate CER metrics')  
  else:
    ref_str = str(reference_list)
    tr_str = str(transcription_list)
    cer_score = cer(ref_str, tr_str)
    return cer_score






