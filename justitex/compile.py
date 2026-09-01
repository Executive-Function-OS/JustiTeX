"""
JustiTeX Core Compiler Engine
Converts Markdown legal drafts into court-compliant PDFs (Oregon UTCR 28-Line State & U.S. District Court Federal).
Features:
- Exact 2-column caption shell with vertical rule divider
- Centered and bolded section headings
- Dynamic filing date injection in signature and verification blocks
- Clean LaTeX signature rules
- Dynamic running footers
"""

import os
import sys
import subprocess
import argparse
import shutil
import re
from datetime import datetime

class JustiTeXCompiler:
    def __init__(self, template_path=None, court_format="auto"):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.court_format = court_format
        self.template_path = template_path

    def extract_document_title(self, md_text, default="LEGAL PLEADING"):
        lines = md_text.splitlines()
        for line in lines[:35]:
            clean = line.strip().strip("#* ").strip()
            if any(term in clean.upper() for term in ["COMPLAINT", "MOTION", "DECLARATION", "PETITION", "MEMORANDUM", "ANSWER", "REPLY", "NOTICE"]):
                clean_title = re.sub(r'[*_#]', '', clean).strip()
                if len(clean_title) > 65:
                    clean_title = clean_title[:62] + "..."
                return clean_title
        return default

    def detect_court_format(self, md_text):
        text_upper = md_text.upper()
        if "UNITED STATES DISTRICT COURT" in text_upper or "DISTRICT OF OREGON" in text_upper or "42 U.S.C." in text_upper or "PORTLAND DIVISION" in text_upper:
            return "federal"
        return "state"

    def inject_dynamic_dates(self, text):
        now = datetime.now()
        curr_day = now.strftime("%-d") if sys.platform != "win32" else now.strftime("%d").lstrip("0")
        full_date = now.strftime(f"%B {curr_day}, %Y")
        
        # Replace blanks like 'Executed on September ____, 2026' or 'Executed on September , 2026'
        text = re.sub(r'Executed on\s+[A-Za-z]+(?:\s+_+|\s*,|\s*\d*),\s*\d{4}', f"Executed on {full_date}", text)
        text = re.sub(r'Dated:\s*(?:_+|[A-Za-z]+\s+\d{1,2},\s+\d{4}|[A-Za-z]+\s+_+,\s+\d{4})', f"Dated: {full_date}", text)
        return text

    def parse_markdown_to_latex(self, md_text, court_format):
        # Inject dynamic execution dates
        md_text = self.inject_dynamic_dates(md_text)
        
        latex_lines = []
        lines = md_text.splitlines()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_str = line.strip()
            
            # Skip empty lines
            if not line_str:
                i += 1
                continue

            # Court Header (Top centered)
            if line_str.startswith("# ") and i < 5:
                court_title = line_str.strip("# *").strip()
                i += 1
                while i < len(lines) and (lines[i].startswith("## ") or lines[i].startswith("**")):
                    court_title += " \\\\\n" + lines[i].strip("# *").strip()
                    i += 1
                
                clean_court = self._escape_latex(court_title)
                latex_lines.append(f"\\begin{{center}}\\textbf{{\\large {clean_court}}}\\end{{center}}\\vspace{{1em}}")
                continue
            
            # Two-Column Caption Box parsing (for lines before the first major section)
            if line_str.startswith("**ANNIKA ERIKSSON") and i < 20:
                left_parties = [
                    r"\textbf{ANNIKA ERIKSSON and DONALD BUCKHOUT,}",
                    r"\hspace*{1.5em}\textit{Plaintiffs,}",
                    r"\vspace{0.5em}",
                    r"\textit{v.}",
                    r"\vspace{0.5em}",
                    r"\textbf{CITY OF OREGON CITY,} an Oregon municipal corporation; \textbf{TONY KONKOL,} individually; \textbf{TODD KENNEDY,} individually; \textbf{ASHLEY FRAIJO,} individually; \textbf{ALEXANDRA TROUTMAN,} individually; \textbf{RAMON HENDERSON,} individually; and \textbf{VANCE WALKER,} individually,",
                    r"\hspace*{1.5em}\textit{Defendants.}"
                ]
                
                right_info = [
                    r"\textbf{Case No. \underline{\hspace{1.8in}}}",
                    r"\vspace{0.75em}",
                    r"\textbf{COMPLAINT FOR VIOLATIONS OF CIVIL RIGHTS}",
                    r"\textit{(42 U.S.C. \S\ 1983; Americans with Disabilities Act, Title II; Rehabilitation Act \S\ 504; Fair Housing Act, 42 U.S.C. \S\ 3617)}",
                    r"\vspace{0.75em}",
                    r"\textbf{DEMAND FOR JURY TRIAL}"
                ]
                
                left_tex = " \\\\\n".join(left_parties)
                right_tex = " \\\\\n".join(right_info)
                
                caption_tex = f"""
\\begin{{singlespace}}
\\noindent
\\begin{{minipage}}[t]{{0.50\\textwidth}}
\\small\\raggedright
{left_tex}
\\end{{minipage}}%
\\hspace{{0.03\\textwidth}}%
\\vrule width 0.75pt%
\\hspace{{0.03\\textwidth}}%
\\begin{{minipage}}[t]{{0.44\\textwidth}}
\\small\\raggedright
{right_tex}
\\end{{minipage}}
\\end{{singlespace}}
\\vspace{{1em}}
\\hrule
\\vspace{{1em}}
"""
                latex_lines.append(caption_tex)
                while i < len(lines) and not lines[i].startswith("## I. INTRODUCTION") and not lines[i].startswith("# I. INTRODUCTION"):
                    i += 1
                continue
                
            # Section Headings (Level 1: Centered & Bolded)
            if line_str.startswith("## ") or line_str.startswith("# "):
                title = line_str.strip("# *").strip()
                clean_title = self._escape_latex(title)
                latex_lines.append(f"\\vspace{{1.25em}}\\begin{{center}}\\textbf{{\\large {clean_title}}}\\end{{center}}\\vspace{{0.5em}}")
            # Sub-Section Headings (Level 2: Centered for claims, left-aligned bold for topics)
            elif line_str.startswith("### "):
                title = line_str.strip("# *").strip()
                clean_title = self._escape_latex(title)
                if any(k in title.upper() for k in ["COUNT ", "FIRST CLAIM", "SECOND CLAIM", "THIRD CLAIM", "FOURTH CLAIM", "FIFTH CLAIM", "SIXTH CLAIM", "SEVENTH CLAIM", "EIGHTH CLAIM"]):
                    latex_lines.append(f"\\vspace{{1em}}\\begin{{center}}\\textbf{{\\normalsize {clean_title}}}\\end{{center}}\\vspace{{0.4em}}")
                else:
                    latex_lines.append(f"\\vspace{{0.75em}}\\noindent\\textbf{{{clean_title}}}\\par\\vspace{{0.25em}}")
            # Horizontal rule
            elif line_str.startswith("---"):
                latex_lines.append("\\vspace{0.75em}\\hrule\\vspace{0.75em}")
            # Signature underscore lines (e.g. "____________________")
            elif re.match(r'^_{5,}$', line_str):
                latex_lines.append("\\vspace{1.5em}\\noindent\\rule{3in}{0.5pt}\\par\\vspace{0.25em}")
            # Skip markdown table rows in body text
            elif line_str.startswith("|"):
                i += 1
                continue
            # Numbered paragraph (e.g. "1. Plaintiff...")
            elif re.match(r'^\d+\.\s+', line_str):
                m = re.match(r'^(\d+)\.\s+(.*)', line_str)
                num = m.group(1)
                text = self._escape_latex(m.group(2))
                latex_lines.append(f"\\noindent\\textbf{{{num}.}}\\hspace{{0.5em}}{text}\\par\\vspace{{0.5em}}")
            # Lettered sub-paragraph (e.g. "a. Sub-point")
            elif re.match(r'^[a-z]\.\s+', line_str):
                m = re.match(r'^([a-z])\.\s+(.*)', line_str)
                letter = m.group(1)
                text = self._escape_latex(m.group(2))
                latex_lines.append(f"\\hspace*{{0.3in}}\\textbf{{{letter}.}}\\hspace{{0.5em}}{text}\\par\\vspace{{0.3em}}")
            # Blockquote
            elif line_str.startswith(">"):
                quote_text = self._escape_latex(line_str[1:].strip())
                latex_lines.append(f"\\begin{{quote}}\\textit{{{quote_text}}}\\end{{quote}}")
            # Normal text / paragraph
            else:
                clean_text = self._escape_latex(line_str)
                latex_lines.append(f"{clean_text}\\par\\vspace{{0.5em}}")
            i += 1

        return "\n".join(latex_lines)

    def _escape_latex(self, text):
        text = text.replace("&", "\\&").replace("#", "\\#").replace("$", "\\$").replace("%", "\\%").replace("_", "\\_")
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)
        text = text.replace("&nbsp;", " ")
        return text

    def compile(self, input_md_path, output_pdf_path, template_path=None, court_format="auto"):
        if not os.path.exists(input_md_path):
            raise FileNotFoundError(f"Input file not found: {input_md_path}")

        with open(input_md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        if court_format == "auto":
            court_format = self.detect_court_format(md_text)

        if template_path is None:
            if court_format == "federal":
                template_path = os.path.join(self.base_dir, "templates", "federal_district_court.tex")
            else:
                template_path = os.path.join(self.base_dir, "templates", "oregon_28line_FROZEN.tex")

        doc_title = self.extract_document_title(md_text)
        print(f"[JustiTeX] Court Format: {court_format.upper()} | Footer Title: '{doc_title}'")

        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        template_content = template_content.replace("DYNAMIC_FOOTER_TITLE", doc_title)
        template_content = template_content.replace("Defendant's Consolidated Petition for Hardship Relief", doc_title)

        parsed_body = self.parse_markdown_to_latex(md_text, court_format)

        if "\\end{document}" in template_content:
            full_tex = template_content.replace("\\end{document}", f"{parsed_body}\n\\end{{document}}")
        else:
            full_tex = template_content + "\n" + parsed_body + "\n\\end{document}\n"

        out_dir = os.path.dirname(os.path.abspath(output_pdf_path))
        os.makedirs(out_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(output_pdf_path))[0]
        tex_file = os.path.join(out_dir, f"{base_name}.tex")

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(full_tex)

        sty_path = os.path.join(self.base_dir, "templates", "pleading.sty")
        if os.path.exists(sty_path):
            shutil.copy(sty_path, os.path.join(out_dir, "pleading.sty"))

        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={out_dir}", tex_file]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pdf_file = os.path.join(out_dir, f"{base_name}.pdf")
        if os.path.exists(pdf_file):
            print(f"✅ [JustiTeX] Successfully generated {court_format.upper()} pleading PDF: {pdf_file}")
            return pdf_file
        else:
            print(f"❌ [JustiTeX] Compilation failed. See log: {os.path.join(out_dir, base_name + '.log')}")
            return None


def main():
    parser = argparse.ArgumentParser(description="JustiTeX Pleading Paper & Appellate Compiler")
    parser.add_argument("input", help="Path to input Markdown pleading file")
    parser.add_argument("output", help="Path to output compiled PDF file")
    parser.add_argument("--format", choices=["auto", "federal", "state"], default="auto", help="Court format")
    parser.add_argument("--template", help="Custom LaTeX template path")
    args = parser.parse_args()

    compiler = JustiTeXCompiler()
    compiler.compile(args.input, args.output, template_path=args.template, court_format=args.format)

if __name__ == "__main__":
    main()
