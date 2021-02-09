Windows Packages
================

First steps
-----------

* Install updates
* Update drivers
* Remove unwanted apps

Software
-----------

* Firefox
* Chrome
* Edge
* Gimp https://www.gimp.org/downloads/
* Putty https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
* Wireshark https://www.wireshark.org/#download
* Vim https://www.vim.org/download.php#pc
* Vlc Media Player https://www.videolan.org/vlc/index.html
* Visual Studio https://visualstudio.microsoft.com/
* Vscode https://code.visualstudio.com/
* Git Windows https://git-scm.com/download/win
* HWMonitor https://www.cpuid.com/softwares/hwmonitor.html
* Discord https://discord.com/
* Plex https://www.plex.tv/media-server-downloads/#plex-app
* Roon https://roonlabs.com/downloads
* Spotify https://www.spotify.com/us/download/windows/
* Steam https://store.steampowered.com/about/
* Synergy https://symless.com/synergy
* WinSCP https://winscp.net/eng/download.php
* Notepad++ https://notepad-plus-plus.org/downloads/
* x410 Windows Store
* Intel Vtune https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit/download.html#operatingsystem=Windows&#distributions=Web%20&%20Local%20(recommended)&#options=Online
* VPN apps

WSL Setup
---------

https://docs.microsoft.com/en-us/windows/wsl/install-win10

```
sudo cp windows/wsl.conf /etc/wsl.conf
```

Vcpkg install
------------

```
vcpkg install --triplet x64-windows-static --recurse libpng[core] expat[core] pixman[core] freetype[core] harfbuzz[core] libvorbis[core] libsndfile[core] wildmidi[core] libxmp-lite[core] speexdsp[core] mpg123[core] opusfile[core] fluidlite[core] sdl2-image[core] sdl2-mixer[core,nativemidi] icu-easyrpg[core] nlohmann-json[core] fmt[core]
```

Using Solarized Theme for Windows cmd.exe
-----------------------------------------

Use the provided registry file.

```
regedit /s windows\solarized-dark.reg
```

