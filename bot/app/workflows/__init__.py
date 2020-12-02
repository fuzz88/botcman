__version__ = "1.0"


def init(bot):
    from . import save_new_user
    save_new_user.init(bot)
