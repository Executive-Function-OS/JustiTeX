"""
JustiTeX Core Compiler Engine
Converts Markdown legal drafts into court-compliant PDFs (Oregon UTCR 28-Line State & U.S. District Court Federal).
"""

import os
import sys
import subprocess
import argparse
import shutil
import re

class JustiTeXCompiler:
    def __init__(self, template_path=None, court_format="auto"):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.court_format = court_format
        self.template_path = template_path

    def extract_document_title(self, md_text, default="LEGAL PLEADING"):
        """
        Extracts the official document title from markdown headings or caption.
        """
        # Look for explicit title tags or bold capitalized titles
        lines = md_text.splitlines()
        for line in lines[:30]:
            clean = line.strip().strip("#* ").strip()
            # Common pleading titles
            if any(term in clean.upper() for term in ["COMPLAINT", "MOTION", "DECLARATION", "PETITION", "MEMORANDUM", "ANSWER", "REPLY", "NOTICE"]):
                # Clean up markdown formatting
                clean_title = re.sub(r'[*_#]', '', clean).strip()
                # Truncate if excessively long for a running footer
                if len(clean_title) > 65:
                    clean_title = clean_title[:62] + "..."
                return clean_title
                
        return default

    def detect_court_format(self, md_text):
        """
        Detects whether the draft is for U.S. District Court (Federal) or Oregon State Court (UTCR).
        """
        text_upper = md_text.upper()
        if "UNITED STATES DISTRICT COURT" in text_upper or "DISTRICT OF OREGON" in text_upper or "42 U.S.C." in text_upper or "PORTLAND DIVISION" in text_upper:
            return "federal"
        return "state"

    def parse_markdown_to_latex(self, md_text, court_format):
        """
        Converts markdown text to clean LaTeX with proper paragraph spacing,
        preserving headings and numbered paragraphs without numbering captions.
        """
        latex_lines = []
        in_caption = False
        
        for line in md_text.splitlines():
            line_str = line.strip()
            if not line_str:
                latex_lines.append("")
                continue

            # Heading 1 -> Centered Roman Section or Big Header
            if line_str.startswith("# "):
                title = line_str[2:].strip()
                clean_title = self._escape_latex(title)
                latex_lines.append(f"\\begin{{center}}\\textbf{{\\large {clean_title}}}\\end{{center}}\\vspace{{0.5em}}")
            # Heading 2 -> Section
            elif line_str.startswith("## "):
                title = line_str[3:].strip()
                clean_title = self._escape_latex(title)
                latex_lines.append(f"\\vspace{{0.75em}}\\noindent\\textbf{{{clean_title}}}\\par\\vspace{{0.25em}}")
            # Heading 3 -> Subsection
            elif line_str.startswith("### "):
                title = line_str[4:].strip()
                clean_title = self._escape_latex(title)
                latex_lines.append(f"\\vspace{{0.5em}}\\noindent\\textbf{{\\textit{{{clean_title}}}}}\\par\\vspace{{0.2em}}")
            # Horizontal rule
            elif line_str.startswith("---"):
                latex_lines.append("\\vspace{0.5em}\\hrule\\vspace{0.5em}")
            # Tables
            elif line_str.startswith("|"):
                # Simple table line formatting
                continue
            # Numbered paragraph (e.g. "1. Plaintiff is...")
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
            # Normal paragraph
            else:
                clean_text = self._escape_latex(line_str)
                latex_lines.append(f"{clean_text}\\par\\vspace{{0.5em}}")

        return "\n".join(latex_lines)

    def _escape_latex(self, text):
        # Escape special LaTeX characters safely
        text = text.replace("&", r"\&").replace("#", r"\#").replace("$", r"\$").replace("%", r"\%").replace("_", r"\_")
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)
        text = text.replace("&nbsp;", " ")
        return text

    def compile(self, input_md_path, output_pdf_path, template_path=None, court_format="auto"):
        if not os.path.exists(input_md_path):
            raise FileNotFoundError(f"Input file not found: {input_md_path}")

        with open(input_md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        # Determine court format
        if court_format == "auto":
            court_format = self.detect_court_format(md_text)

        # Select template
        if template_path is None:
            if court_format == "federal":
                template_path = os.path.join(self.base_dir, "templates", "federal_district_court.tex")
            else:
                template_path = os.path.join(self.base_dir, "templates", "oregon_28line_FROZEN.tex")

        # Extract document title for footer
        doc_title = self.extract_document_title(md_text)
        print(f"[JustiTeX] Court Format: {court_format.upper()} | Footer Title: '{doc_title}'")

        # Read template
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Inject dynamic footer title
        template_content = template_content.replace("DYNAMIC_FOOTER_TITLE", doc_title)
        template_content = template_content.replace("Defendant's Consolidated Petition for Hardship Relief", doc_title)

        # Parse body
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

        # Copy pleading.sty if needed
        sty_path = os.path.join(self.base_dir, "templates", "pleading.sty")
        if os.path.exists(sty_path):
            shutil.copy(sty_path, os.path.join(out_dir, "pleading.sty"))

        # Run pdflatex twice for LastPage reference
        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={out_dir}", tex_file]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
