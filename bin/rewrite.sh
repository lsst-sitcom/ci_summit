# need to manually copy and update the python path
echo "#!$(command -v python)" > bin/ci_summit_run.py
cat bin.src/ci_summit_run.py >> bin/ci_summit_run.py

# verify that the file is executable
chmod ug+x bin/ci_summit_run.py

