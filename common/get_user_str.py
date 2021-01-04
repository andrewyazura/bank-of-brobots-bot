from aiogram import types


def get_user_str(user: types.User):
    return user.first_name + (' ' + user.last_name if user.last_name else '')
