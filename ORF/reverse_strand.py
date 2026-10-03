# In the name of Allah
from .ORF import ORF, ORFDetector

class ReverseStrand(ORFDetector):

    def detect(self):
        orfs = []

        for reverse_frame in range(3):
            start_pos = None
            for i in range(reverse_frame, len(self.sequence) - 2, 3):
                codon = self.sequence[i:i + 3]

                if codon == self.start_codon:
                    if start_pos is None:
                        start_pos = i

                elif (codon in self.stop_codon and start_pos is not None):
                    protein_sequence = []
                    for j in range(start_pos, i, 3):
                        protein_sequence.append(self.sequence[j:j+3])
                    original_start_pos = len(self.sequence) - start_pos - 1
                    orf = ORF(
                        strand="Reverse",
                        frame=reverse_frame,
                        start_pos=original_start_pos,
                        protein=protein_sequence,
                        is_complete=True
                    )

                    orfs.append(orf)
                    start_pos = None

            if start_pos is not None:
                protein_sequence= []
                for j in range (start_pos,len(self.sequence) - 2, 3):
                    protein_sequence.append(self.sequence[j:j + 3])
                original_start_pos = len(self.sequence) - start_pos - 1
                orf=ORF(
                    strand="Reverse",
                    frame=reverse_frame,
                    start_pos=original_start_pos,
                    protein=protein_sequence,
                    is_complete=False
                    )

        return orfs


# Finall changes
