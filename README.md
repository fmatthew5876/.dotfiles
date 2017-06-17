# home
Home dir configs

Notes
=================


Mounting NTFS drives
----------------------

Mount an NTFS partition with no exec and owned by uid/gid 1000.

DEVICE DIR ntfs	rw,uid=1000,gid=1000,noatime,fmask=0137,dmask=0027
