from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import mm
from xml.sax.saxutils import escape


def build_pdf_report(symbol, snapshot, fundamentals, technicals, report_text):
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=15*mm,bottomMargin=15*mm)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("Title2",parent=styles["Title"],fontSize=20,leading=24,spaceAfter=12)
    currency=fundamentals.get("currency") or "USD"
    name=fundamentals.get("display_name") or symbol
    story=[
        Paragraph("FinSight AI — Global Financial Research Report",title),
        Paragraph(f"<b>Security:</b> {escape(name)}",styles["BodyText"]),
        Paragraph(f"<b>Ticker:</b> {escape(symbol)} &nbsp;&nbsp; <b>Exchange:</b> {escape(str(fundamentals.get('exchange') or fundamentals.get('fullExchangeName') or 'N/A'))} &nbsp;&nbsp; <b>Currency:</b> {escape(str(currency))}",styles["BodyText"]),
        Spacer(1,8), Paragraph("Market snapshot",styles["Heading2"]),
    ]
    data=[
        ["Last Price", f"{currency} {snapshot.get('price','N/A')}"],
        ["1D Change %", str(snapshot.get("change_pct","N/A"))],
        ["P/E", str(fundamentals.get("trailingPE","N/A"))],
        ["Debt / Equity", str(fundamentals.get("debtToEquity","N/A"))],
        ["Revenue Growth", str(fundamentals.get("revenueGrowth","N/A"))],
        ["Technical Signal", str(technicals.get("signal",{}).get("label","N/A"))],
        ["RSI Zone", str(technicals.get("signal",{}).get("rsi_zone","N/A"))],
    ]
    table=Table(data,colWidths=[55*mm,110*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#f3f4f6")),
        ("GRID",(0,0),(-1,-1),0.4,colors.grey),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("PADDING",(0,0),(-1,-1),6),
    ]))
    story += [table, Spacer(1,10), Paragraph("Research memo",styles["Heading2"])]
    for block in report_text.split("\n"):
        if block.strip():
            clean=escape(block).replace("**", "")
            story.append(Paragraph(clean,styles["BodyText"]))
            story.append(Spacer(1,4))
    story += [Spacer(1,8), Paragraph("Educational use only. This report is not investment advice. Verify market data and consult a qualified professional.", styles["BodyText"])]
    doc.build(story)
    return buf.getvalue()
