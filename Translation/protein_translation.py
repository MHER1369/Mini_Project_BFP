
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
                    raise ValueError(
                        f"Invalid codon table format at line {line_number}"
                    )

                codon = parts[0].upper()
                amino_acid = parts[1].upper()

                if len(codon) != 3 or any(char not in valid_nucleotide for char in codon):
                    raise ValueError(
                        f"Invalid codon '{codon}' at line {line_number}"
                    )

                self.codon_table[codon] = amino_acid

    def load_amino_weights(self):

        with open(self.amino_weights_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split()

                if len(parts) != 2:
                    raise ValueError(f"Invalid amino weight line: {line_number}")

                amino_acid = parts[0].upper()

                try:
                    weight = float(parts[1])
                except ValueError:
                    raise ValueError(
                        f"Invalid amino acid weight at line {line_number}: "
                        f"{parts[1]}"
                    )

                self.amino_weights[amino_acid] = weight


class Translator:

    def __init__(self, data):
        self.data = data

    def translate(self, codons):

        protein = ""

        for codon in codons:

            codon = codon.upper()

            try:
                amino_acid = self.data.codon_table[codon]
            except KeyError:
                raise ValueError(f"Unknown codon: {codon}")

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
                raise ValueError(
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


