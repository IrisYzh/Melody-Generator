# Melody Generator

## 🎵 Overview

This project generates personalized musical melodies based on a user’s birthday, using a bigram note-transition model trained from NES-style MIDI datasets as well as custom training melodies.
Melodies can be exported in three formats:
- text note sequences (.txt)
- MIDI files (.mid)
- audio waveform (.wav)

## 👩🏻‍💻 Author

**Zihan Yang**  
TECHIN 509 - Technology Foundations  
MSTI, University of Washington

## 🎹 Features
1. Extract melody data from NES MIDI dataset
2. Build a Bigram probability model of note transitions
3. Generate unique personalized melodies based on birthday information
4. Export melody as: .txt .mid .wav
5. Save results into birthday folders
6. Supports reproducible results

## ⚙️ Setup & Installation
### Step 1: Clone the repository
```python
git clone <https://github.com/IrisYzh/melody-generator.git>
cd melody_generator
```
### Step 2: Install dependencies
```python
pip install -r requirements.txt
```
### Step 3: Ensure SoundFont is available
You must have:
```
data/GeneralUser.sf2
data/nesmdb_midi
``` 
If missing, download them here:
- GeneralUser.sf2: https://schristiancollins.com/generaluser.php  
- nesmdb_midi: https://github.com/chrisdonahue/nesmdb?tab=readme-ov-file#download-links (Download NES-MDB in MIDI Format)

## 🎧 Running the Program
```
python3 composer.py
```

You will be prompted to enter a birthday:
```
Enter birthday (YYYY-MM-DD): 2025-01-01
```

The program will print the generated melody and create a folder:
```
output/2025-01-01/
```

Containing:
```
2025-01-01_melody.txt
2025-01-01_melody.mid
2025-01-01_melody.wav
```

Example Output (from terminal):
```
Start: C4  |  Length: 18

Generated Melody:
C4 E4 G4 C5 B4 A4 G4 E4 ...
```

### 🥳 Now you can enjoy your music!