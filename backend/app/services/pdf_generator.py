import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = "generated"

def create_resume_pdf(
    filename,
    content
):
    
    folder = os.path.join(
        BASE_DIR,
        "resumes"
    )
    
    os.makedirs(
        folder,
        exist_ok=True
    )
    
    file_path = os.path.join(
        folder,
        filename
    )
    
    doc = SimpleDocTemplate(
        file_path
    )
    
    styles = getSampleStyleSheet()
    
    story = []
    
    story.append(
        Paragraph(
            "Resume",
            styles["Title"]
        )
    )
    
    story.append(
        Spacer(1,12)
    )
    
    story.append(
        Paragraph(
            content.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )
    
    doc.build(story)
    
    return file_path