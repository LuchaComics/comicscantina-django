# eCantina Production Server Documentation
## Description
The production server is responsible for running the Python Django instance of eCantina along with the Postgres database. 

This documentation will provide two sections: Section 1 will provide detailed instructions on how to setup the web-app and Section 2 will provide details on how to maintain it.


## (1) Setup
### Requirements
* Hosting with **Vultr**
* 1 **FreeBSD 64bit** Droplet (IP: 108.61.119.219, Gateway: 108.61.119.1)
* Must have **private networking** enabled


### (a) Login & Change Swap & Add Private Newtwork
We will login and change our password to something we use.

1. Run from your local machine. When asked a question, select **yes**. Use the **initial password** found on Vultr.
  ```
  ssh 108.61.119.219 -l root
  ```
  
2. Vultr does not configure swap, we have to do it manually. Instructions taken from here: [11.12. Adding Swap Space](https://www.freebsd.org/doc/handbook/adding-swap-space.html) 
  ```
  dd if=/dev/zero of=/usr/swap0 bs=1m count=5000;  
  chmod 0600 /usr/swap0;
  swapon -aL;
  mdconfig -a -t vnode -f /usr/swap0 -u 0 && swapon /dev/md0;
  ```
  
3. Run the following command to confirm swap was added.
  ```
  swapinfo
  ````

4. Go the this file and add:
  ```
  vi /etc/rc.conf
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  defaultrouter="108.61.119.1"
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
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
We will enable public-private key based authentication and ensure every user that logs in must have the registered key to access. These instructions where summarized from: here: [How To Configure SSH Key-Based Authentication on a FreeBSD Server](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-freebsd-server)

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
  PubkeyAuthentication yes
  PasswordAuthentication no
  ChallengeResponseAuthentication no
  ```
  
6. For the changes to take effect, you must restart the sshd service. To restart the SSH daemon on FreeBSD, use this command:
  ```
  service sshd restart
  ```
  
7. Log out and log back in, you should be automatically authenticated.


### (d) Recompile Kernel
We will recompile the Kernel for our server and enable PF firewall. The recompiling instructions are summarized from this article: [How To Customize and Recompile Your Kernel on FreeBSD 10.1](https://www.digitalocean.com/community/tutorials/how-to-customize-and-recompile-your-kernel-on-freebsd-10-1)

1. Install subversion
  ```
  pkg install subversion  
  rehash
  ```
  
2. Download our source
  ```
  svn co https://svn0.us-east.FreeBSD.org/base/stable/10 /usr/src
  
  Note:
  i. Choose (p) to accept
  ```
  
3. Setup our configuration file
  ```
  cd /usr/src/sys/amd64/conf
  cp GENERIC COMICSCANTINA
  ```
  
4. Go into our new file and perform the following modifications:
  ```
  vi COMICSCANTINA
  
  (a) Rename "GENERIC" to "COMICSCANTINA"
  (b) Scroll to the bottom fo the file and add:
  - - - - - - - - - - 
  # pf firewall
  device pf
  device pflog
  device pfsync
  - - - - - - - - - - 
  ```
  
5. Compile
  ```
  cd /usr/src
  make buildkernel KERNCONF=COMICSCANTINA
  make installkernel KERNCONF=COMICSCANTINA
  reboot
  ```
  
6. To confirm our new Kernel has been built, simply run the following and confirm:
  ```
  sysctl kern.conftxt | grep ident
  
  Note:
  i. You should see "ident COMICSCANTINA"
  ```

### (e) Security
#### (i) SSH Banners
1. Update MOTD
  ```
  cat > /etc/motd
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
WARNING: Unauthorized access to this system is forbidden and will be prosecuted
by law. By accessing this system, you agree that your actions may be
be monitored if unauthorized usage is suspected.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ```

2. Update WELCOME.
  ```
  cat > /etc/welcomemsg
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                                  -------
                                  WARNING
                                  -------
                     THIS IS A PRIVATE COMPUTER SYSTEM.

This computer system including all related equipment, network devices
(specifically including Internet access), are provided only for authorized use.
All computer systems may be monitored for all lawful purposes, including to
ensure that their use is authorized, for management of the system, to facilitate
protection against unauthorized access, and to verify security procedures,
survivability and operational security. Monitoring includes active attacks by
authorized personnel and their entities to test or verify the security of the
system. During monitoring, information may be examined, recorded, copied and
used for authorized purposes. All information including personal information,
placed on or sent over this system may be monitored. Uses of this system,
authorized or unauthorized, constitutes consent to monitoring of this system.
Unauthorized use may subject you to criminal prosecution. Evidence of any such
unauthorized use collected during monitoring may be used for administrative,
criminal or other adverse action. Use of this system constitutes consent to
monitoring for these purposes.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ```
  
3. Update the SSH configuration to play our welcome message.
  ```
  vi /etc/ssh/sshd_config
  
  Note:
  i. Add/Change: "Banner /etc/welcomemsg"
  ```
  
#### (ii) Firewall
1. Populate our firewall ruleset
  ```
  cat > /etc/pf.conf
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ext_if="vtnet0"

  webports = "{http, https}"
  int_tcp_services = "{domain, ntp, smtp, www, https, ftp, 465, 587}"
  int_udp_services = "{domain, ntp}"

  set skip on lo
  set loginterface $ext_if

  # Normalization
  scrub in all random-id fragment reassemble

  block return in log all
  block out all

  antispoof quick for $ext_if

  # Block 'rapid-fire brute force attempts
  table <bruteforce> persist
  block quick from <bruteforce>

  # ftp-proxy needs to have an anchor
  anchor "ftp-proxy/*"

  # SSH is listening on port 22
  pass in quick proto tcp to $ext_if port 22 keep state (max-src-conn 15, max-src-conn-rate 5/3, overload <bruteforce> flush global)

  # Webserver
  pass proto tcp from any to $ext_if port $webports

  # Allow essential outgoing traffic
  pass out quick on $ext_if proto tcp to any port $int_tcp_services
  pass out quick on $ext_if proto udp to any port $int_udp_services
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ```

2. Update **rc.conf**:
  ```
  vi /etc/rc.conf
  
  - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - 
  ###### FIREWALL
  #
  pf_enable="YES" 		         # Turn PF on when pc boots.
  pf_rules="/etc/pf.conf"        # Define the rules for the firewall
  pf_flags=""			         # Additional flags (none).
  pflog_enable="YES"		     # Turn on packet loggin support.
  pflog_logfile="/var/log/pflog" # Where to log data to, used by pflog daemon
  pflog_flags=""			     # Additional flags (None).
  - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - 
  ```

3. To start the firewall, run the following. Note: More instructions can be found here: [PF Firewall](https://www.freebsd.org/doc/handbook/firewalls-pf.html)
  ```
  service pf start
  service pflog start
  ```

#### (iii) Hardening rc.conf
1. Load up our file
  ```
  vi /etc/rc.conf
  ```
  
2. Notes: When we are doing modification to the Kernel, use this:
  ```
  kern_securelevel_enable="YES" 
  kern_securelevel="1"	 
  ```
  
3. Else when we are running production, use this:
  ```
  kern_securelevel_enable="YES"  
  kern_securelevel="4"			    
  ```

3. Now append the file with the following.
  ```
  ###### SECURITY
  #
  kern_securelevel_enable="YES" # Enable Kernel Security
  kern_securelevel="4"              # Network Secure Level
  sendmail_enable="NONE"            # Disable Sendmail
  nfs_server_enable="NO"            # Disable NFS Server
  nfs_client_enable="NO"            # Disable NFS Client
  portmap_enable="NO"               # Disable portmap
  syslogd_enable="YES"              # Allow system logging
  syslogd_flags="-ss"               # Disable remote system logging
  #tcp_drop_synfin="YES"             # Drop OS Fingerprinting
  icmp_drop_redirect="YES"
  icmp_log_redirect="YES"
  log_in_vain="YES"                 # Root login security thingy
  #accounting_enable="YES"           # Logs all attempts to closed ports
  clear_tmp_enable="YES"            # Clear /tmp on startup
  ```
 
 4. Reboot the computer to apply all our changes.
  ```
  reboot
  ```


### (e) eCantina Service User
It's a key security ingredient that we have our applications running on a non-root user. Therefore these steps will get us setup with a user that we will be running all our applications on.

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
  ssh 108.61.119.219 -l freebsd
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

  cd /usr/ports/converters/libiconv && make install clean;

  # Bugfix - For some reason this library messes up on install unless you 
  #          run the following commands manually.
  cd /usr/ports/devel/gettext-tools && make install clean MAKE_JOBS_UNSAFE=yes;
  ```
  
  
### (f) Python
#### (i) Python 3.4
1. Compile from source Python 3.4
  ```
  cd /usr/ports/lang/python34 && make install clean;
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
  cd /usr/ports/devel/py-setuptools27 && make deinstall clean;
  cd /usr/ports/devel/py-setuptools34 && make install clean;
  ```

2. Lets install GD:
  ```
  cd /usr/ports/graphics/gd && make install clean;
  
  Note:
  i. Select all at the beginning
  ```

3. Lets install FreeType
  ```
  cd /usr/ports/print/freetype2 && make install clean;
  ```
  
4. Lets install memcached.
  ```
  cd /usr/ports/databases/memcached && make install clean;
  cd /usr/ports/databases/libmemcached && make install clean;
  ```

5. Edit /etc/rc.conf and add the following.  
  ```
  memcached_enable="YES"
  ```

6. Add screen
  ```
  cd /usr/ports/sysutils/screen && make install clean;
  ```


####(iii) pip
1. Lets install pip:
  ```
  cd /usr/ports/ftp/curl && make install clean;
  
  cd ~/;
  curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py;
  python get-pip.py;
  rm get-pip.py;
  ```
  
2. Verify pip was installed
  ```
  pip -V
  ```
  
  
####(iv) Virtualenv
To install:
  ```
  pip install virtualenv
  ```
  
  
###(g) Postgres 9.4
1. Compile from source
  ```  
  cd /usr/ports/databases/postgresql94-client && make install clean;
  cd /usr/ports/databases/postgresql94-server && make install clean;
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
  vi /usr/local/pgsql/data/postgresql.conf
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
  ssh 108.61.119.219 -l root
  ```

7. Create our administrator User & our database
  ```
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

9. Run the following commands to ensure our Database is accessible remotely:
  ```
  psql -h localhost -U django -d ecantina_db
  ```


###(h) NGINX 
1. Compile from source
  ```
  cd /usr/ports/www/nginx && make install clean
  rehash

  # Make sure the following are selected:
  HTTP_GZIP_STATIC      Enable http_gzip_static module
  HTTP_GUNZIP_FILTER    Enable http_gunzip_filter module
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
http://108.61.119.219 


###(i) Depyloment
####(i) Source Code
1. Load up CyberDuck and copy the project into freebsd home directory

2. Go into the directory
  ```
  su freebsd
  cd ~/;
  mkdir py-ecantina;
  cd ~/py-ecantina;
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
  pip3 install django;                 
  pip3 install psycopg2;              
  pip3 install gunicorn;               
  pip3 install Pillow;                 
  pip3 install django-simple-captcha;  
  pip3 install pep8;                   
  pip3 install urllib3;                
  pip3 install beautifulsoup4;        
  pip3 install simplejson;             
  pip3 install djangorestframework;    
  pip3 install markdown;               
  pip3 install django-filter;          
  pip3 install qrcode;                
  pip3 install pylibmc --install-option="--with-libmemcached=/usr/local"; 
  pip3 install django-paypal;          
  ```

6. Initialize the **secret_settings.py** file with what we have on record for the **prod** server.

7. Initialize database and make the server run.
  ```
  cd ecantina_project/
  python manage.py migrate
  python manage.py runserver  # Verify server can run. Close once verified.
  ```



####(ii) Nginx

1. Nginx needs updating, make the following adjustments to:
  ```
  exit
  vi /usr/local/etc/nginx/nginx.conf
  ```

2. And then scroll to the ***server*** line and replace the code with the following.
  ```


service nginx restart
   http {
         # some directives ...

         client_max_body_size 0;

         # some more directives ...
  }

  # some code ...

  server {
        server_name ~(?<short_url>\w+)\.comicscantina\.com$;

        access_log off;

        gzip on;

        location /static/rest_framework/ {
            alias /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/rest_framework/static/rest_framework/; 
        }

        location /static/admin/ {
            alias /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/django/contrib/admin/static/admin/; 
        }

        location /static/ {
            alias /usr/home/freebsd/py-ecantina/ecantina_project/static/;
        }

        location /media/ {
            alias /usr/home/freebsd/py-ecantina/ecantina_project/media/;
        }

        location / {
            proxy_set_header X-CustomUrl $short_url;
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
  }
  ```

3. We need to restart NGINX though so that it knows to look for our changes. To do this run the following:
  ```
  service nginx restart
  ```
  
  

####(iii) Grand Comic Database
#####(Part 1) Import XML Files
1. Load up CyberDuck and copy the gcd folder into the ~/py-ecantina folder.

2. Run the script to import
  ```
  su freebsd
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
  
3. Then in your browser checkout: http://108.61.119.219


4. Now go to http://108.61.119.219/admin and log in.


5. Go to the 'Sites' model and change 'example.com' to 'comicscantina.com'


##(2) Maintenance
1. Load up CyberDuck and copy the project into freebsd home directory

2. Run:
  ```
  ssh 108.61.119.219 -l freebsd
  cd ~/py-ecantina
  source env/bin/activate.csh
  cd ecantina_project/
  python manage.py migrate
  python manage.py syncdb
  ln -s /usr/home/freebsd/py-ecantina/env/lib/python3.4/site-packages/django/contrib/admin/static/admin/usr/home/freebsd/py-ecantina/ecantina_project/static/admin
  gunicorn -c gunicorn_config.py ecantina_project.wsgi
  ```
