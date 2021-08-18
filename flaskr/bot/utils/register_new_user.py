import os
from flaskr.models import User


def register_new_user(session, first_name, last_name, telegram_id):

    is_owner, is_admin = False, False

    if str(telegram_id) in os.getenv('OWNER_IDS'):
        is_owner, is_admin = True, True


    user = session.query(User).filter(User.telegram_id==telegram_id).one_or_none()

    if not user:
        user = User(
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
            is_admin=is_admin,
            is_owner=is_owner
        )
        session.add(user)
        session.commit()

    return user
