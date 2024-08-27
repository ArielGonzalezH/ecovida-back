from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class Comment:
    def __init__(self, product_id, user_id, comment_text):
        self.product_id = product_id
        self.user_id = user_id
        self.comment_text = comment_text

    def as_dict(self):
        return {
            'product_id': self.product_id,
            'user_id': self.user_id,
            'comment_text': self.comment_text
        }
