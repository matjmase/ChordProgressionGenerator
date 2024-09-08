from midiutil import MIDIFile


def print_to_midi_file(list: list[list[int]], name: str) -> None:
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 4  # In beats
    tempo = 180  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitches in enumerate(list):
        for pitch in pitches:
            MyMIDI.addNote(track, channel, pitch, time + i * duration, duration, volume)

    with open(name, "wb") as output_file:
        MyMIDI.writeFile(output_file)