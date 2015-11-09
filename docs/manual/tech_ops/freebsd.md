# HOWTO: Setup eCantina on DigitalOcean using FreeBSD 
## DigitalOcean 
### Droplet Setup
1. Create droplet a new FreeBSD droplet named "ecantina.com"

2. Add your SSH Key into it. You can find it in your Mac in this location:
  ```
  vi ~/.ssh/id_rsa.pub
  ```

3. From your local Mac, terminal into the server.
  ```
 ssh 45.55.221.217 -l freebsd
  ```

4. Add password for 'root'
  ```
  sudo passwd
  ```
Password: ***REDACTED***

### DNS
1. Inside digitalocean, go to the **DNS section**

2. Add **luchacomics** and select the **ecantina** droplet

3. Click **Add Record** and click **CNAME** with:
  ```
  name = www
  host = ecantina.com.
  ```

4. Click **Add Record** and click **CNAME** with:
  ```
  name = *
  host = ecantina.com.
  ```
  
## GoDaddy
(TODO)

## eCantina Droplet
### Setup C-Shell
1. Load up our C-Shell and open the config
  ```
  cp /usr/share/skel/dot.cshrc ~/.cshrc
  vi ~/.cshrc
  ```
  
2. At the bottom, copy and paste these:
  ```
  if ($term == "xterm" || $term == "vt100" \
            || $term == "vt102" || $term !~ "con*") then
          # bind keypad keys for console, vt100, vt102, xterm
          bindkey "\e[1~" beginning-of-line  # Home
          bindkey "\e[7~" beginning-of-line  # Home rxvt
          bindkey "\e[2~" overwrite-mode     # Ins
          bindkey "\e[3~" delete-char        # Delete
          bindkey "\e[4~" end-of-line        # End
          bindkey "\e[8~" end-of-line        # End rxvt
  endif
  ```
  
3. Make our session run this new shell
  ```
  source ~/.cshrc
  ```  
  
### Ports
Now we need to get the most up-to-date repository of ports and apply it to our system.
  ```
  sudo portsnap fetch extract update
  ```
  
### Python 3.4
1. Become Root
  ```
  su
  ```  
  
2. Fix the following dependancy problem
  ```
  cd /usr/ports/converters/libiconv
  make deinstall clean

  cd /usr/ports/ports-mgmt/pkg/ 
  make deinstall clean
  make install clean
  make deinstall clean
  make install clean

  cd /usr/ports/converters/libiconv
  make install clean
  ```

3. Compile from source Python 3.4
  ```
  cd /usr/ports/lang/python34
  make install clean
  ```
  
4. Find where Python was installed
  ```
  rehash
  find /usr/bin /bin/ /usr/local/bin -iname 'python*'
  ```
  
5. Make the command "python" be available on the FreeBSD system.
  ```
  ln -s /usr/local/bin/python3.4 /usr/local/bin/python
  ```

6. Verify Python was installed and is version 3.4.x
  ```
  python -V
  ```
  
### Extra Python Libraries
To support "django-simple-captcha" rendering, we will have to install these

1. Lets make sure we are using the latest setup tools
  ```
  cd /usr/ports/devel/py-setuptools27
  sudo make deinstall clean
  cd /usr/ports/devel/py-setuptools34
  sudo make install clean
  ```

2. Lets install GD:
  ```
  cd /usr/ports/graphics/gd
  sudo make install clean
  ```

3. Lets install FreeType
  ```
  cd /usr/ports/print/freetype2
  sudo make install clean
  ```
  
4. Lets install memcached.
  ```
  cd /usr/ports/databases/memcached
  make install clean
  cd /usr/ports/databases/libmemcached
  make install clean
  ```

5. Edit /etc/rc.conf and add the following.  
  ```
  memcached_enable="YES"
  ```


### pip
1. Lets install pip:
  ```
  exit
  cd ~/
  curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  sudo python get-pip.py
  rm get-pip.py
  ```
  
2. Verify pip was installed
  ```
  pip -V
  ```
  
### Virtualenv
1. To install:
  ```
  sudo pip install virtualenv
  ```

2. Verify virtualenv is intalled
  ```
  mkdir py-ecantina
  cd py-ecantina
  virtualenv env
  ```


### Postgres 9.4.4   *
1. Compile from source
  ```
  su
  cd /usr/ports/databases/postgresql94-server/ && make
  make install clean
  ```

2. Load up our rc.config
  ```
  vi /etc/rc.conf
  ```
Add this line to /etc/rc.conf:
  ```
  postgresql_enable="YES"
  ```

3. Next, initialize a PostgreSQL database cluster:
  ```
  /usr/local/etc/rc.d/postgresql initdb
  ```

4. Now open the configuration file:
  ```
  sudo vi /usr/local/pgsql/data/postgresql.conf
  ```
  
Then find the following line and remove the hashtag to uncomment the line.
  ```
  listen_addresses = 'localhost'
  ```

