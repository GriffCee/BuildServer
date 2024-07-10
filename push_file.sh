#!/bin/bash

#NOTE: dependent on unzip package (run sudo apt-get install unzip)

newDirName=$(date '+%Y-%m-%d-%H%M%S')
echo ${newDirName}

mkdir raw_data_repo/${newDirName}
cp $1 raw_data_repo/${newDirName}

cd raw_data_repo/${newDirName}

bsdtar --strip-components=1 -xvf ${1}
rm -f ${1}
rm -f -r .git

git status

git add --all 

git commit --all -m "One must imagine Sisyphus happy"

commitTag=`git rev-parse HEAD`
uploadTime=`date`

cd ../..

rm ${1}

mysql --user=root --password=root build_stats_db << EOF
INSERT INTO build_stats (commit_tag, upload_time, artifacts_dir_name) VALUES ("${commitTag}", NOW(), "$newDirName");
EOF
