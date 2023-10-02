import re
import time


def get_index(param):
    print(param)
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


def get_correct_answer(options, correct_answer):
    print(correct_answer)
    if "उत्तर: " in correct_answer:
        correct_answer = correct_answer.split("उत्तर: ")
        if len(correct_answer) == 1 and len(correct_answer[0]) == 1:
            index = get_index(correct_answer[0])
            if isinstance(int, index):
                return options[index]
    elif "Answer: " in correct_answer:
        correct_answer = correct_answer.split("Answer: ")
        if len(correct_answer) == 1 and len(correct_answer[0]) == 1:
            index = get_index(correct_answer[0])
            if isinstance(int, index):
                return options[index]
    else:
        return correct_answer


def def_get_options(options):
    for i in range(0,len(options)):
        if ")" in options[i]:
            # print(options[i])
            options[i]=options[i].split(")")[1]
    return options



def get_quiz_data(param):
    i = 0
    data = []
    try:
        while i < len(param):
            if "?" not in param[i]:
                i += 1
            else:
                question = param[i]
                options = [param[i + 1], param[i + 2], param[i + 3], param[i + 4]]
                correct_answer = (param[i + 5]).split(")")[0] if ")" in param[i + 5] else param[i + 5]
                data.append(
                    {
                        'question': question if ")" not in question else question.split(")")[1],
                        'options': def_get_options(options),
                        'correct_answer': get_correct_answer(options, correct_answer)
                    }
                )
                i += 6
    except Exception as e:
        print(e)

    return data


def get_quiz1(text, response):
    # text = "B\n\n1) सवाल 1: मीर्ज़ा ग़ालिब का असली नाम क्या था?\nए) ग़मरान गुलीया\nबी) मीर ताकि मीर\nसी) महर ताकि महर\nडी) ग़यासुदीन कल्ल\nउत्तर: बी) मीर ताकि मीर\n\n2) सवाल 2: मीर्ज़ा ग़ालिब का जन्म किस शहर में हुआ था?\nए) लाहौर\nबी) दिल्ली\nसी) बाहरेबद\nडी) आगरा\nउत्तर: सी) बाहरेबद\n\n3) सवाल 3: मीर्ज़ा ग़ालिब की रचनाएं किस भाषा में लिखी गई थीं?\nए) उर्दू\nबी) फ़ारसी\nसी) हिंदी\nडी) संस्कृत\nउत्तर: बी) फ़ारसी\n\n4) सवाल 4: मीर्ज़ा ग़ालिब की कविता ‘दीवान-ए-ग़ालिब’ का नाम उनके कौनसे शैत्तनी प्रशंसक के नाम पर है?\nए) मिर ताकि मिर\nबी) महर ताकि महर\nसी) गुलाम अहमद अज्मल\nडी) नवाब मुस्तफ़ा खान\nउत्तर: डी) नवाब मुस्तफ़ा खान\n\n5) सवाल 5: मीर्ज़ा ग़ालिब के दोस्त कौन थे जिनके नाम पर उन्होंने एक मुक़द्दमा भी लिखा था?\nए) अमीर खुसरो\nबी) असदुल्लाह खाँ\nसी) गोपाल दास नीरज\nडी) जगन्नाथ आज़ाद\nउत्तर: डी) जगन्नाथ आज़ाद\n\n6) सवाल 6: मीर्ज़ा ग़ालिब ने किस दुर्ग को कविता में अपना प्रिय स्थान दिया है?\nए) लाल क़िला\nबी) रेड फ़ोर्ट\nसी) अकबराबाद\nडी) ग़ुलेल्डा\nउत्तर: सी) अकबराबाद\n\n7) सवाल 7: मीर्ज़ा ग़ालिब की कविता ‘असदकी आज़ादी के लिए’ का विषय क्या है?\nए) खामोशी\nबी) स्वतंत्रता\nसी) प्यार\nडी) मौत\nउत्तर: बी) स्वतंत्रता\n\n8) सवाल 8: मीर्ज़ा ग़ालिब को उनके व्यक्तिगत जीवन में किन मुश्किलों का सामना करना पड़ा?\nए) पैसे की कमी\nबी) स्वास्थ्य समस्याएं\nसी) अल्पावस्था\nडी) सैलानियों का वापस आना\nउत्तर: बी) स्वास्थ्य समस्याएं\n\n9) सवाल 9: मीर्ज़ा ग़ालिब ने किस तरह की कविताएं लिखीं जो उन्हें अनूठा बनाती थीं?\nए) रोमांचकारी\nबी) संतुष्टिजनक\nसी) विनोदमय\nडी) तीखी-तीखी\nउत्तर: डी) तीखी-तीखी\n\n10) सवाल 10: मीर्ज़ा ग़ालिब ने किस दौर के राजाों को अपना प्रशंसक नहीं माना था?\nए) मुग़ल\nबी) गुलामी और अंग्रेजी\nसी) दिल्ली सुल्तानत\nडी) विजयनगर साम्राज्य\nउत्तर: बी) गुलामी और अंग्रेजी"
    questions_and_answers = re.split(r'\n\n\d+[A-Z]+\n', text)
    questions_and_answers = [q.strip() for q in questions_and_answers if q.strip()]

    # Initialize a dictionary to store the parsed data
    quiz_data = []

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=1):
        # Extract the question

        if "?" in qa:
            data = get_quiz_data(qa.splitlines())
            return data
        question_match = re.match(r'\d+\)\s+(.*?)\n', qa)
        if question_match:
            question_text = question_match.group(1).strip()

            # Extract the answer options
            options_match = re.findall(r'([A-ए])\)\s+(.*?)\n', qa)
            options_dict = {option: text.strip() for option, text in options_match}

            # Extract the correct answer
            answer_match = re.search(r'उत्तर:\s+विकल्प\s+([A-ए])', qa)
            correct_answer = answer_match.group(1) if answer_match else None

            # Create a dictionary entry for the current question
            quiz_data.append({
                'question': question_text,
                'options': options_dict,
                'correct_answer': correct_answer
            })
    return quiz_data


