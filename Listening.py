#someone else got this working, but i have not figured it out yet: https://github.com/ufal/whisper_streaming/blob/main/whisper_online.py


import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave
import torch
import queue
import threading
import librosa
from functools import lru_cache
import time
import logging
import io
import soundfile as sf
import math

logger = logging.getLogger(__name__)

#check if the folder for the  model exists, if not create it
model_dir = os.path.join(os.path.dirname(__file__), "AIModels")
os.makedirs(model_dir, exist_ok=True)

# Configurationimport whisper
model_size = "medium"  # or "base", "small", "large", etc.
model_path = os.path.join(model_dir, f"{model_size}.pt")
# Load the model, downloading it to model_dir if not present
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(model_size, download_root=model_dir).to(device)

# Check if the model is already downloaded, if not download it
if not os.path.exists(model_path):
    print(f"Model {model_size} not found in {model_dir}. Downloading...")
    model = whisper.load_model(model_size, download_root=model_dir).to(device)
else:
    print(f"Loading model {model_size} from {model_dir}.")
    model = whisper.load_model(model_size, download_root=model_dir).to(device)


SAMPLE_RATE = 16000  # Whisper's preferred sample rate
CHANNELS = 1
WHISPER_LANG_CODES = "af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,zh".split(",")


@lru_cache(10**6)
def load_audio(fname):
    a, _ = librosa.load(fname, sr=SAMPLE_RATE, dtype=np.float32)
    return a

def load_audio_chunk(fname, beg, end):
    audio = load_audio(fname)
    beg_s = int(beg*SAMPLE_RATE)
    end_s = int(end*SAMPLE_RATE)
    return audio[beg_s:end_s]

