from .. import admin as admin_mod
from .base import Action


class AdminAction(Action):
    name = "admin"
    admin_only = True

    def run(self, ctx):
        return admin_mod.run(ctx)
