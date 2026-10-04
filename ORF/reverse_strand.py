# In the name of Allah
<<<<<<< HEAD
#دیباگ شده با chatGPT
from .ORF import ORF, ORFDetector

class ReverseStrand(ORFDetector):

    def detect(self):

        orfs = []

        # بررسی سه Frame
        for reverse_frame in range(3):

            start_pos = None

            for i in range(
                reverse_frame,
                len(self.sequence) - 2,
                3
            ):

                codon = self.sequence[i:i + 3]

                # پیدا کردن Start
                if codon == self.START_CODON:

                    if start_pos is None:
                        start_pos = i

                # پیدا کردن Stop
                elif (
                    codon in self.STOP_CODONS
                    and start_pos is not None
                ):

                    protein_sequence = []

                    # Codonهای بین Start و Stop
                    for j in range(start_pos, i, 3):

                        protein_sequence.append(
                            self.sequence[j:j + 3]
                        )

                    # تبدیل مختصات Reverse به Original
                    original_start_pos = (
                        len(self.sequence) - start_pos - 1
                    )

                    orf = ORF(
                        strand="Reverse",
                        frame=reverse_frame,
                        start_pos=original_start_pos,
                        protein=protein_sequence,
                        is_complete=True
                    )

                    orfs.append(orf)

                    # آماده برای ORF بعدی
                    start_pos = None

            # Start پیدا شده ولی Stop پیدا نشده
            if start_pos is not None:

                protein_sequence = []

                for j in range(
                    start_pos,
                    len(self.sequence) - 2,
                    3
                ):

                    protein_sequence.append(
                        self.sequence[j:j + 3]
                    )

                original_start_pos = (
                    len(self.sequence) - start_pos - 1
                )

                orf = ORF(
                    strand="Reverse",
                    frame=reverse_frame,
                    start_pos=original_start_pos,
                    protein=protein_sequence,
                    is_complete=False
                )

                orfs.append(orf)

        return orfs

# Finall changes
=======
from .ORF import ORF, ORFDetector
>>>>>>> 7649bb1 (Update reverse_strand.py)

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

<<<<<<< HEAD
=======

>>>>>>> 7649bb1 (Update reverse_strand.py)
# Finall changes
