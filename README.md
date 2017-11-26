# Toilet tarou

It's a toilet analyze man.

## Development

### set aws env.

```
export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET ACCESS KEY>
export AWS_DEFAULT_REGION=ap-northeast-1
export LAMBDA_TASK_ROOT=../
export CRAWLING_TARGET_URL=<CRAWLING_TARGET>
export UPLOAD_S3_BUCKET=toilet-man
```

### development env build and start.

```
$ docker-compose build
$ docker-compose up -d
```

### coding on anything editor.

### lambda test (on development env)

```
$ docker exec -it toilettarou_python_1 bash
root@7d2f0fdc314d:/usr/src/app# cd LAMBDA_FUNCTION_NAME
root@7d2f0fdc314d:/usr/src/app/LAMBDA_FUNCTION_NAME# python-lambda-local -f lambda_handler -t 300 lambda_function.py event.json
```

## crawling lambda deploy

```
$ docker exec -it toilettarou_python_1 bash
root@7d2f0fdc314d:/usr/src/app# sh lambda-upload-crawler.sh <crawling url>
Î» Building Package
Î» Uploading Package
Î» Fin
```
