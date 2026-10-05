from pathlib import Path


def write_report(orfs):
    report_path = Path(__file__).resolve().parent / "report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        for index, orf in enumerate(orfs, start=1):
            if orf.is_complete:
                status = "Complete"
            else:
                status = "Incomplete"

            file.write(f"ID: BFG_{index:03d}\n")
            file.write(f"Strand: {orf.strand}\n")
            file.write(f"Frame: {orf.frame}\n")
            file.write(f"Start Position: {orf.start_pos}\n")
            file.write(f"Protein: {orf.protein}\n")
            file.write(f"Status: {status}\n\n")
