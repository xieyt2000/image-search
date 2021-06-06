import io

def load_vectors(fname, limit=5000):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    cnt = 0
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
        cnt += 1
        if cnt >= limit:
            break
    return data

if __name__ == '__main__':
    data = load_vectors('../wiki-news-300d-1M.vec/wiki-news-300d-1M.vec')
    print(data.keys())