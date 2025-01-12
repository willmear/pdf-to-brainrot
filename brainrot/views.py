import openai
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Pdf
from .forms import PdfForm
from pypdf import PdfReader
from .video import create_video
from .tts import tts

def index(request):
    return HttpResponse("Hello, world. You're at the brainrot index.")


def upload_pdf(request):
    if request.method == "POST" or request.method == "GET":
        # form = PdfForm(request.POST, request.FILES)
        # if form.is_valid():
        #     pdf = form.save(commit=False)
        #     pdf.user = request.user
        #     pdf.save()
        #     reader = PdfReader(pdf.pdf)
        #     script = ""
        #     for page in reader.pages:
        #         script += page.extract_text()
        #         script += " "

    #   For testing:
        script = "this is a test. The text should overlay"
        print(script)
        try:
            tts(script)
        except openai.APIConnectionError as e:
            # Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            return JsonResponse({"status": "error"}, status=400)
            pass
        except openai.APIError as e:
            print(f"OpenAI Error: {e}")
            return JsonResponse({"status": "error"}, status=400)
            pass
        except openai.RateLimitError as e:
            # Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            return JsonResponse({"status": "error"}, status=400)
            pass

        create_video(script, 1)

    return JsonResponse({"status": "success"}, status=200)

    #         return JsonResponse({"status": "success"}, status=201)
    #     else:
    #         return JsonResponse({"status": "error"}, status=400)
    # else:
    #     return JsonResponse({"status": "only POST method allowed"}, status=405)
    #
