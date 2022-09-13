import json
import tqdm
import os

data_folder = 'webnlg_dataset'
raw_folder = 'raw'
new_folder = 'new'

raw_train_data_file = os.path.join(data_folder, raw_folder, 'webnlg_release_v2.1_train.json')
raw_dev_data_file = os.path.join(data_folder, raw_folder, 'webnlg_release_v2.1_dev.json')
raw_test_data_file = os.path.join(data_folder, raw_folder, 'webnlg_release_v2.1_test.json')



if not os.path.exists(os.path.join(data_folder, new_folder)):
    os.mkdir(os.path.join(data_folder, new_folder))
    
processed_train_data_file = os.path.join(data_folder, new_folder, 'webnlg_train.json')
processed_dev_data_file = os.path.join(data_folder, new_folder, 'webnlg_dev.json')
processed_test_data_file = os.path.join(data_folder, new_folder, 'webnlg_test.json')



unused_labels = ['originaltriplesets', 'xml_id', 'size', 'shape', 'shape_type']
relations = set()

def generate(data:list):
    ans = []
    
    for tri in data:
        sub, obj, rel = tri['object'], tri['subject'] , tri['property']
        ans.append([sub, rel, obj])
        relations.add(rel)
    return ans
    root = list(parent.keys())[0]
    while root in parent:
        root = parent[root]
        
    seq = []
    relation_list = []
    def dfs(root:str):
        seq.append(root)
        if root in children:
            for child in children[root]:
                relation_list.append(relations[(root, child)])
                seq.append('[P]')
                dfs(child)
    dfs(root)
    return seq, relation_list


if __name__ == '__main__':
    
    print('Collect process data...')
    file_dict = {'Train' : (raw_train_data_file, processed_train_data_file), 
                'Dev' : (raw_dev_data_file, processed_dev_data_file), 
                'Test' : (raw_test_data_file, processed_test_data_file)}
    for k, v in file_dict.items():
        print('Processing %s file' % k)
        raw_data = json.load(open(v[0]))['entries']
        data_samples = [data_sample[list(data_sample.keys())[0]] for data_sample in raw_data]
        
        new_data_samples = []
        for data_sample in tqdm.tqdm(data_samples):
            new_data_sample = {}
            for label in unused_labels:
                data_sample.pop(label)
            triples = data_sample['modifiedtripleset']
            new_data_sample['triple_list'] = generate(triples)
            new_data_sample['text'] = ' '.join([sent['lex'] for sent in data_sample.pop('lexicalisations')])
            new_data_samples.append(new_data_sample)
        
        with open(v[1], 'w') as f:
            json.dump(new_data_samples, f)
            print("write into file overing...")
    
    rel2id, id2rel = {}, {}
    for i, value in enumerate(list(relations)):
        rel2id[str(i)] = value
        id2rel[value] = i

    result = [rel2id, id2rel]
    with open("rel2id.json", 'w') as f:
        json.dump(result, f)
        print("write into file overing...")
    