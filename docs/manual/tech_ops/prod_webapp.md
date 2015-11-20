# eCantina Web-Application Documentation
## Description
The Web-Application (aka web-app) server is responsible for running the Python Django instance of eCantina. No database handling is done on this server as it will be connected to another server responsible for running as database host.

This documentation will provide two sections: Section 1 will provide detailed instructions on how to setup the web-app and Section 2 will provide details on how to maintain it.


## (1) Setup
### Requirements
* 1 **FreeBSD 64bit** Droplet (IP: 104.238.162.153)
* Must have **private networking** enabled


### (a) Login
We will login and change our password to something we use.

Run from your local machine. When asked a question, select **yes**. Use the **initial password** found on Vultr.
  ```
  ssh 104.238.162.153 -l root
  ```
  
  
### (b) Change Shell & Password
1. We will be using the **TC-Shell** in for our environment. Check what Shell we are currently using on our inital install.
  ```
  echo $SHELL

  Notes:
  /bin/sh : This is the Bourne shell.
  /bin/ksh93 : This is the Korn shell.
  /bin/bash : This is the Bash shell.
  /bin/zsh : This is the Z shell.
  /bin/csh : This is the C Shell.
  /bin/tcsh : This is the TC Shell.
  ```
  
2. And see what Shells we have installed:
  ```
  cat /etc/shells
  ```
  
3. We will be using TC-Shell, to change the shell, at prompt type this:
  ```
  chsh -s /bin/tcsh

  Notes:
  i. The chsh is a command that means change shell.
  ii. The -s sets it for you without having to go into the editor to do it.
  iii. The /usr/local/bin/bash tells your profile where to find the shell. 
  iv. When you log out and log back in, the new shell environment will be set.
  ```

7. It could have easily looked like these if you want to use a different shell.
  ```
  chsh -s /usr/local/bin/ksh93
  chsh -s /usr/local/bin/zsh
  chsh -s /bin/sh
  chsh -s /bin/csh
  chsh -s /bin/tcsh
  ```
  
8. To change password for 'root', type:
  ```
  passwd
  ```
Password: ***REDACTED***


### (c) SSH
We will enable PAM based authentication and ensure every user that logs in must have the registered key to access. These instructions where summarized from: here: [How To Configure SSH Key-Based Authentication on a FreeBSD Server](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-freebsd-server)

1. Generate a private and public key (if you haven't done this already) on your local machine. If you don't know how to do this, read the article mentioned above.

2. Once you have generated the **private-public keys**, run the following command on your local machine which will print to the terminal screen what your public key is. Copy the output to your clipboard as you will be pasting it in our servers **authorization** file.
  ```
  cat ~/.ssh/id_rsa.pub
  ```
  
3. Go into the SSH folder and paste our key into it.
  ```
  vi ~/.ssh/authorized_keys
  ```
  
4. Now we need to disable password based authentication and enable public-private key based.
  ```
  vi /etc/ssh/sshd_config
  ```
  
5. Change the following line to look like this.
  ```
  PasswordAuthentication no
  ChallengeResponseAuthentication no
  ```
  
6. For the changes to take effect, you must restart the sshd service. To restart the SSH daemon on FreeBSD, use this command:
  ```
  service sshd restart
  ```
  
7. Log out and log back in, you should be automatically authenticated.


### (d) FreeBSD new user
1. Create a web-developer account to run our services.
  ```
  adduser -v

  Fill In:
  Username: freebsd
  Fullname: Comics Cantina Service
  Uid: (Leave Blank)
  Login Group: (Leave Blank)
  Login Class: (Leave Blank)
  Shell: tcsh
  Home directory: (Leave Blank)
  Home directory permissions: (Leave Blank)
  Use password-based authentication: no
  Use an empty password: no
  Use a random password: no
  Enter password: **REDACTED**
  Enter password again: **REDACTED**
  Lock out the account after creation: no

  ```
  
2. Log into our new user by SSH'ing into it. Be sure to use the password you set.
  ```
  ssh 104.238.162.153 -l freebsd
  ```


### (e) Ports
1. Now we need to get the most up-to-date repository of ports and apply it to our system.
  ```
  sudo portsnap fetch extract update
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
  
  
### (f) Python
#### (i) Python 3.4
1. Compile from source Python 3.4
  ```
  cd /usr/ports/lang/python34
  make install clean
  ```
  
2. Find where Python was installed
  ```
  rehash
  find /usr/bin /bin/ /usr/local/bin -iname 'python*'
  ```
  
3. Make the command "python" be available on the FreeBSD system.
  ```
  ln -s /usr/local/bin/python3.4 /usr/local/bin/python
  ```

4. Verify Python was installed and is version 3.4.x
  ```
  python -V
  ```
  
  
#### (ii) Extra Python Libraries
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


####(iii) pip
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
  
  
####(iv) Virtualenv
1. To install:
  ```
  pip install virtualenv
  ```

2. Verify virtualenv is intalled
  ```
  su freebsd
  cd ~/
  mkdir py-ecantina
  cd py-ecantina
  virtualenv env
  ```
  
  
###(g) Postgres 9.4
Please read the instructions in **prod_database.md**.


###(h) NGINX 
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
http://45.55.221.217


###(i) Depyloment
####(i) Source Code
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

####(ii) Nginx

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
  
  
####(iii) Grand Comic Database
#####(Part 1) Import XML Files
1. Load up CyberDuck and copy the gcd folder into the ~/py-ecantina folder.

2. Run the script to import
  ```
  python manage.py import_gcd /usr/home/freebsd/xml
  ```
#####(Part 2) Import Cover Images
See file **gcd.txt**

#####(Part 3) eCantina Initial Values
Now lets initial the web-application database to default values.
  ```
  python manage.py setup_ecantina
  ```

#####(Part 4) Staff User
1. Lets add eCantina user
  ```
  python manage.py createsuperuser
  ```
  
2. Fill in the following:
  ```
  username: bart
  email: bart@mikasoftware.com
  password: ***REDACTED***
  password: ***REDACTED***
  ```

####(j) Run

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


##(2) Maintenance
1. Load up CyberDuck and copy the project into freebsd home directory

2. Run:
  ```
  ssh 45.55.221.217 -l freebsd
  cd ~/py-ecantina
  source env/bin/activate.csh
  cd ecantina_project/
  python manage.py migrate
  python manage.py syncdb
  ln -s /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/django/contrib/admin/static/admin/usr/home/freebsd/py-ecantina/ecantina_project/static/admin
  gunicorn -c gunicorn_config.py ecantina_project.wsgi
  ```
