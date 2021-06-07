from db.models import ImageEntry
from django.http import HttpResponse, Http404
from .utils import gen_response, search_query
from PIL import Image
import io

def get_image(request):
    image_id = request.GET.get('image', '')
    size =request.GET.get('size', '')

    query = ImageEntry.objects.filter(nid=image_id)
    if query.exists():
        path = query[0].path
        if size != '':
            w, h = size.split('*')
            w, h = int(w), int(h)
            im = Image.open(path)
            im.thumbnail((w, h), Image.ANTIALIAS)
            buf = io.BytesIO()
            im.save(buf, format='JPEG')
            content = buf.getvalue()
        else:
            f_img = open(path, 'rb')
            content = f_img.read()

        return HttpResponse(content=content, content_type='image/jpg')
    else:
        return Http404('image not found')


def main_search(request):
    query = request.GET.get('query', '')
    size = request.GET.get('size', 'Any Size')
    color_type = request.GET.get('colorType', 'Any Color')
    color = request.GET.get('color', '')
    page = int(request.GET.get('page', '1'))
    num = int(request.GET.get('num', '20'))

    images = search_query(query)
    total = len(images)
    if total == 0:
        return gen_response(code=201, data='', msg='No image found, please change your query')

    data = {'total': total, 'page': page, 'num': num, 'images': images[(page-1)*num:page*num]}
    return gen_response(data)


def get_similar(request):
    image = request.GET.get('image', '')
    num = int(request.GET.get('num', ''))
    images = []
    ie_objs = ImageEntry.objects.all()
    for ie in ie_objs[:num]:
        images.append(ie.nid)
    data = {'num': num, 'images': images}
    return gen_response(data)
