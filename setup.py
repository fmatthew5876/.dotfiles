#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import logging
import shutil
import glob

# Don't clobber system installed .bashrc, instead source this one at the end.
_bashrc_custom='.bashrc.custom'

# List of files to symlink into home.
# Must be relative paths to this git repo root.
_files=[
        # Bash Environment file
        '.bashrc.custom',
        # Solarized Dark 256 colors for gnu coreutils
        '.dircolors',
        # Gdb
        '.gdbinit',
        # Git
        '.gitconfig',
        '.git-prompt.sh',
        # Tmux
        '.tmux.conf',
        # Vim
        '.vim',
        '.vimrc',
        # Xterm, urxvt, etc..
        '.Xresources',
        # Cywgin mintty
        '.minttyrc',
        ]

_homedir = os.path.expanduser('~')
_repodir = _homedir + "/.dotfiles"

print(os.path.dirname(__file__))
print(os.path.split(os.path.dirname(__file__))[-1])
print(_repodir)

_vundle_url="https://github.com/VundleVim/Vundle.vim.git"

def runCmd(cmd, dry_run):
    logging.info("Running cmd: %s ...", cmd)
    if not dry_run:
        subprocess.check_call(cmd, shell=True)

def makeLink(target, link, dry_run):
    logging.info("Symlinking %s -> %s ...", link, target)
    if not dry_run:
        os.symlink(target, link)

def remove(target, dry_run):
    logging.info("Removing %s ...", target)
    if not dry_run:
        os.remove(target)

def rmTree(path, dry_run):
    if not os.path.exists(path):
        return
    logging.info("%s: Removing directory tree...", path)
    if not dry_run:
        shutil.rmtree(path)

def mkdir(path, dry_run):
    logging.info("%s: Creating directory...", path)
    if not dry_run:
        os.mkdir(path)

def genXresources(dry_run):
    logging.info("Generating .Xresources...")
    if not dry_run:
        with open('.Xresources', 'w') as f:
            f.write('!Auto-generated! Do not edit directly!\n\n')
    runCmd("cpp -undef Xresources.pre >> .Xresources", dry_run)

def createLinks(allow_custom, dry_run, rebuild_links):
    logging.info("Creating symlinks in home directory...")
    for f in _files:
        link = os.path.join(_homedir, f)
        #Construct link path relatively from ~. This allows easy compatibility with environments that have /home setup
        #symlinks to complex underlying path structures which differ across hosts.
        target = os.path.join(_repodir, f)

        if not os.path.exists(target):
            raise FileNotFoundError(target)

        if os.path.exists(link):
            if os.path.islink(link):
                if os.path.realpath(target) == os.path.realpath(link):
                    logging.info("%s: already linked! Skipping...", link)
                    continue
                if not rebuild_links:
                    if allow_custom:
                        logging.warn("%s: is already a link! Skipping due to --allow-custom...", link)
                        continue
                    raise Exception("{}: link exists but points to {}! Please fix!".format(link, os.path.realpath(link)))
            else:
                if allow_custom:
                    logging.warn("%s: already a file! Skipping due to --allow-custom...", link)
                    continue
                raise Exception("{}: file already exists! Please fix!".format(link))

            if rebuild_links:
                remove(link, dry_run)

        makeLink(target, link, dry_run)

def patchBashrc(dry_run):
    bashrc = os.path.join(_homedir, '.bashrc')
    logging.info("Patching %s ...", bashrc)
    if os.path.exists(os.path.join(_homedir, '.bashrc')):
        with open(bashrc) as f:
            for line in f:
                if _bashrc_custom in line:
                    logging.info("%s: Already patched! Skipping...", bashrc)
                    return

    if not dry_run:
        with open(bashrc, 'a') as f:
            f.write('\n#Source home git customizations\n')
            f.write('. ~/{}\n'.format(_bashrc_custom))


def setupVim(dry_run):
    logging.info("Doing initial vim setup...")
    vimrc = os.path.join(_homedir, ".vimrc")
    bundledir = os.path.join(_homedir, ".vim", "bundle")

    if not os.path.exists(vimrc):
        raise FileNotFoundError(vimrc)

    if not os.path.isdir(bundledir):
        raise FileNotFoundError(bundledir)

    python_ver=2
    vim_ver = subprocess.check_output("vim --version", shell=True).decode('utf-8')
    if "+python3" in vim_ver:
        python_ver=3
        logging.info("Detected python3 support in vim!")
    elif "+python" in vim_ver:
        python_ver=2
        logging.info("Detected python2 support in vim!")
    else:
        raise Exception("No python support detected in vim binary!")


    # Clone vundle repo
    vundledir = os.path.join(bundledir, "Vundle.vim")
    if not os.path.exists(vundledir):
        logging.info("Bootstrapping vundle...")
        runCmd("git clone {} {}".format(_vundle_url, vundledir), dry_run)

    # Tell vim to install packages
    runCmd("vim +PluginInstall +qall", dry_run)

def main():
    parser = argparse.ArgumentParser("Home directory setup script")
    parser.add_argument('-n', '--dry-run', action='store_true', help="Run through script but don't actually run commands")
    parser.add_argument("--no-links", action='store_true', help="Don't create symlinks")
    parser.add_argument("--no-bashrc", action='store_true', help="Don't patch .bashrc")
    parser.add_argument("--no-vim", action='store_true', help="Don't do vim setup")
    parser.add_argument("--rebuild-links", action='store_true', help='Overwrite links')
    parser.add_argument("--allow-custom", action='store_true', default=None, help="Don't die if custom configs already exist")

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    dry_run = args.dry_run
    do_links = not args.no_links
    do_bashrc = not args.no_bashrc
    do_vim = not args.no_vim
    allow_custom = args.allow_custom
    rebuild_links = args.rebuild_links

    logging.info("Changing directory to script dir...")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    genXresources(dry_run)

    if do_links:
        createLinks(allow_custom, dry_run, rebuild_links)

    if do_bashrc:
        patchBashrc(dry_run)

    if do_vim:
        setupVim(dry_run)


if __name__ == "__main__":
    main()
