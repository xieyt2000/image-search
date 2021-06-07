from db.models import ImageEntry, ImageLabel
import json

image_entry_cache = {obj.nid: (json.loads(obj.main_color), obj.size) for obj in ImageEntry.objects.all()}

all_labels_cache = [(q['name'], q['embed']) for q in ImageLabel.objects.values("name", "embed")]
