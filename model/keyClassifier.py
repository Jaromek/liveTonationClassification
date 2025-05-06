class keyClassifier:
    def __init__(self, notes):
        self.notes = notes
        self.key = None
        self.predicted_key = None

    def classify(self, notes):
        # minor and major keys starts from C and ends with B. It shifts 12 times and returns the most common key
        # all notes: C, C#/Db, D, D#/Eb, E, F, F#/Gb, G, G#/Ab, A, A#/Bb, B
        # C minor: C, D, Eb, F, G, Ab, Bb
        # C major: C, D, E, F, G, A, B

        minor_key_template = (1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0)
        major_key_template = (1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1)
        
        


        return self.predicted_key