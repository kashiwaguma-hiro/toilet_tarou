# Toilet tarou

It's a toilet analyze man.

## Development

### set aws env.

```
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXX
export AWS_DEFAULT_REGION=ap-northeast-1
export LAMBDA_TASK_ROOT=.
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
root@7d2f0fdc314d:/usr/src/app# python-lambda-local -f lambda_handler -t 300 lambda_function.py event.json
```

## lambda deploy

```
$ docker exec -it toilettarou_python_1 bash
root@7d2f0fdc314d:/usr/src/app# lambda-uploader --variables "{\"CRAWLING_TARGET_URL\": \"$CRAWLING_TARGET_URL\"}" --extra-file /usr/local/lib/python3.6/site-packages/
Î» Building Package
Î» Uploading Package
Î» Fin
```


# TODO

- [] Dockerの実行をナウい感じに治す
- [] 実行環境をTerraform化する
- [] URLの渡し方を考える