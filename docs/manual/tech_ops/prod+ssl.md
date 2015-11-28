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
  ssh 108.61.119.219 -l freebsd
  ```


2. Generate private key and certificate signing request
  ```
  openssl genrsa -des3 -out comicscantina.com.key 2048


  Note:
  i. You will be prompted to enter a password
  ```


3. Enter next.
  ```
  openssl rsa -in comicscantina.com.key -out comicscantina.com.key.nopass
  ```


4. You will be prompted to enter the password you chose in last step
  ```
  openssl req -new -key comicscantina.com.key.nopass -out comicscantina.com.csr


  Note:
  i. You will be prompted for a bunch of information, don’t worry about most of it but make sure for “Common Name” you input your domain name. Do not choose a challenge password
  ```


5. Submit certificate signing request to PositiveSSL/Comodo

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

After you are finished with that process you will just have to wait for a verification email at the email you provided them. (webmaster@mydomain.com in my case). When you get the email you click the link and enter a verification code in. Then you just need to wait for your final signed certificate to arrive in your primary email box. When you get the email it should have a zip file attached containing three files. yourdomain_com.crt, PositiveSSLCA2.crt and AddTrustExternalCARoot.crt. Copy these files somewhere on your server.




### Setting up Nginx *
1. Install signed certificate
  ```
  cat yourdomain_com.crt PositiveSSLCA2.crt AddTrustExternalCARoot.crt > yourdomain.com.pem

  cat comicscantina_com.crt COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt COMODORSADomainValidationSecureServerCA.crt > comicscantina.com.pem
  ```


2. Configure Nginx virtualhost to enable SSL:
Nginx needs updating, make the following adjustments to:
  ```
  sudo vi /usr/local/etc/nginx/nginx.conf
  ```

3. change your “listen” line to read as follows:
  ```
  listen    443 ssl;
  ```

4. Add these 2 lines below the listen line in the same server block (substitute with your path to your certificate files)
  ```
  ssl_certificate        /usr/home/freebsd/ssl/comicscantina.com.pem;
  ssl_certificate_key    /usr/home/freebsd/ssl/comicscantina.com.key.nopass;
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
      ssl_certificate        /usr/home/freebsd/ssl/comicscantina.com.pem;
      ssl_certificate_key    /usr/home/freebsd/ssl/comicscantina.com.key.nopass;
      server_name comicscantina.com www.comicscantina.com;

      access_log off;

      location /static/ {
          alias /usr/home/freebsd/py-mikasoftware/mikasoftware_project/static/;
      }

      location /media/ {
          alias /usr/home/freebsd/py-mikasoftware/mikasoftware_project/media/;
      }

      location / {
      ...
      ...
      ...
  ```
