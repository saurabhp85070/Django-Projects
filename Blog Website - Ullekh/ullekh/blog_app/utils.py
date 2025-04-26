from io import BytesIO
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.staticfiles import finders
import os

def fetch_resources(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ""))
    else:
        path = None

    if path and os.path.isfile(path):
        return path
    return uri

def generate_pdf(blog_post):
    template = get_template('blog_app/pdf_template.html')
    context = {
        'blog_post': blog_post,
    }
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
    
    if not pdf.err:
        return result.getvalue()
    return None
