#!/bin/bash

cd /home/griffin/repos/${1}
make > compile_log.txt

find . -type f -executable -print
