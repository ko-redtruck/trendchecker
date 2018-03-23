from steem import Steem
from steem import account
import requests
import json
import time

node = ["https://api.steemit.com"]
trx_list = json.load(open("trx_list.json"))
settings = json.load(open("settings.json"))

acc_name = settings["account name"]
keys=[settings["private posting key"], settings["private active key"]]

s = Steem(node,keys=keys)
ac= account.Account(acc_name,s)

def check_trending(url):
    
    memo = "TRENDCHECKER by @wil1liam: "
    #post to check
    try:
        author = url.split("/")[4].replace("@","")
        post_identifier = url.split("/")[5]
        post = s.get_content(author,post_identifier)
        tags = json.loads(post["json_metadata"])["tags"] + list([""])
    except:
        return "TRENDCHECKER error! wrong url or post doesn't exist..."


    for i in tags:
        trending_posts = s.get_discussions_by_trending({"limit":100,"tag":i.replace("-","")})
        hot_posts = s.get_discussions_by_hot({"limit":100,"tag":i})
        promoted_posts = s.get_discussions_by_promoted({"limit":100,"tag":i})

        count1 = 1
        count2 = 1
        count3 = 1
        
        if (i==""):
            memo += "All: "
        else:
            memo += i + ": "
            
        for o in trending_posts:
            if (o["author"]==author):
                print("trending---")
                print(i+ " --tag")
                print(count1)
                memo += str(count1)  +". in trending, "
                break
            count1 += 1

        for o in hot_posts:
            if (o["author"]==author):
                print("hot---")
                print(i+ " --tag")
                print(count2)
                memo += str(count2)  +". in hot "
                break
            count2 += 1

        for o in promoted_posts:
            if (o["author"]==author):
                print("promoted---")
                print(i + " --tag")
                print(count2)
                memo += str(count3)  +". in promoted"
                break
            count3 += 1
            
        memo += ", "
        
    return memo 
 

def validate_memo(memo):
    try:
        request = requests.get(memo)
        if (request.status_code == 200):
            return True
        else:
            return False

    except:
        return False
    
def send_back(trx,memo):
    amount,asset = trx["amount"].split(" ")
    sender = trx["from"]
    s.commit.transfer(sender,amount,asset,memo,account=acc_name)
    print("sending " + str(amount) + " to " + sender)

def generate_memo(url):
    memo = check_trending(url)
    return memo    
    
def add_to_trx_list(trx_id):
    trx_list["trx_id"].append(trx_id)

    with open('trx_list.json', 'w') as outfile:
        json.dump(trx_list, outfile)
    
        
while 1:
    try:
        transfers = ac.get_account_history(-1,500,filter_by=['transfer'])
    except:
        time.sleep(30)
        s = Steem(node,keys=keys)
        ac= account.Account(acc_name,s)

    for i in transfers:
        if(i["trx_id"] not in trx_list["trx_id"]):
            if (i["to"]==acc_name):
                if(i["memo"]!=""):
                    if (validate_memo(i["memo"])==True):

                        add_to_trx_list(i["trx_id"])
                        response = generate_memo(i["memo"])
                        send_back(i,response)

