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
  h) `npm install -g heroku`
  i) `npm install --save-dev css-loader` :warning: Important! In order for the module to properly pack stylesheets, open webpack.config.js and add this loader to the rules[] in module: :warning: `{ test: /.css$/, loader: "style-loader!css-loader" }`
  j) `npm install url-loader --save-dev` warning: Important! In order for the module to properly pack images, open webpack.config.js and add this loader to the rules[] in module: :warning: `{test: /\.(jpg|png)$/, use: {loader: 'url-loader',},}`
  k) `pip install --upgrade google-auth`
  l) `npm install react-google-login`
  m) `npm install --save prop-types`
  o) `pip install pylint-flask-sqlalchemy`
  p) `npm install eslint --save-dev`
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
  g) `cd` into `project2-m1-dfb8` and create a `sql.env` file. create two variables `export SQL_USER=` and `export SQL_PASSWORD=` in, substituting the created username and password exactly.
```
4. Enable SQLAlchemy and grant it permissions to write to the database by modifying the following files: 
```
  a) Open file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
      i) or using `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
  b) Replace all values of `ident` and `peer` with `md5` in Vim: `:%s/ident/md5/g` & `:%s/peer/md5/g`  
  c) Run `sudo service postgresql restart`  
  d) Ensure that `sql.env` has the username/password of the created superuser. Add: export DATABASE_URL='postgresql://{your_SQL_USER}:{your_SQL_PASSWORD}@localhost/postgres'
  e) If you would like to view your tables after the code is run, do the following:
    i) `psql`
    ii) `\c postgres`
    iii) `\dt`
 ```   
## Deploying onto Heroku
5. To deploy on heroku, create an account at http://heroku.com/
6. cd into project2-m1-dfb8 and log into heroku by performing the follow:
```
  a) `heroku login -i`
  b) Input your heroku username and password.
  c) Create an app with `heroku create -a {your_app_name}`
  d) Install postgres on heroku with `heroku addons:create heroku-postgresql:hobby-dev`
  e) Set your heroku app as a git remote via `heroku git:remote -a {your_app_name}`
  f) Push your database into heroku:
    i) Run `psql`, then type ALTER DATABASE posgres OWENER TO {your_SQL_USER};
    ii) Type \l and ensure your superuser is the owner of the Postgres database.
    iii) Exit to terminal, then type `PGUSER={your_SQL_USER} heroku pg:push postgres DATABASE_URL`
    iv) Input password when prompted.
  g) Push repository to heroku using `git push heroku master.`
  h) Open your app in your heroku dashboard.
```  
## Running the Program
5. Run the code using the following:  
```
  a) `npm run watch`. If prompted to install webpack-cli, type "yes." Allow this program to indefinitely run in order to pack react.js into javascript scripts.
  b) Open a new terminal and run `python app.py`  
  c) Preview Running Application. If there are any errors, hard referesh your cache and reload the page.
```  
6. Login with any nickname of your choosing and begin to chat away. The bot supports the following commands, preceded by "!! ":
```
  a) `help`
  b) `about`
  c) `funtranslate {translation_query}`
  d) `dad`
  e) `anime {anime_query}`
```  

## Documentation: Questions

7. Issues encountered and fixed:
```
  a) Why did you choose to test the code that you did?
    - For unmocked tests, normal input and malformed input were tested to get maximum coverage in code, ensuring that each path for each
    deterministic chatbot function properly ran. This was because malformed user input in terms of bot commands are extremely common, as many users
    are not immediately aware of the syntax of each command for the bot. Furthermore, making sure that basic images could be properly rendered was important
    in unmocked testing, as typically one properly wrapped image handled all image cases. For mocked testing, each API was handled (dad, funtranslate, and anime)
    and tested for proper input to ensure that the business logic in handling requests was always successful. The most common malformed input, that is a command prefix
    without a space was extensively tested to ensure that the proper exceptions were raised when the bot came across these common user issues, and that if the input was normal yet
    the bot failed in a response, that it was not the business logic but rather the API's end. Login verification and new messages were tested, as these were integral
    to the user experience.
  b) Is there anything else you would like to test if you had the time (or was asked to do so)?
    - Given more time, I would have liked to do more extensive mock testing on sockets with the front-end, as there could very well be many bugs in the communication between these
    two ends. Implementation of a mock-socket library would be paramount in doing this.
```


