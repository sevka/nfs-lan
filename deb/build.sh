#!/bin/bash
cp ./../nfs-share/nfs_share.py ./nfs_lan-1.0/usr/share/pyshared/nfs_lan/
cp ./../nfs-share/exports_sharing.py ./nfs_lan-1.0/usr/share/pyshared/nfs_lan/
cp ./../nfs-browse/nfs_browse.py ./nfs_lan-1.0/usr/share/pyshared/nfs_lan/

cp ./../nfs-share/nfs_share_nautilus.py ./nfs_lan-1.0/usr/share/nautilus-python/extensions/
cp ./../nfs-browse/nfs_browse_nautilus.py ./nfs_lan-1.0/usr/share/nautilus-python/extensions/

touch ./nfs_lan-1.0/usr/share/pyshared/nfs_lan/__init__.py

dpkg -b ./nfs_lan-1.0 ./nfs_lan-1.0.deb
