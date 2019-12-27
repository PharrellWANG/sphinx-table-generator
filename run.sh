#!/usr/bin/env bash
PY_PATH_STR="$(which python)"

if [[ ${PY_PATH_STR} == *"/venv/"* ]]; then
    echo -e "\033[1;31m [INFO] yes, venv activated already \033[0m"
else
    echo -e "\033[1;31m [INFO] no, activate venv now \033[0m"
    source ./venv/bin/activate
    echo -e "\033[1;31m [INFO] venv activated \033[0m"
fi

python main.py
echo -e "\033[1;31m [INFO] Table generated and copied to clipboard already. \033[0m"
echo -e "\033[1;31m [INFO] End. \033[0m"