from django.core.management.base import BaseCommand, CommandError
from db.models import ImageEntry, ImageLabel, WordEmbed
import fiftyone.zoo as foz
from tqdm import tqdm
from collections import OrderedDict
import json
import io
import os
import gc

def load_vectors(fname, limit=5000):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    data = OrderedDict()
    cnt = 0
    for line in tqdm(fin):
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = [float(t) for t in tokens[1:]]
        cnt += 1
        if cnt >= limit:
            break
    return data


def list_add(l1, l2):
    return [a1 + a2 for (a1, a2) in zip(l1, l2)]



class Command(BaseCommand):
    help = 'get all data from fiftyone'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str, default='')
        parser.add_argument('num_img', type=int, default=5000)

    def handle(self, *args, **options):
        print('Save image info...')
        dataset = foz.load_zoo_dataset(
            "open-images-v6",
            split="validation",
            dataset_dir=options['data_dir'],
            max_samples=options['num_img'],
            label_types=["classifications"],
            seed=0,
            shuffle=True,
        )
        all_labels = set()
        for sample in tqdm(dataset):
            ie = ImageEntry()
            ie.nid = sample.open_images_id
            ie.path = sample.filepath
            ie.pos_labels = json.dumps([l.label.lower() for l in sample.positive_labels.classifications])
            ie.neg_labels = json.dumps([l.label.lower() for l in sample.negative_labels.classifications])
            ie.save()
            for label in sample.positive_labels.classifications + sample.negative_labels.classifications:
                all_labels.add(label.label.lower())
        for l in tqdm(all_labels):
            il = ImageLabel()
            il.name = l.lower()
            il.save()

        del dataset
        gc.collect()

        vectors = load_vectors(os.path.join(options['data_dir'], 'wiki-news-300d-1M.vec'), limit=500000)
        print('Processing labels...')
        all_tokens = set()
        all_labels = ImageLabel.objects.all()
        for label_obj in all_labels:
            label = label_obj.name
            tokens = label.split(' ')
            embed = [0 for _ in range(300)]
            for token in tokens:
                token = token.replace('(', '')
                token = token.replace(')', '')
                token = token.strip()
                all_tokens.add(token)
                embed = list_add(embed, vectors[token])
            label_obj.embed = embed
            label_obj.save()
        print(all_tokens)
        all_tokens = all_tokens | set(list(vectors.keys())[:20000])
        print('Save word vectors...')
        for word in tqdm(all_tokens):
            if not word.isalpha(): continue
            if len(word) <= 2: continue
            we = WordEmbed()
            we.word = word.lower()
            we.embed = json.dumps(vectors[word])
            we.save()
