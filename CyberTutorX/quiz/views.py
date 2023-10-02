import json
import os
import re
import easyocr
import openai
import requests
from PIL import Image
from django.shortcuts import render
from rest_framework.views import APIView

from .chat_api import chat
from .gpt_fine_model import get_quiz, get_explaination
from utils.CustomResponse import success_response, error_400

from .models import QuestionImage, TopicExplaination


def solve_question(question):
    api_key = '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'
    prompt = f"Question: {question}\n\nProvide step-by-step instructions and explanations for solving the problem."

    openai.api_key = api_key
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3000,
        temperature=0.2  # Adjust max_tokens as needed.
    )

    generated_content = response.choices[0].text.strip()
    lines = generated_content.split('\n')
    return success_response(lines)


# Create your views here.
class QuizView(APIView):

    def get(self, request):
        data = request.GET
        for_class = data.get("class", None)
        subject = data.get("subject", None)
        topic = data.get("topic", None)
        language = data.get("language", "english")
        if language != "english" and language != "hindi":
            return error_400("We only support hindi and English for now")
        if not for_class or not subject or not topic:
            return error_400("class and subject and topic are required field")
        quiz, text = get_quiz(for_class, subject, topic, language)
        data = {"quiz": quiz, "text": text}
        # answers = re.findall(r'उत्तर: (\S+)', text)
        # print(answers)
        if len(text) > 0:
            return success_response(data)
        else:
            return error_400(quiz)


class ExplainationView(APIView):

    def get(self, request):
        data = request.GET
        for_class = data.get("class", None)
        subject = data.get("subject", None)
        index = data.get("index", 0)
        topic = data.get("topic", None)
        language = data.get("language", "english")
        if language != "english" and language != "hindi":
            return error_400("We only support hindi and English for now")
        if not for_class or not subject or not topic:
            return error_400("class and subject and topic are required field")
        if TopicExplaination.objects.filter(for_class__iexact=for_class, topic__iexact=topic,
                                            language__iexact=language).exists() and len(
                TopicExplaination.objects.filter(for_class__iexact=for_class, topic__iexact=topic,
                                                 language__iexact=language)) >= 20:
            return success_response({"explaination": TopicExplaination.objects.filter(for_class__iexact=for_class,
                                                                                      topic__iexact=topic,
                                                                                      language__iexact=language)[
                index].explaintaion, "index": index + 1})
        explaination = get_explaination(for_class, subject, topic, language)
        data = {"explaination": explaination, "index": 0}

        if len(explaination) > 0:
            if not TopicExplaination.objects.filter(for_class=for_class, topic=topic,
                                                 language=language,explaintaion__iexact=language).exists():
                TopicExplaination.objects.create(for_class=for_class, topic=topic,
                                                 language=language, explaintaion=explaination)
            return success_response(data)

        else:
            return error_400("Opps Something wend wrong")


class OCRView(APIView):
    def post(self, request):
        image = request.data.get('image', None)
        if not image:
            return error_400("Invalid image")
        question_image = QuestionImage.objects.create(image=image)
        print(question_image.get_image_url())
        payload = {
            "url": "https://cdae-182-73-20-27.ngrok-free.app" + question_image.get_image_url(),
            "language": "eng",
            "isOverlayRequired": True,
            "FileType": ".Auto",
            "IsCreateSearchablePDF": False,
            "isSearchablePdfHideTextLayer": True,
            "detectOrientation": "false",
            "isTable": "false",
            "scale": "true",
            "OCREngine": 3,
            "detectCheckbox": False,
            "checkboxTemplate": 0
        }
        headers = {"Apikey": "K82327630188957"}
        request = requests.post(url="https://api8.ocr.space/parse/image", headers=headers, data=payload)
        response = request.json()
        question_image.delete()
        text = response["ParsedResults"][0]["ParsedText"]
        # print(text)
        return solve_question(text)


class ChatView(APIView):

    def get(self, request):
        data = request.GET
        for_class = data.get("class", None)
        subject = data.get("subject", None)
        topic = data.get("topic", None)
        language = data.get("language", "english")
        # if language != "english" and language != "hindi":
        #     return error_400("We only support hindi and English for now")
        if not for_class or not subject or not topic:
            return error_400("class and subject and topic are required field")
        quiz = chat(for_class, subject, topic, language, "chatcmpl-83K3ld9DDGmy5vjMo5exuvmqKSKnW")
        data = []
        for temp_data in quiz:
            # print(temp_data)
            data.append(temp_data)
        return success_response(quiz)
