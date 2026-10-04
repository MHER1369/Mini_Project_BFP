#تغییرات لازم اعمال شدند. 
class TranslationData:

    def __init__(self, codon_table_path, amino_weights_path):

        self.codon_table = {}
        self.amino_weights = {}

        self.load_codon_table(codon_table_path)
        self.load_amino_weights(amino_weights_path)

    def load_codon_table(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                codon = parts[0].upper()
                amino_acid = parts[1].upper()

                self.codon_table[codon] = amino_acid

    def load_amino_weights(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                amino_acid = parts[0].upper()
                weight = float(parts[1])

                self.amino_weights[amino_acid] = weight


class Translator:

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

        protein = ""

        for codon in codons:

            codon = codon.upper()

            amino_acid = self.data.codon_table[codon]

            # Stop Codon
            if amino_acid == "*":
                continue

            protein += amino_acid

        return protein

    def calculate_weight(self, protein):

        total_weight = 0.0

        for amino_acid in protein:

            total_weight += self.data.amino_weights[amino_acid]

        return total_weight

    def translate_orf(self, orf):

        protein = self.translate(orf.protein)

        weight = self.calculate_weight(protein)

        orf.protein = protein
        orf.molecular_weight = weight

        return orf

    def translate_orfs(self, orfs):

        translated_orfs = []

        for orf in orfs:

            translated_orf = self.translate_orf(orf)

            translated_orfs.append(translated_orf)

        return translated_orfs
        pass

    def calculate_weight(self, protein):
        pass

    def translate_orf(self, orf):
        pass

    def translate_orfs(self, orfs):
        pass
