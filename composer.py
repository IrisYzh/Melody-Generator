import random
from typing import List, Dict
import os
import pretty_midi
import soundfile as sf
import fluidsynth

# ==========================================================
# Load TXT melodies
# ==========================================================
def load_melodies(path: str) -> List[List[str]]:
    """Read melodies from a file and return as list of note lists."""
    try:
        with open(path, "r") as f:
            lines = f.readlines()
            melodies = [line.strip().split() for line in lines]
            print(f"Successfully loaded {len(melodies)} melodies from:", path)
            return melodies
    except FileNotFoundError:
        print(f"File not found: {path}")
        print("Please make sure the dataset file exists.")
        return []


# ==========================================================
# Save TXT melody
# ==========================================================
def save_melodies(melodies: List[List[str]], path: str) -> None:
    """Save a list of generated melodies to a text file."""
    with open(path, "w") as f:
        for melody in melodies:
            f.write(" ".join(melody) + "\n")
    print(f"Saved text result:", path)


# ==========================================================
# Extract melody from NES MIDI files
# ==========================================================
def extract_melodies_from_midi_folder(folder: str) -> List[List[str]]:
    """Extract dominant pitch sequence from each NES MIDI file."""
    melodies = []
    for filename in os.listdir(folder):
        if filename.endswith(".mid"):
            midi_path = os.path.join(folder, filename)
            try:
                pm = pretty_midi.PrettyMIDI(midi_path)

                # Get most active instrument
                best = None
                most_notes = 0
                for inst in pm.instruments:
                    if inst.is_drum:
                        continue
                    if len(inst.notes) > most_notes:
                        best = inst
                        most_notes = len(inst.notes)

                if best:
                    melody = [
                        pretty_midi.note_number_to_name(n.pitch)
                        for n in best.notes
                    ]
                    melodies.append(melody)
                    print("Extracted:", filename)
            except:
                print("Skipped (error):", filename)
    return melodies


# ==========================================================
# Build bigram model
# ==========================================================
def build_bigram(melody_sequences: List[List[str]]) -> Dict[str, Dict[str, int]]:
    """Construct bigram transition model."""
    bigram = {}
    for seq in melody_sequences:
        for i in range(len(seq) - 1):
            cur_note = seq[i]
            nxt_note = seq[i + 1]
            if cur_note not in bigram:
                bigram[cur_note] = {}
            bigram[cur_note][nxt_note] = bigram[cur_note].get(nxt_note, 0) + 1
    print("Bigram keys:", len(bigram))
    return bigram


# ==========================================================
# Weighted selection
# ==========================================================
def weighted_choice(dic):
    return random.choices(list(dic.keys()), list(dic.values()), k=1)[0]


# ==========================================================
# Birthday parameter mapping
# ==========================================================
def birthday_to_start_note_and_length(birthday: str) -> tuple[str, int]:
    """Convert birthday into melody settings."""
    y, m, d = map(int, birthday.replace("/","-").split("-"))
    start_candidates = ["C4","D4","E4","F4","G4","A4","B4","C5"]
    start_note = start_candidates[d % len(start_candidates)]
    length = 8 + (y % 12)
    return start_note, length


# ==========================================================
# Generate melody
# ==========================================================
def generate_melody(bigram: dict, start_note: str, length: int = 12) -> List[str]:
    melody = [start_note]
    curr = start_note

    for _ in range(length):
        if curr in bigram and bigram[curr]:
            curr = weighted_choice(bigram[curr])
        else:
            curr = random.choice(list(bigram.keys()))
        melody.append(curr)

    return melody


# ==========================================================
# Save MIDI file
# ==========================================================
def write_melody_to_midi(melody: List[str], midi_path: str):
    """Save melody to MIDI file."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=0)

    start = 0.0
    dur = 0.5

    for note in melody:
        try:
            midi_n = pretty_midi.note_name_to_number(note)
        except:
            continue

        inst.notes.append(pretty_midi.Note(
            pitch=midi_n,
            velocity=100,
            start=start,
            end=start + dur
        ))
        start += dur

    pm.instruments.append(inst)
    pm.write(midi_path)
    print("MIDI file written:", midi_path)


# ==========================================================
# Save as WAV
# ==========================================================
def write_melody_to_wav(melody: List[str], wav_path: str, soundfont_path="data/GeneralUser.sf2"):
    """Render melody into WAV using FluidSynth."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=0)

    start = 0.0
    dur = 0.5

    for note in melody:
        try:
            midi_n = pretty_midi.note_name_to_number(note)
        except:
            continue
        inst.notes.append(pretty_midi.Note(
            velocity=100,
            pitch=midi_n,
            start=start,
            end=start + dur
        ))
        start += dur

    pm.instruments.append(inst)

    # Render to audio
    audio_data = pm.fluidsynth(fs=44100, sf2_path=soundfont_path)
    sf.write(wav_path, audio_data, 44100)
    print("WAV file written:", wav_path)


# ==========================================================
# MAIN
# ==========================================================
def main():
    txt = load_melodies("data/melodies.txt")
    midi = extract_melodies_from_midi_folder("data/nesmdb_midi/")
    all_data = txt + midi

    bigram = build_bigram(all_data)

    birthday = input("\nEnter birthday (YYYY-MM-DD): ")
    start, length = birthday_to_start_note_and_length(birthday)

    print(f"\nStart: {start}  |  Length: {length}")

    melody = generate_melody(bigram, start, length)
    print("\nGenerated Melody:")
    print(" ".join(melody))

    # create directory for this birthday
    output_dir = f"output/{birthday}/"
    os.makedirs(output_dir, exist_ok=True)

    # save files
    save_melodies([melody], f"{output_dir}/{birthday}melody.txt")
    write_melody_to_midi(melody, f"{output_dir}/{birthday}melody.mid")
    write_melody_to_wav(melody, f"{output_dir}/{birthday}melody.wav")


if __name__ == "__main__":
    main()