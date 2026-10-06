from Error_and_Logging.errors import BioForgeError, DataFileError, InvalidSequenceError
from math import isfinite
import logging

logger = logging.getLogger("bioforge")

class TranslationData:

    codon_table_path = "BioForge/data/codon_table.txt"
    amino_weights_path = "BioForge/data/amino_weights.txt"

    def __init__(self):

        self.codon_table = {}
        self.amino_weights = {}

        self.load_codon_table()
        self.load_amino_weights()

    def load_codon_table(self):

        #xxx#
        try:

            with open(self.codon_table_path, "r", encoding="utf-8") as file:

                valid_nucleotide = set("AUCG")

                for line_number, line in enumerate(file, start=1):

                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()

                    if len(parts) != 2:
                        raise DataFileError(
                            f"Invalid codon table format at line {line_number}"
                        )

                    codon = parts[0].upper()
                    amino_acid = parts[1].upper()

                    if len(codon) != 3 or any(char not in valid_nucleotide for char in codon):
                        raise DataFileError(
                            f"Invalid codon '{codon}' at line {line_number}"
                        )

                    if amino_acid not in set("ACDEFGHIKLMNPQRSTVWY*"):
                        raise DataFileError(
                            f"Invalid amino acid '{amino_acid}' at line {line_number}"
                        )

                    self.codon_table[codon] = amino_acid
            if not self.codon_table:
                raise DataFileError("Data file contains no entries")
        except DataFileError as error:
            logger.error("Data file %s: %s", self.codon_table_path, error)
            raise
        except (OSError, UnicodeError) as error:
            logger.error("Cannot read data file %s: %s", self.codon_table_path, error)
            raise DataFileError(f"Cannot read data file {self.codon_table_path}: {error}") from error

    def load_amino_weights(self):

        #xxx#
        try:

            with open(self.amino_weights_path, "r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()

                    if len(parts) != 2:
                        raise DataFileError(f"Invalid amino weight line: {line_number}")

                    amino_acid = parts[0].upper()

                    try:
                        weight = float(parts[1])
                    except ValueError:
                        raise DataFileError(
                            f"Invalid amino acid weight at line {line_number}: "
                            f"{parts[1]}"
                        )

                    if amino_acid not in set("ACDEFGHIKLMNPQRSTVWY"):
                        raise DataFileError(
                            f"Invalid amino acid '{amino_acid}' at line {line_number}"
                        )
                    if not isfinite(weight) or weight <= 0:
                        raise DataFileError(
                            f"Invalid amino acid weight at line {line_number}: {parts[1]}"
                        )

                    self.amino_weights[amino_acid] = weight
            if not self.amino_weights:
                raise DataFileError("Data file contains no entries")
        except DataFileError as error:
            #loggerconnect
            logger.error("Data file %s: %s", self.amino_weights_path, error)
            raise
        except (OSError, UnicodeError) as error:
            #loggerconnect
            logger.error("Cannot read data file %s: %s", self.amino_weights_path, error)
            raise DataFileError(f"Cannot read data file {self.amino_weights_path}: {error}") from error


class Translator:

    def __init__(self, data):
        self.data = data

    def translate(self, codons):

        protein = ""

        for codon in codons:

            codon = codon.upper()

            #xxx#
            if len(codon) != 3 or any(base not in "AUCG" for base in codon):
                raise InvalidSequenceError(f"Invalid RNA codon: {codon}")

            try:
                amino_acid = self.data.codon_table[codon]
            except KeyError:
                #xxx#
                raise DataFileError(f"Unknown codon: {codon}")

            # Stop Codon
            if amino_acid == "*":
                break

            protein += amino_acid

        return protein

    def calculate_weight(self, protein):

        total_weight = 0.0

        for amino_acid in protein:

            weight = self.data.amino_weights.get(amino_acid)

            if weight is None:
                #xxx#
                raise DataFileError(
                    f"Unknown amino acid: {amino_acid}"
                )

            total_weight += weight

        return total_weight

    def translate_orf(self, orf):

        #xxx#
        try:
            protein = self.translate(orf.protein)
            weight = self.calculate_weight(protein)
        except BioForgeError as error:
            logger.error(
                "ORF strand=%s frame=%s start=%s: %s",
                orf.strand, orf.frame, orf.start_pos, error,
            )
            raise

        orf.protein = protein
        orf.molecular_weight = weight

        return orf

    def translate_orfs(self, orfs):

        translated_orfs = []

        for orf in orfs:

            try:
                translated_orf = self.translate_orf(orf)
            except InvalidSequenceError:
                # خطا در translate_orf ثبت شده؛ پردازش بقیه ادامه دارد.
                continue

            translated_orfs.append(translated_orf)

        return translated_orfs


