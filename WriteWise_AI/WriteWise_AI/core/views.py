import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Local AI API URL
AI_API_URL = "http://localhost:11434/api/generate"

def generate_ai_response(user_input):
    """ Call local AI API to generate an article """
    data = {
        "model": "WriteWiseAI:latest",
        "prompt": user_input
    }

    try:
        response = requests.post(AI_API_URL, json=data, stream=True)

        if response.status_code == 200:
            generated_text = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    result = json.loads(decoded_line)
                    generated_text += result.get("response", "")
            return generated_text
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def home(request):
    """ Render HTML Page """
    return render(request, 'core/index.html')

@csrf_exempt
def generate_article(request):
    """ API to handle user input and return generated article """
    if request.method == "POST":
        user_input = request.POST.get('title', '')
        generated_content = generate_ai_response(user_input)
        return JsonResponse({"article": generated_content})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def save_article(request):
    """ Save the edited article """
    if request.method == "POST":
        edited_content = request.POST.get('content', '')
        print("Updated Article:\n", edited_content)  # Debugging
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
