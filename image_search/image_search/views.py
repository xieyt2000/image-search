from db.models import ImageEntry
from django.http import HttpResponse, Http404
from .utils import gen_response


def get_image(request):
    image_id = request.GET.get('image', '')
    query = ImageEntry.objects.filter(nid=image_id)
    if query.exists():
        f_img = open(query[0].path, 'rb')
        return HttpResponse(content=f_img.read(), content_type='image/jpg')
    else:
        return Http404('image not found')


def main_search(request):
    query_word = request.GET.get('query', '')
    size = request.GET.get('size', 'Any Size')
    color_type = request.GET.get('colorType', 'Any Color')
    color = request.GET.get('color', '')
    page = int(request.GET.get('page', '1'))
    num = int(request.GET.get('num', '20'))
    images = []
    total = 50
    ie_objs = ImageEntry.objects.all()
    for ie in ie_objs[:total]:
        images.append(ie.nid)
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
