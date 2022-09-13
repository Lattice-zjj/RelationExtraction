import json
import tqdm
import os

data_folder = 'webnlg_dataset'
raw_folder = 'raw'
new_folder = 'new'

raw_train_data_file = os.path.join('../data', data_folder, raw_folder, 'webnlg_release_v2.1_train.json')
raw_dev_data_file = os.path.join('../data', data_folder, raw_folder, 'webnlg_release_v2.1_dev.json')
raw_test_data_file = os.path.join('../data', data_folder, raw_folder, 'webnlg_release_v2.1_test.json')

unused_labels = ['originaltriplesets', 'xml_id', 'size', 'shape', 'shape_type']


def generate(data:list):
    ans = []
    
    for tri in data:
        sub, obj, rel = tri['subject'], tri['object'], tri['property']
        ans.append([sub, rel, obj])
    return ans


def getAlltriples():
    
    all_ans = []
    
    print('Collecting process data...')
    file_dict = {'Test' : (raw_test_data_file)}
    for k, v in file_dict.items():
        print('Processing %s file %s' % (k, v))
        raw_data = json.load(open(v))['entries']
        data_samples = [data_sample[list(data_sample.keys())[0]] for data_sample in raw_data]
        
        new_data_samples = []
        for data_sample in tqdm.tqdm(data_samples):
            new_data_sample = {}
            for label in unused_labels:
                data_sample.pop(label)
            triples = data_sample['modifiedtripleset']
            all_ans.extend(triples)
    print(len(all_ans))
    return all_ans
    