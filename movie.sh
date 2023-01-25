# bash script to run app.py with args from cmdline and set alias of app.py to movie

# init conda shell workaround
eval "$($(which conda) 'shell.zsh' 'hook')"
echo "Inititalizing conda environment....."
# activate conda env
conda activate moviecli
conda info | egrep "conda version|active environment"
echo "\n"

# run app.py with args from cmdline
# check if args are passed
if [ $# -eq 0 ]
  then
    echo "\n***No arguments supplied***\n"
    python "app.py" -h
  else
    python "app.py" $@
fi
