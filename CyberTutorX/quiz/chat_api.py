import re

import openai


def get_question_options(options):
    mod_options = []
    for option in options:
        try:
            output = re.split(r'\d+\:', option)
            print(output)
            mod_options.append(output[1])
        except Exception as e:
            mod_options.append(mod_options)

    return mod_options


def get_option_index(param):
    params = re.split(r"Correct Answer+\:", param)
    if len(params) > 1:
        return params[1]
    param = params[0]

    if param == "ए":
        return 0
    elif param == "बी":
        return 1
    elif param == "सी":
        return 2
    elif param == "डी":
        return 3
    elif param == 'a' or param == 'A':
        return 0
    elif param == 'b' or param == 'B':
        return 1
    elif param == 'c' or param == 'C':
        return 2
    elif param == 'd' or param == 'D':
        return 3
    else:
        return param


def chat(for_class, subject, topic, language, conversation_id):
    api_key = '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'

    openai.api_key = api_key
    prompt = (
            "Generate 5 number of multiple-choice questions and every quetion must be unique with options for class " + for_class + " in suject " + subject + "in topic " + topic + " and question must be written in " + language + " language :\n"
                                                                                                                                                                                                                                     "Question [question_no] : [ blank ] \n"
                                                                                                                                                                                                                                     "Option 1: [option]\n"
                                                                                                                                                                                                                                     "Option 2: [option]\n"
                                                                                                                                                                                                                                     "Option 3: [option]\n"
                                                                                                                                                                                                                                     "Option 4: [option]\n"
                                                                                                                                                                                                                                     "Correct Answer: [option]\n"
    )

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=3000,
        temperature=0.2  # Adjust max_tokens as needed.
    )

    generated_content = response.choices[0].text.strip()
    lines = generated_content.split('\n')
    # print(generated_content)
    # Initialize variables for question, options, and correct answer.

    new_lines = []
    for line in lines:
        line = line.strip()
        if (len(line) > 0):
            new_lines.append(line)

    i = 0
    quiz_data = []
    # print(new_lines)
    print(new_lines)
    while i < len(new_lines):
        options = get_question_options([new_lines[i + 1], new_lines[i + 2], new_lines[i + 3], new_lines[i + 4]])

        answer = options[get_option_index(new_lines[i + 5])] if isinstance(
            get_option_index(get_option_index(new_lines[i + 5])), int) else get_option_index(new_lines[i + 5])
        quiz_data.append(
            {
                "question": new_lines[i],
                "options": options,
                "answer": answer
            }
        )
        i += 6
    # Return the generated question, options, and correct answer.

    return quiz_data, ""
