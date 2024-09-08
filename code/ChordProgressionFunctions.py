import math
from random import random

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}

def swap_accidentals(note: str):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'
    if note == 'Cb':
        return 'B'
    if note == 'Bbb':
        return 'A'
    if note == 'Ebb':
        return 'D'

    return note

def PositiveModulus(val: int, mod: int) -> int:
    val %= mod
    val += mod
    val %= mod

    return val

def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    if note not in NOTES:
        print(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note

def number_to_note(number: int) -> (str, int):
    noteNumber = number % NOTES_IN_OCTAVE
    octaveNumber = math.floor(number / NOTES_IN_OCTAVE)
    return NOTES[noteNumber], octaveNumber

def Shuffle(list: list) -> list:
    currentIndex = len(list)

    while currentIndex != 0:
        randomIndex = math.floor(random() * currentIndex)
        currentIndex -= 1

        temp = list[currentIndex]
        list[currentIndex] = list[randomIndex]
        list[randomIndex] = temp
    return list

def GetTopTwoNotes(notes: list[str]) -> (str, str):
    notes.sort(reverse=True)

    first = notes[-1]
    second = notes[-2]

    return (first, second)

def NoteDifferential(first: str, second: str) -> int:
    firstNum = note_to_number(first)
    secondNum = note_to_number(second)

    return PositiveModulus(firstNum - secondNum, len(NOTES))

def DiffAnchor(firstNum: int, secondNum: int) -> (int, int):
    diff = 0
    anchor = 0
    if firstNum >= secondNum:
        diff = firstNum - secondNum
        anchor = secondNum
    else:
        diff = secondNum - firstNum
        anchor = firstNum

    return (diff, anchor)

def CheckNoteSequenceForDiff(anchor: int, diff: int, patternNotes: list[str]) -> list[list[str]]:
    output: list[list[str]] = []

    for patA in patternNotes:
        for patB in patternNotes:
            patANumber = note_to_number(patA, 0)
            patBNumber = note_to_number(patB, 0)

            if PositiveModulus(patANumber - patBNumber, len(NOTES)) == diff:
                newList = list(patternNotes)

                newList.remove(patA)
                newList.remove(patB)

                _, newAnchor = DiffAnchor(patANumber, patBNumber)

                change = newAnchor - anchor

                print(patA + '->' + number_to_note(note_to_number(patA, 0) - change))
                print(patB + '->' + number_to_note(note_to_number(patB, 0) - change))

                transform = [number_to_note(note_to_number(x, 0) - change) for x in newList]

                print("pat")
                print([x for x in patternNotes])
                print([number_to_note(note_to_number(x, 0) - change) for x in patternNotes])
                print("TTTT")
                print(transform)

                output.append(transform)

    return output