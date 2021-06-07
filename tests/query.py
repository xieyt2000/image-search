import pickle 
import io 
import numpy as np
from translate import Translator

def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

class QueryEngine:
    def __init__(self):
        self.class_embedding = pickle.load(open('class_embedding.pkl', 'rb'))
        self.embedding = self._load_vectors(limit=10000)
        self.classes = list(self.class_embedding.keys())
        self.embed_dim = 300 
        self.translator= Translator(from_lang="chinese",to_lang="english")


    def _load_vectors(self, limit=5000):
        fname = '../data/wiki-news-300d-1M.vec'
        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        data = {}
        cnt = 0
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = [float(t) for t in tokens[1:]] 
            cnt += 1
            if cnt >= limit:
                break
        return data

    def query(self, sentence, top=5):
        def cosine_sim(x, y):
            return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
        sentence = sentence.lower()
        words = sentence.split(' ')
        embed = np.zeros(self.embed_dim)
        for word in words:
            if word in self.embedding:
                embed += self.embedding[word]
        
        if np.sum(embed) == 0:
            return []
        similarity = []
        for c, c_embed in self.class_embedding.items():
            similarity.append(cosine_sim(c_embed, embed))
        similarity = np.asarray(similarity)
        indices = np.argsort(similarity)[::-1][:top]
        
        print(similarity[indices])
        ans = []
        for idx in indices:
            ans.append(self.classes[idx])
        return ans 
    
    def serve(self):
        while True:
            sentence = input('>> ')
            if is_chinese(sentence):
                sentence = self.translator.translate(sentence)
            if sentence == 'q':
                break
            print(self.query(sentence))

engine = QueryEngine()
engine.serve()