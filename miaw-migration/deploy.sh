  
#!/bin/bash

OPTIONS=ibdr
LONGOPTS=install,build,deploy,remove

! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")

if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
  exit 2
fi

i=0 p=0 b=0 d=0

CF_FILE="/tmp/cf_file.txt"
DEPLOYMENTS_BUCKET="cualquier-bucket-123-mascotaws"

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
  pip install -t build/ -r requirements.txt
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
  --parameter-overrides Project=cf_lab2  \
  --stack-name "miaw-stack-bucket-excel" \
  --capabilities CAPABILITY_NAMED_IAM
fi

if [[ $r -eq 1 ]]; then
    echo remove
fi