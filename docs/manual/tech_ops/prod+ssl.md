# eCantina Production Server SSL Configuration Instructions
## Description
This document will provide the detailed instruction set on how to setup SSL for the eCantina PROD server.

## Source:
http://www.rubynginx.com/index.php/2013/03/15/installing-positivessl-certificate-with-nginx-on-ubuntu-12-04/

## Instructions
### Register "Wildcard SSL" Certificate
Go to www.namecheap.com and purchase a SSL from them.



### Setting up Server
1. Login
  ```
  ssh 108.61.119.219 -l root
  su freebsd;
  cd ~/;
  mkdir ~/ssl;
  mkdir ~/ssl/private;
  mkdir ~/ssl/certs;
  ```


2. Generate private key and certificate signing request
  ```
  cd ~/ssl/private;
  openssl genrsa -des3 -out comicscantina.com.key 2048


  Note:
  i. You will be prompted to enter a password, enter a password.
  ```


3. Enter this command and you will be prompted to enter the password you chose in last step.
  ```
  openssl rsa -in comicscantina.com.key -out comicscantina.com.key.nopass
  ```


4. Next enter this command as well.
  ```
  openssl req -new -key comicscantina.com.key.nopass -out comicscantina.com.csr


  Note:
  i. You will be prompted for a bunch of information, don’t worry about most of it but make sure for “Common Name” you input your is "*.comicscantina.com" and Do not choose a challenge password
  ii. Make sure it ends up looking like this:
  - - - - - - - - - - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  - 
  Country Name (2 letter code) [AU]:CA
  State or Province Name (full name) [Some-State]:Ontario
  Locality Name (eg, city) []:London
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:The Shooting Star Press inc.
  Organizational Unit Name (eg, section) []:Comics Cantina
  Common Name (e.g. server FQDN or YOUR name) []:*.comicscantina.com
  Email Address []:support@comicscantina.com

  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []:
  An optional company name []:
  - - - - - - - - - - - - - - - - - - -  -  -  -  -  -  -  -  -  -  -  -  -  - 
  ```


5. Submit certificate signing request to EssentialSSL/Comodo
  ```
  cat comicscantina.com.csr
  ```

Depending on where you bought your certificate, log in to your control panel and “activate” your certificate by submitting the contents of your .csr file to them. In my case it would be namecheap.com, go to manage ssl certificates and click activate link next to the certificate. Select “other” from the web server type dropdown and then paste in your key and submit.

example csr file contents:

  ```
  -----BEGIN CERTIFICATE REQUEST-----
  MIIBnTCCAQYCAQAwXTELMAkGA1UEBhMCU0cxETAPBgNVBAoTCE0yQ3J5cHRvMRIw
  EAYDVQQDEwlsb2NhbGhvc3QxJzAlBgkqhkiG9w0BCQEWGGFkbWluQHNlcnZlci5l
  eGFtcGxlLmRvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAr1nYY1Qrll1r
  uB/FqlCRrr5nvupdIN+3wF7q915tvEQoc74bnu6b8IbbGRMhzdzmvQ4SzFfVEAuM
  MuTHeybPq5th7YDrTNizKKxOBnqE2KYuX9X22A1Kh49soJJFg6kPb9MUgiZBiMlv
  tb7K3CHfgw5WagWnLl8Lb+ccvKZZl+8CAwEAAaAAMA0GCSqGSIb3DQEBBAUAA4GB
  AHpoRp5YS55CZpy+wdigQEwjL/wSluvo+WjtpvP0YoBMJu4VMKeZi405R7o8oEwi
  PdlrrliKNknFmHKIaCKTLRcU59ScA6ADEIWUzqmUzP5Cs6jrSRo3NKfg1bd09D1K
  9rsQkRc9Urv9mRBIsredGnYECNeRaK5R1yzpOowninXC
  -----END CERTIFICATE REQUEST-----
  ```

After you are finished with that process you will just have to wait for a verification email at the email you provided them. (webmaster@mydomain.com in my case). When you get the email you click the link and enter a verification code in. Then you just need to wait for your final signed certificate to arrive in your primary email box. When you get the email it should have a zip file attached containing two files: A .crt and .ca-bundle: Copy these files somewhere on your server.




### Setting up Nginx *
1. Install signed certificate here using **CyberDuck**.
  ```
  su freebsd
  cd ~/ssl/certs
  
  Note:
  i. Copy *STAR_comicscantina_com.ca-bundle* and *STAR_comicscantina_com.crt* into this folder.
  ```


2. Copy the CSR and Private keys into the **certs** folder.
  ```
  cp /usr/home/freebsd/ssl/private/comicscantina.com.csr /usr/home/freebsd/ssl/certs/comicscantina.com.csr
  cp /usr/home/freebsd/ssl/private/comicscantina.com.key /usr/home/freebsd/ssl/certs/comicscantina.com.key


3. Create a PEM file 

  cat comicscantina.com.key comicscantina.com.csr STAR_comicscantina_com.crt STAR_comicscantina_com.ca-bundle > comicscantina.com.pem

  Note:
  i. If you get an error, try to re-arrange the order until it works.
  ii. Special thanks to this link, reference it if you have any problems: http://stackoverflow.com/a/17420863
  ```


2. Configure Nginx virtualhost to enable SSL:
Nginx needs updating, make the following adjustments to:
  ```
  vi /usr/local/etc/nginx/nginx.conf
  ```


3. Append your “listen 80” line to include this as well:
  ```
  listen    443 ssl;
  ```


4. Add these 2 lines below the listen line in the same server block (substitute with your path to your certificate files)
  ```
  ssl_certificate        /usr/home/freebsd/ssl/certs/comicscantina.com.pem;
  ssl_certificate_key    /usr/home/freebsd/ssl/private/comicscantina.com.key.nopass;
  ```


5. (Optional Step) If you want your site to always use SSL then add this block to the top of your file:
  ```
  server {
      listen    80;
      server_name    yourdomain.com;
      rewrite ^(.*) https://www.yourdomain.com$1 permanent;
  }
  ```


6. You should be good to go now, restart nginx and test it out
  ```
  sudo service nginx restart
  ```


7. In summary it hsould look like this:
  ```
  server {
      listen         80;
      listen    443 ssl;
      ssl_certificate        /usr/home/freebsd/ssl/certs/comicscantina.com.pem;
      ssl_certificate_key    /usr/home/freebsd/ssl/private/comicscantina.com.key.nopass;

      server_name ~(?<short_url>\w+)\.comicscantina\.com$;

      access_log off;

      location /static/rest_framework/ {
      ...
      ...
      ...
  ```
