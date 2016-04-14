
def check(filename):
    fr = open(filename, 'r')
    sku_idx = fr.readline().replace('\n', '').split('\t').index('sku_id')
    count = 0
    sku_id_list = []
    while True:
        line = fr.readline().strip().replace('\n', '')
        if not line:
            break
        else:
            count += 1
            sku_id = line.split('\t')[sku_idx]
            if sku_id in sku_id_list:
                print count
                continue
            else:
                sku_id_list.append(sku_id)
    print count, len(sku_id_list)

if __name__ == '__main__':
    check("E:1688_04-06-2016_productInfo.csv")