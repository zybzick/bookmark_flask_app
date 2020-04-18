from app import db
from models import Category, Post


# db.drop_all()
db.create_all()


anime = Category(name='Anime')
hentai = Category(name='Hentai')
naruto = Post(title='naruto', url='123', category=anime)
madoka = Post(title='madoka', url='123', category=anime)
boku = Post(title='boky no piko', url='432', category=hentai)
hentai.posts.append(boku)
anime.posts.append(naruto)
anime.posts.append(madoka)
db.session.add(anime)
db.session.add(hentai)
db.session.commit()

#
#
# print(anime.posts)
# print(hentai.posts)
# print(hentai.__dict__)


