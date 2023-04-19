#!/bin/bash

echo "Deploying..."
printf "Current version: %s\n" "$(grep "version" pyproject.toml)"
echo "Are you sure you want to upload? [y/N]"
read answer
case ${answer:0:1} in
    y|Y )
        echo "Proceeding..."
    ;;
    * )
        echo "Aborting"
        exit 1
    ;;
esac

echo "Building..."
rm -r dist/*.whl dist/*.tar.gz 2> /dev/null
python3 -m build

echo "Uploading..."
TWINE_USERNAME=__token__ TWINE_PASSWORD="$(grep "pypitoken" .env | cut -d= -f2-)" python3 -m twine upload --repository pypi dist/*
