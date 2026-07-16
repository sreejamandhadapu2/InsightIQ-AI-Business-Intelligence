"""
PDF Report Generator
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors


class PDFGenerator:

    @staticmethod
    def generate(
        question,
        sql,
        dataframe,
        insight,
        alerts=None,
    ):

        buffer = BytesIO()

        document = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        # =====================================
        # Title
        # =====================================

        story.append(
            Paragraph(
                "<b>InsightIQ AI Business Intelligence Report</b>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 15))

        # =====================================
        # Date
        # =====================================

        story.append(
            Paragraph(
                f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        # =====================================
        # Business Question
        # =====================================

        story.append(
            Paragraph(
                "<b>Business Question</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                question,
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 12))

        # =====================================
        # Generated SQL
        # =====================================

        story.append(
            Paragraph(
                "<b>Generated SQL</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                sql.replace("\n", "<br/>"),
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 12))
        # =====================================
# Business Alerts
# =====================================

        if alerts:

            story.append(
                Paragraph(
                    "<b>Business Alerts</b>",
                    styles["Heading2"],
                )
            )

            for alert in alerts:

                story.append(
                    Paragraph(
                        f"• {alert}",
                        styles["BodyText"],
                    )
                )

            story.append(Spacer(1, 20))

        # =====================================
        # Result Summary
        # =====================================

        story.append(
            Paragraph(
                "<b>Result Summary</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"Rows Returned : {len(dataframe)}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Columns Returned : {len(dataframe.columns)}",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 12))

        # =====================================
        # Result Preview
        # =====================================

        story.append(
            Paragraph(
                "<b>Result Preview (First 10 Rows)</b>",
                styles["Heading2"],
            )
        )

        preview = dataframe.head(10)

        table_data = [preview.columns.tolist()]

        table_data.extend(
            preview.astype(str).values.tolist()
        )

        table = Table(table_data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 15))

        # =====================================
        # AI Business Insight
        # =====================================

        story.append(
            Paragraph(
                "<b>AI Business Insight</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                insight.replace("\n", "<br/>"),
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        # =====================================
        # Footer
        # =====================================

        story.append(
            Paragraph(
                "<i>Generated by InsightIQ AI Business Intelligence Platform</i>",
                styles["Italic"],
            )
        )

        document.build(story)

        buffer.seek(0)

        return buffer