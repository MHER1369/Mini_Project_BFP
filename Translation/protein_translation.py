#اسکلت اولیه کد ترجمه. تغییرات لازم اعمال خواهد شد
from orf import ORF


class DataFileError(Exception):
    pass


class TranslationData:
    def __init__(self, codon_table_path, amino_weights_path):
        self.codon_table = {}
        self.amino_weights = {}

    def load_codon_table(self):
        pass

    def load_amino_weights(self):
        pass


class Translator:
    def __init__(self, data):
        self.data = data

    def translate(self, codons):
        pass

    def calculate_weight(self, protein):
        pass

    def translate_orf(self, orf):
        pass

    def translate_orfs(self, orfs):
        pass
