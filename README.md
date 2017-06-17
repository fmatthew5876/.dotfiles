Home Directory Configs Repo
===========================

Quick Start
===========

Clone the repo to `~/home`

```
cd ~
git clone git@github.com:fmatthew5876/home.git
```

Add any site specific customizations to `~/.bashrc`:


Run the setup script:

```
cd ~/home/
./setup.py
```

Notes
=================


Mounting NTFS drives
----------------------

Mount an NTFS partition with no exec and owned by uid/gid 1000.

DEVICE DIR ntfs	rw,uid=1000,gid=1000,noatime,fmask=0137,dmask=0027
