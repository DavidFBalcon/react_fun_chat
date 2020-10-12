# Funbot - Project 2 Milstone 1
0. Clone this repository using your CLI:
`cd ~/environment && git clone https://github.com/NJIT-CS490/project2-m1-dfb8 && cd project2-m1-dfb8`
1. Then, we need to install the following packages to run this program.
```
  a) `npm install`  
  b) `pip install flask-socketio`  
  c) `pip install eventlet`  
  e) `pip install jikanpy`
  d) `npm install -g webpack`  
  e) `npm install --save-dev webpack`  
  f) `npm install socket.io-client --save`  
  g) `npm install --save-dev style-loader`
  h) `npm install --save-dev css-loader` :warning: Important! In order for the module to properly pack stylesheets, open webpack.config.js and ensure that  the loader rule in module is set to: :warning: `{ test: /.css$/, loader: "style-loader!css-loader" }`
  ```
 ## Getting PSQL and running SQLAlchemy
2. Set up PSQL by installing the following packages
```
  a) Update yum: `sudo yum update`, and enter yes to all prompts    
  b) Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
  c) Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
  d) Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`   
  e). Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
```    
3. Initialize the database for storing messages.
```
  a) Initialize PSQL database: `sudo service postgresql initdb`    
  b) Start PSQL: `sudo service postgresql start`    
  c) Make a new superuser: `sudo -u postgres createuser --superuser $USER`     
  d) Make a new database: `sudo -u postgres createdb $USER`
  e) Make sure your user shows up:
      i) `psql`    
      ii) `\du` look for ec2-user as a user    
      iii) `\l` look for ec2-user as a database   
  f) Make a new user:
      i) `psql` (if you already quit out of psql)    
      ii) Create a superuser with a password using the below command.
          `create user [some_username_here] superuser password '[some_unique_new_password_here]';`  
      iii) `\q` to quit out of sql
  g) `cd` into `project2-m1-dfb8` and create a `sql.env` file. create two variables `SQL_USER=` and `SQL_PASSWORD=` in, substituting the created username and password exactly.
```
4. Enable SQLAlchemy and grant it permissions to write to the database by modifying the following files: 
```
  a) Open file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
      i) or using `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
  b) Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
  c) Run `sudo service postgresql restart`  
  d) Ensure that `sql.env` has the username/password of the created superuser.
  e) If you would like to view your tables after the code is run, do the following:
    i) `psql`
    ii) `\c postgres`
    iii) `\dt`
 ```   
5. Run the code using the following:  
```
  a) `npm run watch`. If prompted to install webpack-cli, type "yes." Allow this program to indefinitely run in order to pack react.js into javascript scripts.
  b) Open a new terminal and run `python app.py`  
  c) Preview Running Application. If there are any errors, hard referesh your cache and reload the page.
```  
6. Login with any nickname of your choosing and begin to chat away. The bot supports the following commands, preceded by !!:
```
  a) `help`
  b) `about`
  c) `funtranslate {translation_query}`
  d) `dad`
  e) `anime {anime_query}`
```  
