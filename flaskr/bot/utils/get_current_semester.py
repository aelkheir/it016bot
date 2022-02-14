


from flaskr.models import CurrentSemester


def get_current_semester(session):
    """
    Returns the current semester.
    return: CurrentSemester()
    """

    current = session.query(CurrentSemester).first()

    if not current:
        current = CurrentSemester()
        session.add(current)
        session.commit()

    return current