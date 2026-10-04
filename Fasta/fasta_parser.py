import re

pattern = r"^\>\s*(?P<id>\S+)\s*(?P<desc>.*)$"

def parse_fasta(file_path):

    try: #مدیریت خطا در بخش logging تکمیل شود
        with open(file_path, "r") as file:

            records = []

            current_record = None

            while True:
                line = file.readline()
                if line == "" :
                    break

                if line.strip() == "":
                    continue

                if line.startswith(">") :
                    match = re.match(pattern, line)
            
                    if match is None:
                        raise ValueError("Invalid FASTA header")
                    sequence_id = match.group("id")
                    description = match.group("desc")

                    if sequence_id.startswith("organism=") or sequence_id.startswith("sample="):
                        raise ValueError("Invalid FASTA header: sequence ID is missing")

                    for record in records:
                        if record["id"] == sequence_id:
                            print("Warning: Duplicate sequence ID") #این هشدار باید در لاگین جایگزین شود

                    if current_record is not None :
                        if current_record["id"] == sequence_id:
                            print("Warning: Duplicate sequence ID") # این هشدار باید در لاگین جایگزین شود

                    organism = None

                    for part in description.split():
                        if part.startswith("organism="):
                            organism = part.split("=")[1]
                    
                    if current_record is not None :
                        if current_record["sequence"] == "":
                            raise ValueError("Header found without sequence")
                        records.append(current_record)
        
                    sample = None

                    for part in description.split():
                        if part.startswith("sample="):
                            sample = part.split("=")[1]


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
            
                    current_record["sequence"] += line.strip()

            if len(records) == 0 and current_record is None:
                raise ValueError("FASTA file is empty")

            if current_record is not None :
                if current_record["sequence"] == "":
                    raise ValueError("Header found without sequence")
                records.append(current_record)

    except FileNotFoundError:
        raise ValueError("FASTA file not found")

    return records
