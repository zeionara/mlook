#!/bin/bash

echo 'Starting server...'

conda activate mlook
python -m server start > server/log.txt 2>&1 &

echo 'Started server, starting client...'

cd client
npm run serve > log.txt 2>&1 &
cd -

echo 'Started client, try opening http://localhost:3000 in browser'
