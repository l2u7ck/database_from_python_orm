import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
import models as m


# connecting environment variables (env)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    print(load_dotenv(dotenv_path))

# Database connection
DSN = (f'{dotenv_values()['connection_driver']}://'
       f'{dotenv_values()['login']}:'
       f'{dotenv_values()['password']}@'
       f'{dotenv_values()['host']}:'
       f'{dotenv_values()['port']}/'
       f'{dotenv_values()['title_database']}')

engine = sqlalchemy.create_engine(DSN)
m.create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Add publishers
publisher1 = m.Publisher(name='Пушкин')
publisher2 = m.Publisher(name='Толстой')

session.add_all([publisher1, publisher2])
session.commit()

# Add books
book1 = m.Book(title='Капитанская дочка', publisher_id=1)
book2 = m.Book(title='Руслан и Людмила', publisher_id=1)
book3 = m.Book(title='Евгений Онегин ', publisher_id=1)
book4 = m.Book(title='Война и мир', publisher_id=2)
book5 = m.Book(title='Детство', publisher_id=2)

session.add_all([book1, book2, book3, book4, book5])
session.commit()

# Add shops
shop1 = m.Shop(name='Буквоед')
shop2 = m.Shop(name='Лабиринт')
shop3 = m.Shop(name='Книжный дом')

session.add_all([shop1, shop2, shop3])
session.commit()

# Add stocks
stock1 = m.Stock(book_id=1, shop_id=1, count=60)
stock2 = m.Stock(book_id=2, shop_id=1, count=50)
stock3 = m.Stock(book_id=1, shop_id=2, count=40)
stock4 = m.Stock(book_id=3, shop_id=3, count=30)
stock5 = m.Stock(book_id=1, shop_id=1, count=45)
stock6 = m.Stock(book_id=4, shop_id=1, count=35)
stock7 = m.Stock(book_id=5, shop_id=2, count=90)
stock8 = m.Stock(book_id=5, shop_id=1, count=46)

session.add_all([stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8])
session.commit()

# Add sales
sale1 = m.Sale(price=600, date_sale='09-11-2022', stock_id=1, count=20)
sale2 = m.Sale(price=500, date_sale='08-11-2022', stock_id=2, count=60)
sale3 = m.Sale(price=580, date_sale='05-11-2022', stock_id=3, count=70)
sale4 = m.Sale(price=490, date_sale='02-11-2022', stock_id=4, count=50)
sale5 = m.Sale(price=600, date_sale='26-10-2022', stock_id=5, count=30)
sale6 = m.Sale(price=700, date_sale='07-10-2022', stock_id=6, count=30)
sale7 = m.Sale(price=650, date_sale='17-09-2022', stock_id=7, count=50)
sale8 = m.Sale(price=350, date_sale='20-09-2022', stock_id=7, count=70)
sale9 = m.Sale(price=350, date_sale='12-09-2022', stock_id=8, count=76)

session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8, sale9])
session.commit()


def get_shops(data_author):

    # Merge all tables and selection by publisher
    query = (session.query(..., ..., ..., ...,).select_from(m.Shop).
             join(m.Sale.stock).
             join(m.Stock.book).
             join(m.Book.publisher).
             join(m.Sale))

    if data_author.isdigit():
        author = query.filter(m.Publisher.id == data_author).all()
    else:
        author = query.filter( m.Publisher.name == data_author ).all()
    for title, shop, cost, date in author:
        print(f"{title: <40} | {shop: <10} | {cost: <8} | {date.strftime('%d-%m-%Y')}")

        # Information output
    for st in query:
        for s in st.sales:
            print(f'{st.book.title.ljust(20)} | {st.shop.name.ljust(15)} | '
                  f'{str(s.price).ljust(5)} | {s.date_sale}')


if __name__ == '__main__':

    # Publisher input - valid names(Пушкин, Tолстой)
    data_author = input("Enter the publisher's name or id:")
    get_shops(data_author)

    session.close()
