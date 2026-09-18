import os, shutil, zipfile

src_dir = '/home/annika/JustiTeX/templates'
pack_dir = '/home/annika/JustiTeX/template_pack_staging'
os.makedirs(pack_dir, exist_ok=True)

shutil.copy('/home/annika/JustiTeX/templates/oregon_28line_FROZEN.tex', os.path.join(pack_dir, 'oregon_pleading_28line.tex'))
shutil.copy('/home/annika/JustiTeX/templates/pleading.sty', os.path.join(pack_dir, 'pleading.sty'))
shutil.copy('/home/annika/JustiTeX/templates/federal_district_court.tex', os.path.join(pack_dir, 'federal_pleading_template.tex'))
shutil.copy('/home/annika/JustiTeX/examples/sample_motion.md', os.path.join(pack_dir, 'sample_motion.md'))

quickstart = """# JustiTeX Open-Access Template Pack (Beta)

Thank you for downloading the JustiTeX open-source legal typesetting template pack.

## Files Included:
1. `oregon_pleading_28line.tex` — Official Oregon UTCR 2.010 compliant 28-line pleading paper template.
2. `pleading.sty` — Core LaTeX grid geometry and margin rule definitions.
3. `federal_pleading_template.tex` — Federal District Court pleading template (FRCP / Local Rules).
4. `sample_motion.md` — Sample pro se motion layout.

## How to Compile:
To compile your document into an e-filing ready PDF using pdfTeX or XeLaTeX:

pdflatex -interaction=nonstopmode oregon_pleading_28line.tex

or

xelatex oregon_pleading_28line.tex

## Open-Source Access to Justice
JustiTeX is released under the GNU AGPLv3 license. Free for pro se litigants, legal aid clinics, and community legal workers.
"""

with open(os.path.join(pack_dir, 'README.md'), 'w') as f:
    f.write(quickstart)

zip_path = '/home/annika/JustiTeX/justitex-oregon-template-pack.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(pack_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, pack_dir)
            zipf.write(file_path, arcname)

if os.path.exists('/home/annika/JustiTeX/web'):
    shutil.copy(zip_path, '/home/annika/JustiTeX/web/justitex-oregon-template-pack.zip')

print(f"Successfully created {zip_path} ({os.path.getsize(zip_path):,} bytes)")
