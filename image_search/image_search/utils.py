from django.http.response import JsonResponse


def gen_response(data, msg='', code=200):
    return JsonResponse({
        'code': 200,
        'data': data,
        'msg': msg
    })
