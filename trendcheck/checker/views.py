from django.http import HttpResponse
from steem import Steem
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def check(request,tag,user_name,post_identifier):
    return HttpResponse(check_trending(user_name,post_identifier))


node = ["https://api.steemit.com"]
s = Steem(node)

def check_trending(user_name,post_identifier):

    memo = "TRENDCHECKER by @wil1liam: "
    #post to check
    try:
        author = user_name.replace("@","")
        post_identifier = post_identifier
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
