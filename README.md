# trendchecker
## instructions
#### 1. get a computer that runs 24/7 without going into sleep mode ( I use a raspberry pi 3)
#### 2. install all requirements
- Python 3.6
- [steem-python](https://github.com/steemit/steem-python)
- requests

#### 3. 
<code>
git clone https://github.com/ko-redtruck/trendchecker
</code>
<br>
<code>
cd trendchecker  
</code>
<br>

#### 4. edit the settings.json with your details

#### 5. 
<code>
python3 trendchecker.py
</code>



## functionality

#### basics
- tells you how high your post is ranking within the top 100 in hot/trending/promoted 

#### "user interface"
- send any amount of SBD/STEEM --> execute the baisc function --> send money back with a memo containing the information  

#### experimental/ upcoming features
- in case your transaction wasn't sent back you can try to send one again with the memo "refund" --> every transaction to the bot which hasn't been sent back will now be refunded and sent back


[![HitCount](http://hits.dwyl.io/ko-redtruck/trendchecker.svg)](http://hits.dwyl.io/ko-redtruck/trendchecker)

