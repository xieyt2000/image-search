from django.http.response import JsonResponse
from db.models import WordEmbed, ImageLabel
import math
import json


def gen_response(data, msg='', code=200):
    return JsonResponse({
        'code': code,
        'data': data,
        'msg': msg
    })


def list_add(l1, l2):
    return [a1 + a2 for (a1, a2) in zip(l1, l2)]

def cosine_sim(l1, l2):
    dot = sum([a1*a2 for (a1, a2) in zip(l1, l2)])
    norm1 = math.sqrt(sum([a*a for a in l1]))
    norm2 = math.sqrt(sum([a*a for a in l2]))
    return dot/(norm1*norm2)


def search_query(query):
    query = query.lower()
    tokens = query.split(' ')
    embed = [0 for _ in range(300)]
    for token in tokens:
        token = token.strip()

        try:
            obj = WordEmbed.objects.get(word=token)
            embed = list_add(embed, json.loads(obj.embed))
        except:
            continue
    if sum(embed) == 0: return []
    all_labels = [(q['name'], q['embed']) for q in ImageLabel.objects.values("name", "embed")]
    all_sim = [(q[0], cosine_sim(embed, json.loads(q[1]))) for q in all_labels]
    all_sim.sort(key=lambda x: x[1], reverse=True)

    candidates = {}
    for label, sim in all_sim[:10]:
        label_obj = ImageLabel.objects.get(name=label)
        invert_idx = json.loads(label_obj.invert_idx)
        for img, score in invert_idx:
            if img in candidates:
                candidates[img] += score*sim
            else:
                candidates[img] = score*sim
    candidates = list(candidates.items())
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [c[0] for c in candidates]