# analyzer/resume_analysis.py

from django.shortcuts import render
from docx import Document
from PyPDF2 import PdfReader
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")


def analyze_job_and_resume(request):
    if request.method == 'POST':
        # Capture the job description and the resume file
        job_description = request.POST.get('job_description', '')
        resume_file = request.FILES.get('resume')

        # Validate inputs
        if not job_description or not resume_file:
            return render(request, 'error.html', {'message': 'Both job description and resume are required.'})

        # Extract keywords from the job description
        job_doc = nlp(job_description)
        job_keywords = {token.text.lower() for token in job_doc if token.is_alpha and not token.is_stop}

        # Check the resume file type and extract text
        file_name = resume_file.name
        resume_text = ""

        if file_name.endswith('.docx'):
            document = Document(resume_file)
            resume_text = "\n".join([para.text for para in document.paragraphs])
        elif file_name.endswith('.pdf'):
            reader = PdfReader(resume_file)
            resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            return render(request, 'error.html',
                          {'message': 'Unsupported file type. Please upload a .docx or .pdf file.'})

        # Process resume text using NLP
        resume_doc = nlp(resume_text)
        resume_keywords = {token.text.lower() for token in resume_doc if token.is_alpha and not token.is_stop}

        # Identify common keywords between the job description and the resume
        common_keywords = job_keywords.intersection(resume_keywords)

        # Pass extracted keywords and common keywords to the template for rendering
        context = {
            'job_keywords': job_keywords,
            'resume_keywords': resume_keywords,
            'common_keywords': common_keywords,
        }
        return render(request, 'job_and_resume_analysis_result.html', context)

    # Handle GET request - show upload form
    return render(request, 'upload_job_and_resume.html')