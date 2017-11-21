import os

flags = [
    '-x',
    'c++',
    '-Wall',
    '-Wextra',
    '-std=c++17',
]

def FlagsForFile( filename, **kwargs ):
  return {

    'flags': flags,

    'do_cache': True

  }
