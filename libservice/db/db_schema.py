import mysql.connector
import json


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="root"
# )
#
# print(mydb)
#
# mycursor = mydb.cursor()
#
# try:
#     mycursor.execute("CREATE DATABASE IF NOT EXISTS Catalog")
# except ConnectionError:
#     print("Error : ")
#
# mycursor.execute("SHOW DATABASES")
#
# for x in mycursor:
#     print(x)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Catalog"
)

print(mydb)

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Catalog")
except ConnectionError:
    print("Error : ")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

##############################CRETE TABLE TEST for connection testing #####################################################

mycursor.execute("CREATE TABLE test ("
                 "id    INT     NOT NULL    AUTO_INCREMENT,"
                 "name         VARCHAR(255) NOT NULL,"
                 "pop       DECIMAL(5,1),"
                 "address      VARCHAR(255),"
                 "PRIMARY KEY ( id )"
                 ");")

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

sql = "INSERT INTO test (name, pop, address) VALUES (%s, %s, %s)"
val = ("John3", "10.5", "Highway 21")
# val = {"John", "10.5", "Highway 21"}
mycursor.execute(sql, val)
mydb.commit()

##############################CRETE TABLE Catalog #####################################################
mycursor.execute("CREATE TABLE content ("
                 "content_id    INT     NOT NULL    AUTO_INCREMENT,"
                 "title         VARCHAR(255) NOT NULL,"
                 "popularity    DECIMAL(5,1),"
                 "director      VARCHAR(255),"
                 "genre         VARCHAR(255),"
                 "imdb_score    DECIMAL(3,1),"
                 "PRIMARY KEY ( content_id )"
                 ");")

# mycursor.execute("DROP TABLE contents")
#
# mycursor.execute("CREATE TABLE contents ("
#                  "content_id    INT     NOT NULL    AUTO_INCREMENT,"
#                  "title         VARCHAR(255) NOT NULL,"
#                  "popularity    VARCHAR(10),"
#                  "director      VARCHAR(255),"
#                  "genre         VARCHAR(255),"
#                  "imdb_score    VARCHAR(10),"
#                  "PRIMARY KEY ( content_id )"
#                  ");")
#
#
#
with open('imdb.json') as f:
    data = json.load(f)

print(data)
# mycursor.execute("TRUNCATE TABLE content")

sql = "INSERT INTO content (title, popularity, director, genre, imdb_score) VALUES (%s, %s, %s, %s, %s)"
for contents in data:
    # print(contents["name"])
    value = (contents["name"], contents["99popularity"], contents["director"], json.dumps(contents["genre"]), contents["imdb_score"])
    print(value)
    mycursor.execute(sql, value)
    mydb.commit()


##############################CRETE TABLE Users #####################################################
# mycursor.execute("DROP TABLE user_info")
# mycursor.execute("DROP TABLE user_auth")
# mycursor.execute("DROP TABLE archive_user")
# mycursor.execute("DROP TABLE admin_info")
# mycursor.execute("DROP TABLE admin_auth")
# mycursor.execute("DROP TABLE archive_admin")
#
mycursor.execute("CREATE TABLE user_info ("
                 "uuid    VARCHAR(128),"
                 "firstname  VARCHAR(128),"
                 "lastname   VARCHAR(128),"
                 "email      VARCHAR(128),"
                 "created_on DATETIME"
                 ");")

mycursor.execute("CREATE TABLE archive_user ("
                 "uuid    VARCHAR(128),"
                 "firstname  VARCHAR(128),"
                 "lastname   VARCHAR(128),"
                 "email      VARCHAR(128),"
                 "created_on DATETIME,"
                 "deleted_on DATETIME"
                 ");")

mycursor.execute("CREATE TABLE admin_info ("
                 "uuid   VARCHAR(128),"
                 "firstname  VARCHAR(128),"
                 "lastname   VARCHAR(128),"
                 "email      VARCHAR(128),"
                 "created_on DATETIME"
                 ");")

mycursor.execute("CREATE TABLE archive_admin ("
                 "uuid    VARCHAR(128),"
                 "firstname  VARCHAR(128),"
                 "lastname   VARCHAR(128),"
                 "email      VARCHAR(128),"
                 "created_on DATETIME,"
                 "deleted_on DATETIME"
                 ");")

mycursor.execute("CREATE TABLE admin_auth ("
                 "uuid   VARCHAR(128),"
                 "username   VARCHAR(128),"
                 "password   VARCHAR(128),"
                 "created_on DATETIME"
                 ");")

mycursor.execute("CREATE TABLE user_auth ("
                 "uuid    VARCHAR(128),"
                 "login      VARCHAR(128),"
                 "password   VARCHAR(128),"
                 "created_on DATETIME"
                 ");")

## mycursor.execute("ALTER TABLE provider DROP PRIMARY KEY, ADD PRIMARY KEY(admin_id, email);")
# mycursor.execute("ALTER TABLE user_info DROP PRIMARY KEY, ADD PRIMARY KEY(email, user_id);")
# mycursor.execute("ALTER TABLE admin_info DROP PRIMARY KEY, ADD PRIMARY KEY(admin_id, email);")

mycursor.execute("ALTER TABLE user_info ADD PRIMARY KEY( uuid);")
mycursor.execute("ALTER TABLE admin_info ADD PRIMARY KEY(uuid);")
mycursor.execute("ALTER TABLE user_auth ADD PRIMARY KEY( uuid);")
mycursor.execute("ALTER TABLE admin_auth ADD PRIMARY KEY(uuid);")
mycursor.execute("ALTER TABLE content ADD FULLTEXT(title, director, genre)")
