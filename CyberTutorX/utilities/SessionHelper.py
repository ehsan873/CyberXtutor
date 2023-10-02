def is_valid_session(session):
    try:

        year1 = int(session.split("-")[0])

        year2 = 2000 + int(session.split("-")[1])
        print(year2)
        return year2 == year1+1
    except Exception as e:
        return False
