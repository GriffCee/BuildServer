#!/bin/bash

cp -R /home/griffin/repos/${1} /home/griffin/repos/build_artifacts

cd /home/griffin/repos/build_artifacts

git add --all && git commit --all -m "One must imagine Sisyphus happy"

cd ..
