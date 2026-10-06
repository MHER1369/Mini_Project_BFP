

from pathlib import Path
from math import isfinite

from Error_and_Logging.errors import DataFileError, FastaFormatError, InvalidSequenceError
from Error_and_Logging.logger_config import setup_logger
from Fasta.fasta import parse_fasta, rna, gc_content
from ORF.forward_strand import ForwardORFDetector
from ORF.reverse_strand import ReverseStrand
from Translation.protein_translation import TranslationData, Translator
from Filters.protein_filters import LengthFilter, WeightFilter


BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "Output" / "report.txt"


def get_input_file(logger):

    while True:
        value = input("Enter FASTA file path: ").strip().strip('"')

        if not value:
            logger.warning("FASTA file path cannot be empty.")
            continue

        try:
            path = Path(value).expanduser()
            if not path.is_absolute():
                path = BASE_DIR / path
            path = path.resolve()

            if not path.exists():
                logger.warning("File not found: %s", path)
                continue
            if not path.is_file():
                logger.warning("This path is not a file: %s", path)
                continue
        except (OSError, ValueError, RuntimeError) as error:
            logger.warning("Cannot use input path %r: %s", value, error)
            continue
        if path.suffix.lower() not in {".fasta", ".fa", ".fna"}:
            logger.warning("File must have .fasta, .fa or .fna extension.")
            continue

        return path


def get_min_length(logger):

    while True:
        value = input("Enter minimum protein length: ").strip()
        try:
            min_length = int(value)
        except ValueError:
            logger.warning("Minimum length must be an integer.")
            continue
        if min_length < 1:
            logger.warning("Minimum length must be at least 1.")
            continue
        return min_length


def get_min_weight(logger):

    while True:
        value = input("Enter minimum protein weight: ").strip()
        try:
            min_weight = float(value)
        except ValueError:
            logger.warning("Minimum weight must be a number.")
            continue
        if not isfinite(min_weight) or min_weight < 0:
            logger.warning("Minimum weight must be a finite, non-negative number.")
            continue
        return min_weight


def process_record(record, translator, logger):

    dna_sequence = record["sequence"]
    rna_sequence = rna(dna_sequence)

    print("\n" + "-" * 70)
    print(f"Sequence ID : {record['id']}")
    print(f"DNA length  : {len(dna_sequence)}")
    print(f"GC content  : {gc_content(dna_sequence):.2f}%")

    forward_orfs = ForwardORFDetector(rna_sequence).detect()
    reverse_orfs = ReverseStrand(rna_sequence).detect()
    orfs = forward_orfs + reverse_orfs

    logger.info(
        "Record %s: found %s Forward and %s Reverse ORFs; translating",
        record["id"], len(forward_orfs), len(reverse_orfs),
    )
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
    try:
        logger = setup_logger()
    except OSError as error:
        # اگر فایل لاگ باز نشود، خطا فقط در کنسول نمایش داده می‌شود.
        print(f"Cannot initialize logging: {error}")
        return 1
    logger.info("BioForge pipeline started")

    print("=" * 70)
    print("BioForge Pipeline")
    print("=" * 70)


    try:
        input_file = get_input_file(logger)
        min_length = get_min_length(logger)
        min_weight = get_min_weight(logger)
    except (EOFError, KeyboardInterrupt):
        logger.warning("Pipeline cancelled while reading user input.")
        return 1

    print("\nPipeline configuration:")
    print(f"  FASTA file       : {input_file}")
    print(f"  Minimum length   : {min_length}")
    print(f"  Minimum weight   : {min_weight}")

    logger.info(
        "Input: %s; minimum length: %s; minimum weight: %s",
        input_file, min_length, min_weight,
    )
    logger.info("Reading and validating FASTA file: %s", input_file)
    try:
        records = parse_fasta(input_file)
    except (FastaFormatError, OSError, UnicodeError) as error:
        logger.error("Pipeline stopped: cannot read FASTA file %s: %s", input_file, error)
        return 1
    if not records:
        logger.warning("Pipeline stopped: no valid FASTA records; report not updated.")
        return 1
    logger.info("Valid FASTA records: %s", len(records))

    logger.info("Loading codon table and amino acid weights")
    try:
        translation_data = TranslationData()
    except (DataFileError, OSError, UnicodeError) as error:
        logger.error("Pipeline stopped: cannot load translation data: %s", error)
        return 1
    translator = Translator(translation_data)
    logger.info("Translation data loaded successfully")

    all_orfs = []
    processed_records = 0
    for record in records:
        logger.info("Processing record: %s", record["id"])
        try:
            record_orfs = process_record(record, translator, logger)
        except InvalidSequenceError as error:
            logger.error("Skipping record %s: %s", record["id"], error)
            continue
        except DataFileError as error:
            logger.error("Pipeline stopped at record %s: %s", record["id"], error)
            return 1
        all_orfs.extend(record_orfs)
        processed_records += 1
        logger.info("Record %s: translated %s ORFs", record["id"], len(record_orfs))

    if processed_records == 0:
        logger.warning("Pipeline stopped: no records could be processed; report not updated.")
        return 1

    logger.info("Filtering %s ORFs", len(all_orfs))
    try:
        proteins, length_filtered, filtered_proteins, filtered_orfs = filter_orfs(
            all_orfs,
            min_length,
            min_weight,
            translation_data.amino_weights,
        )
    except DataFileError as error:
        logger.error("Pipeline stopped during filtering: %s", error)
        return 1
    logger.info(
        "Filtering results: %s after length filter; %s after weight filter",
        len(length_filtered), len(filtered_proteins),
    )

    logger.info("Writing report with IDs for %s ORFs: %s", len(filtered_orfs), REPORT_FILE)
    try:
        write_report(filtered_orfs, min_length, min_weight)
    except (OSError, UnicodeError) as error:
        logger.error("Pipeline stopped: cannot write report %s: %s", REPORT_FILE, error)
        return 1
    logger.info("Report saved: %s", REPORT_FILE)

    print("\n" + "=" * 70)
    print("Filtering Results")
    print("=" * 70)
    print(f"Total translated proteins : {len(proteins)}")
    print(f"After length filter       : {len(length_filtered)}")
    print(f"After length + weight     : {len(filtered_proteins)}")
    print(f"Report ORFs               : {len(filtered_orfs)}")
    print(f"Report file               : {REPORT_FILE}")
    logger.info(
        "Pipeline completed: %s records processed; %s records skipped during processing",
        processed_records, len(records) - processed_records,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
