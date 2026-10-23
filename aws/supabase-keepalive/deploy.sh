#!/bin/bash
# deploy.sh : supabase-keepalive Lambda'sini kurar ya da gunceller (tekrar calistirmak guvenli). Yonetici kimligi vidberry/.env'den (cli-access.md).
set -euo pipefail
set -a; source ~/Mac-Projects/vidberry/.env; set +a
export AWS_REGION=eu-central-1 AWS_DEFAULT_REGION=eu-central-1
cd "$(dirname "$0")"
ACC=573199225040; FN=supabase-keepalive; ROLE=supabase-keepalive-lambda; RULE=supabase-keepalive-12h
TMP=$(mktemp -d)
if ! aws iam get-role --role-name $ROLE >/dev/null 2>&1; then
  echo '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' > $TMP/trust.json
  aws iam create-role --role-name $ROLE --assume-role-policy-document file://$TMP/trust.json --description "Supabase free projelerini aktif tutan Lambda" >/dev/null
  aws iam attach-role-policy --role-name $ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  sleep 10
fi
python3 -c "import json;print(json.dumps({'Variables':{'PROJECTS':json.dumps(json.load(open('projects.json')))}}))" > $TMP/env.json
(cd . && zip -q $TMP/fn.zip handler.py)
if aws lambda get-function --function-name $FN >/dev/null 2>&1; then
  aws lambda update-function-code --function-name $FN --zip-file fileb://$TMP/fn.zip >/dev/null
  aws lambda wait function-updated --function-name $FN
  aws lambda update-function-configuration --function-name $FN --environment file://$TMP/env.json >/dev/null
else
  aws lambda create-function --function-name $FN --runtime python3.12 --handler handler.handler --role arn:aws:iam::$ACC:role/$ROLE \
    --zip-file fileb://$TMP/fn.zip --timeout 60 --memory-size 128 --environment file://$TMP/env.json >/dev/null
fi
aws lambda wait function-updated --function-name $FN 2>/dev/null || aws lambda wait function-active --function-name $FN
aws logs put-retention-policy --log-group-name /aws/lambda/$FN --retention-in-days 30 2>/dev/null || true
aws events put-rule --name $RULE --schedule-expression "rate(12 hours)" >/dev/null
aws lambda add-permission --function-name $FN --statement-id events-12h --action lambda:InvokeFunction \
  --principal events.amazonaws.com --source-arn arn:aws:events:$AWS_REGION:$ACC:rule/$RULE >/dev/null 2>&1 || true
aws events put-targets --rule $RULE --targets "Id=1,Arn=arn:aws:lambda:$AWS_REGION:$ACC:function:$FN" >/dev/null
TOPIC=$(aws sns create-topic --name supabase-keepalive-hata --query TopicArn --output text)
aws sns list-subscriptions-by-topic --topic-arn $TOPIC --query "Subscriptions[].Endpoint" --output text | grep -q contact@parallaxtechnologies.net || \
  aws sns subscribe --topic-arn $TOPIC --protocol email --notification-endpoint contact@parallaxtechnologies.net >/dev/null
aws cloudwatch put-metric-alarm --alarm-name supabase-keepalive-hata --namespace AWS/Lambda --metric-name Errors \
  --dimensions Name=FunctionName,Value=$FN --statistic Sum --period 43200 --evaluation-periods 1 --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions $TOPIC --ok-actions $TOPIC
aws lambda invoke --function-name $FN $TMP/out.json >/dev/null && cat $TMP/out.json; echo
rm -rf $TMP
