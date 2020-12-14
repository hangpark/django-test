#!/usr/bin/env bash
WORKDIR=$(cd `dirname ${BASH_SOURCE[0]}`; pwd)

# --------

echo 'Install Django dependencies'
cd "$WORKDIR/django/tests"
pip install -e ..
pip install -r ./requirements/py3.txt

cd "$WORKDIR"

# --------

echo 'Generate possible config input values'
cat django/django/conf/global_settings.py \
    | grep -E '= (True|False)$' \
    | sed -E 's/ = (True|False)$/: True False/g' \
    > input.txt

# --------

echo 'Generate configurations'
python ./generate.py

# --------

echo 'Export environment variables for Django tests'
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export PYTHONPATH="$WORKDIR/django/tests/cit_configs"

# --------

echo 'Run test for each configuration'
cd "$WORKDIR/django/tests"

CONFIGS=$(ls './cit_configs' \
    | grep -E '\.py$' \
    | grep -v '__init__.py' \
    | sed 's/\//./g' \
    | sed 's/\.py$//g')

for CONFIG in $CONFIGS; do
    python ./runtests.py --parallel=1 --settings="$CONFIG"
done

