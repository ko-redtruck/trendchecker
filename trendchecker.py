from steem import Steem
from steem import account
import requests
import json
import time

node = ["https://rpc.buildteam.io","https://api.steemit.com"]
trx_list = json.load(open("trx_list.json"))
upvote_list = json.load(open("upvotes.json"))
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
        trending_posts = s.get_discussions_by_trending({"limit":50,"tag":i})
        hot_posts = s.get_discussions_by_hot({"limit":50,"tag":i})

        count1 = 1
        count2 = 1
        
        if (i==""):
            memo += "All: "
        else:
            memo += i + ": "
            
        for o in trending_posts:
            if (o["author"]==author):
                print("trending---")
                print(i+ " --tag")
                print(count1)
                memo += str(count1)  +". in TRENDING "
                break
            count1 += 1

        for o in hot_posts:
            if (o["author"]==author):
                print("hot---")
                print(i+ " --tag")
                print(count2)
                memo += str(count2)  +". in HOT "
                break
            count2 += 1
            
        memo += "| "
        
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
    
def send_back(trx,memo,post_identifier):
    asset = trx["amount"].split(" ")[1]
    sender = trx["from"]
    s.commit.transfer(sender,0.001,asset,memo,account=acc_name)
    print("sending " + "0.001" + " to " + sender)
    
    if(post_identifier not in upvote_list["post_identifier"]):
        s.commit.vote(post_identifier,100,account=acc_name)
        body = "Hello, <br> I'm bot. I am here because " + "@" +sender + " wanted to know how high this post is in Hot or Trending. <br><br> You want to know what your post's rank in Hot or Trending is? <br><br> 1. copy your Steemit.com post url <br> 2. send 0.001 SBD/STEEM to @trendchecker with the url as the memo <br> 3. wait 20 seconds to receive the results <br><br> <b> As a gift your post will be upvoted for free! </b> <br> <hr>- This bot was development by @wil1liam."
        s.commit.post("",body,author=acc_name, reply_identifier="@"+post_identifier)
        print("commented")
        
        upvote_list["post_identifier"].append(post_identifier)

        with open('upvotes.json', 'w') as outfile:
            json.dump(upvote_list, outfile)
        
def generate_memo(url):
    memo = check_trending(url)
    return memo    
    
def add_to_trx_list(trx_id):
    trx_list["trx_id"].append(trx_id)

    with open('trx_list.json', 'w') as outfile:
        json.dump(trx_list, outfile)
    
        
while 1:
   
    transfers = ac.get_account_history(-1,500,filter_by=['transfer'])
    
    try:
        for i in transfers:
            if(i["trx_id"] not in trx_list["trx_id"]):
                if (i["to"]==acc_name):
                    if(i["memo"]!=""):
                        if (validate_memo(i["memo"])==True):

                            add_to_trx_list(i["trx_id"])
                            response = generate_memo(i["memo"])
                            
                            post_identifier = i["memo"].split("/")[4].replace("@","") + "/" + i["memo"].split("/")[5]
                            send_back(i,response,post_identifier)               
    except:
        time.sleep(30)
        s = Steem(node,keys=keys)
        ac= account.Account(acc_name,s)

