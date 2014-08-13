#!/bin/bash

OD_DIR=/work/asr/demos/morfessor-demo
rm -Rf build
mkdir build && cd build
CUR_VERSION=$(cat $OD_DIR/morfessor-demo-data-version)
NEXT_VERSION=$(echo $CUR_VERSION | awk -F. '{$NF+=1; OFS="."; print $0}') 
cmake -DCPACK_PACKAGE_VERSION=$NEXT_VERSION -DModels_DIR=$OD_DIR/models/ ..
echo $NEXT_VERSION > $OD_DIR/morfessor-demo-data-version
make package
cp morfessor-demo-data-${NEXT_VERSION}-Linux.deb $OD_DIR
echo "New package can be found here: $OD_DIR/morfessor-demo-data-${NEXT_VERSION}-Linux.deb"

