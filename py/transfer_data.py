import redis
import re
import json
from py2neo import Graph,Node,Relationship,NodeSelector


rds = redis.Redis(host='192.168.1.235', port=6380,password='qx123456!@#',decode_responses=True)

#graph = Graph("http://localhost:7474",auth=("neo4j","neo4j"))
graph = Graph("bolt://localhost:7687", username="neo4j", password = "neo4j")

                  
c_s_relatiions = {}
c_s_keys = []
c_s_msgs = []

tmp_keys = rds.keys('qxy:chatRelation*')
#print(tmp_keys)

for key in tmp_keys:
    if re.match(r'qxy:chatRelation:S[0-9]{7}', key):
        c_s_keys.append(key)
        
    
for key in c_s_keys:
    customers = []
    customers = rds.smembers(key)
    c_s_relatiions[key.split(':')[2]] = customers
    
'''
sid is the key of c_s_relatiions, for example S0000003
'''
selector = NodeSelector(graph)
for sid in c_s_relatiions:
    c_set =  c_s_relatiions[sid]
#    if sid != 'S0000003':
#        continue
    _snode = selector.select('Servicer', servicer_id = sid).first()
    _node = Node('Servicer', servicer_id = sid)
    _servicer = rds.hgetall('qxy:servicer:' + sid)
    if _snode:
        _snode.update(_servicer)
        graph.push(_snode)
    else:
        _node.update(_servicer)
        graph.create(_node)
        _snode = _node

    for c in c_set:
#        if c != '13551472168':
#            continue
        _cnode = selector.select('Customer', pid = c).first()
        if not _cnode:
            _node = Node('Customer', pid = c)
            graph.create(_node)
            _cnode = _node
        
        _msg_keys = [] # msg:sid:pid:*
        _str = 'qxy:msgRecord:' + sid + ':' + c + '*'
        _dates = rds.keys(_str)
        for key in _dates:
            _msgs = rds.zrange(key, 0, -1)
            for msg in _msgs:
                #c_s_msgs.append(msg)
                _json_msg = json.loads(msg)
                if 'extras' in _json_msg.keys():
                    _json_msg['extras'] =  json.dumps(_json_msg['extras'])
                if 'item' in _json_msg.keys():
                    _json_msg['item'] = json.dumps(_json_msg['item'])
                _from = _json_msg['from']
                if _from == sid:
                    _chat_relation = Relationship(_snode, "CHAT_" + str(_json_msg['createTime']), _cnode)
                    _chat_relation.update(_json_msg)
                    graph.create(_chat_relation)
                else:
                    _chat_relation = Relationship(_cnode, "CHAT_" + str(_json_msg['createTime']), _snode)
                    _chat_relation.update(_json_msg)
                    graph.create(_chat_relation)
                    
            

       
 
graph.delete_all()    
    

'''
s = Node('Servicer')
c = Node('Customer', pid = '17830746958')
graph.create(s)
graph.create(c)


cs = Relationship(c, "CHAT", s)
graph.create(cs)


### update data of node or relationship
sc['time'] = '2019-12-23 00:00:00'
sc['chatType'] = '0'
graph.push(sc)

servicer = {
        "servicer_id": "S0000005",
        "registration_id": "",
        "type": "0",
        "lastTime": "2019-12-16 10:24:15.802",
        "count": 0,
        "status": "quit",
        "realName": "体验馆客服"
    }

print('name' in servicer.keys())


s.update(servicer)
graph.push(s)


### delete node or relationship
relationship = graph.match_one(r_type = 'CHAT')
graph.delete(relationship)
graph.delete(s)
graph.delete(c)


### NodeSelector 根据多个条件进行 Node 的查询
selector = NodeSelector(graph)
servicers = selector.select('Servicer', servicer_id = 'S0000005')
graph.delete(list(servicers)[1])
'''











