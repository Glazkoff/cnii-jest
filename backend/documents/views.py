import os
import io
from django.http import HttpResponse
from secretary import Renderer
from backend.settings import MEDIA_ROOT
from django.http import FileResponse
from tempfile import TemporaryFile, NamedTemporaryFile


def doc_test(request):
    engine = Renderer()
    # template = open(os.path.join(MEDIA_ROOT, "template.odt"), 'rb')
    # output = open(os.path.join(MEDIA_ROOT, 'output.odt'), 'wb')
    # doc = engine.render(template, title="NGLAZKOV studio")

#     doc.render(context)
    # doc_io = io.BytesIO()  # create a file-like object
    # doc.save(doc_io)  # save data to file-like object
    # doc_io.seek(0)  # go to the beginning of the file-like object
    templatePath = os.path.join(MEDIA_ROOT, "template.fodt")
    template = open(templatePath, 'rb')
    # context = {
    #     'title': 'TITLE'
    # }
    # result = engine.render(templatePath, **context)
    countries = [
        {'country': 'United States', 'capital': 'Washington', 'cities': [
            'miami', 'new york', 'california', 'texas', 'atlanta']},
        {'country': 'England', 'capital': 'London', 'cities': ['gales']},
        {'country': 'Japan', 'capital': 'Tokio',
            'cities': ['hiroshima', 'nagazaki']},
        {'country': 'Nicaragua', 'capital': 'Managua',
            'cities': ['leon', 'granada', 'masaya']},
        {'country': 'Argentina', 'capital': 'Buenos aires'},
        {'country': 'Chile', 'capital': 'Santiago'},
        {'country': 'Mexico', 'capital': 'MExico City',
            'cities': ['puebla', 'cancun']},
    ]
    result = engine.render(template, countries=countries)
    resp = HttpResponse(
        content_type='application/vnd.oasis.opendocument.text;   charset=UTF-8')
    resp["Content-Disposition"] = "inline; filename=generated_doc.odt"

    with NamedTemporaryFile() as temp:
        # Encode your text in order to write bytes
        temp.write(result)
        # put file buffer to offset=0
        # temp.seek(0)
        temp.flush()
        temp = open(temp.name, 'rb')
        resp.write(temp.read())
        return resp
