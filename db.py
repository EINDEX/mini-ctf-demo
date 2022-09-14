import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# cursor.execute('create table user (username varchar(20) primary key, password varchar(20))')
print(cursor.execute('insert into user (username,password) values ("admin", "password")').rowcount)
print(cursor.execute('select * from user').fetchall())
conn.commit()
# cursor.commit()