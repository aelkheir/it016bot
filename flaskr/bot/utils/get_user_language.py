
from flaskr.bot.localization.ar import ar
from flaskr.bot.localization.en import en


def get_user_language(language: str):
  return ar if language == 'ar' else en