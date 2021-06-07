import fiftyone.zoo as foz
import fiftyone 
import io 
import numpy as np 
import pickle 
import csv

def load_vectors(fname, limit=5000):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    cnt = 0
    for line in fin:
        tokens = line.rstrip().split(' ')
        #print(tokens[0])
        data[tokens[0]] = [float(t) for t in tokens[1:]] 
        cnt += 1
        if cnt >= limit:
            break
    return data

NUM_SAMPLE = 5000
DATA_DIR = '../data'
def main():
    # dataset = foz.load_zoo_dataset(
    #     "open-images-v6",
    #     split="validation",
    #     dataset_dir=DATA_DIR,
    #     max_samples=NUM_SAMPLE,
    #     label_types=["classifications"],
    #     seed=0,
    #     shuffle=True,
    # )
    
    # all_labels = set()
    # all_names = set()
    # for idx, sample in enumerate(dataset):
    #     for label in sample.positive_labels.classifications + sample.negative_labels.classifications:
    #         all_labels.add((label.id, label.label))
    #         all_names.add(label.label)
    # print(len(all_labels))
    # print(len(all_names))
    
    classes = []
    with open('../data/validation/metadata/classes.csv')as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            classes.append(row[1])
    embedding = load_vectors('../data/wiki-news-300d-1M.vec', limit=500000)

    class_embedding = {}
    for c in classes:
        c = c.lower()
        tokens = c.split(' ')
        cls_embed = np.zeros(300)
        for token in tokens:
            token = token.replace('(', ' ')
            token = token.replace(')', ' ')
            token = token.strip()
            if token in embedding:
                token_embed = np.asarray(embedding[token])
            else:
                print(token)
                token_embed = np.zeros(300)
            
            cls_embed += token_embed
        if np.sum(np.abs(cls_embed)) > 0:
            class_embedding[c] = cls_embed
    
    with open('class_embedding.pkl','wb') as f:
        pickle.dump(class_embedding, f)




if __name__ == '__main__':
    main()
