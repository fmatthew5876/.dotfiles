Home Directory Configs Repo
===========================

Quick Start
===========

Install the following software packages:

* bash
* bash-completion
* git
* gcc (g++)
* clang (libclang-devel)
* make
* cmake
* python3 (libpython3-devel)
* vim (with python support)

Clone the repo to `~/.dotfiles`

```
cd ~
git clone git@github.com:fmatthew5876/.dotfiles.git
```

Add any site specific customizations to `~/.bashrc`


Run the setup script:

```
cd ~/home/
./setup.py
```

Installing configs for root
---------------------------

This must be done manually.

```
sudo cp ~/.dotfiles/root/.bashrc.custom /root
echo "source /root/.bashrc.custom" >> /root/bashrc
```

OS Specific Notes
================

Ubuntu
------

Auto install common packages

```
cat pkg.ubuntu | xargs apt install -y
```

Windows
-------

[README.Windows.md](README.windows.md)


New System Build Notes
======================


Mounting NTFS drives
--------------------

Mount an NTFS partition with no exec and owned by uid/gid 1000.

```
DEVICE PATH ntfs	rw,uid=1000,gid=1000,noatime,fmask=0137,dmask=0027
```
