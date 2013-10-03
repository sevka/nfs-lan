NFS-LAN
=======
Overview
--------
NFS-LAN - plugin for Nautilus file manager (GNOME environment default file manager), that allows to share and browse NFS network (NFS - Network File System). 
It's missing functionality in Gnome.

There are two branches exist now. 

 * 1.x - for Gnome3/Nautilus3 (Ubuntu 12.04 for example)
 * 0.x - for Gnome2/Nautilus2 (Ubuntu 10.04 for example)

Technical summary
-----------------
It based on such technologies and packages :

 * Python. All code written on Python.
 * python-gtk for GUI 
 * python-nautilus for Nautilus python plugin
 * nfs-client and nfs-server for NFS support
 * autofs for auto mounting
 * avahi-browse (avahi-utils) and avahi-daemon for computers' list
 * showmount - to get only computers with shares

Installation
------------
Just install *.deb package. Autofs package is in the dependecies, but you have to configure it by yourself, if you want to browse NFS shares automatically. 
Please edit /etc/auto.master and uncomment this line:

    /net -hosts

You can add --timeout parameter (in this case you have a problems with unmounting shares which going down):

    /net -hosts --timeout=60

Then restart autofs:

    sudo service autofs restart

Usage
-----
###NFS sharing
To share folder in Nautilus, just right-click on folder and choose "Share this folder through NFS...". Then setup sharing options and click Ok.

  **Behind the scene**: NFS-LAN modify /etc/exports file and restarts NFS server

###NFS browsing
Go to /net folder in Nautilus. When you open /net folder first time in the session, NFS-LAN do `Refresh` action. 
NFS-LAN search for remote computers with avahi daemon activated (in Ubuntu avahi daemon activated by default). If your remote PC doesn't have avavi you can:

  * use `Computer name or ip` area
  * or just go to URI: /net/your_computer_name_or_ip
  
  **Behind the scene**. When you first time open /net folder or press Refresh button in the top panel, NFS-LAN search for remote PCs
  with avahi-daemon activated, then search for shares on these PCs. And then just do command 'cd /net/computer_name'.
  Autofs do the rest.
