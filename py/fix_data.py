## coding = utf-8

#pip install redis
#pip install pymysql

import pymysql
import redis

#rds = redis.Redis(host='192.168.1.235', port=6380,password='qx123456!@#',decode_responses=True)
rds = redis.Redis(host='127.0.0.1', port=6380 ,password='qx123456!@#',decode_responses=True)
                  
rds.hset('qxy:servicer:S0000002', 'type','1')
rds.hset('qxy:servicer:S0000002', 'status','quit')

'''
host = '192.168.1.234'
port = 3306
user = 'root'
pwd = '123456'
db = 'ox_user'
'''

host = '127.0.0.1'
port = 3306
user = 'db_ox'
pwd = 'Db1123_Rd_Qx'
db = 'ox_user'


conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=db)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

sql = 'select u.servicer_id, u.servicer_type, us.scope_id, u.`name`,u.phone, u.name from m_user u ,m_user_scope us where u.id=us.user_id and u.servicer_id !="" order by u.servicer_id'
cursor.execute(sql)

rows = cursor.fetchall()
#print('records:\n'+str(rows))

for r in rows:
    sid = r['servicer_id']
    stype = r['servicer_type']
    shopId = r['scope_id']
    shopName = r['name']
    phone = r['phone']
    uname = r['name']
    rds.hset('qxy:servicer:' + sid, 'status','quit')
    print('sid:' + sid + '_stype:' + stype +'_shopId:' + shopId + '_shopName:' + shopName)
    if stype == 'SHOP_IM':
        #print('sid:' + sid + '_stype:' + stype +'_shopId:' + shopId + '_shopName:' + shopName)
        tmp = rds.hget('qxy:servicer:' + sid, 'shopId')
        if tmp != None and tmp != shopId:
           shopId = shopId + ',' + tmp
        rds.hset('qxy:servicer:' + sid, 'shopName',shopName)
        rds.hset('qxy:servicer:' + sid, 'shopId',shopId)
        rds.hset('qxy:servicer:' + sid, 'phone',phone)
        rds.hset('qxy:servicer:' + sid, 'uname',uname)
    if stype == 'PLATFORM_IM':
        rds.hset('qxy:servicer:' + sid, 'type','0')
        
cursor.close()
conn.close()

rds.close()

print('fix data done')