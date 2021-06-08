from django.http import HttpResponse, Http404, JsonResponse
from .utils import search_query, filter_color_size
from PIL import Image
import io
import time
from image_search.db import DB

def gen_response(data, msg='', code=200):
    return JsonResponse({
        'code': code,
        'data': data,
        'msg': msg
    })


def get_image(request):
    image_id = request.GET.get('image', '')
    size = request.GET.get('size', '')

    if image_id in DB.img_info:
        path = DB.img_info['path']
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
    size = request.GET.get('size', '')
    color = request.GET.get('color', '')
    page = int(request.GET.get('page', '1'))
    num = int(request.GET.get('num', '20'))

    start = time.time()
    images = search_query(query)
    print(time.time() - start)
    images = filter_color_size(images, color, size)
    print(time.time() - start)
    total = len(images)
    if total == 0:
        return gen_response(code=201, data='', msg='No image found, please change your query')

    data = {'total': total, 'page': page, 'num': num, 'images': images[(page - 1) * num:page * num]}
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
