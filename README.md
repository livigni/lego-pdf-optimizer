# 🧱 LEGO PDF Optimizer (`lego-pdf-optimizer`)

A Python script designed to optimize digital LEGO® instruction manuals in PDF format. Many digital LEGO manuals use blue or dark gray backgrounds which waste a significant amount of ink when printed.

This tool analyzes the raw content stream of the PDF and replaces all color commands (fill and stroke) with a solid black color, preserving all construction details (text, piece numbers, arrows) while effectively making the background white.

Result: A print-optimized PDF for economical printing.

## 🚀 Usage

### Prerequisites

You must have Python 3 and the `pypdf` library installed.

```bash
pip install pypdf
