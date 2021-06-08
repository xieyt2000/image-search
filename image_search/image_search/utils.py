import math
import json
import time
from image_search.db import DB
import colorsys

def list_add(l1, l2):
    return [a1 + a2 for (a1, a2) in zip(l1, l2)]


def cosine_sim(l1, l2):
    dot = sum([a1 * a2 for (a1, a2) in zip(l1, l2)])
    norm1 = math.sqrt(sum([a * a for a in l1]))
    norm2 = math.sqrt(sum([a * a for a in l2]))
    return dot / (norm1 * norm2)


def search_query(query):
    query = query.lower()
    tokens = query.split(' ')
    embed = [0 for _ in range(300)]
    for token in tokens:
        token = token.strip()
        if token in DB.word_vec:
            embed = list_add(embed, DB.word_vec[token])
        else:
            continue
    if sum(embed) == 0: return []

    all_sim = [(k, cosine_sim(embed, v['embed'])) for k, v in DB.label_info.items()]
    all_sim.sort(key=lambda x: x[1], reverse=True)
    # print(all_sim[:10])
    candidates = {}
    for i, (label, sim) in enumerate(all_sim[:3]):
        label_info = DB.label_info[label]
        for img, score in label_info['invert_idx']:
            val = math.pow(100, sim)
            if val < 0: val = 0
            if img in candidates:
                candidates[img] += score * val
            else:
                if score > 0.05:
                    candidates[img] = score * val
    candidates = list(candidates.items())
    candidates.sort(key=lambda x: x[1], reverse=True)

    # for can in candidates[:10]:
    #     can_id = can[0]
    #     obj = ImageEntry.objects.get(nid=can_id)
    #
    #     print(can[1], obj.pos_labels, obj.neg_labels)
    return [c[0] for c in candidates]


def search_similar(image_id, num):
    if image_id in DB.img_info:
        pos_labels = DB.img_info[image_id]
        candidates = {}
        for label in pos_labels:
            invert_idx = DB.label_info[label]
            for img, score in invert_idx:
                if score < 0.05: break
                if img in candidates:
                    candidates[img] += score
                else:
                    candidates[img] = score
        candidates = list(candidates.items())
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:num]]
    else:
        return []



def hex2rgb(hexcode):
    r = int(hexcode[1:3], 16)
    g = int(hexcode[3:5], 16)
    b = int(hexcode[5:7], 16)
    return r, g, b


def rgb_dist(c1, c2):
    # https://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way/8863952
    rmean = (c1[0] + c2[0]) / 2
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return math.sqrt(((512 + rmean) * dr * dr) / 256 + 4 * dg * dg + ((767 - rmean) * db * db) / 256)


def filter_color_size(images, color, size):
    if color == '' and size == '':
        return images
    ans = []
    if color != '':
        color_rgb = hex2rgb(color)

    # objs = ImageEntry.objects.all()
    # list(objs)

    for img in images:
        info = DB.img_info[img]
        main_color = info['main_color']
        img_size = info['size']
        match = False
        if color != '':
            diff = []
            for c in main_color:
                c_rgb = c[0]
                c_prop = c[1]
                diff = rgb_dist(color_rgb, c_rgb)
                if c_prop > 0.2 and diff < 300:
                    match = True

        if (size == '' or img_size == size) and (color == '' or match):
            ans.append(img)
    return ans

