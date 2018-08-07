# monochrome
for file in *.jpg
do
    if test -f $file
    then
        echo $file
        magic $file -monochrome ./mono/$file
    fi
done