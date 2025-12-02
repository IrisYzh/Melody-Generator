import unittest
import os
from composer import load_melodies, save_melodies, build_bigram, generate_melody

class TestMelodyGenerator(unittest.TestCase):

    def test_load_melodies_missing(self):
        """Ensure missing file does not crash the program."""
        melodies = load_melodies("data/not_exist.txt")
        self.assertEqual(melodies, [])

    def test_save_and_load(self):
        """Test saving melodies and loading them back"""
        test_data = [["C4","E4","G4"], ["A4","B4","C5"]]
        test_file = "data/test_output.txt"

        save_melodies(test_data, test_file)
        loaded_data = load_melodies(test_file)

        self.assertEqual(test_data, loaded_data)

        os.remove(test_file)

    def test_bigram_count(self):
        """Ensure bigram counts transitions"""
        melodies = [
            ["C4","E4","G4","E4"],
            ["C4","E4","C5"]
        ]
        bigram = build_bigram(melodies)

        self.assertEqual(bigram["C4"]["E4"], 2)
        self.assertEqual(bigram["E4"]["G4"], 1)
        self.assertEqual(bigram["E4"]["C5"], 1)

    def test_generated_melody_length(self):
        """Ensure generated melody has expected length"""
        bigram = {"C4": {"E4": 1}, "E4": {"C4": 1}}
        melody = generate_melody(bigram, "C4", length=8)
        self.assertEqual(len(melody), 9)  # including start note

if __name__ == '__main__':
    unittest.main()