from django.conf import settings
from django.core.mail import EmailMessage
from pdf2image import convert_from_path
import os, tempfile

class Page:
    def __init__(self, number, pathname, formato, *args, **kwargs):
        self.number = number
        self.path = pathname
        self.formato = formato
        self.url = "{}.{}".format(self.path, self.formato)

def convertPdf(pdf):
    output_folder = os.path.dirname(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, pdf))
    pdfPath = os.path.abspath(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, pdf))
    # with tempfile.TemporaryDirectory() as path:
    pages = []
    try:
        images = convert_from_path(
            pdfPath,
            output_folder=output_folder,
            fmt='jpeg',
            thread_count=4
            )
        with open("tmp_log.txt", "w") as myfile:
            myfile.write("Imagenes creadas correctamente")
    except Exception as e:
        with open("tmp_log.txt", "w") as myfile:
            myfile.write("Error al crear imagenes")
        body = str(e)
        email = EmailMessage(
            subject="error",
            body=body+"\npdfManager.py",
            to=['andresfelipe.2031@gmail.com']
            )
        email.content_subtype = 'html'
        email.send()
        return []
    counter = 1
    for image in images:
        filename, ext = os.path.basename(image.filename).split(".")
        image_out_url = "/{}/{}".format(os.path.dirname(pdf), filename)
        pages.append(Page(
            counter,
            image_out_url,
            ext
        ))
        counter+=1
    return pages
