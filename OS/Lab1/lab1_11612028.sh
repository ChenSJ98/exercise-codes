#!/bin/sh

# This script displays all the subdirectory and files under the given directory in
# a BFS fashion and put the result in the designated location
#
# This script deals with spaces in file/directory names by switching the internal
# field separator (IFS)

#check number of arguments
if [ "$#" != 2 ]
then
echo 'Please provide exactly 2 arguments'
exit 1
fi

fileCount=0
dirCount=0

#use an array to implement a queue, see https://blog.csdn.net/zhuying_linux/article/details/6779211
dirQueue=($1/)
dirNameQueue=($1)

#backup original IFS
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
# create or empty the target file
echo -n > $2
# BFS and print  directories and files
while [ ${#dirQueue[@]} -gt 0 ]
do
    dirName=${dirNameQueue[0]}
    curDir=${dirQueue[0]}
    echo >> $2 [$dirName]
    for file in $(ls $curDir)
    do
        if [ -d $curDir$file ]
        then
            echo >> $2 $curDir$file
            dirCount=`expr $dirCount + 1`
            dirQueue=(${dirQueue[@]} $curDir$file/) # queue.push()
            dirNameQueue=(${dirNameQueue[@]} $file) # queue.push()
        else
            echo >> $2 $curDir$file
            fileCount=`expr $fileCount + 1`
        fi
    done
    echo >> $2
    dirNameQueue=(${dirNameQueue[@]:1:$((${#dirNameQueue[@]}-1))}) # queue.pop()
    dirQueue=(${dirQueue[@]:1:$((${#dirQueue[@]}-1))}) # queue.pop()
done

#echo >> $2 put result to "$2"
echo >> $2 [Directories Count]:$dirCount
echo >> $2 [Files Count]:$fileCount
#restore IFS
IFS=$SAVEIFS
exit 0
