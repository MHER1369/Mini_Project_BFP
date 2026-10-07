# BioForge

BioForge is a Python-based command-line pipeline for analyzing DNA sequences from FASTA files.

The project reads and validates FASTA records, performs DNA/RNA transformations, detects Open Reading Frames (ORFs) on both forward and reverse strands, translates ORFs into protein sequences, calculates molecular weights, filters proteins based on user-defined criteria, and generates a final report.

---

# 1. Features

BioForge provides the following functionality:

- FASTA file parsing and validation
- DNA sequence validation
- DNA complement and reverse-complement generation
- DNA to RNA conversion
- GC-content calculation
- Forward-strand ORF detection
- Reverse-strand ORF detection
- ORF translation
- Protein molecular-weight calculation
- Protein filtering by length
- Protein filtering by molecular weight
- Custom error handling
- Console and file logging
- Final report generation

---

# 2. Requirements / Installation

## Requirements

BioForge requires:

- Python 3.10 or newer
- No external Python packages are required.
- The project uses Python standard-library modules such as:
  - `pathlib`
  - `logging`
  - `re`
  - `math`

## Installation

Clone the repository:

```bash
git clone https://github.com/MHER1369/Mini_Project_BFP.git
```

Enter the project directory:

```bash
cd Mini_Project_BFP
```

No additional `pip install` command is required because the project currently uses only Python standard-library modules.

Make sure the project structure and biological data files are present before running the program.

---

# 3. How to Run

The main entry point is:

```text
Main/main.py
```

Run the program from the project root:

```bash
python Main/main.py
```

The program starts interactively and asks the user for:

1. FASTA file path
2. Minimum protein/ORF length
3. Minimum molecular weight

Example:

```text
Enter FASTA file path: Input/input.fasta
Enter minimum protein length: 3
Enter minimum molecular weight: 300
```

The program then executes the complete BioForge pipeline.

---

# 4. Command-Line Arguments

BioForge currently does **not** use command-line arguments such as `argparse`.

Instead, input values are requested interactively after the program starts.

Therefore, the normal execution command is:

```bash
python Main/main.py
```

The interactive inputs are:

| Input | Description |
|---|---|
| FASTA file path | Path to the input FASTA file |
| Minimum length | Minimum allowed protein/ORF length |
| Minimum weight | Minimum allowed molecular weight |

### FASTA path

The input path can be:

- An absolute path
- A project-relative path

Example:

```text
Input/input.fasta
```

or:

```text
C:\path\to\input.fasta
```

Supported FASTA extensions are:

```text
.fasta
.fa
.fna
```

---

# 5. Exit Codes

The program uses the return value of `main()` as its process exit status.

The expected exit codes are:

| Exit Code | Meaning |
|---:|---|
| `0` | Successful execution |
| `1` | Pipeline execution failed because of an error handled by the main program |

A successful execution therefore ends with:

```text
Process finished with exit code 0
```

The project uses:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

so the value returned by `main()` becomes the operating-system process exit code.

---

# 6. Project Structure