def get_quiz2(text):
    questions_and_answers = re.split(r'\n\d+\n', text)
    questions_and_answers = [q.strip() for q in questions_and_answers if q.strip()]

    # Initialize a dictionary to store the parsed data
    quiz_data = []

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=1):
        # Extract the question
        question_match = re.match(r'\d+\)\s+(.*?)\n', qa)
        if question_match:
            question_text = question_match.group(1).strip()

            # Extract the answer options
            options_match = re.findall(r'([A-D])\)\s+(.*?)\n', qa)
            options_dict = {option: text.strip() for option, text in options_match}

            # Extract the correct answer
            answer_match = re.search(r'Answer:\s+(.*)', qa)
            correct_answer = answer_match.group(1).strip() if answer_match else None

            # Create a dictionary entry for the current question
            quiz_data.append({
                'question': question_text,
                'options': options_dict,
                'correct_answer': correct_answer
            })
    return quiz_data


def get_quiz3(text):
    questions_and_answers = re.split(r'\n\d+\n', text)
    questions_and_answers = [q.strip() for q in questions_and_answers if q.strip()]

    # Initialize a dictionary to store the parsed data
    quiz_data = []

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=1):
        # Extract the question
        question_match = re.match(r'\d+\)\s+(.*?):', qa)
        if question_match:
            question_text = question_match.group(1).strip()

            # Extract the answer options
            options_match = re.findall(r'([A-D])\)\s+(.*?)\n', qa)
            options_dict = {option: text.strip() for option, text in options_match}

            # Extract the correct answer
            answer_match = re.search(r'उत्तर:\s+(.*)', qa)
            correct_answer = answer_match.group(1).strip() if answer_match else None

            # Create a dictionary entry for the current question
            quiz_data.append({
                'question': question_text,
                'options': options_dict,
                'correct_answer': correct_answer
            })
    return quiz_data


def get_quiz4(text):
    questions_and_answers = re.split(r'\n\d+\n', text)
    questions_and_answers = [q.strip() for q in questions_and_answers if q.strip()]

    # Initialize a dictionary to store the parsed data
    quiz_data = []

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=1):
        # Extract the question
        question_match = re.match(r'\d+\)\s+(.*?):', qa)
        if question_match:
            question_text = question_match.group(1).strip()

            # Extract the correct answer
            answer_match = re.search(r'कॉरेक्ट उत्तर:\s+(.*)', qa)
            correct_answer = answer_match.group(1).strip() if answer_match else None

            # Create a dictionary entry for the current question
            quiz_data.append({
                'question': question_text,
                'correct_answer': correct_answer
            })
    return quiz_data


def get_quiz5(text):
    questions_and_answers = re.split(r'\n\d+\)\s+', text)
    questions_and_answers = [qa.strip() for qa in questions_and_answers if qa.strip()]

    # Initialize a dictionary to store the parsed data
    quiz_data = []

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=2):
        # Extract the question

        question_text, qa = qa.split('\n', 1)

        # Extract the answer options
        options_block, answer_block = qa.split('\nAnswer:')
        options = re.findall(r'\s*([A-D])\)\s+(.*?)\s*', options_block)

        # Extract the correct answer
        correct_answer = answer_block.strip()

        # Create a dictionary entry for the current question
        quiz_data.append({
            'question': question_text.strip(),
            'options': options,
            'correct_answer': correct_answer,
        })
    return quiz_data


def get_quiz6(text):
    quiz_data = []

    # Split text into individual questions and answers
    questions_and_answers = re.split(r'\n\d+\)', text)[1:]

    # Iterate through each question and answer block
    for i, qa in enumerate(questions_and_answers, start=1):
        # Extract the question

        try:
            question_text, qa = qa.split('\n', 1)
        except Exception as e:
            question_text, qa = qa.split('?', 1)

        # Extract the answer options and correct answer
        print(qa)
        try:
            options_block, answer_block = qa.strip().split('Answer:')
        except Exception as e:

            options_block, answer_block = qa.strip().split('उत्तर:')
        options = re.findall(r'([A-D])\)\s(.*?)', options_block)
        correct_answer = answer_block.strip()

        # Create a dictionary entry for the current question
        quiz_data.append({
            'question': question_text.strip(),
            'options': options,
            'correct_answer': correct_answer,
        })
    return quiz_data
