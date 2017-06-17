#!/usr/bin/env bash
set -x

FILES="
.gitconfig
.tmux.conf
.Xdefaults
.vimrc
"

for f in $FILES; do
	if ! [ -f "$f" ]; then
		echo "$f: Does not exist! Bug in $0?"
		exit 1
	fi
	if [ -L ~/"$f" ]; then
		echo ~/"$f: Already linked! Skipping..."
		continue
	fi
	if [ -f ~/"$f" ]; then
		echo ~/"$f: File already exists! Please fix..."
		exit 1
	fi
	target=`realpath "$f"`
	ln -s "$target" ~/"$f"
done
