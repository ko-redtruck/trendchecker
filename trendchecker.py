from steem import Steem
from steem import account
import requests
import json

node = ["https://api.steemit.com"]
acc_name = "wil1liam"

s = Steem(node)
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
        
while 1:
    gen1= ac.get_account_history(-1500,filter_by=['transfer'])

    for i in gen1:
        if (i["to"]==acc_name):
            if(i["memo"]!=""):
                if (validate_memo(i["memo"])==True):
                    check_trending(i["memo"])            
