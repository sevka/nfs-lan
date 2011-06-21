#!/bin/bash
cp ./../nfs-share/nfs_share.py ./nfs_lan-0.2/usr/share/pyshared/nfs_lan/
cp ./../nfs-browse/nfs_browse.py ./nfs_lan-0.2/usr/share/pyshared/nfs_lan/

cp ./../nfs-share/nfs_share_nautilus.py ./nfs_lan-0.2/usr/lib/nautilus/extensions-2.0/python/
cp ./../nfs-browse/nfs_browse_nautilus.py ./nfs_lan-0.2/usr/lib/nautilus/extensions-2.0/python/

touch ./nfs_lan-0.2/usr/share/pyshared/nfs_lan/__init__.py

dpkg -b ./nfs_lan-0.2 ./nfs_lan-0.2.deb