5. Restarting Postres
  ```
  /usr/local/etc/rc.d/postgresql stop
  /usr/local/etc/rc.d/postgresql start
  /usr/local/etc/rc.d/postgresql restart
  ```

6. Reboot the server & reconnect
  ```
  reboot
  ssh 45.55.221.217 -l freebsd
  ```

7. Create our administrator User & our database
  ```
  su
  su pgsql
  createuser -sdrP django
  ```

8. Now you can look at 'postgres.txt' and setup the DB. Help taken from:
http://www.freebsddiary.org/postgresql.php

In summary, run the following codes and eCantina Database will be setup.
  ```
  /usr/local/bin/dropdb ecantina_db;
  /usr/local/bin/createdb ecantina_db;
  /usr/local/bin/psql ecantina_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE ecantina_db to django;
  ALTER USER django CREATEDB;
  ```
  
### NGINX 
1. Compile from source
  ```
  cd /usr/ports/www/nginx && make install clean
  rehash
  ```

2. add the following line to /etc/rc.conf:
  ```
  nginx_enable="YES"
  ```

3. Start the service:
  ```
  service nginx start
  ```
  
4. In your browser, verify this brings up a page. Go to:
http://http://45.55.221.217


### Depyloment
#### Source Code
1. Load up CyberDuck and copy the project into freebsd home directory

2. Go into the directory
  ```
  exit
  cd ~/py-ecantina
  ```

3. Setup our virtual environment
  ```
  virtualenv env --distribute
  ```

4. Now lets activate virtualenv
  ```
  source env/bin/activate.csh
  ```

5. Now lets install the libraries this project depends on.
  ```
  sudo pip install -r requirements.txt
  ```

6. Initialize database and make the server run.
  ```
  cd ecantina_project/
  python manage.py migrate
  python manage.py runserver  # Verify server can run. Close once verified.
  ```

#### Nginx

1. Nginx needs updating, make the following adjustments to:
  ```
  sudo vi /usr/local/etc/nginx/nginx.conf
  ```

2. And then scroll to the ***server*** line and replace the code with the following.
  ```
  server {
        server_name comicscantina.com;

        access_log off;

        location /static/ {
            alias /usr/home/freebsd/py-ecantina/ecantina_project/static/;
        }

        location /media/ {
            alias /usr/home/freebsd/py-ecantina/ecantina_project/media/;
        }

        location / {
                proxy_pass http://127.0.0.1:8001;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
  }
  ```

3. We need to restart NGINX though so that it knows to look for our changes. To do this run the following:
  ```
  sudo service nginx restart
  ```
  
#### Grand Comic Database
##### Import XML Files
1. Load up CyberDuck and copy the gcd folder into the ~/py-ecantina folder.

2. Run the script to import
  ```
  python manage.py import_gcd /usr/home/freebsd/xml
  ```
##### Import Cover Images
See file **gcd.txt**

#### eCantina Database
##### Initial Values
Now lets initial the web-application database to default values.
  ```
  python manage.py setup_ecantina
  ```

##### Staff User
Lets add eCantina user
  ```
  python manage.py createsuperuser
  ```
  
3. Fill in the following:
  ```
  username: bart
  email: bart@mikasoftware.com
  password: ***REDACTED***
  password: ***REDACTED***
  ```

#### Run

1. FreeBSD Bug Fix: This fixes the issue with missing CSS/JS for admin.
  ```
  ln -s /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/django/contrib/admin/static/admin     /usr/home/freebsd/py-ecantina/ecantina_project/static/admin
  ```

2. Now lets verify if we run gunicorn, the website will work.
  ```
  gunicorn -c gunicorn_config.py ecantina_project.wsgi
  ```
  
3. Then in your browser checkout: http://45.55.221.217


4. Now go to http://45.55.221.217admin and log in.


5. Go to the 'Sites' model and change 'example.com' to 'comicscantina.com'

### Maintenance
1. Load up CyberDuck and copy the project into freebsd home directory

2. Run:
  ```
  ssh 45.55.221.217 -l freebsd
  cd ~/py-ecantina
  source env/bin/activate.csh
  cd ecantina_project/
  python manage.py migrate
  python manage.py syncdb
  ln -s /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/django/contrib/admin/static/admin /usr/home/freebsd/py-ecantina/ecantina_project/static/admin
  gunicorn -c gunicorn_config.py ecantina_project.wsgi
  ```

### Help:
* http://blog.richardknop.com/2012/01/install-postgresql-on-freebsd-8-2-and-make-it-work-with-django/
* http://tenderlovingcode.com/blog/uncategorized/ec2-freebsd-nginx-uwsgi-django/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn
* http://stackoverflow.com/questions/15742383/django-with-gunicron-and-nginx
* http://www.michielovertoom.com/freebsd/flask-gunicorn-nginx-supervisord/
* http://stackoverflow.com/questions/19669376/django-rest-framework-absolute-urls-with-nginx-always-return-127-0-0-1
