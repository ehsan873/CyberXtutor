totalMarksData = {
    'heading_text': 'Total Marks',
    'primary_text': '534',
    'secondary_text': '700',
    'reverse_text_boldness': False
}
percentageData = {
    'heading_text': 'Percentage',
    'primary_text': '76.2%',
    'reverse_text_boldness': False
}
excellenceData = {
    'heading_text': 'Excellent at',
    'primary_text': 'Mathematics',
    'reverse_text_boldness': False
}
improvementData = {
    'heading_text': 'Needs Improvement',
    'primary_text': 'Social Science',
    'reverse_text_boldness': False
}
def get_remark(remark):
    remarkData = {
        'heading_text': 'Remark',
        'primary_text': remark,
        'reverse_text_boldness': True
    }
    return  remarkData


def get_mark_tableData(subject, obtained, total, arr):
    arr.append(
        {subject: str(obtained) + "/" + str(total)} if obtained else {subject:"AB"}
    )
    return arr


def get_marksObtainedData(arr):
    return {
        'heading': 'Marks Obtained',
        'columnHeading1': 'Subjects',
        'columnHeading2': 'Marks',
        'tableData': arr
    }


marksObtainedData = {
    'heading': 'Marks Obtained',
    'columnHeading1': 'Subjects',
    'columnHeading2': 'Marks',
    'tableData': [
        {'Maths': '92/100'},
        {'Science': '81/100'},
        {'Social Science': '55/100'},
        {'English': '72/100'},
        {'Hindi': '65/100'},
        {'Computer': '75/100'},
        {'EVS': '94/100'}
    ]
}


def get_subject_rank_table_data(arr, subject, rank):
    arr.append({subject, rank})
    return arr

def get_subjectRankData(arr):
    return {
        'heading': 'Subject wise Rank',
        'columnHeading1': 'Subjects',
        'columnHeading2': 'Rank',
        'tableData': arr
    }


def get_activites_table_data(arr, subject, grade):
    arr.append(
        {subject: grade}
    )
    return arr


def get_activitesData(data):
    activitesData = {
        'heading': 'Co-Scholastic Activities',
        'columnHeading1': 'Activities',
        'columnHeading2': 'Grade',
        'tableData': data
    }
    return activitesData


activitesData = {
    'heading': 'Co-Scholastic Activities',
    'columnHeading1': 'Activities',
    'columnHeading2': 'Grade',
    'tableData': [
        {'Work Education': 'A+'},
        {'Games': 'B+'},
        {'Health and Fitness': 'A+'},
        {'Music': 'A+'}
    ]
}


def get_attendence_response(Absent, Present):
    attendanceData = [
        {'name': 'Present', 'value': Present},
        {'name': 'Absent', 'value': Absent}
    ]
    return attendanceData


def get_marksObtainedGraphData(subject, mark, arr):
    arr.append({
        'subject': subject,
        'marks': mark
    })
    return arr


marksObtainedGraphData = [
    {
        'subject': 'Maths',
        'marks': 92
    },
    {
        'subject': 'Science',
        'marks': 81
    },
    {
        'subject': 'Social Science',
        'marks': 55
    },
    {
        'subject': 'English',
        'marks': 72
    },
    {
        'subject': 'Hindi',
        'marks': 65
    },
    {
        'subject': 'Computer',
        'marks': 75
    },
    {
        'subject': 'EVS',
        'marks': 99
    },
]


def get_obtained_average_top(arr, obtainedMarks, averageMarks, subject,top10):

    arr.append({
        'subject': subject,
        'obtainedMarks': obtainedMarks,
        'averageMarks': averageMarks,
        'topTenAverageMarks': top10
    })
    return arr


obtained_average_top = [
    {
        'subject': 'Maths',
        'obtainedMarks': 92,
        'averageMarks': 60,
        'topTenAverageMarks': 84
    },
    {
        'subject': 'Science',
        'obtainedMarks': 81,
        'averageMarks': 64,
        'topTenAverageMarks': 76
    },
    {
        'subject': 'Social Science',
        'obtainedMarks': 55,
        'averageMarks': 73,
        'topTenAverageMarks': 91
    },
    {
        'subject': 'English',
        'obtainedMarks': 72,
        'averageMarks': 71,
        'topTenAverageMarks': 89
    },
    {
        'subject': 'Hindi',
        'obtainedMarks': 65,
        'averageMarks': 80,
        'topTenAverageMarks': 92
    },
    {
        'subject': 'Computer',
        'obtainedMarks': 75,
        'averageMarks': 67,
        'topTenAverageMarks': 82
    },
    {
        'subject': 'EVS',
        'obtainedMarks': 94,
        'averageMarks': 87,
        'topTenAverageMarks': 91
    },
]
