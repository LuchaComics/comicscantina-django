# eCantina Database Documentation
## Description
Database server runs only the Postgres database and does not accept any other connections form the internet; furthermore, this server only accept database calls from the private network that the web-application is running on.


## (1) Setup
### Requirements
* Hosting with **Vultr**
* 1 **FreeBSD 64bit** Droplet (IP: 107.191.50.75)
* Must have **private networking** enabled


### (a) Login 
We will login and change our password to something we use.

1. Run from your local machine. When asked a question, select **yes**. Use the **initial password** found on Vultr.
```
ssh 107.191.50.75 -l root
```


2. Go the this file and add:
  ```
  vi /etc/rc.conf

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  defaultrouter="107.191.50.1"
  ifconfig_vtnet1="inet 10.99.0.10 netmask 255.255.0.0"  # DATABASEAPP
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  ```


3. Please follow along the instructions in the **prod_webapp.md** file until you get to step **e-ii-1** and then continue following the instructions below:


## Firewall
1. Populate our firewall ruleset
  ```
  cat > /etc/pf.conf
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ext_if="vtnet0"
  int_if="vtnet1"

  databaseports = "{5432, 5433}"
  int_tcp_services = "{domain, ntp}"
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

  # Database Access
  pass proto tcp from any to $int_if port $databaseports

  # Allow essential outgoing traffic
  pass out quick on $ext_if proto tcp to any port $int_tcp_services
  pass out quick on $ext_if proto udp to any port $int_udp_services
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ```


2. Please resume follow along the instructions in the **prod_webapp.md** file - resme at step **e-ii-1** and then continue following the instructions until step **(f) Python**.



### Postgres 9.4.4   *
1. Compile from source
  ```
  # Bugfix - For some reason this library messes up on install unless you 
  #          run the following commands manually.
  cd /usr/ports/devel/gettext-tools
  make install clean

  cd /usr/ports/databases/postgresql94-client
  make install clean

  cd /usr/ports/databases/postgresql94-server
  make install clean
  ```

2. Load up our rc.config
  ```
  vi /etc/rc.conf
  ```

  Add this line to /etc/rc.conf:
  ```
  ###### DATABASE
  #
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

Then find the following line and remove the hashtag to uncomment the line.
  ```
  listen_addresses = '*'
  port = 5432
  ```

5. 
  ```
  vi /usr/local/pgsql/data/pg_hba.conf

  Add
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  host    all             all            10.99.0.11/24          trust
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ```

6. Restarting Postres
  ```
  /usr/local/etc/rc.d/postgresql stop
  /usr/local/etc/rc.d/postgresql start
  /usr/local/etc/rc.d/postgresql restart
  ```

7. Reboot the server & reconnect
  ```
  reboot
  ssh 107.191.50.75 -l root
  ```

8. Create our administrator User & our database
  ```
  su pgsql
  createuser -sdrP django
  ```

9. Now you can look at 'postgres.txt' and setup the DB. Help taken from:
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

10. Test:
  ```
  psql -h 10.99.0.11 -U django -d ecantina_db
  psql -h localhost -U django -d ecantina_db
  ```