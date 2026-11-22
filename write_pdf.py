# Step1: Install tectonic & Import deps

from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil


@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to professional IEEE-style PDF."""

    if shutil.which("tectonic") is None:
        raise RuntimeError(
            "tectonic is not installed. Install it first on your system."
        )

    try:

        # =========================================
        # Step2: Create output directory
        # =========================================

        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        # =========================================
        # Step3: Setup filenames
        # =========================================

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        tex_file = output_dir / tex_filename

        # =========================================
        # Step4: IEEE Template
        # =========================================

        ieee_template = f"""
\\documentclass[conference]{{IEEEtran}}

\\usepackage{{cite}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{url}}
\\usepackage{{hyperref}}

\\begin{{document}}

{latex_content}

\\end{{document}}
"""

        # =========================================
        # Step5: Write TEX File
        # =========================================

        tex_file.write_text(
            ieee_template,
            encoding="utf-8"
        )

        # =========================================
        # Step6: Generate PDF using tectonic
        # =========================================

        result = subprocess.run(
            [
                "tectonic",
                tex_filename,
                "--outdir",
                str(output_dir)
            ],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        # =========================================
        # Step7: Error Handling
        # =========================================

        if result.returncode != 0:

            print("Tectonic Compilation Error:")
            print(result.stderr)

            raise RuntimeError(
                f"LaTeX compilation failed:\n{result.stderr}"
            )

        # =========================================
        # Step8: Final PDF Check
        # =========================================

        final_pdf = output_dir / pdf_filename

        if not final_pdf.exists():
            raise FileNotFoundError(
                "PDF file was not generated"
            )

        print(f"Successfully generated PDF at {final_pdf}")

        return str(final_pdf)

    except Exception as e:

        print(f"Error rendering LaTeX: {str(e)}")
        raise