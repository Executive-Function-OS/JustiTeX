from pathlib import Path
import unittest

from justitex.compile import JustiTeXCompiler


ROOT = Path(__file__).resolve().parents[1]


class TemplateFormattingTests(unittest.TestCase):
    def setUp(self):
        self.compiler = JustiTeXCompiler(court_format="state")

    def test_emotional_does_not_match_motion_title_keyword(self):
        title = "### Intentional Infliction of Emotional Distress & Bodily Harm"

        self.assertEqual(self.compiler.extract_document_title(title), "LEGAL PLEADING")
        self.assertEqual(self.compiler._escape_latex("COMPLAINT & MOTION"), r"COMPLAINT \& MOTION")

    def test_claim_labels_and_subtitles_render_as_two_line_macros(self):
        markdown = """### FIFTH CLAIM FOR RELIEF
Intentional Infliction of Emotional Distress & Bodily Harm

### SIXTH CLAIM FOR RELIEF
Security Deposit Accounting & Reservation of Rights (ORS 90.300 / ORS 71.3080)
"""

        latex = self.compiler.parse_markdown_to_latex(markdown, "state")

        self.assertIn(
            r"\claimheading{FIFTH CLAIM FOR RELIEF}{Intentional Infliction of Emotional Distress \& Bodily Harm}",
            latex,
        )
        self.assertIn(
            r"\claimheading{SIXTH CLAIM FOR RELIEF}{Security Deposit Accounting \& Reservation of Rights (ORS 90.300 / ORS 71.3080)}",
            latex,
        )

    def test_major_and_subsection_headings_use_named_styles(self):
        markdown = "## I. INTRODUCTION\n\n### Background\n\nBody text."

        latex = self.compiler.parse_markdown_to_latex(markdown, "state")

        self.assertIn(r"\romanhead{I. INTRODUCTION}", latex)
        self.assertIn(r"\subhead{Background}", latex)

    def test_state_caption_wins_over_federal_statute_citations(self):
        markdown = (
            "# IN THE CIRCUIT COURT OF THE STATE OF OREGON\n"
            "# FOR THE COUNTY OF CLACKAMAS\n\n"
            "The claim arises under 42 U.S.C. § 1983 and Oregon law."
        )

        self.assertEqual(self.compiler.detect_court_format(markdown), "state")

    def test_federal_format_requires_federal_court_caption(self):
        markdown = (
            "# IN THE UNITED STATES DISTRICT COURT\n"
            "# FOR THE DISTRICT OF OREGON\n\n"
            "Complaint for civil-rights violations."
        )

        self.assertEqual(self.compiler.detect_court_format(markdown), "federal")

    def test_adjacent_court_header_lines_share_one_centered_block(self):
        markdown = (
            "# IN THE CIRCUIT COURT OF THE STATE OF OREGON\n"
            "# FOR THE COUNTY OF CLACKAMAS"
        )

        latex = self.compiler.parse_markdown_to_latex(markdown, "state")

        self.assertEqual(latex.count(r"\begin{center}"), 1)
        self.assertIn("IN THE CIRCUIT COURT OF THE STATE OF OREGON \\", latex)
        self.assertIn("FOR THE COUNTY OF CLACKAMAS", latex)

    def test_separated_numbered_body_is_not_consumed_as_claim_subtitle(self):
        markdown = "### FIRST CLAIM FOR RELIEF\n\n1. Plaintiff alleges a numbered fact."

        latex = self.compiler.parse_markdown_to_latex(markdown, "state")

        self.assertIn(r"\claimheading{FIRST CLAIM FOR RELIEF}{}", latex)
        self.assertIn(r"\textbf{1.}", latex)

    def test_active_oregon_template_starts_first_page_at_line_seven(self):
        template = (ROOT / "templates" / "oregon_28line_FROZEN.tex").read_text()

        self.assertIn(r"\vspace*{6\gridline}", template)
        self.assertIn(r"\AtBeginDocument{\pleadingfirstpage}", template)
        self.assertIn(r"\newcommand{\claimheading}[2]", template)

    def test_federal_template_defines_shared_claim_heading_macro(self):
        template = (ROOT / "templates" / "federal_district_court.tex").read_text()

        self.assertIn(r"\newcommand{\claimheading}[2]", template)


if __name__ == "__main__":
    unittest.main()
