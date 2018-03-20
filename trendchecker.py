from steem import Steem
from steem import account
import requests
import json

node = ["https://api.steemit.com"]
trx_list = json.load(open("trx_list.json"))
settings = json.load(open("settings.json"))

acc_name = settings["account name"]
keys=[settings["private posting key"], settings["private active key"]]

s = Steem(node,keys=keys)
ac= account.Account(acc_name,s)

def check_trending(url):

    #post to check
    author = url.split("/")[4].replace("@","")
    post_identifier = url.split("/")[5]
    post = s.get_content(author,post_identifier)
    tags = json.loads(post["json_metadata"])["tags"] + list([""])


    for i in tags:
        trending_posts = s.get_discussions_by_trending({"limit":100,"tag":i.replace("-","")})
        hot_posts = s.get_discussions_by_hot({"limit":100,"tag":i})
        promoted_posts = s.get_discussions_by_promoted({"limit":100,"tag":i})

        count1 = 1
        count2 = 1
        count3 = 1

        for o in trending_posts:
            if (o["author"]==author):
                print("trending---")
                print(i+ " --tag")
                print(count1)
                break
            count1 += 1

        for o in hot_posts:
            if (o["author"]==author):
                print("hot---")
                print(i+ " --tag")
                print(count2)
                break
            count2 += 1

        for o in promoted_posts:
            if (o["author"]==author):
                print("promoted---")
                print(i + " --tag")
                print(count2)
                break
            count3 += 1

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

def generate_memo(url):
    memo = check_trending(url)
    memo = memo
    return memo    
    
def add_to_trx_list(trx_id):
    trx_list["trx_id"].append(trx_id)

    with open('trx_list.json', 'w') as outfile:
        json.dump(trx_list, outfile)
        
def refund(username):
    sent_amount_SBD = 0
    received_amount_SBD = 0
    sent_amount_STEEM = 0
    received_amount_STEEM = 0

    refund_transfers = ac.get_account_history(-1,1000,filter_by=['transfer'])

    for i in refund_transfers:
        if (i["from"]==username):
            if(i["amount"].split(" ")[1]=="SBD"):
                sent_amount_SBD += float(i["amount"].split(" ")[0])
            if(i["amount"].split(" ")[1]=="STEEM"):
                sent_amount_STEEM += float(i["amount"].split(" ")[0])

        if (i["to"]==username):
            if(i["amount"].split(" ")[1]=="SBD"):
                received_amount_SBD += float(i["amount"].split(" ")[0])
            if(i["amount"].split(" ")[1]=="STEEM"):
                received_amount_STEEM += float(i["amount"].split(" ")[0])

    refundable_SBD = sent_amount_SBD - received_amount_SBD
    refundable_STEEM = sent_amount_STEEM - received_amount_STEEM

    print(refundable_SBD)
    print(refundable_STEEM)
    if (refundable_SBD>0):
        s.commit.transfer(username,refundable_SBD,"SBD","your SBD refund",account=acc_name)
        print("sending " + str(refundable_SBD)+"SBD back")

    if (refundable_STEEM>0):
        print("sending " + str(refundable_STEEM)+"steem back")
        s.commit.transfer(username,refundable_STEEM,"STEEM","your STEEM refund",account=acc_name)
    
        
while 1:
    transfers = ac.get_account_history(-1,500,filter_by=['transfer'])

    for i in transfers:
        if(i["trx_id"] not in trx_list["trx_id"]):
            
            if (i["memo"]=="refund"):
                add_to_trx_list(i["trx_id"])
                refund(i["from"])
                
            if (i["to"]==acc_name):
                if(i["memo"]!=""):
                    if (validate_memo(i["memo"])==True):

                        add_to_trx_list(i["trx_id"])
                        #response = generate_memo(i["memo"])
                        send_back(i,response)

