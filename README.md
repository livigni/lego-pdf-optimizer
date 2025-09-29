# 🧱 LEGO PDF Optimizer (`lego-pdf-optimizer`)

A Python script designed to optimize digital LEGO® instruction manuals in PDF format. Many digital LEGO manuals use blue or dark gray backgrounds which waste a significant amount of ink when printed.

This tool analyzes the raw content stream of the PDF and replaces all color commands (fill and stroke) with a solid black color, preserving all construction details (text, piece numbers, arrows) while effectively making the background white.

Result: A print-optimized PDF for economical printing.

## 🚀 Usage

### Prerequisites

You must have Python 3 and the `pypdf` library installed.

```bash
pip install pypdf
```

### Execution
Run the script from the command line, providing the name of the LEGO PDF file as an argument.


```bash
python3 lego_pdf.py <input_file_name.pdf>
```

Example:

```bash
python3 lego_pdf.py 6099685.pdf
```
A new file will be generated with the _optimized suffix (e.g., 6099685_optimized.pdf).

## How It Works
The tool acts directly on the embedded PostScript language within the PDF (the "content stream") using the pypdf library for parsing and reconstruction.

Content Extraction: It analyzes the /Contents object of each page, handling complex PDF structures (indirect references, arrays, and binary data) to extract the command stream.

Color Replacement Strategy: It uses regular expressions (regex) to find and replace all color setting commands (both Fill and Stroke) in both CMYK (K, C) and RGB (rg, RG) formats.

Print Optimization: All found colors are forced to solid black (0.0 0.0 0.0 1.0 K or 0.0 0.0 0.0 rg/RG). This prevents the blue details from turning white (which would make them disappear) while allowing the colored background to render as white.

Reconstruction: The modified content is re-inserted into the page, using specific pypdf objects (NameObject, StreamObject) to ensure compatibility, and the new PDF is saved.
