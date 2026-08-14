# JustiTeX: Golden Open-Access Court Pleading Generator

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Court Grid](https://img.shields.io/badge/Pleading_Grid-28--Line_UTCR_Compliant-gold.svg)]()

**JustiTeX** is a modular, high-precision legal document assembly engine designed to convert plain Markdown or text files into pristine, court-compliant 28-line legal pleadings.

Built to bridge the Access to Justice gap, **JustiTeX** provides pro se litigants, legal aid clinics, and legal professionals with typesetting quality that matches or exceeds expensive commercial legal software.

---

## 🌟 Key Features

- **Frozen 28-Line Pleading Grid**: Sub-millimeter tracking matching official Uniform Trial Court Rules (UTCR) and Federal Rules of Civil Procedure (FRCP).
- **Automated Caption Parsing**: Automatically structures Plaintiff(s), Defendant(s), Court Name, Case Number, and Document Title into a locked single-spaced 10.5pt caption box.
- **Zero Widow/Orphan Enforcement**: Advanced LaTeX typesetting preventing floating headers or single-line page splits (`\widowpenalty=10000`, `\clubpenalty=10000`).
- **Markdown to Court PDF**: Write pleadings in clean Markdown format; JustiTeX handles grid alignment, page numbers, line numbers, and footers automatically.
- **Dual-Model Philosophy**: Free for pro se litigants, legal aid, and public defenders; funded through government legal aid grants (LSC TIG / State A2J) and enterprise law firm subscriptions.

---

## 🚀 Quick Start (CLI)

### Prerequisites

- Python 3.9+
- TeX Live / pdfTeX (e.g., `sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended`)

### Installation

```bash
git clone https://github.com/YourUsername/JustiTeX.git
cd JustiTeX
pip install -r requirements.txt
```

### Basic Usage

Generate a court-compliant PDF pleading from a Markdown document:

```bash
python3 -m justitex.compile --input examples/sample_motion.md --output build/Sample_Motion.pdf
```

---

## 🏗️ Project Architecture

```
JustiTeX/
├── templates/
│   ├── oregon_28line_FROZEN.tex      # Locked 28-line golden layout template
│   └── pleading.sty                  # Core TeX style & grid macros
├── justitex/
│   ├── __init__.py
│   ├── compile.py                    # Core Markdown -> LaTeX -> PDF compiler
│   └── parser.py                     # Caption & metadata parser
├── examples/
│   └── sample_motion.md              # Sample pro se motion
├── tests/
│   └── test_compile.py               # Automated layout & regression tests
├── LICENSE                           # GNU AGPLv3 License
└── README.md
```

---

## ⚖️ Licensing & Philosophy

JustiTeX is released under the **GNU Affero General Public License v3.0 (AGPLv3)**. 

### Why AGPLv3?
We believe access to justice tools should belong to the public. The AGPLv3 guarantees that any organization or vendor taking this core engine to build commercial software must keep their improvements open-source and freely accessible to the public.

- **Pro Se Litigants & Legal Aid**: 100% Free forever.
- **Government & Justice Innovation Grants**: Eligible for Legal Services Corporation (LSC) Technology Initiative Grants (TIG) and State Access to Justice innovation funds.

---

## 🤝 Contributing & Beta Testers

We are actively recruiting pro se advocates, legal aid technologists, and attorneys to beta test JustiTeX across different court jurisdictions.

To report a bug, request a state template, or contribute:
1. Open an issue on GitHub.
2. Submit a Pull Request following our `CONTRIBUTING.md` guidelines.
