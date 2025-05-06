import numpy as np 
class keyClassifier:
    
    def __init__(self, pitch):
        self.pitch = pitch
        self.key_minor = -1
        self.key_major = -1       
        self.mode = None
        self.predicted_key = None
        self.minor_key_template = np.array([3, 0, 1, 2, 0, 1, 0, 2, 1, 0, 1, 0])
        self.major_key_template = np.array([3, 0, 1, 0, 2, 1, 0, 2, 0, 1, 0, 1])
        self.key_map = {
            0: "C",
            1: "C#",
            2: "D",
            3: "D#",
            4: "E",
            5: "F",
            6: "F#",
            7: "G",
            8: "G#",
            9: "A",
            10: "A#",
            11: "B"
        }

        
    def get_key(self):
        return self.predicted_key
    
    def set_key(self, key, mode):
        if mode == "minor":
            self.key_minor = key
        else:
            self.key_major = key

    def get_mode(self):
        return self.mode
    
    def set_mode(self, mode):
        self.mode = mode

    def classify(self, pitch_array):
        # minor and major keys starts from C and ends with B. It shifts 12 times and returns the most common key
        # all notes: C, C#/Db, D, D#/Eb, E, F, F#/Gb, G, G#/Ab, A, A#/Bb, B
        # C minor: C, D, Eb, F, G, Ab, Bb
        # C major: C, D, E, F, G, A, B

        minor_key_score = float('-inf') 
        major_key_score = float('-inf')  

        for key_index in range(12):
            window = np.array([pitch_array[(key_index + i) % 12] for i in range(12)])
            minor_key_score_new = np.sum(self.minor_key_template * window)   
            major_key_score_new = np.sum(self.major_key_template * window)

            if minor_key_score_new > minor_key_score:
                minor_key_score = minor_key_score_new
                self.key_minor = key_index

            
            if major_key_score_new > major_key_score:
                major_key_score = major_key_score_new
                self.key_major = key_index

        if minor_key_score > major_key_score:
            self.mode = "minor"
        else:
            self.mode = "major"

        self.predicted_key = self.key_map[self.key_minor] if self.mode == "minor" else self.key_map[self.key_major]
        print(f"Predicted key: {self.predicted_key} ({self.mode})")
        self.set_key(self.predicted_key, self.mode)
        self.set_mode(self.mode)
        return self.predicted_key
