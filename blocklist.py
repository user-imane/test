from adblockparser import AdblockRules
import sqlite3
import sys
import os
'''
raw_rules = [
     "||ads.example.com^",
    "@@||ads.example.com/notbanner^$~script",
]
'''
results = "/user/ifouad/home/Phd/blocklist"
raw_rules = []
raw_rules_easyp = []
db = os.path.join(results, 'allhomeblocked.sqlite')
conn2 = sqlite3.connect(db)
cur2 = conn2.cursor()
print db

cur2.execute(
    'CREATE TABLE IF NOT EXISTS blocked (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, '
    ' resp_id INTEGER NOT NULL, url TEXT, list TEXT ,'
    'PRIMARY KEY(site_id, link_id, resp_id )'
    ' )')

with open("/user/ifouad/home/PycharmProjects/OpenWpm/addblock/easylist", 'r') as f:
    for line in f:
        raw_rules.append(line)

with open("/user/ifouad/home/PycharmProjects/OpenWpm/addblock/easyprivacy", 'r') as f:
    for line in f:
        raw_rules_easyp.append(line)
rules = AdblockRules(raw_rules)
rules_priv = AdblockRules(raw_rules_easyp)
db2 = sys.argv[1]
conn = sqlite3.connect(db2)
curr = conn.cursor()
for site_id, link_id, response_id, url in curr.execute('select site_id, link_id, response_id, url from http_responses where link_id = 0 order by site_id ASC').fetchall():
    print  site_id, link_id, url
    if rules.should_block(url):
        cur2.execute("insert into blocked (site_id , link_id  , resp_id , url, list ) Values (?,?,?,?,?)",
                    (site_id,link_id, response_id, url, "easylist"))
    elif  rules_priv.should_block(url):
        cur2.execute("insert into blocked (site_id , link_id  , resp_id , url, list ) Values (?,?,?,?,?)",
                    (site_id,link_id, response_id, url, "easyprivacy"))
    else:
        cur2.execute("insert into blocked (site_id , link_id  , resp_id , url ) Values (?,?,?,?)",
                     (site_id, link_id, response_id, url))

    '''        
    print rules.should_block("http://search.ch/htmlbanner.html")
    print rules.should_block("g.doubleclick.net")
    print rules.should_block("http://ads.example.com/notbanner", {'script': False})
    '''

conn2.commit()
conn2.close()