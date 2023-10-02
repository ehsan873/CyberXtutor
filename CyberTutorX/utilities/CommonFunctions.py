import re
from operator import itemgetter, attrgetter


def is_valid_class(name):
    test = ""
    if test.__contains__(" "):
        return False


def sort_class(data):
    class_sort_order = {
        'playgroup': 0,
        'nursery': 1,
        'lkg': 2,
        'ukg': 3,
        'kg': 4
    }

    # Sort the data based on class_name, section_name, and class_id
    sorted_data = sorted(data, key=lambda x: (class_sort_order.get(x['class_name'].lower(), float('inf')),
                                              int(x['class_name']) if x['class_name'].isdigit() else float('inf'),
                                              x['section_name']))
    return sorted_data


def valid_website(web):
    if not web:
        return True
    pattern = "^(https?:\/\/)?([a-zA-Z0-9-]+\.)*[a-zA-Z0-9]+\.[a-zA-Z]{2,}(\/[^\s]*)?$"
    is_valid = re.search(pattern, web)
    if is_valid:
        return True
    return False


def validate_pincode(pincode):
    pattern = r'^[1-9][0-9]{5}$'
    is_valid = re.match(pattern, pincode)
    if is_valid:
        return True
    return False


def sort_sessions_by_name(sessions):
    sorted_sessions = sorted(sessions, key=attrgetter('name'), reverse=True)
    return sorted_sessions


def marksParticipation(MS, MI, MSN):
    return max(MS, MI, MSN)


def alpha(PS, AP):
    if PS > AP:
        return 1
    return PS / AP


def beta(PI):
    if PI:
        return 1
    return 0


def gamma(WI):
    if WI:
        return 1
    return 0


def delta(PSN, WSN):
    if PSN and WSN:
        return 1
    if PSN:
        return 0.99
    return 0


def marksSchool(PS, AP, WS):
    return 0.9 * (0.75 * alpha(PS, AP) + 0.25 * WS)


def marksInterschool(PI, WI, PS, WS, AP):
    return 0.9 * beta(PI) + 0.025 * gamma(WI) + 0.025 * (0.75 * alpha(PS, AP) + 0.25 * WS)


def marksStateOrNational(PSN, WSN):
    return delta(PSN, WSN)


def grading(values):
    """
    Note Every value is per category
    PI- boolean -- True if any participated event is interschool
    WI- boolean -- True if any result in insterschool is 1,2,3
    PSN-boolean -- True if any participated event is state or national
    WSN- boolean -- True if any result in state or national is 1,2,3
    AP- float-- Average participation- total numner of average of eventparticipated/totalevent of all students
    MT- Teacher marks out of 100
    """
    eventParticipated = values[0]
    totalEvent = values[1]
    eventWinning = values[2]
    PI = values[3]
    WI = values[4]
    PSN = values[5]
    WSN = values[6]
    AP = values[7]
    MT = values[8] / 100
    PS = eventParticipated / totalEvent
    WS = eventWinning / totalEvent
    MS = marksSchool(PS, AP, WS)
    MI = marksInterschool(PI, WI, PS, WS, AP)
    MSN = marksStateOrNational(PSN, WSN)
    return 0.15 * MT + 0.85 * marksParticipation(MS, MI, MSN)


def finalGrades(finalMarks):
    res = dict()
    for category, values in finalMarks.items():
        res[category] = grading(values) * 100
    return res

grading_to_makrs = swapped_grades = {
    100: "A+",
    94: "A",
    89: "A-",
    84: "B+",
    79: "B",
    74: "B-",
    69: "C+",
    64: "C",
    59: "C-",
    54: "D+",
    49: "D",
    44: "F"
}


def get_grade(mark):
    found_grade = None
    if not mark:
        return None
    for score, grade in grading_to_makrs.items():
        if float(mark) >= score:
            found_grade = grade
            break
    return found_grade