from image_search.db import DB
import colorsys
import math



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
    candidates = {}

    for token in tokens:
        token = token.strip()
        if not token in DB.word_vec: continue
        embed = DB.word_vec[token]
        all_sim = [(k, max([round(cosine_sim(embed, e), 4) for e in v['embed']])) for k, v in DB.label_info.items()]
        all_sim.sort(key=lambda x: x[1], reverse=True)
        print(all_sim[:3])
        for i, (label, sim) in enumerate(all_sim[:3]):
            label_info = DB.label_info[label]
            for img, score in label_info['invert_idx']:
                val = math.pow(10000, sim)
                if val < 0: val = 0
                if img in candidates:
                    candidates[img] += score * val
                else:
                    if score > 0.05:
                        candidates[img] = score * val
    candidates = list(candidates.items())
    candidates.sort(key=lambda x: x[1], reverse=True)

    for can in candidates[:10]:
        can_id = can[0]
        pos_labels = DB.img_info[can_id]['pos_labels']
        print(can[0], can[1], pos_labels)
    return [c[0] for c in candidates]


def search_similar(image_id, num):
    if image_id in DB.img_info:
        pos_labels = DB.img_info[image_id]['pos_labels']
        candidates = {}
        for label in pos_labels:
            invert_idx = DB.label_info[label]['invert_idx']
            for img, score in invert_idx:
                if img == image_id: continue
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
    c1 = colorsys.rgb_to_hsv(c1[0]/255, c1[1]/255, c1[2]/255)
    c2 = colorsys.rgb_to_hsv(c2[0]/255, c2[1]/255, c2[2]/255)
    dh = min(abs(c1[0] - c2[0]), 1 - abs(c1[0] - c2[0])) / 0.5
    ds = abs(c1[1] - c2[1])
    dv = abs(c1[2] - c2[2])
    distance = math.sqrt(dh * dh + ds * ds + dv * dv)
    return distance


def filter_color_size(images, color, size):
    if color == '' and size == '':
        return images
    if color != '':
        color_rgb = hex2rgb(color)

    candidates = []
    for img in images:
        info = DB.img_info[img]
        main_color = info['main_color']
        img_size = info['size']
        match = False
        match_diff = 0
        if color != '':
            for c in main_color:
                c_rgb = c[0]
                c_prop = c[1]
                diff = rgb_dist(color_rgb, c_rgb)
                if c_prop > 0.1 and diff < 0.25:
                    match = True
                    match_diff = diff
                    break
        if (size == '' or img_size == size) and (color == '' or match):
            candidates.append((img, match_diff))
    # candidates.sort(key=lambda x: x[1])
    return [c[0] for c in candidates]

