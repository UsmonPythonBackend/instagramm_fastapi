from models import User, Post, Comment, Likes, Follows, Tags, Stories, Messages

from database import ENGINE, Base

if __name__ == '__main__':
    Base.metadata.create_all()