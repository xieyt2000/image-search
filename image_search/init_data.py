import os, json, argparse, io, gc, pickle
from collections import OrderedDict
from tqdm import tqdm
from PIL import Image
import colorgram
import fiftyone.zoo as foz
import math

parser = argparse.ArgumentParser('Initialize Data For the Search Engine')
parser.add_argument('--img_size', type=int, default=5000)
parser.add_argument('--word_size', type=int, default=20000)
parser.add_argument('--data_dir', type=str, default='../data')
parser.add_argument('--build_index', action='store_true', default=False, help='Build Index Only')
args = parser.parse_args()

IMG_SIZE = args.img_size
WORD_SIZE = args.word_size
DATA_DIR = args.data_dir


def load_vectors(fname, limit=5000, filter=[]):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    data = OrderedDict()
    cnt = 0
    for line in tqdm(fin):
        cnt += 1
        if cnt >= limit:
            break
        tokens = line.rstrip().split(' ')
        if (not tokens[0] in filter) and cnt > WORD_SIZE: continue
        data[tokens[0].lower()] = [float(t) for t in tokens[1:]]

    return data


def list_add(l1, l2):
    return [a1 + a2 for (a1, a2) in zip(l1, l2)]


def init_data():
    print('Save image info...')
    dataset = foz.load_zoo_dataset(
        "open-images-v6",
        split="validation",
        dataset_dir=DATA_DIR,
        max_samples=IMG_SIZE,
        label_types=["classifications"],
        seed=0,
        shuffle=True,
    )
    img_info = {}
    all_labels = set()
    for sample in tqdm(dataset):
        img_info[sample.open_images_id] = dict(
            path=sample.filepath,
            pos_labels=[l.label.lower() for l in sample.positive_labels.classifications],
            neg_labels=[l.label.lower() for l in sample.negative_labels.classifications]
        )
        for label in sample.positive_labels.classifications + sample.negative_labels.classifications:
            all_labels.add(label.label.lower())

    label_info = {l: {} for l in all_labels}

    del dataset
    gc.collect()


    print('Processing labels...')
    all_tokens = set()
    for label in all_labels:
        tokens = label.split(' ')
        for token in tokens:
            token = token.replace('(', '')
            token = token.replace(')', '')
            token = token.strip()
            all_tokens.add(token)
    vectors = load_vectors(os.path.join(DATA_DIR, 'wiki-news-300d-1M.vec'), limit=500000, filter=all_tokens)
    for label in all_labels:
        tokens = label.split(' ')
        embed = []
        for token in tokens:
            token = token.replace('(', '')
            token = token.replace(')', '')
            token = token.strip()
            embed.append(vectors[token])
        label_info[label]['embed'] = embed

    all_words = [w.lower() for w in vectors.keys()]
    all_tokens = all_tokens | set(all_words)
    print('Save word vectors...')
    filtered_tokens = []
    for word in tqdm(all_tokens):
        if word.isalpha() and len(word) > 2:
            filtered_tokens.append(word)
    word_vec = {word: vectors[word] for word in filtered_tokens}

    db = dict(
        img_info=img_info,
        label_info=label_info,
        word_vec=word_vec
    )

    print('Analyze img metainfo')
    for info in tqdm(db['img_info'].values()):
        path = info['path']
        file_size = os.path.getsize(path)
        if file_size > 350 * 1024:
            info['size'] = 'Large'
        elif file_size > 150 * 1024:
            info['size'] = 'Medium'
        else:
            info['size'] = 'Small'
        im = Image.open(path)
        im.thumbnail((100, 100))
        main_colors = colorgram.extract(im, 5)
        color_list = [(tuple(c.rgb), c.proportion) for c in main_colors]
        info['main_color'] = color_list

    pickle.dump(db, open(os.path.join(DATA_DIR, 'db.pkl'), 'wb'))
    return db


def build_index(db=None):
    if db is None:
        db = pickle.load(open(os.path.join(DATA_DIR, 'db.pkl'), 'rb'))
    const = 0.05
    all_label = list(db['label_info'].keys())
    all_score = {l: {} for l in all_label}

    print('Computing index')
    for img, info in tqdm(db['img_info'].items()):
        pos_labels = info['pos_labels']
        neg_labels = info['neg_labels']
        for l in pos_labels:
            all_score[l][img] = 1 + 1 / (1 + math.log(len(pos_labels)))
        for l in neg_labels:
            all_score[l][img] = const / len(neg_labels)

    for label, info in tqdm(db['label_info'].items()):
        indices = list(all_score[label].items())
        indices.sort(key=lambda x: x[1], reverse=True)
        info['invert_idx'] = indices
    pickle.dump(db, open(os.path.join(DATA_DIR, 'db.pkl'), 'wb'))



if __name__ == '__main__':
    if not args.build_index:
        build_index(init_data())
    else:
        build_index()
