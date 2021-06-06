# Image Search

A simple image search engine.



### Backend Usage

```
cd image_search
python manage.py makemigrations
python manage.py migrate
python manage.py init_data [path-to-image-folder] [number of images]
python manage.py runserver 127.0.0.1:8000
```

[path-to-image-folder] should be the absolute path of the `data/` folder in the root directory
