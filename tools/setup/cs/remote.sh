#!/bin/bash

echo 'Starting server...'

. $CONDA_DIR/etc/profile.d/conda.sh
conda activate mlook
python -m server start > server/log.txt 2>&1 &
 
echo 'Started server, starting client...'

cd client
npm start > log.txt 2>&1 &
cd -

echo 'Started client, try opening http://localhost:3000 in browser'
