import pickle


class DB:
    _db = pickle.load(open('../data/db.pkl', 'rb'))
    img_info = _db['img_info']
    label_info = _db['label_info']
    word_vec = _db['word_vec']

# image_entry_cache = {obj.nid: (json.loads(obj.main_color), obj.size) for obj in ImageEntry.objects.all()}
#
# all_labels_cache = [(q['name'], q['embed']) for q in ImageLabel.objects.values("name", "embed")]
