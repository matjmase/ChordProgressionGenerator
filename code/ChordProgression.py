import pickle
import ChordProgressionFunctions

from midiutil import MIDIFile
from mingus.core import chords as mingChords

import MidiFunctions

# chord progression length

progression_length = 4

# diffs

chordDiffs: dict[str, int] = {
    'i': 0,
    'ii': 2,
    'iii': 4,
    'iv': 5,
    'v': 7,
    'vi': 9,
    'vii': 11,
}

# Load Network

compatibility: dict[str, set[str]] = {}

file = open('commonChords.txt', "r")
lines = file.readlines()
file.close()


def add_to_network(first_chord: str, second_chord: str):
    if first_chord not in compatibility:
        compatibility[first_chord] = set()
    if second_chord not in compatibility[first_chord]:
        compatibility[first_chord].update([second_chord])


for line in lines:
    chords = line.strip().split("-")
    previousChord = ''

    for i, chord in enumerate(chords):
        if i == 0:
            previousChord = chord
            continue
        else:
            add_to_network(previousChord, chord)
            previousChord = chord

    # loop last to first
    add_to_network(previousChord, chords[0])

for i, (key, value) in enumerate(compatibility.items()):
    print(key)
    for element in value:
        print('\t' + element)


queue1: list[list[str]] = []
queue2: list[list[str]] = []

is_queue1 = True

# load up all starting chords
for key, value in compatibility.items():
    queue1.append([key])

for _ in range(progression_length - 1):
    focus = queue1 if is_queue1 else queue2
    newQueue: list[list[str]] = []

    for progression in focus:
        lastChord = progression[len(progression) - 1]

        for nextChord in compatibility[lastChord]:
            newQueue.append([*progression, nextChord])

    # get ready for next round
    if is_queue1:
        queue2 = newQueue
    else:
        queue1 = newQueue

    is_queue1 = not is_queue1

raw_progressions: list[list[str]] = queue1 if is_queue1 else queue2

looping_progressions: list[list[str]] = []

for pattern in raw_progressions:
    if pattern[0] in compatibility[pattern[len(pattern) - 1]]:
        looping_progressions.append(pattern)

for i, progression in enumerate(looping_progressions):
    print(i.__str__(), end=' ')
    for chord in progression:
        print(chord, end=' ')
    print()

indexNumber = int(input("Enter selection."))

chosen_progression = looping_progressions[indexNumber]

for chord in chosen_progression:
    print(chord, end=' ')
print()

array_of_chords: list[list[int]] = []

for chord in chosen_progression:
    diff = chordDiffs[chord.lower().replace('o', '')]

    chord_notes: any

    if chord == chord.lower():
        chord_notes = mingChords.minor_triad
    else:
        chord_notes = mingChords.major_triad

    adjust = -1 if chord.endswith('o') else 0

    notes_to_add: list[str] = []

    for pitch in chord_notes('C'):
        notes_to_add.append(ChordProgressionFunctions.note_to_number(pitch, 4) + diff + adjust)

    array_of_chords.append(notes_to_add)

print(array_of_chords)

MidiFunctions.print_to_midi_file(array_of_chords, "chordProgression.mid")
