#!/bin/sh
# URLごとにLambda関数を作るためのアップロード処理

now=`date "+%Y%m%d%H%M%S"`
crawling_target_url=$1

# copy
cd ./crawling/
config_file="/tmp/lambda.json.$now"
cp lambda.json $config_file

# replace function name
function_name=`echo "$crawling_target_url" | sed s%https://%%g | sed s%[¥/¥.]%_%g`
echo $function_name
sed -i.org -e "s%##CRAWLING_FUNCTION_NAME##%$function_name%g" $config_file

# upload
lambda-uploader --variables "{\"CRAWLING_TARGET_URL\": \"$crawling_target_url\", \"UPLOAD_S3_BUCKET\": \"$UPLOAD_S3_BUCKET\"}" --extra-file /usr/local/lib/python3.6/site-packages/ --config $config_file