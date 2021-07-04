import redis
from werkzeug.wrappers import Request
from datetime import datetime
from slugify import slugify
import ast


class DataStorage:
    """Provides interface of interaction with redis"""

    def __init__(self, host, port):
        self.redis = redis.Redis(host, port)

    def is_valid(self, request: Request) -> bool:
        """Returns if data of post is valid"""
        f = request.form
        if f['author'] and f['title'] and ['text']:
            return True
        return False
    
    def is_valid_comment(self, request: Request) -> bool:
        """Returns if data of comment is valid"""
        f = request.form
        if f['author'] and ['text']:
            return True
        return False
    
    def post_data_to_save(self, request) -> str:
        """Returns prepared data to save"""
        data = dict()
        author = request.form['author']
        title = request.form['title']
        data["author"] = author
        data["title"] = title
        data["text"] = request.form['text']
        now = datetime.now()
        data["data"] = now.strftime("%d/%m/%Y %H:%M:%S")
        data["slug"] = slugify(title + author)
        return str(data)
    
    def comment_data_to_save(self, request, id: str) -> str:
        """Returns prepared comment data to save"""
        data = dict()
        data["author"] = request.form['author']
        data["text"] = request.form['text']
        data["post"] = id 
        return str(data)
    
    def save_post(self, request: Request) -> None:
        self.redis.rpush("posts", self.post_data_to_save(request))
    
    def save_comment(self, request: Request, id: str) -> None:
        self.redis.rpush("comments", self.comment_data_to_save(request, id))

    def get_comments(self, id: str) -> list:
        res = []
        for el in self.redis.lrange("comments", 0, -1):
            dict_str = el.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata["post"] == id:
                res.append(mydata)
        res = res[::-1]
        return res
    
    def get_posts(self) -> list:
        """Returns detailed post"""
        res = []
        for el in self.redis.lrange("posts", 0, -1):
            dict_str = el.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            mydata['text'] = mydata['text'][:250] + "..."
            res.append(mydata)
        res = res[::-1]
        return res
    
    def get_post(self, id: str) -> list:
        res = []
        for el in self.redis.lrange("posts", 0, -1):
            dict_str = el.decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            if mydata["slug"] == id:
                res.append(mydata)
                return res
        return res
