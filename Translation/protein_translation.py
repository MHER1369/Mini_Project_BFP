from math import isfinite

from Error_and_Logging.errors import DataFileError, InvalidSequenceError

class TranslationData:

    codon_table_path = "BioForge/data/codon_table.txt"
    amino_weights_path = "BioForge/data/amino_weights.txt"

    def __init__(self):

        self.codon_table = {}
        self.amino_weights = {}

        self.load_codon_table()
        self.load_amino_weights()

    def load_codon_table(self):

        with open(self.codon_table_path, "r", encoding="utf-8") as file:

            valid_nucleotide = set("AUCG")

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split()

                if len(parts) != 2:
                    raise DataFileError(
                        f"{self.codon_table_path}: invalid format at line {line_number}"
                    )

                codon = parts[0].upper()
                amino_acid = parts[1].upper()

                if len(codon) != 3 or any(char not in valid_nucleotide for char in codon):
                    raise DataFileError(
                        f"{self.codon_table_path}: invalid codon '{codon}' at line {line_number}"
                    )

                if amino_acid not in set("ACDEFGHIKLMNPQRSTVWY*"):
                    raise DataFileError(
                        f"{self.codon_table_path}: invalid amino acid at line {line_number}: {amino_acid}"
                    )

                self.codon_table[codon] = amino_acid

        if not self.codon_table:
            raise DataFileError(f"Data file contains no entries: {self.codon_table_path}")

    def load_amino_weights(self):

        with open(self.amino_weights_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split()

                if len(parts) != 2:
                    raise DataFileError(f"{self.amino_weights_path}: invalid format at line {line_number}")

                amino_acid = parts[0].upper()

                try:
                    weight = float(parts[1])
                except ValueError:
                    raise DataFileError(
                        f"{self.amino_weights_path}: invalid weight at line {line_number}: "
                        f"{parts[1]}"
                    )

                if amino_acid not in set("ACDEFGHIKLMNPQRSTVWY"):
                    raise DataFileError(
                        f"{self.amino_weights_path}: invalid amino acid at line {line_number}: {amino_acid}"
                    )
                if not isfinite(weight) or weight <= 0:
                    raise DataFileError(
                        f"{self.amino_weights_path}: invalid weight at line {line_number}: {parts[1]}"
                    )

                self.amino_weights[amino_acid] = weight

        if not self.amino_weights:
            raise DataFileError(f"Data file contains no entries: {self.amino_weights_path}")


class Translator:

    def __init__(self, data):
        self.data = data

    def translate(self, codons):

        protein = ""

        for codon in codons:

            codon = codon.upper()

            if len(codon) != 3 or any(base not in "AUCG" for base in codon):
                raise InvalidSequenceError(f"Invalid RNA codon: {codon}")

            try:
                amino_acid = self.data.codon_table[codon]
            except KeyError:
                raise DataFileError(f"Unknown codon: {codon}")

            # Stop Codon
            if amino_acid == "*":
                break

            protein += amino_acid

        return protein

    def calculate_weight(self, protein):

        total_weight = 18.015

        for amino_acid in protein:

            weight = self.data.amino_weights.get(amino_acid)

            if weight is None:
                raise DataFileError(
                    f"Unknown amino acid: {amino_acid}"
                )

            total_weight += weight

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


