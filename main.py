import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base  
from sqlalchemy.engine import URL
from datetime import datetime 
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

load_dotenv()
url = URL.create(
    drivername = os.getenv("DRIVERNAME"),
    username = os.getenv("USERNAME"),
    host = os.getenv("HOST"),
    database = os.getenv("DATABASE"),
    port = os.getenv("PORT"),
    password = os.getenv("PASSWORD")
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base() 

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    content = Column(Text)
    author_id = Column(Integer(), ForeignKey('authors.id'))

#print(Article.__table__)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer(), primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(255), nullable=False)
    joined = Column(DateTime(), default=datetime.now)
    articles = relationship('Article', backref='author')

Base.metadata.create_all(engine)   

Session = sessionmaker(bind=engine) 
session = Session()

mary = Author(
    firstname="Mary",
    lastname="Maina",
    email="mary.maina@gmail.com"
)
john = Author(
    firstname="John",
    lastname="Kibet",
    email="john.kibet@gmail.com"
)

# article1 = Article(
#     slug="data-visualization",
#     title="Data visualization in python",
#     content="Python offers several plotting libraries, namely Matplotlib, Seaborn and many other such data visualization packages with different features for creating informative, customized, and appealing plots to present data in the most simple and effective way.",
#     author=mary
#     )
# session.add(article1)
# session.commit()

#print(article1.title)

article2 = Article(
    slug="Electric light orchestra",
    title="Hold on tight to your dreams",
    content="When you get so down that you can't get up,and you want so much but you're all out of luck,when you're so downhearted and misunderstood,just over and over and over you could.",
    author=mary
    )

article3 = Article(
    slug="About databases",
    title="Types of databases",
    content="There are many different types of databases, including relational databases, object-oriented databases, and NoSQL databases, and they can be used in a variety of applications, such as data warehousing, online transaction processing, and more.",
    author=mary
    )

article4 = Article(
    slug="Microsoft Excel",
    title="Data analysis in Excel",
    content="Microsoft Excel is a sought-after analytical tool that is an all-in-one data management software that allows you to easily import, explore, clean, analyze and visualize your data.It is also equiped with biult-in pivot tables.",
    author=john
    )

# session.add_all([article2, article3, article4])
# session.flush()
# session.commit()

#check if database updated
articles_objs = session.query(Article)
for article in articles_objs:
    print(article.title)

#Get a column
session.query(Article.slug, Article.title)[2]

#Next we will update the tables from a text/csv file