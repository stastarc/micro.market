
from dataclasses import dataclass

from sqlalchemy import func

from database.feed import Feed
from .products import ShortProductData, Products

@dataclass
class FeedData:
    title: str
    search_type: str
    content: str
    products: list[ShortProductData]

class Feeds:
    @staticmethod
    def session_get_feed(sess, limit=5):
        feed_titles = sess.query(Feed).order_by(func.rand()).limit(limit).all()
        return [
            FeedData(
                title=feed_title.title, 
                search_type=feed_title.content_type, 
                content=feed_title.content,
                products=Products.session_search_short(sess, feed_title.content, mode=feed_title.content_type)
            ) for feed_title in feed_titles
        ]