import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "common.users"
    verbose_name = _("User")

    def ready(self):
        with contextlib.suppress(ImportError):
            import common.users.signals  # noqa: F401
