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

_vundle_url="https://github.com/VundleVim/Vundle.vim.git"

def runCmd(cmd, dry_run):
    logging.info("Running cmd: %s", cmd)
    if not dry_run:
        subprocess.check_call(cmd, shell=True)

def makeLink(target, link, dry_run):
    logging.info("Symlinking %s -> %s", link, target)
    if not dry_run:
        os.symlink(target, link)

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

def createLinks(dry_run):
    logging.info("Creating symlinks in home directory...")
    for f in _files:
        link = os.path.join(_homedir, f)
        target = os.path.abspath(f)

        if not os.path.exists(target):
            raise FileNotFoundError(target)

        if os.path.islink(link):
            if os.path.realpath(target) == os.path.realpath(link):
                logging.info("%s already linked! Skipping...", link)
                continue
            raise Exception("{}: link exists but points to {}! Please fix!".format(link, os.path.realpath(link)))
        if os.path.exists(link):
            raise Exception("{}: file already exists! Please fix!".format(link))

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


def setupVim(rebuild_ycmd, libclang_path, dry_run):
    logging.info("Doing initial vim setup...")
    vimrc = os.path.join(_homedir, ".vimrc")
    bundledir = os.path.join(_homedir, ".vim", "bundle")

    if not os.path.exists(vimrc):
        raise FileNotFoundError(vimrc)

    if not os.path.isdir(bundledir):
        raise FileNotFoundError(bundledir)

    # Clone vundle repo
    vundledir = os.path.join(bundledir, "Vundle.vim")
    if not os.path.exists(vundledir):
        logging.info("Bootstrapping vundle...")
        runCmd("git clone {} {}".format(_vundle_url, vundledir), dry_run)

    # Tell vim to install packages
    runCmd("vim +PluginInstall +qall", dry_run)

    ycmd_path = os.path.join(_homedir,
            bundledir, 'YouCompleteMe/third_party/ycmd/cpp')

    # Possible clang libraries (linux, cygwin, etc..)
    target_libclangs = glob.glob(os.path.join(ycmd_path, '../libclang.*'))

    if not rebuild_ycmd and len(target_libclangs) > 0:
        logging.info("Found %s : Skipping ycmd build...", target_libclangs)
    else:
        logging.info("Building ycmd...")

        builddir="./ycm_build"
        rmTree(builddir, dry_run)
        mkdir(builddir, dry_run)
        cmd="cd {}; cmake -G 'Unix Makefiles' . {}".format(builddir, ycmd_path)
        if libclang_path is None:
            cmd+=" -DUSE_SYSTEM_LIBCLANG=ON"
        else:
            cmd+=" -DEXTERNAL_LIBCLANG_PATH=\"{}\"".format(libclang_path)
        runCmd(cmd, dry_run)
        cmd = "cd {}; cmake --build . --target ycm_core --config Release".format(builddir)
        runCmd(cmd, dry_run)




def main():
    parser = argparse.ArgumentParser("Home directory setup script")
    parser.add_argument('-n', '--dry-run', action='store_true', help="Run through script but don't actually run commands")
    parser.add_argument("--no-links", action='store_true', help="Don't create symlinks")
    parser.add_argument("--no-bashrc", action='store_true', help="Don't patch .bashrc")
    parser.add_argument("--no-vim", action='store_true', help="Don't do vim setup")
    parser.add_argument("--rebuild-ycmd", action='store_true', help='Always rebuild vim ycmd')
    parser.add_argument("--libclang-path", action='store', default=None, help='Path to custom built libclang.so')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    dry_run = args.dry_run
    do_links = not args.no_links
    do_bashrc = not args.no_bashrc
    do_vim = not args.no_vim
    rebuild_ycmd = args.rebuild_ycmd
    libclang_path = args.libclang_path

    logging.info("Changing directory to script dir...")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    genXresources(dry_run)

    if do_links:
        createLinks(dry_run)

    if do_bashrc:
        patchBashrc(dry_run)

    if do_vim:
        setupVim(rebuild_ycmd, libclang_path, dry_run)


if __name__ == "__main__":
    main()
