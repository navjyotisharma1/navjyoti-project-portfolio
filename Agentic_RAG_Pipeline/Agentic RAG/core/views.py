from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import UploadedDocument
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF
import json
import os
import time
# Import functions from your AI RAG module
from agentic_rag import setup_vector_db, get_local_content, process_query as ai_process_query

# Initialize global vector DB (initially empty)
vector_db = None
local_context = ""


def index(request):
    """
    Renders the main HTML page.
    """
    return render(request, 'index.html')


@csrf_exempt
def process_query(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get('query')

            if not query:
                return JsonResponse({"error": "Query is required"}, status=400)

            # Use your AI pipeline
            answer = ai_process_query(query, vector_db, local_context)
            return JsonResponse({"response": answer})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

@csrf_exempt
def upload_document(request):
    """
    Handles multiple PDF uploads.
    """
    global vector_db, local_context
    start_time = time.time()

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

    files = request.FILES.getlist('file')
    if not files:
        return JsonResponse({'error': 'No files uploaded'}, status=400)

    uploaded_files = []
    combined_text = ""

    for uploaded_file in files:
        document = UploadedDocument.objects.create(file=uploaded_file)

        pdf = fitz.open(document.file.path)
        text = ""
        for page in pdf:
            text += page.get_text("text")
        pdf.close()

        document.content = text
        document.save()

        combined_text += text + "\n"
        uploaded_files.append(document.file.name)

    # ✅ Rebuild the vector DB
    try:
        first_file_path = UploadedDocument.objects.latest('id').file.path
        vector_db = setup_vector_db(first_file_path)
        local_context = get_local_content(vector_db, "")
    except Exception as e:
        print("Vector DB setup failed:", e)

    return JsonResponse({
        'message': f'{len(uploaded_files)} file(s) uploaded successfully.',
        'uploaded_files': uploaded_files,
        'time_taken': f"{time.time() - start_time:.2f}s"
    }, status=200)