#!/bin/bash

OPTIONS=ibdr
LONGOPTS=install,build,deploy,remove

! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")

if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
  exit 2
fi

i=0 p=0 b=0 d=0

CF_FILE="/tmp/cf_file.txt"
DEPLOYMENTS_BUCKET="conversiondeimagen"

case "$1" in
  -i|--install)
    i=1
    shift
    ;;
  -r|--remove)
    r=1
    shift
    ;;
  -b|--build)
    b=1
    shift
    ;;
  -d|--deploy)
    d=1
    shift
    ;;
  --)
    shift
    break
    ;;
  *)
    ;;
esac

if [[ $i -eq 1 ]]; then
  mkdir -p build
  cp -r src/* build/
pip3 install --target package -r src/requirements.txt
cd package
zip -r9 ../function1.zip .
cd ../src
zip -g ../function1.zip lambda1.py
cd ..  
fi

if [[ $b -eq 1 ]]; then
aws cloudformation package \
--template-file template.yaml \
--s3-bucket $DEPLOYMENTS_BUCKET \
--output-template-file $CF_FILE
fi

if [[ $d -eq 1 ]]; then
  
aws cloudformation deploy \
--no-fail-on-empty-changeset \
--template-file $CF_FILE \
--parameter-overrides Project=CloudFormationLab2 \
--stack-name "convert-image-stack5" \
--capabilities CAPABILITY_NAMED_IAM
aws lambda update-function-code --function-name convert-image-lambda --zip-file fileb://function1.zip
fi
