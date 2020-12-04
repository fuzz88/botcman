__version__ = "1.0"


def init(bot):
    from . import greet_and_save_new_user

    greet_and_save_new_user.init(bot)

    from . import mover_registration

    mover_registration.init(bot)
