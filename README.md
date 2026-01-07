# Harmony Indexfile Parser

A utility for extracting plate barcodes and measurement signatures from Revvity Harmony high-content imaging system export files.

## Background

When exporting image data from Harmony (Revvity's high-content analysis software), each plate measurement generates an `indexfile.txt` containing metadata about the acquired images. These indexfiles are organised in directories named with the plate barcode and timestamp.

This script parses the directory structure and extracts:
- **Plate barcode** - from the folder name (e.g., `30082` from `30082__2025-05-31T01_01_45-Measurement 1`)
- **Measurement signature** - the UUID from image URLs within the indexfile (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

The output CSV maps plate barcodes to their measurement signatures, which is useful for:
- Linking plate metadata to image analysis pipelines
- Batch processing of multi-plate screening experiments
- Tracking measurements across CellProfiler or other analysis workflows

## Installation

```bash
git clone https://github.com/yourusername/harmony-indexfile-parser.git
cd harmony-indexfile-parser

# Optional: create conda environment
conda env create -f environment.yml
conda activate harmony-indexfile-parser
```

No external dependencies required - uses Python standard library only.

## Usage

```bash
python parse_indexfiles.py -i /path/to/indexfiles/
```

### Expected directory structure

```
indexfiles/
├── 30082__2025-05-31T01_01_45-Measurement 1/
│   └── indexfile.txt
├── 30083__2025-05-31T02_15_30-Measurement 1/
│   └── indexfile.txt
└── 30084__2025-05-31T03_30_00-Measurement 1/
    └── indexfile.txt
```

### Output

The script generates `plates_measurement_signatures.csv` in the input directory:

```csv
Plate_Barcode,Measurement_Signature
30082,a1b2c3d4-e5f6-7890-abcd-ef1234567890
30083,b2c3d4e5-f6a7-8901-bcde-f12345678901
30084,c3d4e5f6-a7b8-9012-cdef-123456789012
```