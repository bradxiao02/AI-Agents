
from io import BytesIO
from html import escape
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

from docx import Document
from docx.shared import Inches, Pt, RGBColor


def clean_inline_markdown(text):
    """Convert basic Markdown formatting into readable text."""

    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^)]+)\)',
        r'\1 (\2)',
        text
    )

    return text


def create_pdf(report):
    """Generate a formatted PDF research report."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=14,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8
    ))

    story = []

    for line in report.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        if line == "---":
            story.append(HRFlowable(
                width="100%",
                color=colors.lightgrey,
                spaceBefore=5,
                spaceAfter=10
            ))
            continue

        line = clean_inline_markdown(line)

        # Escape HTML before adding supported formatting.
        line = escape(line)

        line = re.sub(
            r'\*\*(.*?)\*\*',
            r'<b>\1</b>',
            line
        )

        line = re.sub(
            r'\*(.*?)\*',
            r'<i>\1</i>',
            line
        )

        line = re.sub(
            r'`(.*?)`',
            r'<font name="Courier">\1</font>',
            line
        )

        if line.startswith("# "):
            story.append(Paragraph(
                line[2:],
                styles["ReportTitle"]
            ))

        elif line.startswith("## "):
            story.append(Paragraph(
                line[3:],
                styles["SectionHeading"]
            ))

        elif line.startswith("### "):
            story.append(Paragraph(
                line[4:],
                styles["Heading3"]
            ))

        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph(
                "&#8226; " + line[2:],
                styles["BodyTextCustom"]
            ))

        elif re.match(r"^\d+\.\s", line):
            story.append(Paragraph(
                line,
                styles["BodyTextCustom"]
            ))

        else:
            story.append(Paragraph(
                line,
                styles["BodyTextCustom"]
            ))

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)

        canvas.drawString(
            20 * mm,
            12 * mm,
            "AI Research Agent"
        )

        canvas.drawRightString(
            A4[0] - 20 * mm,
            12 * mm,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)
    return buffer.getvalue()


def create_docx(report):
    """Generate an editable Word research report."""

    document = Document()

    section = document.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    # Document styles.
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)

    title_style = document.styles["Title"]
    title_style.font.name = "Arial"
    title_style.font.size = Pt(22)
    title_style.font.color.rgb = RGBColor(23, 54, 93)

    heading_style = document.styles["Heading 1"]
    heading_style.font.color.rgb = RGBColor(23, 54, 93)

    for line in report.splitlines():

        line = line.strip()

        if not line:
            continue

        line = clean_inline_markdown(line)

        if line.startswith("# "):
            document.add_heading(line[2:], level=0)

        elif line.startswith("## "):
            document.add_heading(line[3:], level=1)

        elif line.startswith("### "):
            document.add_heading(line[4:], level=2)

        elif line.startswith("- ") or line.startswith("* "):
            document.add_paragraph(
                line[2:],
                style="List Bullet"
            )

        elif re.match(r"^\d+\.\s", line):
            document.add_paragraph(
                re.sub(r"^\d+\.\s", "", line),
                style="List Number"
            )

        elif line == "---":
            document.add_paragraph(
                "________________________________________"
            )

        else:
            document.add_paragraph(line)

    buffer = BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()
