from django.conf import settings
from django.shortcuts import render


# Classes
# =======
class LayoutMixin(object):
    def get_context_data(self, **kwargs):
        # Get base context
        ctx = super().get_context_data(**kwargs)

        # Add layout context variables
        ctx["WEBSITE_NAME"] = settings.WEBSITE_NAME
        ctx["AUTHOR_NAME"] = settings.AUTHOR_NAME
        return ctx
