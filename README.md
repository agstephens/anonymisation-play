# Setting up and running Presidio on Docker Desktop on Windows

## Run Docker Desktop and start PowerShell

Run Docker Desktop as ADMIN user (otherwise you won't see the relevant Docker images).

Start PowerShell as normal user.

## Create a container based on "continuum/miniconda3"

# Set up the container at the start
docker pull continuumio/miniconda3

# If not built yet, run with...
docker run -i -t  -p 8181:8181 continuumio/miniconda3 /bin/bash

# If already built (and renamed to "ai_play"), then run and login with:
docker run -i -t  -p 8181:8181 ai_play /bin/bash

## Setting up a non-root account

mkdir /home/ag
useradd -d /home/ag ag
chown ag.users /home/ag

# Login as: ag
su --shell /bin/bash - ag

## Setting up the user account

# Login as: ag
su --shell /bin/bash - ag

# Now, as user
cd ~

# Create the .profile file
echo "source /opt/conda/etc/profile.d/conda.sh" > .profile
echo "conda activate base" >> .profile

echo "syntax off" > .vimrc
echo "set paste" >> .vimrc

mkdir -p ~/venvs
exit

# Login again and the conda base env is sourced
su --shell /bin/bash - ag

## Install virtualenv with required packages

python -m venv ~/venvs/venv-presidio
source ~/venvs/venv-presidio/bin/activate
export PS1="$ "

Install, with:

pip install presidio_analyzer presidio_anonymizer bs4

See: https://microsoft.github.io/presidio/installation/#__tabbed_1_1

# Install the main language model content (very large file!) - required by presidio
# $ du -sh  ~/venvs/venv-presidio/lib/python3.12/site-packages/en_core_web_lg
# 620M    /home/ag/venvs/venv-presidio/lib/python3.12/site-packages/en_core_web_lg
python -m spacy download en_core_web_lg

## Put in github and clone

git clone https://github.com/agstephens/anonymisation-play

## Test presidio code

cd ~/anonymisation-play/
. ./setup-env.sh

python test1.py
python test2.py
python test3.py

And my own version with amendments, and ceda query:

python test4.py


