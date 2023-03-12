mkdir old
for i in *.jpg
do
    echo "output: $i"
    mv $i old/$i 
    convert -strip -interlace Plane -gaussian-blur 0.05 -quality 50% old/$i $i
done
