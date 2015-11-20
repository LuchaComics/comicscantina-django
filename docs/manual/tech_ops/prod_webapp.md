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

#### (d) Setting up a default non-root user to run our services on.
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
  
2. Log into our new user by SSH'ing into it.
  ```
  ssh 104.238.162.153 -l freebsd
  ```
  
3. Read the above instructions on SSH and make this user account into a public-private key authentication scheme.
