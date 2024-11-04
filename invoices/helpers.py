import os
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
from xhtml2pdf import pisa


def is_convertible_to_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def generate_pdf(template_path, context={}, css_path=None):
    html = render_to_string(template_path, context)

    if css_path:
        with open(os.path.join(settings.BASE_DIR, css_path)) as css_file:
            css_content = css_file.read()
            html = f"<style>{css_content}</style>" + html

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()
    return None
