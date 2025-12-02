from django.conf import settings


# Context Processor Functions
# ===========================
def layout(request):
    return {
        "WEBSITE_NAME": settings.WEBSITE_NAME,
        "AUTHOR_NAME": settings.AUTHOR_NAME
    }
