from django.http.response import JsonResponse
from db.models import WordEmbed, ImageLabel, ImageEntry
import math
import json
import time




def list_add(l1, l2):
    return [a1 + a2 for (a1, a2) in zip(l1, l2)]

def cosine_sim(l1, l2):
    dot = sum([a1*a2 for (a1, a2) in zip(l1, l2)])
    norm1 = math.sqrt(sum([a*a for a in l1]))
    norm2 = math.sqrt(sum([a*a for a in l2]))
    return dot/(norm1*norm2)


def search_query(query):
    from image_search import cache
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

    all_sim = [(q[0], cosine_sim(embed, json.loads(q[1]))) for q in cache.all_labels_cache]
    all_sim.sort(key=lambda x: x[1], reverse=True)
    # print(all_sim[:10])
    candidates = {}
    for i, (label, sim) in enumerate(all_sim[:3]):
        label_obj = ImageLabel.objects.get(name=label)
        invert_idx = json.loads(label_obj.invert_idx)
        for img, score in invert_idx[:(3-i)*100]:
            if score < 0.05: break
            val = math.pow(100, sim)
            if val < 0: val = 0
            if img in candidates:
                candidates[img] += score*val
            else:
                candidates[img] = score*val
    candidates = list(candidates.items())
    candidates.sort(key=lambda x: x[1], reverse=True)

    # for can in candidates[:10]:
    #     can_id = can[0]
    #     obj = ImageEntry.objects.get(nid=can_id)
    #
    #     print(can[1], obj.pos_labels, obj.neg_labels)
    return [c[0] for c in candidates]


def hex2rgb(hexcode):
    r = int(hexcode[1:3], 16)
    g = int(hexcode[3:5], 16)
    b = int(hexcode[5:7], 16)
    return (r,g,b)

def rgb_dist(c1, c2):
    # https://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way/8863952
    rmean = (c1[0] + c2[0]) / 2
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return math.sqrt(((512+rmean)*dr*dr)/256 + 4*dg*dg + ((767-rmean)*db*db)/256)


def filter_color_size(images, color, size):
    from image_search import cache
    if color == '' and size == '':
        return images
    ans = []
    if color != '':
        color_rgb = hex2rgb(color)

    # objs = ImageEntry.objects.all()
    # list(objs)

    for img in images:
        main_color, img_size = cache.image_entry_cache[img]
        if color != '':
            diff = 0
            for c in main_color:
                c_rgb = c[0]
                c_prop = c[1]
                diff += rgb_dist(color_rgb, c_rgb) * c_prop
        if (size == '' or img_size == size) and (color == '' or diff < 250):
            ans.append(img)
    return ans


