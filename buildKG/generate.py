import json
import collections
if __name__ == "__main__":
    links = []
    nodes = []
    raw_data = json.load(open('all_triples.json'))
    ifobjs = collections.defaultdict(int)
    ifsubs = collections.defaultdict(int)
    for triple in raw_data:
        # "group": 1,
        # "class": "character",
        # "size": 5,
        # "id": "IG-88"
        # {
        #     "source": "The Force Awakens",
        #     "value": 3,
        #     "target": "Luke Skywalker"
        # },
        obj, pro, sub = triple['object'], triple['property'], triple['subject']
        links.append({'relation':pro, 'source': obj, 'value' : 3, 'target' : sub})
        # {
        #     "class": "原料",
        #     "group": "2",
        #     "id": "蛋白",
        #     "size": "8"
        # },
        if ifobjs[obj] == 0:
            nodes.append({'class':'object', 'group': 0, 'id': obj ,'size':'8'})
            ifobjs[obj] += 1
        if ifsubs[sub] == 0:
            nodes.append({'class':'subject', 'group': 1, 'id': sub ,'size':'8'})
            ifsubs[sub] += 1
    ans = {'links':links, 'nodes':nodes}
    with open("d3_KG.json", 'w') as f:
        json.dump(ans, f)
        print("write into file overing...")