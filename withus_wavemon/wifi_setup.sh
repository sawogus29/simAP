DIR=../myvenv/lib/python3.6/site-packages/wavemon/

make
mkdir $DIR
mv ./wavemon.py $DIR
mv ./_wavemon.so $DIR

