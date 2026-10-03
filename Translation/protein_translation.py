#اسکلت اولیه کد ترجمه. تغییرات لازم اعمال خواهد شد
from ..ORF.ORF import ORF

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

                if len(parts) != 2:
                    raise DataFileError(
                        f"Malformed codon table at line {line_number}"
                    )

                codon = parts[0].upper()
                amino_acid = parts[1].upper()

                if len(codon) != 3:
                    raise DataFileError(
                        f"Invalid codon at line {line_number}: {codon}"
                    )

                if any(base not in "AUCG" for base in codon):
                    raise DataFileError(
                        f"Invalid codon at line {line_number}: {codon}"
                    )

                if len(amino_acid) != 1:
                    raise DataFileError(
                        f"Invalid amino acid at line {line_number}: "
                        f"{amino_acid}"
                    )

                if codon in self.codon_table:
                    raise DataFileError(
                        f"Duplicate codon at line {line_number}: {codon}"
                    )

                self.codon_table[codon] = amino_acid

    def load_amino_weights(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) != 2:
                    raise DataFileError(
                        f"Malformed amino weight file at line {line_number}"
                    )

                amino_acid = parts[0].upper()

                if len(amino_acid) != 1:
                    raise DataFileError(
                        f"Invalid amino acid at line {line_number}: "
                        f"{amino_acid}"
                    )

                try:
                    weight = float(parts[1])
                except ValueError:
                    raise DataFileError(
                        f"Invalid weight at line {line_number}: "
                        f"{parts[1]}"
                    )

                if weight <= 0:
                    raise DataFileError(
                        f"Invalid weight at line {line_number}: "
                        f"{weight}"
                    )

                if amino_acid in self.amino_weights:
                    raise DataFileError(
                        f"Duplicate amino acid at line {line_number}: "
                        f"{amino_acid}"
                    )

                self.amino_weights[amino_acid] = weight


class Translator:

    def __init__(self, data):
        self.data = data

    def translate(self, codons):

        protein = ""

        for codon in codons:

            codon = codon.upper()

            if codon not in self.data.codon_table:
                raise DataFileError(
                    f"Codon not found in codon table: {codon}"
                )

            amino_acid = self.data.codon_table[codon]

            if amino_acid == "*":
                continue

            protein += amino_acid

        return protein

    def calculate_weight(self, protein):

        total_weight = 0.0

        for amino_acid in protein:

            if amino_acid not in self.data.amino_weights:
                raise DataFileError(
                    f"Amino acid not found in weight table: {amino_acid}"
                )

            total_weight += self.data.amino_weights[amino_acid]

        return total_weight

    def translate_orf(self, orf):

        protein = self.translate(orf.protein)

        weight = self.calculate_weight(protein)

        orf.protein = protein
        orf.molecular_weight = weight

        return orf

    def translate_orfs(self, forward_orfs, reverse_orfs):

        translated_orfs = []

        for orf in forward_orfs:
            translated_orf = self.translate_orf(orf)
            translated_orfs.append(translated_orf)

        for orf in reverse_orfs:
            translated_orf = self.translate_orf(orf)
            translated_orfs.append(translated_orf)

        return translated_orfs
