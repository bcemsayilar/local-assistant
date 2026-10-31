#!/bin/bash
# deploy.sh : TikTok yayinci arka ucunu kurar (yoksa) ve Lambda kodunu gunceller. Tekrar calistirmak guvenli.
# Kullanim: ./deploy.sh [sandbox|prod]  (varsayilan sandbox). Anahtarlar kasadan (aws ve tiktok servisleri), ekrana yazilmaz.
set -e
cd "$(dirname "$0")" || { echo "CD BASARISIZ"; exit 1; }
MODE=${1:-sandbox}
set -a; source ~/.config/parallax/secrets/aws.env; source ~/.config/parallax/secrets/tiktok.env; set +a
if [ "$MODE" = sandbox ]; then CK=$TIKTOK_SANDBOX_CLIENT_KEY; CS=$TIKTOK_SANDBOX_CLIENT_SECRET; else CK=$TIKTOK_CLIENT_KEY; CS=$TIKTOK_CLIENT_SECRET; fi
export AWS_REGION=eu-central-1 AWS_DEFAULT_REGION=eu-central-1 AWS_PAGER=""
ACC=573199225040; FN=tiktok-publisher; ROLE=tiktok-publisher-lambda; TBL=tiktok-publisher
SITE=https://parallaxtechnologies.net
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

if ! aws dynamodb describe-table --table-name $TBL >/dev/null 2>&1; then
  aws dynamodb create-table --table-name $TBL --billing-mode PAY_PER_REQUEST \
    --attribute-definitions AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S \
    --key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE >/dev/null
  aws dynamodb wait table-exists --table-name $TBL
  aws dynamodb update-time-to-live --table-name $TBL --time-to-live-specification Enabled=true,AttributeName=ttl >/dev/null
  echo "tablo kuruldu"
fi

if ! aws iam get-role --role-name $ROLE >/dev/null 2>&1; then
  aws iam create-role --role-name $ROLE --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null
  aws iam attach-role-policy --role-name $ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  echo "rol kuruldu"; sleep 10
fi
cat > "$TMP/pol.json" <<P
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["dynamodb:GetItem","dynamodb:PutItem","dynamodb:DeleteItem"],"Resource":"arn:aws:dynamodb:eu-central-1:$ACC:table/$TBL"}]}
P
aws iam put-role-policy --role-name $ROLE --policy-name tiktok-publisher-data --policy-document "file://$TMP/pol.json"

python3 -I - "$TMP/env.json" "$CK" "$CS" "$SITE" <<'P'
import json, sys
json.dump({"Variables": {"TABLE": "tiktok-publisher", "TIKTOK_CLIENT_KEY": sys.argv[2], "TIKTOK_CLIENT_SECRET": sys.argv[3],
  "REDIRECT_URI": sys.argv[4] + "/publisher/callback", "ALLOWED_ORIGIN": sys.argv[4]}}, open(sys.argv[1], "w"))
P
zip -q -j "$TMP/fn.zip" handler.py
if ! aws lambda get-function --function-name $FN >/dev/null 2>&1; then
  aws lambda create-function --function-name $FN --runtime python3.12 --handler handler.handler --timeout 30 --memory-size 256 \
    --role arn:aws:iam::$ACC:role/$ROLE --zip-file "fileb://$TMP/fn.zip" --environment "file://$TMP/env.json" >/dev/null
  aws lambda wait function-active --function-name $FN
  aws lambda create-function-url-config --function-name $FN --auth-type NONE \
    --cors "AllowOrigins=$SITE,AllowMethods=POST,AllowHeaders=content-type,MaxAge=3600" >/dev/null
  aws lambda add-permission --function-name $FN --statement-id url-public --action lambda:InvokeFunctionUrl \
    --principal "*" --function-url-auth-type NONE >/dev/null
  aws lambda add-permission --function-name $FN --statement-id url-invoke --action lambda:InvokeFunction \
    --principal "*" --invoked-via-function-url >/dev/null
  echo "fonksiyon kuruldu"
else
  aws lambda update-function-code --function-name $FN --zip-file "fileb://$TMP/fn.zip" >/dev/null
  aws lambda wait function-updated --function-name $FN
  aws lambda update-function-configuration --function-name $FN --environment "file://$TMP/env.json" >/dev/null
  aws lambda wait function-updated --function-name $FN
  echo "kod guncellendi ($MODE)"
fi
aws lambda get-function-url-config --function-name $FN --query FunctionUrl --output text