```text
Mini_Project_BFP/
│
├── BioForge/
│   └── data/
│       ├── codon_table.txt
│       └── amino_weights.txt
│
├── Error_and_Logging/
│   ├── errors.py
│   └── logger_config.py
│
├── Fasta/
│   └── fasta.py
│
├── Filters/
│   └── protein_filters.py
│
├── ORF/
│   ├── ORF.py
│   ├── forward_strand.py
│   └── reverse_strand.py
│
├── Translation/
│   └── protein_translation.py
│
├── Input/
│   └── input.fasta
│
├── Output/
│   ├── report.txt
│   └── bioforge.log
│
├── Main/
│   └── main.py
│
└── README.md
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `Fasta` | FASTA parsing and DNA validation |
| `ORF` | ORF data model and detection |
| `Translation` | Codon translation and molecular weight |
| `Filters` | Protein filtering |
| `Error_and_Logging` | Custom exceptions and logging |
| `Main` | Pipeline orchestration |
| `BioForge/data` | Biological reference data |
| `Input` | Example/input FASTA files |
| `Output` | Generated report and log |

---

# 7. Input Format

BioForge accepts standard FASTA files.

Each record starts with a header beginning with `>` followed by the sequence ID.

The header may also contain:

- `organism=`
- `sample=`
- A free-text description

## Example

```text
>seq001 organism=E_coli sample=A enzyme test
ATGCTTTCATAG
```

Another example:

```text
>seq002 organism=Human sample=B example sequence
CCCATGGGGTAA
```

A header without organism/sample information is also accepted:

```text
>seq003 some description
ATGCCCTA
```

The parser extracts the information into a record similar to:

```text
id          = seq001
organism    = E_coli
sample      = A
description = enzyme test
sequence    = ATGCTTTCATAG
```

DNA sequences may span multiple lines:

```text
>seq001 organism=E_coli sample=A
ATGCTT
TCATAG
```

The parser combines the sequence lines into a single sequence before analysis.

---

# 8. FASTA Parsing and Validation

The `Fasta` module is responsible for reading FASTA files and converting their contents into structured records.

The parser:

- Reads FASTA headers and sequences.
- Extracts sequence ID, organism, sample, and description.
- Supports multi-line DNA sequences.
- Validates DNA bases.
- Accepts only `A`, `T`, `C`, and `G`.
- Detects invalid FASTA headers.
- Detects sequences appearing before a FASTA header.
- Detects empty FASTA files.
- Warns about duplicate sequence IDs.
- Skips invalid records while allowing valid records to continue.

The main parsing function is:

```python
parse_fasta(file_path)
```

---

# 9. DNA Processing

The FASTA module provides independent DNA-processing functions:

- `validate_sequence()` — validates DNA characters.
- `complement()` — generates the complementary DNA sequence.
- `reverse_complement()` — generates the reverse-complement sequence.
- `rna()` — converts DNA to RNA by replacing `T` with `U`.
- `gc_content()` — calculates GC percentage.

These operations do not need to maintain object state, so they are implemented as functions.

---

# 10. ORF Detection

ORF detection uses an object-oriented structure.

The base class is:

```python
ORFDetector
```

Two specialized detectors inherit from it:

```text
ORFDetector
├── ForwardORFDetector
└── ReverseStrand
```

Both provide a common:

```python
detect()
```

interface while implementing different algorithms.

---

# 11. Forward ORF Detection

`ForwardORFDetector` analyzes the sequence in the forward direction.

It checks all three reading frames and searches for:

- Start codons
- Stop codons
- Codons between start and stop

For every complete ORF, an `ORF` object is created.

---

# 12. Reverse ORF Detection

`ReverseStrand` implements ORF detection for the reverse strand.

It checks three reading frames and identifies:

- Start codons
- Stop codons
- Complete ORFs
- Incomplete ORFs

If a start codon is found without a corresponding stop codon, the ORF is stored with:

```text
is_complete = False
```

Reverse coordinates are converted back to the original sequence coordinates.

---

# 13. Translation

The `TranslationData` class loads and validates:

```text
BioForge/data/codon_table.txt
BioForge/data/amino_weights.txt
```

The `Translator` class uses this data to:

- Translate RNA codons into amino acids.
- Stop at stop codons.
- Calculate protein molecular weight.
- Translate individual ORFs.
- Translate multiple ORFs.

Translation data is loaded once and reused through the corresponding objects.

---

# 14. Protein Filtering

BioForge provides two filters:

```python
LengthFilter
WeightFilter
```

Both inherit from:

```python
Filter
```

### LengthFilter

Keeps proteins whose length is greater than or equal to the configured minimum.

### WeightFilter

Keeps proteins whose molecular weight is greater than or equal to the configured minimum.

The filters use the common:

```python
filtering()
```

interface.

---

# 15. Why Classes vs. Functions?

Classes are used when an object needs to:

- Store related attributes.
- Maintain state.
- Keep configuration.
- Represent a project entity.
- Provide a common interface.
- Support inheritance or polymorphism.

Functions are used when an operation:

- Is independent.
- Does not need persistent state.
- Receives input and returns a result.
- Does not benefit from creating an object.

Examples of functions:

```python
validate_sequence()
complement()
reverse_complement()
rna()
gc_content()
```

Examples of classes:

```python
ORF
TranslationData
Translator
Filter
LengthFilter
WeightFilter
ORFDetector
ForwardORFDetector
ReverseStrand
```

For example, an `ORF` contains several related attributes:

```text
strand
frame
start_pos
protein
is_complete
molecular_weight
```

These attributes belong to one object, so a class is appropriate.

In contrast, `gc_content()` simply receives a sequence and calculates a value, so a function is simpler.

---

# 16. Four OOP Concepts Used in BioForge

BioForge uses the four main Object-Oriented Programming concepts.

## 16.1 Encapsulation

Encapsulation means keeping related data and behavior together inside an object.

For example, an `ORF` object stores information belonging to one ORF:

```text
strand
frame
start_pos
protein
is_complete
molecular_weight
```

`TranslationData` also encapsulates the codon table and amino-acid weights.

---

## 16.2 Inheritance

Inheritance allows a class to reuse or extend another class.

For example:

```text
ORFDetector
├── ForwardORFDetector
└── ReverseStrand
```

and:

```text
Filter
├── LengthFilter
└── WeightFilter
```

The child classes inherit the structure of their parent classes.

---

## 16.3 Polymorphism

Polymorphism allows different classes to provide the same interface with different implementations.

Both:

```python
ForwardORFDetector.detect()
ReverseStrand.detect()
```

use the same method name but implement different ORF detection algorithms.

Similarly:

```python
LengthFilter.filtering()
WeightFilter.filtering()
```

implement different filtering rules through the same method interface.

---

## 16.4 Abstraction

Abstraction means defining a general structure while hiding implementation details.

For example:

```python
class ORFDetector:
    def detect(self):
        raise NotImplementedError()
