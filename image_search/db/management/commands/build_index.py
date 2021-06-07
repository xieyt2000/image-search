from django.core.management.base import BaseCommand, CommandError
from db.models import ImageEntry, ImageLabel, WordEmbed
import json
from tqdm import tqdm
import os
import colorgram
from PIL import Image


class Command(BaseCommand):
    help = 'build label index, analyze image'

    def handle(self, *args, **options):

        const = 0.05
        all_label = [q['name'] for q in ImageLabel.objects.values("name")]
        all_score = {l: {} for l in all_label}
        for img_obj in tqdm(ImageEntry.objects.all()):
            pos_labels = json.loads(img_obj.pos_labels)
            neg_labels = json.loads(img_obj.neg_labels)
            score_tot = len(pos_labels) + const * len(neg_labels) + 1 # in case of no pos label
            for l in pos_labels:
                all_score[l][img_obj.nid] = 1 / score_tot
            for l in neg_labels:
                all_score[l][img_obj.nid] = const / score_tot
        for label_obj in tqdm(ImageLabel.objects.all()):
            indices = list(all_score[label_obj.name].items())
            indices.sort(key=lambda x: x[1], reverse=True)
            label_obj.invert_idx = json.dumps(indices)
            label_obj.save()

        for img_obj in tqdm(ImageEntry.objects.all()):
            path = img_obj.path
            file_size = os.path.getsize(path)
            if file_size > 350*1024:
                img_obj.size = 'Large'
            elif file_size > 150*1024:
                img_obj.size = 'Medium'
            else:
                img_obj.size = 'Small'
            im = Image.open(path)
            im.thumbnail((100, 100))
            main_colors = colorgram.extract(im, 5)
            color_list = [(tuple(c.rgb), c.proportion) for c in main_colors]
            img_obj.main_color = json.dumps(color_list)
            img_obj.save()

