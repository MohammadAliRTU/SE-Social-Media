import random
import Social_DB
import re
import hashlib
import secrets
import time



class Social_Backend:

    def __init__(self):
        self.pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def signup(self, email, password, username, common_person_id, name, city, age):
        # Check the validation of the email
        if re.match(self.pattern, email):
            authentication = Social_DB.Authentication("Social_DB", "Authentication")
            exist_user_email = authentication.get_data_by_email(email)
            exist_user_username = authentication.get_data_by_username(username)
            # Check the email in the database
            if len(exist_user_email) == 0:
                if len(exist_user_username) == 0:
                    if len(password) > 8 and re.search(r'\d', password) and re.search(r'[A-Z]', password) and re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\\-/]', password):
                        salt_part = secrets.token_hex(16)
                        salt_password = (password + salt_part).encode('utf-8')
                        hashed_password = hashlib.sha256(salt_password).hexdigest()
                        for counter in range(10):
                            user_number = random.randint(10000000,99999999)
                            if len(authentication.get_data_by_user_number(user_number)) == 0: 
                                authentication.insert_data(user_number, common_person_id, email, hashed_password, salt_part, username, name, city, age)
                                break                    
                        return "Authentication completed"
                    else:
                        return "Weak password"
                else:
                    return "Duplicate username"
            else:
                return "Duplicate email"
        else:
            return "Invalid email"
        
    def signin(self, email, password):
        if re.match(self.pattern, email):
            authentication = Social_DB.Authentication("Social_DB", "Authentication")
            exist_user = authentication.get_data_by_email(email)
            if len(exist_user) == 1:
                salt_part = exist_user[0][4]
                salt_password = (password + salt_part).encode('utf-8')
                hashed_password = hashlib.sha256(salt_password).hexdigest()
                if hashed_password == exist_user[0][3]:
                    return "Authentication completed"
                else:
                    return "Invalid password"
            else:
                return "Invalid email"
        else:
            return "Invalid email"

    def date(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")
        
    def tweet(self, common_person_id, tweet):
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        exist_user = authentication.get_data_by_common_person_id(common_person_id)
        if len(tweet) > 0 and len(tweet) < 251:
            if len(exist_user) == 1:
                tweet_db = Social_DB.Tweet("Social_DB", "Tweets")
                user_number = exist_user[0][0]
                for counter in range(10):
                    tweet_number = random.randint(10000000,99999999)
                    if len(authentication.get_data_by_user_number(user_number)) == 0: 
                        tweet_db.insert_data(tweet_number, user_number, tweet, self.date)
                        break              
                return f"Tweet: {tweet_number}"
            else:
                return "Invalid common_person_id"
        else:
            return "Invalid tweet"
        
    def like(self, common_person_id, tweet_number):
        like_db = Social_DB.Likes("Social_DB", "Likes")
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        user_number = authentication.get_data_by_common_person_id(common_person_id)[0][0]
        Liked_previously = like_db.get_data_by_user_number_and_tweet_number(user_number, tweet_number)
        if len(Liked_previously) == 0:
            for counter in range(10):
                like_number = random.randint(10000000,99999999)
                if len(Liked_previously) == 0:
                    like_db.insert_data(like_number, user_number, tweet_number)
                    break
            return "Liked"
        else:
            return "Liked previously"
        
    def comment(self, common_person_id, tweet_number, comment):
        comment_db = Social_DB.Comments("Social_DB", "Comments")
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        user_number = authentication.get_data_by_common_person_id(common_person_id)[0][0]
        for counter in range(10):
            comment_number = random.randint(10000000,99999999)
            if len(comment_db.get_data_by_comment_number(comment_number)) == 0:
                comment_db.insert_data(comment_number, user_number, tweet_number, comment, self.date)
                break
        return "Commented"
    
    def follow(self, common_person_id, follow_common_person_id):
        follow_db = Social_DB.Follows("Social_DB", "Follows")
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        user_number = authentication.get_data_by_common_person_id(common_person_id)[0][0]
        follow_user_number = authentication.get_data_by_common_person_id(follow_common_person_id)[0][0]
        for counter in range(10):
            follow_number = random.randint(10000000,99999999)
            if len(follow_db.get_data_by_follow_number(follow_number)) == 0:
                follow_db.insert_data(follow_number, user_number, follow_user_number)
                break
        return "Followed"
    
    def search_username(self, username):
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        exist_user = authentication.get_data_by_username(username)
        if len(exist_user) == 1:
            return exist_user[0]
        else:
            return "Invalid username"
        
    def sort_tweets(self, tweet_list):
        sorted_data_desc = sorted(tweet_list, key=lambda x: x[0], reverse=True)
        return sorted_data_desc
        

    def feed_page(self, common_person_id):
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        follows = Social_DB.Follows("Social_DB", "Follows")
        tweet_db = Social_DB.Tweet("Social_DB", "Tweets")
        exist_user = authentication.get_data_by_common_person_id(common_person_id)
        if len(exist_user) == 0:
            return "Invalid common_person_id"
        all_tweets = []
        followings = follows.get_data_by_follower_user_number(common_person_id)
        for following in followings:
            following_user_number = following[2]
            tweets = tweet_db.get_data_by_user_number(following_user_number)
            for tweet in tweets:
                all_tweets.append([tweet[1] ,tweet[2], tweet[3]])
        sorted_tweets = self.sort_tweets(all_tweets)
        data = {"user": exist_user, "tweets": sorted_tweets}
        return data
    
    def home_page(self, common_person_id):
        following = []
        authentication = Social_DB.Authentication("Social_DB", "Authentication")
        tweet_db = Social_DB.Tweet("Social_DB", "Tweets")
        follows = Social_DB.Follows("Social_DB", "Follows")
        exist_user = authentication.get_data_by_common_person_id(common_person_id)
        if len(exist_user) == 0:
            return "Invalid common_person_id"
        follows = follows.get_data_by_follower_user_number(exist_user[0][0])
        for follow in follows:
            following.append(follow[2])
        tweets = tweet_db.get_data_by_user_number(exist_user[0][0])
        sorted_tweets = self.sort_tweets(tweets)
        data = {"user": exist_user, "tweets": sorted_tweets, "following": following}
        return data
    
    def tweet_page(self, tweet_number):
        tweet_db = Social_DB.Tweet("Social_DB", "Tweets")
        comment_db = Social_DB.Comments("Social_DB", "Comments")
        tweet = tweet_db.get_data_by_tweet_number(tweet_number)
        comments = comment_db.get_data_by_tweet_number(tweet_number)
        data = {"tweets": tweet, "following": comments}
        return data
        


if __name__=="__main__":

    social_backend = Social_Backend()
    print(social_backend.signup("hassan@gmail.com", "Hassan123%", "Hassan", 123456, "Hassan", "Tehran", 30))
    print(social_backend.signin("hassan@gmail.com",  "Hassan123%"))
    print(social_backend.tweet(123456, "Hello World"))
    print(social_backend.like(123456, 99110383))
    