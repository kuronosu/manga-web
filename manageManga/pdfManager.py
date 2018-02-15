import PyPDF2
from PIL import Image
from os import path
from django.conf import settings

class Page:
    def __init__(self, number, pathname, formato, *args, **kwargs):
        self.number = number
        self.path = pathname
        self.formato = formato

def recurse(page, xObject, abspath):
    xObject = xObject['/Resources']['/XObject'].getObject()
    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj]._data
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"
            imagenamepath = "%s_page_%s"%(abspath[:-4], page)
            if xObject[obj]['/Filter'][0] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                formato = ".png"
                img.save(imagenamepath + formato)
            elif xObject[obj]['/Filter'][0] == '/DCTDecode':
                formato = ".jpg"
                img = open(imagenamepath + formato, "wb")
                img.write(data)
                img.close()
            elif xObject[obj]['/Filter'][0] == '/JPXDecode':
                formato = ".jp2"
                img = open(imagenamepath + formato, "wb")
                img.write(data)
                img.close()
        else:
            recurse(page, xObject[obj], abspath)
        return(imagenamepath, formato)

def extract_page(filename):
    file = PyPDF2.PdfFileReader(open(settings.BASE_DIR + "/media/" + filename, "rb"))
    abspath = path.abspath(settings.BASE_DIR + "/media/" + filename)
    pages = list(range(1, file.numPages+1))
    created_pages = []
    for p in pages:
        page0 = file.getPage(p-1)
        imagenamepath, formato = recurse(p, page0, abspath)
        page = Page(p, imagenamepath, formato)
        created_pages.append(page)
    return created_pages
