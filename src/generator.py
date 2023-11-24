#!/usr/bin/python
# This class handles the generation of a new song given a list of markov chains
# containing the note transitions and their frequencies.

from markov_chain import MarkovChain
import os

import random
import mido

class Generator:

    def __init__(self, markov_chains):
        self.markov_chains = markov_chains

    @staticmethod
    def load(markov_chains):
        assert all(isinstance(chain, MarkovChain) for chain in markov_chains)
        return Generator(markov_chains)

    def _note_to_messages(self, note):
        return [
            mido.Message('note_on', note=note.note, velocity=127,
                         time=0),
            mido.Message('note_off', note=note.note, velocity=0,
                         time=note.duration)
        ]

    def generate(self, filename):
        with mido.midifiles.MidiFile() as midi:
            track = mido.MidiTrack()
            last_note = None
            # Generate a sequence of 100 notes
            for i in range(100):
                # Randomly choose a markov chain for each iteration
                selected_chain = random.choice(self.markov_chains)
                new_note = selected_chain.get_next(last_note)
                track.extend(self._note_to_messages(new_note))
            midi.tracks.append(track)
            midi.save(filename)

    def print_transition_matrices(self):
        for idx, chain in enumerate(self.markov_chains):
            print(f"Transition Matrix for Markov Chain {idx + 1}:")
            chain.print_as_matrix()
            print()

if __name__ == "__main__":
    import sys

    midi_folder = "midi"  # Folder containing MIDI files

    from parser import Parser
    if len(sys.argv) == 2:
        output_file = sys.argv[1]

        # Load multiple markov chains from all MIDI files in the specified folder
        chains = [Parser(os.path.join(midi_folder, file)).get_chain() for file in os.listdir(midi_folder) if file.endswith(".mid")]

        # Generate a new song using the provided markov chains
        generator = Generator.load(chains)
        generator.generate(output_file)

        # Print transition matrices
        generator.print_transition_matrices()
        
        print('Generated markov chain and printed transition matrices.')
    else:
        print('Invalid number of arguments:')
        print('Example usage: python generator.py <out.mid>')
