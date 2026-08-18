"""
JustiTeX Parser & Compiler Module
Converts raw Markdown / text legal drafts into court-grade 28-line Oregon legal pleadings (PDF & LaTeX).
"""

import os
import re
import sys
import shutil
import subprocess

class JustiTeXCompiler:
    def __init__(self, template_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if template_path is None:
            self.template_path = os.path.join(base_dir, "templates", "oregon_28line_FROZEN.tex")
        else:
            self.template_path = template_path

        self.sty_path = os.path.join(os.path.dirname(self.template_path), "pleading.sty")

    def parse_markdown_to_latex(self, md_content):
        """
        Parses Markdown text into Oregon UTCR 28-line legal pleading commands (\para, \subpara, \romanhead, etc.)
        """
        latex_lines = []
        para_counter = 1
        
        for line in md_content.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            # Heading 1 -> \romanhead
            if line_str.startswith("# "):
                title = line_str[2:].strip().upper()
                latex_lines.append(f"\\romanhead{{{title}}}")
            # Heading 2 -> \subhead
            elif line_str.startswith("## "):
                title = line_str[3:].strip()
                latex_lines.append(f"\\subhead{{{title}}}")
            # Heading 3 -> Bold Subhead
            elif line_str.startswith("### "):
                title = line_str[4:].strip()
                latex_lines.append(f"\\subhead{{{title}}}")
            # Numbered paragraph (e.g., "1. This is a paragraph")
            elif re.match(r'^\d+\.\s+', line_str):
                text_part = re.sub(r'^\d+\.\s+', '', line_str)
                text_part = self._escape_latex_chars(text_part)
                latex_lines.append(f"\\para{{{para_counter}}}{{{text_part}}}")
                para_counter += 1
            # Lettered sub-paragraph (e.g., "a. Sub-point")
            elif re.match(r'^[a-z]\.\s+', line_str):
                letter = line_str[0]
                text_part = line_str[2:].strip()
                text_part = self._escape_latex_chars(text_part)
                latex_lines.append(f"\\subpara{{{letter}}}{{{text_part}}}")
            # Regular paragraph
            else:
                clean_text = self._escape_latex_chars(line_str)
                latex_lines.append(f"\\para{{{para_counter}}}{{{clean_text}}}")
                para_counter += 1

        return "\n\n".join(latex_lines)

    def _escape_latex_chars(self, text):
        # Escape special LaTeX characters safely
        text = text.replace("&", r"\&").replace("#", r"\#").replace("$", r"\$").replace("%", r"\%")
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)
        return text

    def compile(self, input_md_path, output_pdf_path):
        if not os.path.exists(input_md_path):
            raise FileNotFoundError(f"Input file not found: {input_md_path}")

        with open(input_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        parsed_body = self.parse_markdown_to_latex(md_content)

        with open(self.template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

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

        # Copy pleading.sty to build output dir if available
        if os.path.exists(self.sty_path):
            shutil.copy(self.sty_path, os.path.join(out_dir, "pleading.sty"))

        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            f"-output-directory={out_dir}",
            tex_file
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pdf_file = os.path.join(out_dir, f"{base_name}.pdf")

        if os.path.exists(pdf_file):
            print(f"[JustiTeX] Compiled court-grade 28-line pleading: {pdf_file}")
            return pdf_file
        else:
            print(f"[JustiTeX] LaTeX compilation failed. Log file: {os.path.join(out_dir, base_name + '.log')}")
            return None


def main():
    if len(sys.argv) < 3:
        print("Usage: justitex-compile <input.md> <output.pdf>")
        sys.exit(1)
        
    compiler = JustiTeXCompiler()
    compiler.compile(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
