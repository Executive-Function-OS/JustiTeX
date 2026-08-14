"""
JustiTeX Core Compiler Engine
Converts Markdown legal drafts into court-compliant 28-line LaTeX PDFs.
"""

import os
import sys
import subprocess
import argparse
import shutil
import re

def compile_markdown_to_pdf(input_md_path, output_pdf_path, template_path=None):
    """
    Compiles a Markdown pleading into a 28-line UTCR-compliant PDF using pdflatex.
    """
    if not os.path.exists(input_md_path):
        raise FileNotFoundError(f"Input file not found: {input_md_path}")
        
    if template_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(base_dir, "templates", "oregon_28line_FROZEN.tex")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Read markdown content
    with open(input_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Simple conversion logic for core text block
    tex_body = []
    for line in md_text.splitlines():
        if line.startswith("# "):
            tex_body.append(f"\\section*{{{line[2:].strip()}}}")
        elif line.startswith("## "):
            tex_body.append(f"\\subsection*{{{line[3:].strip()}}}")
        elif line.startswith("### "):
            tex_body.append(f"\\subsubsection*{{{line[4:].strip()}}}")
        elif line.strip() == "":
            tex_body.append("\\par\\vspace{0.5em}")
        else:
            clean_line = line.replace("&", "\\&").replace("_", "\\_").replace("%", "\\%")
            clean_line = re.sub(r'\*(.*?)\*', r'\\textit{\1}', clean_line)
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', clean_line)
            tex_body.append(clean_line)
            
    body_content = "\n".join(tex_body)

    # Read base template
    with open(template_path, "r", encoding="utf-8") as f:
        tex_template = f.read()

    # Replace end{document} with content + end{document}
    if "\\end{document}" in tex_template:
        full_tex = tex_template.replace("\\end{document}", f"{body_content}\n\\end{{document}}")
    else:
        full_tex = tex_template + "\n\\begin{document}\n" + body_content + "\n\\end{document}\n"

    # Temporary build directory
    build_dir = os.path.dirname(os.path.abspath(output_pdf_path))
    os.makedirs(build_dir, exist_ok=True)
    
    tex_filename = os.path.join(build_dir, "temp_pleading.tex")
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(full_tex)

    # Copy dependency pleading.sty to build dir if present
    template_dir = os.path.dirname(template_path)
    sty_path = os.path.join(template_dir, "pleading.sty")
    if os.path.exists(sty_path):
        shutil.copy(sty_path, os.path.join(build_dir, "pleading.sty"))

    # Invoke pdflatex
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={build_dir}",
        tex_filename
    ]
    
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    generated_pdf = os.path.join(build_dir, "temp_pleading.pdf")
    
    if os.path.exists(generated_pdf):
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
        os.rename(generated_pdf, output_pdf_path)
        print(f"Successfully compiled JustiTeX pleading: {output_pdf_path}")
        return True
    else:
        print(f"Failed to generate PDF. Check LaTeX logs at {os.path.join(build_dir, 'temp_pleading.log')}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JustiTeX 28-Line Legal Pleading Compiler")
    parser.add_argument("--input", required=True, help="Path to input Markdown pleading file")
    parser.add_argument("--output", required=True, help="Path to output compiled PDF file")
    parser.add_argument("--template", help="Optional path to custom .tex template")
    args = parser.parse_args()

    compile_markdown_to_pdf(args.input, args.output, args.template)
