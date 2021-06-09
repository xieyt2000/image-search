# Image Search

A simple image search engine. 

Project of *Fundamentals of Search Engine Technology* (THU 2021).

**Developer**: yueyang2000, xieyt2000

### Backend Usage

- Download FastText [word vectors](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip) , decompress and save to `./data/wiki-news-300d-1M.vec`  
- Run commands:

```
cd image_search
python init_data.py
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

- For `init_data.py`, full usage:

    - `--img_size`: how many image to include, default 5000

    - `--word_size`: how many word vectors to save, default 20000

    - `--build_index`: to build index only, without init data again

### Frontend Usage

- You shoud have node.js installed, then run:

```
cd frontend
npm install
npm run dev
```

