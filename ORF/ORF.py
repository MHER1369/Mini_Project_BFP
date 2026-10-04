#به نام ایزد منان
class ORF:

    def __init__(self, strand, frame, start_pos, protein, is_complete):
        self.strand = strand
        self.frame = frame
        self.start_pos = start_pos
        self.protein = protein
        self.is_complete = is_complete
        self.molecular_weight = None


class ORFDetector:

    START_CODON = "AUG"
    STOP_CODONS = {"UAA", "UAG", "UGA"}

    def __init__(self, sequence):
        self.sequence = sequence

    def detect(self):
        raise NotImplementedError

