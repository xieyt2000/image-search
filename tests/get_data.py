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
        data[tokens[0]] = [float(t) for t in tokens[1:]] 
        cnt += 1
        if cnt >= limit:
            break
    return data

NUM_SAMPLE = 50
DATA_DIR = './data'
def main():
    
    dataset = foz.load_zoo_dataset(
        "open-images-v6",
        split="validation",
        dataset_dir=DATA_DIR,
        max_samples=NUM_SAMPLE,
        label_types=["classifications"],
        seed=0,
        shuffle=True,
    )
    print(dataset)
    info = dataset.info 
    print(info.keys()) # ['hierarchy', 'classes_map']
    classes = list(info['classes_map'].values())
    

    for idx, sample in enumerate(dataset):
        print(sample.filepath, sample.open_images_id)
        # for label in sample.positive_labels.classifications:
        #     print(label.label, label.confidence, label.id) # label is of type Classification
        for label in sample.negative_labels.classifications:
            print(label.label, label.confidence, label.id) # label is of type Classification
        break

    
    # classes = []
    # with open('./data/validation/metadata/classes.csv')as f:
    #     f_csv = csv.reader(f)
    #     for row in f_csv:
    #         classes.append(row[1])
    # embedding = load_vectors('../wiki-news-300d-1M.vec/wiki-news-300d-1M.vec', limit=300000)

    # class_embedding = {}
    # for c in classes:
    #     c = c.lower()
    #     tokens = c.split(' ')
    #     cls_embed = np.zeros(300)
    #     for token in tokens:
    #         token = token.replace('(', ' ')
    #         token = token.replace(')', ' ')
    #         token = token.strip()
    #         if token in embedding:
    #             token_embed = np.asarray(embedding[token])
    #         else:
    #             print(token)
    #             token_embed = np.zeros(300)
            
    #         cls_embed += token_embed
    #     if np.sum(np.abs(cls_embed)) > 0:
    #         class_embedding[c] = cls_embed
    
    # with open('class_embedding.pkl','wb') as f:
    #     pickle.dump(class_embedding, f)




if __name__ == '__main__':
    main()
