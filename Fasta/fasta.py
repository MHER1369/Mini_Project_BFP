import re
import logging

from Error_and_Logging.errors import FastaFormatError, InvalidSequenceError

logger = logging.getLogger("bioforge")

pattern = r"^>\s*(?P<id>\S+)\s*(?P<desc>.*)$"

def validate_sequence(sequence):
    valid_bases = "ATCG"
    for base in sequence.upper():
        if base not in valid_bases:
            raise InvalidSequenceError(f"Invalid DNA character: {base}")
        
def complement(sequence):
    translation_table = str.maketrans("ATCG", "TAGC")
    return sequence.upper().translate(translation_table)

def reverse_complement(sequence):
    result = complement(sequence)
    return result[::-1]

def rna(sequence):
    return sequence.upper().replace("T", "U")

def gc_content(sequence):
    if len(sequence) == 0:
        return 0
    seq = sequence.upper()
    gc_count = seq.count("G") + seq.count("C")
    return (gc_count / len(sequence)) * 100

def parse_fasta(file_path):
    records = []
    current_record = None
    seen_ids = set()
    seen_header = False

    def save_record(record):
        # خطای قابل‌بازیابی اینجا ثبت می‌شود تا رکوردهای سالم ادامه پیدا کنند.
        try:
            if not record["sequence"]:
                raise FastaFormatError("Header found without sequence")
            validate_sequence(record["sequence"])
        except (FastaFormatError, InvalidSequenceError) as error:
            logger.error("%s: skipping record %s: %s", file_path, record["id"], error)
            return
        records.append(record)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if line == "":
                    continue
                if line.startswith(">"):
                    seen_header = True
                    if current_record is not None:
                        save_record(current_record)
                    current_record = None

                    try:
                        match = re.match(pattern, line)
                        if match is None:
                            raise FastaFormatError("Invalid FASTA header")

                        sequence_id = match.group("id")
                        description = match.group("desc")
                        if sequence_id.startswith("organism=") or sequence_id.startswith("sample="):
                            raise FastaFormatError("Sequence ID is missing")
                    except FastaFormatError as error:
                        logger.error("%s: skipping record at line %s: %s", file_path, line_number, error)
                        continue

                    if sequence_id in seen_ids:
                        logger.warning("%s: Duplicate ID: %s", file_path, sequence_id)

                    seen_ids.add(sequence_id)

                    organism = None
                    sample = None
                    description_parts = []

                    for part in description.split():
                        if part.startswith("organism="):
                            organism = part.split("=", 1)[1]
                        elif part.startswith("sample="):
                            sample = part.split("=", 1)[1]
                        else:
                            description_parts.append(part)

                    description = " ".join(description_parts)

                    current_record = {
                        "id" : sequence_id,
                        "description" : description,
                        "organism" : organism,
                        "sample" : sample,
                        "sequence" : ""
                    }
                else:
                    if current_record is None:
                        if not seen_header:
                            raise FastaFormatError("Sequence found before first header")
                        continue

                    current_record["sequence"] += line

            if not seen_header:
                raise FastaFormatError("FASTA file is empty")
            
            if current_record is not None:
                save_record(current_record)

    except FileNotFoundError:
        raise
    return records
