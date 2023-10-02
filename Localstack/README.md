# Localstack - Develop AWS locally

Put the script for creating resource in [init-aws.sh](./init-aws.sh)

Check files in bucket:
`awslocal s3 ls s3://my-bucket  --recursive`

Check info about about the lambda function:
`awslocal lambda get-function --function-name <lambda-function-name> --region us-west-2`

Invoke lambda function:
```
awslocal lambda invoke --function-name <lambda-function-name> \ 
--payload `{"key":"value"}` output.txt \
--region us-west-2
```

Handler naming:
Let us say you upload zip named `lambda_zip.zip`, consisting Python script `lambda_func.py`.  
The function inside being called named `lambda_handler()`.

Then the handler should be called `lambda_func.lambda_handler`

ref:
https://erik-ekberg.medium.com/how-to-test-aws-lambda-locally-6f07bd36abd9  
https://stackoverflow.com/questions/48266106/missing-handler-error-in-aws-lambda

---
Draft

```
awslocal lambda invoke --function-name lambda2 \
 --payload '{"""first_name""": """Mei""", """last_name""": """Zhou""" }' output2.txt \
 --region us-west-2
```

```
awslocal lambda invoke --function-name lambda3 \
 --payload '{"first_name": "Mei", "last_name": "Zhou"}' output2.txt \
 --region us-west-2
```


```
awslocal lambda get-function --function-name lambda3 \
--region us-west-2
```

搞明白了Lambda:
- GUI版本，填写函数名,handler名，ARN信息，上传zip包
- invoke(调用) 像API call那样直接调用
