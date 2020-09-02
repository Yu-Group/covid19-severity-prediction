cd ../modeling
pdoc --html . --output-dir ../docs
cp -r ../docs/modeling/* ../docs/
rm -rf ../docs/modeling
cd ../docs
python style_docs.py
