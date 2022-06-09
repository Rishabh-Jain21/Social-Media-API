# Social-Media-API

This a api implementation for a social media app.

The API allows to create user,create a post ,vote a vote and other basic CRUD operations.

It uses JWT token for authentication.

The project uses sqlalchemy and pydantic for creating models and schemas for API respectively.
## Steps to run Project

1.Install the required modules from requirments.txt file
``` bash
pip install -r requirments.txt
```
<br>

2.Create a ".env" file in the main directory which will contain all the enviornment variables for the project.
```
DATABASE_HOSTNAME=#####
DATABASE_PORT=#####
DATABASE_PASSWORD=#####
DATABASE_NAME=#####
DATABASE_USERNAME=#####
SECRET_KEY=#####
ALGORITHM=#####
ACCESS_TOKEN_EXPIRE_MINUTES=#####
```
For **ALGORITHM** value, left column can used and right column tells the type of hashing algorithm being used
|Value|Algorithm|
|:-------:|:-------:|
|HS256| SHA256|
|HS384| SHA384|
|HS512| SHA512|

****
SSCRET_key can be any random alphanumeric value.This key will be used for generating signature for JWT token.

Configure the variables accordingly.(Do not use single quotes or double quotes)

---

<span style="color:red;font-size:20px">DATABASE_HOSTNAME="localhost" (Wrong)</span>

<span style="color:green;font-size:20px">DATABASE_HOSTNAME=localhost (Correct)</span>.


---

3.Setup postgres DBMS in the system.(This project uses postgres as the default database).
if any other database is to be used,then change the database driver in **SQLALCHEMY_DATABASE_URL** variable in database.py file.

<br>

4.Open terminal in the main directory of project and type
```bash
uvicorn app.main:app --reload
```

app before '.main' refer to the directrory name 'app'
main is the python which contains the login to start the API server.
app after 'main' is the variable name which needs to be started.
<br>
<br>
# Notes

* If you change any models in **db_models.py** , then the effects wont be visible in database after server restart.
The tables in DBMS needs to be deleted and then server should be started for sqlalchemy to make those changes.
(This is a drawback for sqlalchemy,In this scenerio use a database migration tool like **'alembic'** which will detect and update the tables.)

* Fast api has inbuilt documentation functionality using swagger.
Go to **{{base-url}}/docs** or '**{base-url}}/redocs**  to view default documentation.


