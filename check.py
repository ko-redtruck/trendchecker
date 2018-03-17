from steem import Steem
import json

node = ["https://api.steemit.com"]

s = Steem(node)

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
