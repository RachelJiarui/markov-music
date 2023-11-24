#!/usr/bin/python
# This class handles the generation of a new song given a list of markov chains
# containing the note transitions and their frequencies.

from markov_chain import MarkovChain

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        # Example usage:
        # python generator.py <in1.mid> <in2.mid> ... <out.mid>
        from parser import Parser

        # Load multiple markov chains from input MIDI files
        chains = [Parser(file).get_chain() for file in sys.argv[1:-1]]

        # Generate a new song using the provided markov chains
        Generator.load(chains).generate(sys.argv[-1])
        print('Generated markov chain')
    else:
        print('Invalid number of arguments:')
        print('Example usage: python generator.py <in1.mid> <in2.mid> ... <out.mid>')
