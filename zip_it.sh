#!/bin/bash

cd build_artifacts
cp -R ${1} ../requested_files

cd ../requested_files

zip -r ${1}.zip ${1}/

rm -r ${1}

cd ..
