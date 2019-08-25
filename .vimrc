set nocompatible
set bs=2

filetype off

" Begin vim-plugin Plugins List
call plug#begin('~/.vim/plugged')
Plug 'tpope/vim-fugitive'
Plug 'vim-syntastic/syntastic'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
"Plug 'Valloric/YouCompleteMe'
"Plug 'rdnetto/YCM-Generator'
Plug 'nvie/vim-flake8'
call plug#end()
" End vim-plug Plugins List

"-------------------------------
" Theme setup
"-------------------------------
set background=dark
" We assume terminal is setup correctly for solarized
colorscheme default
let g:solarized_termcolors=256
if has("gui_running")
	set background=light
	colorscheme solarized
endif

"-------------------------------
"Syntax Highlighting options
"-------------------------------
syntax on
"Highlight whitespace errors
highlight link WhiteSpaceError ErrorMsg
"Flag trailing whitespace as an error
au Syntax * syn match WhiteSpaceError /\(\zs\%#\|\s\)\+$/ display
"Flag mixed leading space/tabs as an error
au Syntax * syn match WhiteSpaceError /^ \+\ze\t/ display

filetype plugin indent on

set incsearch
set hlsearch
set cursorline
set showcmd
set ruler
set number
set relativenumber

set showmatch
"Allow maching angle brackets
set matchpairs+=<:>
set modeline

set wildmode=longest,list,full
set wildmenu

"-------------------------------
"Folding config
"-------------------------------
set nofoldenable
"set foldenable "Enable folding
"set foldlevelstart=9999 "Never fold by default
"set foldnestmax=10 "Maximum 10 nested folds
"set foldmethod=indent "Default fold by indentation

"-------------------------------
"Netrw Configs
"-------------------------------
let g:netrw_liststyle=3 "Preferred listing style
let g:netrw_banner=0 "Don't show useless banner

"-------------------------------
"Python Config
"-------------------------------
let python_highlight_all=1

"-------------------------------
"YCM Configs
"-------------------------------
"Don't ask about extra conf file
let g:ycm_confirm_extra_conf=0
let g:ycm_autoclose_preview_window_after_completion=1
let g:ycm_autoclose_preview_window_after_insertion=1
"Enable location list so we can rapidly jump through errors
let g:ycm_always_populate_location_list=1
"Always use python3
"let g:ycm_python_binary_path='python3'

nnoremap <C-x> :YcmCompleter GoTo<CR>
nnoremap <F6> :YcmCompleter GetType<CR>
"Location List next/prev
nnoremap <C-n> :lnext<CR>
nnoremap <C-N> :lprevious<CR>

"-------------------------------
"Syntastic Configs
"-------------------------------
let g:syntastic_python_checkers=['python']
"Always use python3
"let g:syntastic_python_python_exec='python3'

"-------------------------------
"Vim airline configuration
"-------------------------------
"Enable powerline fancy glyphs
let g:airline_powerline_fonts=1
"Always show the statusbar
set laststatus=2
"Don't show mode below statusline since airline already provides it
set noshowmode

