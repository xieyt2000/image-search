import csv


def cal_stat(labels):
    labels = list(map(int, labels))
    ap = sum([sum(labels[:i]) / i for i in range(1, 11)]) / len(labels)
    p10 = sum(labels) / len(labels)
    s10 = int(1 in labels)
    if s10:
        rr = 1 / (labels.index(1) + 1)
    else:
        rr = 0
    return [labels, ap, p10, rr, s10]


def main():
    with open("data.txt") as file:
        lines = file.read().splitlines()
    res = []
    for i in range(0, len(lines)):
        res.append(cal_stat(lines[i]))
    with open("result.csv", "w", encoding='utf_8_sig') as file:
        writer = csv.writer(file)
        writer.writerow(['labels', 'AP', "P@10", "RR", "success@10"])
        writer.writerows(res)

main()
