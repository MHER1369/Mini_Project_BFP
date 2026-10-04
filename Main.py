#این فایل مین برای تست کردن مابقی کد ها توسط Ai ساخته شده است. 
from ORF.forward_strand import ForwardORFDetector
from ORF.reverse_strand import ReverseStrand

from Translation.protein_translation import (
    TranslationData,
    Translator
)


def reverse_complement(sequence):

    complement = {
        "A": "U",
        "U": "A",
        "C": "G",
        "G": "C"
    }

    complemented = ""

    for base in sequence:
        complemented += complement[base]

    return complemented[::-1]


def main():

    # فعلاً برای تست
    sequence = "ACUAUGACAUAA"

    # Forward
    forward_detector = ForwardORFDetector(sequence)
    forward_orfs = forward_detector.detect()

    # Reverse Complement
    reverse_sequence = reverse_complement(sequence)

    # Reverse
    reverse_detector = ReverseStrand(reverse_sequence)
    reverse_orfs = reverse_detector.detect()

    # ترکیب همه ORFها
    orfs = forward_orfs + reverse_orfs

    # Data
    data = TranslationData(
        "data/codon_table.txt",
        "data/amino_weights.txt"
    )

    # Translator
    translator = Translator(data)

    # Translation
    translated_orfs = translator.translate_orfs(orfs)

    # تست نتیجه
    for orf in translated_orfs:
        print("--------------------")
        print("Strand:", orf.strand)
        print("Frame:", orf.frame)
        print("Start:", orf.start_pos)
        print("Protein:", orf.protein)
        print("Complete:", orf.is_complete)
        print("Weight:", orf.molecular_weight)


if __name__ == "__main__":
    main()
