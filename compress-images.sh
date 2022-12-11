for i in *.jpg
do
    echo "output: $i"
    convert -strip -interlace Plane -gaussian-blur 0.05 -quality 50% $i ./res/$i
done