```

The base class defines the expected `detect()` behavior without implementing a specific detection algorithm.

The subclasses provide the actual implementation.

The same design is used for:

```python
class Filter:
    def filtering(self, proteins):
        raise NotImplementedError()
```

---

# 17. Ten Design Decisions

The following design decisions were made to keep BioForge modular, maintainable, and extensible.

## 1. Separate FASTA Parsing from the Main Pipeline

FASTA parsing is isolated in the `Fasta` module instead of being implemented directly in `main.py`.

**Reason:** This keeps input parsing independent from the rest of the analysis pipeline.

---

## 2. Use Functions for Stateless DNA Operations

Operations such as:

```text
complement
reverse_complement
rna
gc_content
```

are implemented as functions.

**Reason:** These operations do not need persistent state, so classes would add unnecessary complexity.

---

## 3. Represent ORFs as Objects

Each ORF is represented by an `ORF` object.

**Reason:** An ORF contains several related attributes that should remain together.

---

## 4. Use a Base ORF Detector

`ORFDetector` provides the common structure for ORF detection.

**Reason:** Forward and reverse detection share a common purpose and interface but use different algorithms.

---

## 5. Separate Forward and Reverse Detection

`ForwardORFDetector` and `ReverseStrand` implement separate algorithms.

**Reason:** Keeping the algorithms separate makes the code easier to understand and extend.

---

## 6. Use External Biological Data Files

Codon and amino-acid information is stored in:

```text
codon_table.txt
amino_weights.txt
```

**Reason:** Biological reference data can be updated independently from the Python source code.

---

## 7. Separate Translation Data from Translation Logic

`TranslationData` loads and validates biological data, while `Translator` performs translation.

**Reason:** This follows separation of responsibilities and prevents one class from handling unrelated tasks.

---

## 8. Use Filter Classes with a Common Interface

`LengthFilter` and `WeightFilter` inherit from `Filter`.

**Reason:** New filtering strategies can be added using the same interface without changing the main pipeline.

---

## 9. Use Custom Exceptions

BioForge defines:

```text
BioForgeError
FastaFormatError
InvalidSequenceError
DataFileError
```

**Reason:** Specific exception types make biological and input errors easier to identify and handle.

---

## 10. Use Centralized Logging

The project uses one shared logger configured through `setup_logger()`.

**Reason:** Centralized logging provides consistent information in both the console and `bioforge.log`, while preventing duplicate logging handlers.

---

# 18. Error Handling

BioForge defines the following custom exception hierarchy:

```text
BioForgeError
├── FastaFormatError
├── InvalidSequenceError
└── DataFileError
```

### `FastaFormatError`

Used for invalid FASTA structure.

### `InvalidSequenceError`

Used when an invalid DNA or RNA character is detected.

### `DataFileError`

Used for invalid or missing biological reference data.

Recoverable FASTA record errors are logged and skipped so that valid records can continue through the pipeline.

---

# 19. Logging

BioForge uses Python's standard `logging` module.

The logger is configured using:

```python
setup_logger()
```

Log output is written to:

```text
Output/bioforge.log
```

and displayed in the console.

A typical log contains information such as:

```text
INFO - BioForge pipeline started
INFO - Reading and validating FASTA file
INFO - Valid FASTA records: 2
INFO - Loading codon table and amino acid weights
INFO - Translation data loaded successfully
INFO - Processing record: seq001
INFO - Record seq001: found 1 Forward and 1 Reverse ORFs; translating
INFO - Record seq001: translated 2 ORFs
INFO - Filtering ORFs
INFO - Writing report
INFO - Report saved
INFO - Pipeline completed
```

Warnings and errors are also logged.

---

# 20. Output Format

The final report is written to:

```text
Output/report.txt
```

The report contains the filtered ORF results generated by the pipeline.

A representative report structure is:

```text
BioForge Report
===============

