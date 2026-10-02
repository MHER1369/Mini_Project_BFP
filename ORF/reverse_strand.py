# In the name of Allah

class ORF:
    start_codon = "AUG"
    stop_codon = {"UAA", "UAG", "UGA"}

    def __init__(self, rna, reverse_rna):
        self.rna = rna
        self.reverse_rna = reverse_rna


class ReverseStrand(ORF):
    def find_orf(self):
        orfs = []

        for frame in range(3):
            start_pos = None
            for i in range(frame, len(self.reverse_rna) - 2, 3):
                codon = self.reverse_rna[i:i + 3]

                if codon == self.start_codon:
                    if start_pos is None:
                        start_pos = i

                elif codon in self.stop_codon and start_pos is not None:
                    orf = self.reverse_rna[start_pos:i + 3]
                    start_pos = len(self.reverse_rna) - i - 1
                    orfs.append({
                        "Strand" : "Reverse",
                        "Frame" : frame,
                        "Start" : start_pos,
                        "sequence" : orf,
                        "Status" : "Complete"
                    })

                start_pos = None

            if start_pos is not None:
                orf = self.reverse_rna[start_pos:]
                start_pos = len(self.reverse_rna) - i - 1
                orfs.append({
                    "Strand" : "Reverse",
                    "Frame" : frame,
                    "Start" : start_pos,
                    "sequence" : orf,
                    "Status" : "Incomplete"
                })
        return orfs