from setuptools import setup, find_packages

setup(
    name="justitex",
    version="0.1.0",
    description="Open-Source Oregon 28-Line UTCR Legal Pleading Engine (Markdown to LaTeX/PDF)",
    author="Annika Eriksson / Precedent Systems",
    license="AGPL-3.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "justitex=justitex.compile:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.8",
)
