#کد این قسمت با هوش مصنوعی ساخته شده صرفا جهت تست و برقراری ارتباط بین قسمت های ORF با Trnaslator
from ORF.Forward_strand import ForwardORFDetector
from ORF.Reverse_strand import ReverseStrand

from Translation.Translator import (
    TranslationData,
    Translator
)

sequence = "..."

forward_detector = ForwardORFDetector(sequence)
forward_orfs = forward_detector.detect()


reverse_detector = ReverseStrand(sequence)
reverse_orfs = reverse_detector.find_orf()

orfs = forward_orfs + reverse_orfs

data = TranslationData(
    "data/codon_table.txt",
    "data/amino_weights.txt"
)


translator = Translator(data)

translated_orfs = translator.translate_orfs(orfs)
