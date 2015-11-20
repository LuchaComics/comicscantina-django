# eCantina Database Documentation
## Description
Database server runs only the Postgres database and does not accept any other connections form the internet; furthermore, this server only accept database calls from the private network that the web-application is running on.

## (1) Setup
### Requirements
* Hosting with **Vultr**
* 1 **FreeBSD 64bit** Droplet (IP: 104.238.162.153)
* Must have **private networking** enabled

## Firewall
Please follow along the instructions in the **prod_webapp.md** file until you get to step **e-ii-1** and then continue following these instructions.

1. Populate our firewall ruleset
  ```
  cat > /etc/pf.conf
  
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ext_if="vtnet0"

  webports = "{http, https}"
  int_tcp_services = "{domain, ntp, smtp, www, https, ftp, 5432, 5433}"
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
  
  - - - - - - - - - - - - - - - - - - - - - - -   - - - - - - - - - - - - - - 
  ###### FIREWALL
  #
  pf_enable="YES" 		# Turn PF on when pc boots.
  pf_rules="/etc/pf.conf" # Define the rules for the firewall
  pf_flags=""			# Additional flags (none).
  pflog_enabled="YES"		# Turn on packet loggin support.
  pflog_logfile="/var/log/pflog" # Where to log data to, used by pflog daemon
  pflog_flags=""			# Additional flags (None).
  - - - - - - - - - - - - - - - - - - - - - - -   - - - - - - - - - - - - - - 
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
