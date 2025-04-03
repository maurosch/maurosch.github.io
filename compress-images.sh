mkdir $1/old
for i in $1/*.jpg
do
    echo "output: $i"
    fileName=$(basename $i)
    echo "output: $fileName"
    mv $i $1/old/$fileName
    convert -strip -interlace Plane -gaussian-blur 0.05 -quality 50% $1/old/$fileName $i
done
