import sqlite3


class Authentication:
    def __init__(self,database_name='test_database.db',tabel_name = 'Authentications'):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.tabel_name = tabel_name
        self.check_tabel()
    
    def check_tabel(self,):
        with self.conn:
            self.c.execute(f""" CREATE TABLE IF NOT EXISTS {self.tabel_name}(
                user_number INTEGER PRIMARY KEY,
                common_person_id INTEGER,
                email text,
                hashed_password text,
                salt_part text,
                username text,
                name text,
                city text,
                age INTEGER
                ) """)

    def insert_data(self,user_number,common_person_id,email,hashed_password,salt_part,username,name,age,city):
        self.c.execute(f"INSERT INTO {self.tabel_name} VALUES(:user_number,:common_person_id,:email,:hashed_password,:salt_part,:username,:name,:age,:city)",
        {'user_number':user_number,'common_person_id':common_person_id,'email':email,'hashed_password':hashed_password,'salt_part':salt_part,'username':username,'name':name,'age':age,'city':city})
        self.conn.commit()

    def get_data_by_common_person_id(self,common_person_id):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE common_person_id=:common_person_id",
        {'common_person_id':common_person_id})
        return  self.c.fetchall()
    
    def get_data_by_user_number(self,user_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE user_number=:user_number",
        {'user_number':user_number})
        return  self.c.fetchall()
    
    def get_data_by_email(self,email):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE email=:email",
        {'email':email})
        return  self.c.fetchall()
    
    def get_data_by_username(self,username):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE username=:username",
        {'username':username})
        return  self.c.fetchall()
    
    def get_all_data(self):
        self.c.execute(f"SELECT * FROM {self.tabel_name}")
        return  self.c.fetchall()
    
    def drop_table(self):
        self.c.execute(f"DROP TABLE {self.tabel_name}")
        self.conn.commit()

class Tweet:
    def __init__(self,database_name='test_database.db',tabel_name = 'Tweets'):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.tabel_name = tabel_name
        self.check_tabel()
    
    def check_tabel(self,):
        with self.conn:
            self.c.execute(f""" CREATE TABLE IF NOT EXISTS {self.tabel_name}(
                tweet_number INTEGER PRIMARY KEY,
                user_number INTEGER,
                tweet text,
                tweet_date text
                ) """)

    def insert_data(self,tweet_number,user_number,tweet,tweet_date):
        self.c.execute(f"INSERT INTO {self.tabel_name} VALUES(:tweet_number,:user_number,:tweet,:tweet_date)",
        {'tweet_number':tweet_number,'user_number':user_number,'tweet':tweet,'tweet_date':tweet_date})
        self.conn.commit()

    def get_data_by_user_number(self,user_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE user_number=:user_number",
        {'user_number':user_number})
        return  self.c.fetchall()
    
    def get_data_by_tweet_number(self,tweet_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE tweet_number=:tweet_number",
        {'tweet_number':tweet_number})
        return  self.c.fetchall()
        
    def drop_table(self):
        self.c.execute(f"DROP TABLE {self.tabel_name}")
        self.conn.commit()

class Likes:
    def __init__(self,database_name='test_database.db',tabel_name = 'Likes'):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.tabel_name = tabel_name
        self.check_tabel()
    
    def check_tabel(self,):
        with self.conn:
            self.c.execute(f""" CREATE TABLE IF NOT EXISTS {self.tabel_name}(
                like_number INTEGER PRIMARY KEY,
                user_number INTEGER,
                tweet_number INTEGER
                ) """)

    def insert_data(self,like_number,user_number,tweet_number):
        self.c.execute(f"INSERT INTO {self.tabel_name} VALUES(:like_number,:user_number,:tweet_number)",
        {'like_number':like_number,'user_number':user_number,'tweet_number':tweet_number})
        self.conn.commit()

    def get_data_by_tweet_number(self,tweet_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE tweet_number=:tweet_number",
        {'tweet_number':tweet_number})
        return  self.c.fetchall()
    
    def get_data_by_user_number_and_tweet_number(self,user_number,tweet_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE user_number=:user_number AND tweet_number=:tweet_number",
        {'user_number':user_number, 'tweet_number':tweet_number})
        return  self.c.fetchall()
    
    def get_all_data(self):
        self.c.execute(f"SELECT * FROM {self.tabel_name}")
        return  self.c.fetchall()
    
    def drop_table(self):
        self.c.execute(f"DROP TABLE {self.tabel_name}")
        self.conn.commit()


class Comments:
    def __init__(self,database_name='test_database.db',tabel_name = 'Comments'):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.tabel_name = tabel_name
        self.check_tabel()
    
    def check_tabel(self,):
        with self.conn:
            self.c.execute(f""" CREATE TABLE IF NOT EXISTS {self.tabel_name}(
                comment_number INTEGER PRIMARY KEY,
                user_number INTEGER,
                tweet_number INTEGER,
                comment text,
                comment_date text
                ) """)
            
    def insert_data(self,comment_number,user_number,tweet_number,comment,comment_date):
        self.c.execute(f"INSERT INTO {self.tabel_name} VALUES(:comment_number,:user_number,:tweet_number,:comment,:comment_date)",
        {'comment_number':comment_number,'user_number':user_number,'tweet_number':tweet_number,'comment':comment,'comment_date':comment_date})
        self.conn.commit()

    def get_data_by_tweet_number(self,tweet_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE tweet_number=:tweet_number",
        {'tweet_number':tweet_number})
        return  self.c.fetchall()
    
    def get_all_data(self):
        self.c.execute(f"SELECT * FROM {self.tabel_name}")
        return  self.c.fetchall()
    
    def drop_table(self):
        self.c.execute(f"DROP TABLE {self.tabel_name}")
        self.conn.commit()

class Follows:
    def __init__(self,database_name='test_database.db',tabel_name = 'Follows'):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.tabel_name = tabel_name
        self.check_tabel()
    
    def check_tabel(self,):
        with self.conn:
            self.c.execute(f""" CREATE TABLE IF NOT EXISTS {self.tabel_name}(
                follow_number INTEGER PRIMARY KEY,
                follower_user_number INTEGER,
                following_user_number INTEGER
                ) """)

    def insert_data(self,follow_number,follower_user_number,following_user_number):
        self.c.execute(f"INSERT INTO {self.tabel_name} VALUES(:follow_number,:follower_user_number,:following_user_number)",
        {'follow_number':follow_number,'follower_user_number':follower_user_number,'following_user_number':following_user_number})
        self.conn.commit()

    def get_data_by_follower_user_number(self,follower_user_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE follower_user_number=:follower_user_number",
        {'follower_user_number':follower_user_number})
        return  self.c.fetchall()
    
    def get_data_by_following_user_number(self,following_user_number):
        self.c.execute(f"SELECT * FROM {self.tabel_name} WHERE following_user_number=:following_user_number",
        {'following_user_number':following_user_number})
        return  self.c.fetchall()
    
    def get_all_data(self):
        self.c.execute(f"SELECT * FROM {self.tabel_name}")
        return  self.c.fetchall()
    
    def drop_table(self):
        self.c.execute(f"DROP TABLE {self.tabel_name}")
        self.conn.commit()



if __name__=="__main__":

    authentication = Authentication("Social_DB", "Authentication")
    likes = Likes("Social_DB", "Likes")
    #print(authentication.get_all_data())
    #print(authentication.get_data_by_email("hassan@gmail.com"))
    print(likes.get_all_data())




