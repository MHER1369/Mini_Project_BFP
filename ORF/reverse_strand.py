# In the name of Allah

class ORF:
    start_codon = "AUG"
    stop_codon = {"UAA", "UAG", "UGA"}

    def __init__(self, sequence):
        self.sequence = sequence


class ReverseStrand(ORF):

    def find_orf(self):
        orfs = []

        for reverse_frame in range(3):
            start_pos = None
            for i in range(reverse_frame, len(self.sequence) - 2, 3):
                codon = self.sequence[i:i + 3]

                if codon == self.start_codon:
                    if start_pos is None:
                        start_pos = i

                elif codon in self.stop_codon and start_pos is not None:
                    orf = self.sequence[start_pos:i + 3]
                    original_start_pos = len(self.sequence) - start_pos - 1
                    orfs.append({
                        "strand" : "Reverse",
                        "frame" : reverse_frame,
                        "start" : original_start_pos,
                        "stop" : i + 3,
                        "sequence" : orf,
                        "status" : "Complete"
                    })
                    start_pos = None

            if start_pos is not None:
                orf = self.sequence[start_pos:]
                original_start_pos = len(self.sequence) - start_pos - 1
                orfs.append({
                    "strand" : "Reverse",
                    "frame" : reverse_frame,
                    "start" : original_start_pos,
                    "stop" : len(self.sequence),
                    "sequence" : orf,
                    "status" : "Incomplete"
                })
        return orfs