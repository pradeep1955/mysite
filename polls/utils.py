import random

import openai
from django.conf import settings
from django.utils import timezone

from .models import Question


def generate_and_save_daily_poll():
    try:
        openai.api_key = settings.OPENAI_API_KEY
    except AttributeError:
        print("Error: OPENAI_API_KEY not found in Django settings.")
        return None

    topics = [
        "The upcoming ICC Women's Cricket World Cup being hosted in India.",
        (
            "The future of Artificial Intelligence in India, especially "
            "with new services like ChatGPT Go."
        ),
        "Public opinion on the growth of e-sports in India.",
        "The most anticipated upcoming Bollywood movie.",
        "Social issues currently being discussed in India.",
        "Predictions for the next major domestic cricket tournament.",
    ]

    chosen_topic = random.choice(topics)

    prompt = f"""
    You are an assistant that creates engaging poll questions for a general audience website in India.
    Your task is to generate a single, multiple-choice poll question based on the following topic: "{chosen_topic}".

    The question should be timely, relevant, and easy to understand.
    It must have exactly 4 distinct choices. The choices should be brief (2-5 words each).

    Please provide the output in a simple format, with the question on the first line,
    followed by each of the 4 choices on a new line.

    Example format:
    Who do you think will win the next IPL?
    Mumbai Indians
    Chennai Super Kings
    Royal Challengers Bangalore
    Kolkata Knight Riders
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful poll creation assistant "
                        "for an Indian website."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        generated_text = response.choices[0].message.content.strip()
        lines = generated_text.split("\n")

        if len(lines) < 3:
            print("Error: OpenAI returned an invalid format.")
            return None

        question_text = lines[0].strip()
        choices_text = [line.strip() for line in lines[1:] if line.strip()]

        if not Question.objects.filter(question_text__iexact=question_text).exists():
            new_question = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now(),
            )
            for choice_str in choices_text:
                new_question.choice_set.create(choice_text=choice_str, votes=0)

            print(f"Successfully created new poll: {new_question.question_text}")
            return new_question

        print(f"Poll already exists: {question_text}")
        return None

    except Exception as e:
        print(f"An error occurred with the OpenAI API call or database operation: {e}")
        return None
