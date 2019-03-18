echo "hello shell!"
ls | grep .sh
a=10
b=20
if [ $a -eq $b ]
then
    echo $a is equal to $b
elif [ $a -lt $b ]
then
    echo $a is less than $b
else
    echo $a is larger than $b
fi
     
    
