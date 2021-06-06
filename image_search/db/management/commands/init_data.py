from django.core.management.base import BaseCommand, CommandError
from db.models import ImageEntry, ImageLabel
import fiftyone.zoo as foz
from tqdm import tqdm
import colorgram
import json

class Command(BaseCommand):
    help = 'get all data from fiftyone'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str, default='')
        parser.add_argument('num_img', type=int, default=5000)

    def handle(self, *args, **options):
        dataset = foz.load_zoo_dataset(
            "open-images-v6",
            split="validation",
            dataset_dir=options['data_dir'],
            max_samples=options['num_img'],
            label_types=["classifications"],
            seed=0,
            shuffle=True,
        )
        for sample in tqdm(dataset):
            ie = ImageEntry()
            ie.nid = sample.open_images_id
            ie.path = sample.filepath
            ie.pos_labels = json.dumps([l.id for l in sample.positive_labels.classifications])
            ie.neg_labels = json.dumps([l.id for l in sample.negative_labels.classifications])

            ie.save()
            for l in sample.positive_labels.classifications + sample.negative_labels.classifications:
                query = ImageLabel.objects.filter(nid=l.id)
                if not query.exists():
                    il = ImageLabel()
                    il.nid = l.id
                    il.name = l.label
                    il.embed = ''
                    il.save()

