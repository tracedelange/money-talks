#!/bin/bash

git add .
git commit -m "${date}"

if [ -n "$(git status - porcelain)" ];
then
 echo "Were all set here."
else
 git status
 echo "Pushing data to server"
 git push
fi
