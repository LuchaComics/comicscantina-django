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
  host = actfastbookkeeping.com.
  ```

4. Click **Add Record** and click **CNAME** with:
  ```
  name = *
  host = actfastbookkeeping.com.
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
