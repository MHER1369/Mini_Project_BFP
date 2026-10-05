import re
pattern = r">\s*(?P<id>\s+)\s*(?P<desc>.*)$"

def validate_sequence(sequence):
    valid_bases = "ATCG"
    for base in sequence.upper():
        if base not in valid_bases:
            raise ValueError("Invalid DNA sequence")
        
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

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                if line.startswith(">"):
                    match = re.match(pattern, line)
                    if match is None:
                        raise ValueError("Invaid FASTA header")
                    
                    sequence_id = match.group("id")
                    description = match.group("desc")

                    if sequence_id.startswith("oranism=") or sequence_id.startswith("sample="):
                        raise ValueError("Sequence ID is missing")
                    
                    if current_record is not None:
                        if current_record["sequence"] == "":
                            raise ValueError("Header found withouut sequence")
                        validate_sequence(current_record["sequence"])
                        records.append(current_record)
                    if sequence_id in seen_ids:
                        print("Warnin: Duplicate sequence ID") # در فایل لاگ ثبت می شود

                    seen_ids.add(sequence_id)

                    organism = None
                    sample= None
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
                        raise ValueError("Sequence found before first header")

                    current_record["sequence"] += line

            if current_record is None:
                raise ValueError("FASTA file is empty")
            
            if current_record["sequence"] == "":
                raise ValueError("Header found withot sequence")
            validate_sequence(current_record["sequence"])
            records.append(current_record)

    except FileNotFoundError:
        raise
    return records