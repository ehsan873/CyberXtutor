import openai
import random
import re

from quiz.hindi_response_helper import get_quiz1, get_quiz2, get_quiz3, get_quiz4, get_quiz5, get_quiz6

# Set your OpenAI API key here
api_key = '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'


openai.api_key = api_key
pattern = r'Answer:\s+([A-D])\)\s+(.*?)\n'
option_pattern = r'[A-D]\)'
hindi_option_pattern = r'[ए-ड]\) [^\n]+'
def get_quiz(for_class,subject,topic,language):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
            prompt="create a quiz for class " + for_class + " of " + subject + "topic" + topic + "of 10 Question and question should be in "+language+"  with this "
                                                                                                  "format 1)"
                                                                                                  "Question 1 A) option A B) "
                                                                                                  "option B"
                                                                                                  "C) option C D) option D "
                                                                                                  "Answer:"
                                                                                                  "option ",
        temperature=1,
        max_tokens=1782,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,

    )
    text = response["choices"][0]["text"]
    if language =="english":
    # print(response)
        questions_and_answers = re.split(r'\n\n\d+\)\s+', text)
        questions_and_answers = [q.strip() for q in questions_and_answers if q.strip()]

        # Initialize a dictionary to store the parsed data
        quiz_data = []

        # Iterate through each question and answer block
        for i, qa in enumerate(questions_and_answers, start=1):
            # Extract the question
            question_match = re.match(r'(.+?)\n', qa)
            if question_match:
                question_text = question_match.group(1).strip()

                # Extract the answer options
                options_match = re.findall(r'([A-D])\)\s+(.+)', qa)
                options_dict = {option: text.strip() for option, text in options_match}

                # Extract the correct answer
                answer_match = re.search(r'Answer:\s+([A-D])', qa)
                correct_answer = answer_match.group(1) if answer_match else None

                # Create a dictionary entry for the current question
                quiz_data.append({
                    'question': question_text,
                    'options': options_dict,
                    'correct_answer': correct_answer
                })
        return quiz_data , response["choices"][0]["text"]
    elif language=="hindi":
        data = get_quiz1(text,response)
        return data,response["choices"][0]["text"]
    else:
        return "We only support English for now",""


def get_explaination(for_class,subject,topic,language):
    prompt = f"Explain the concept of {topic} of subject {subject} for class {for_class} student  with relevant examples. in language {language} \n explainations : [explainations] \n examples:[examples]"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=1782,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,

    )
    # print(response)
    text = response["choices"][0]["text"].split("\n")
    return text