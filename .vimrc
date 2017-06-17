set nocompatible
set bs=2

filetype off

" set runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

" Begin Vundle Plugins List
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'vim-syntastic/syntastic'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'Valloric/YouCompleteMe'
call vundle#end()
" End Vundle Plugins List

filetype plugin indent on

syntax on
set hlsearch


"Vim airline configuration
let g:airline_powerline_fonts=1
set laststatus=2