ORF ID: BFG_001
Sequence ID: seq001
Organism: E_coli
Sample: A
Strand: Forward
Frame: 0
Start Position: 0
Complete: True
Protein: M...
Molecular Weight: ...

----------------------------------------

ORF ID: BFG_002
Sequence ID: seq002
Organism: Human
Sample: B
Strand: Reverse
Frame: 1
Start Position: ...
Complete: True
Protein: ...
Molecular Weight: ...
```

Each reported ORF receives a unique BioForge identifier such as:

```text
BFG_001
BFG_002
BFG_003
```

The exact number of output records depends on the input FASTA file and the selected filtering thresholds.

---

# 21. Main Pipeline

The main module coordinates the complete workflow.

The pipeline is:

```text
User Input
    ↓
Input Validation
    ↓
FASTA Parsing
    ↓
DNA Validation
    ↓
DNA → RNA Processing
    ↓
Forward ORF Detection
    ↓
Reverse ORF Detection
    ↓
Translation
    ↓
Molecular Weight Calculation
    ↓
Length Filtering
    ↓
Weight Filtering
    ↓
Report Generation
```

`main.py` acts primarily as the coordinator rather than implementing every biological operation itself.

---

# 22. Data Files

## `codon_table.txt`

Contains RNA codons and their corresponding amino-acid codes.

Stop codons are represented by:

```text
*
```

Example:

```text
AUG M
UAA *
UAG *
UGA *
```

## `amino_weights.txt`

Contains one-letter amino-acid codes and molecular weights.

Example:

```text
A 71.037
C 103.009
D 115.027
```

The use of external data files makes biological reference data easier to maintain.

---

# 23. Protein Molecular Weight

Protein molecular weight is calculated from the amino-acid weights stored in `amino_weights.txt`.

The calculation starts with:

```text
18.015
```

representing the mass of water, and then adds the molecular weight of each amino acid in the protein.

The calculated value is stored in the corresponding ORF object.

---

# 24. File Paths and Portability

The project avoids hard-coded personal computer paths such as:

```text
C:\Users\SomeUser\...
```

The main pipeline uses `Path(__file__)` for project-relative locations such as the output report.

The FASTA input path is provided by the user and converted to a `Path` object.

This makes the project easier to move between computers.

The biological data files are currently referenced as:

```text
BioForge/data/codon_table.txt
BioForge/data/amino_weights.txt
```

These files must remain available in the expected project structure.

---

# 25. Team Members

BioForge was developed as a team project.

| Name | Role |
|---|---|
| Mohammad hosein Eteghadi | Developer |
| Arian Alaghband | Developer |
| Mahdi Soltani | Developer |
| Mohamadreza Layeghi | Developer |
| Nasim kolahghochi | Developer |

---

# 26. Summary

BioForge is a modular biological sequence-analysis pipeline implemented in Python.

The project combines:

- FASTA parsing and validation
- DNA/RNA processing
- Forward and reverse ORF detection
- Protein translation
- Molecular-weight calculation
- Configurable filtering
- Custom exception handling
- Centralized logging
- Structured report generation

The architecture uses functions for simple stateless operations and classes for data models, stateful components, shared interfaces, inheritance, and polymorphism.

The design focuses on:

- Separation of responsibilities
- Reusability
- Extensibility
- Maintainability
- Clear error handling
- External biological data management
- Portable project structure