#! -*- coding:utf-8 -*-
from data_loader import data_generator, load_data
from model import E2EModel, Evaluate
from utils import extract_items, get_tokenizer, metric
import os, argparse
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from tensorflow.keras import backend as K

parser = argparse.ArgumentParser(description='Model Controller')
parser.add_argument('--train', default=False, type=bool, help='to train the HBT model, python run.py --train=True')
parser.add_argument('--dataset', default='WebNLG', type=str, help='specify the dataset from ["NYT","WebNLG","ACE04","NYT10-HRL","NYT11-HRL","Wiki-KBP"]')
args = parser.parse_args()


if __name__ == '__main__':
    # pre-trained bert model config
    bert_model = 'cased_L-12_H-768_A-12'
    bert_config_path = 'pretrained_bert_models/' + bert_model + '/bert_config.json'
    bert_vocab_path = 'pretrained_bert_models/' + bert_model + '/vocab.txt'
    bert_checkpoint_path = 'pretrained_bert_models/' + bert_model + '/bert_model.ckpt'

    dataset = args.dataset
    # train_path = '../data/webnlg_dataset/new/webnlg_train.json'
    # dev_path = '../data/webnlg_dataset/new/webnlg_dev.json'
    # test_path = '../data/webnlg_dataset/new/webnlg_test.json' 
    # rel_dict_path = '../data/rel2id.json'
    train_path = './data/WebNLG/train_triples.json'
    dev_path = './data/WebNLG/dev_triples.json'
    test_path = './data/WebNLG/test_triples.json' 
    rel_dict_path = './data/WebNLG/rel2id.json'
    save_weights_path = 'saved_weights/' + dataset + '/best_model.weights'
    
    LR = 1e-5
    tokenizer = get_tokenizer(bert_vocab_path)
    train_data, dev_data, test_data, id2rel, rel2id, num_rels = load_data(train_path, dev_path, test_path, rel_dict_path)
    subject_model, object_model, hbt_model = E2EModel(bert_config_path, bert_checkpoint_path, LR, num_rels)
    
    if args.train:
        BATCH_SIZE = 12
        EPOCH = 100
        MAX_LEN = 400
        STEPS = len(train_data) // BATCH_SIZE
        data_manager = data_generator(train_data, tokenizer, rel2id, num_rels, MAX_LEN, BATCH_SIZE)
        evaluator = Evaluate(subject_model, object_model, tokenizer, id2rel, dev_data, save_weights_path)
        hbt_model.fit_generator(data_manager.__iter__(),
                            steps_per_epoch=STEPS,
                            epochs=EPOCH,
                            callbacks=[evaluator]
                        )
    else:
        hbt_model.load_weights(save_weights_path)
        test_result_path = 'results/' + dataset + '/test_result.json'
        isExactMatch = True if dataset == 'Wiki-KBP' else False
        if isExactMatch:
            print("Exact Match")
        else:
            print("Partial Match")
        precision, recall, f1_score = metric(subject_model, object_model, test_data, id2rel, tokenizer, isExactMatch, test_result_path)
        print(f'{precision}\t{recall}\t{f1_score}')

