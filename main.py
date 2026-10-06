

from pathlib import Path

from Fasta.fasta import parse_fasta, rna, gc_content
from ORF.forward_strand import ForwardORFDetector
from ORF.reverse_strand import ReverseStrand
from Translation.protein_translation import TranslationData, Translator
from Filters.protein_filters import LengthFilter, WeightFilter


BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "Output" / "report.txt"


def get_input_file():

    while True:
        value = input("Enter FASTA file path: ").strip().strip('"')

        if not value:
            print("Error: FASTA file path cannot be empty.")
            continue

        path = Path(value).expanduser()
        if not path.is_absolute():
            path = BASE_DIR / path
        path = path.resolve()

        if not path.exists():
            print(f"Error: File not found: {path}")
            continue
        if not path.is_file():
            print(f"Error: This path is not a file: {path}")
            continue
        if path.suffix.lower() not in {".fasta", ".fa", ".fna"}:
            print("Error: File must have .fasta, .fa or .fna extension.")
            continue

        return path


def get_min_length():

    while True:
        value = input("Enter minimum protein length: ").strip()
        try:
            min_length = int(value)
        except ValueError:
            print("Error: Minimum length must be an integer.")
            continue
        if min_length < 1:
            print("Error: Minimum length must be at least 1.")
            continue
        return min_length


def get_min_weight():

    while True:
        value = input("Enter minimum protein weight: ").strip()
        try:
            min_weight = float(value)
        except ValueError:
            print("Error: Minimum weight must be a number.")
            continue
        if min_weight < 0:
            print("Error: Minimum weight cannot be negative.")
            continue
        return min_weight


def process_record(record, translator):

    dna_sequence = record["sequence"]
    rna_sequence = rna(dna_sequence)

    print("\n" + "-" * 70)
    print(f"Sequence ID : {record['id']}")
    print(f"DNA length  : {len(dna_sequence)}")
    print(f"GC content  : {gc_content(dna_sequence):.2f}%")

    forward_orfs = ForwardORFDetector(rna_sequence).detect()
    reverse_orfs = ReverseStrand(rna_sequence).detect()
    orfs = forward_orfs + reverse_orfs

    translated_orfs = translator.translate_orfs(orfs)

    for orf in translated_orfs:
        orf.source = record["id"]
        orf.organism = record.get("organism") or "Unknown"

    print(f"Forward ORFs: {len(forward_orfs)}")
    print(f"Reverse ORFs: {len(reverse_orfs)}")
    print(f"Total ORFs  : {len(translated_orfs)}")

    return translated_orfs


def filter_orfs(orfs, min_length, min_weight, weights):

    proteins = [orf.protein for orf in orfs]

    length_filter = LengthFilter(min_length)
    length_filtered = length_filter.filtering(proteins)

    weight_filter = WeightFilter(weights, min_weight)
    filtered_proteins = weight_filter.filtering(length_filtered)

    remaining = list(filtered_proteins)
    filtered_orfs = []

    for orf in orfs:
        if orf.protein in remaining:
            filtered_orfs.append(orf)
            remaining.remove(orf.protein)

    return proteins, length_filtered, filtered_proteins, filtered_orfs


def format_report(orfs, min_length, min_weight):

    lines = [
        "BioForge Report",
        f"Total ORFs: {len(orfs)}",
        "",
        "ID       Source   Organism   Strand    Frame   Start   Status      Weight     Protein",
        "------------------------------------------------------------------------------------------",
    ]

    for index, orf in enumerate(orfs, start=1):
        status = "Complete" if orf.is_complete else "Incomplete"
        lines.append(
            f"BFG_{index:03d} "
            f"{orf.source:<8} "
            f"{orf.organism:<10} "
            f"{orf.strand:<9} "
            f"{orf.frame:<7} "
            f"{orf.start_pos:<7} "
            f"{status:<11} "
            f"{orf.molecular_weight:>9.3f}  "
            f"{orf.protein}"
        )

    return "\n".join(lines) + "\n"


def write_report(orfs, min_length, min_weight):

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        format_report(orfs, min_length, min_weight),
        encoding="utf-8",
    )


def main():
    print("=" * 70)
    print("BioForge Pipeline")
    print("=" * 70)


    input_file = get_input_file()
    min_length = get_min_length()
    min_weight = get_min_weight()

    print("\nPipeline configuration:")
    print(f"  FASTA file       : {input_file}")
    print(f"  Minimum length   : {min_length}")
    print(f"  Minimum weight   : {min_weight}")

    records = parse_fasta(input_file)
    translation_data = TranslationData()
    translator = Translator(translation_data)

    all_orfs = []
    for record in records:
        all_orfs.extend(process_record(record, translator))

    proteins, length_filtered, filtered_proteins, filtered_orfs = filter_orfs(
        all_orfs,
        min_length,
        min_weight,
        translation_data.amino_weights,
    )

    write_report(filtered_orfs, min_length, min_weight)

    print("\n" + "=" * 70)
    print("Filtering Results")
    print("=" * 70)
    print(f"Total translated proteins : {len(proteins)}")
    print(f"After length filter       : {len(length_filtered)}")
    print(f"After length + weight     : {len(filtered_proteins)}")
    print(f"Report ORFs               : {len(filtered_orfs)}")
    print(f"Report file               : {REPORT_FILE}")
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
