set -e

mkdir package

poetry export --without-hashes --output=package/requirements.txt
pip install -r package/requirements.txt -t package
rm package/requirements.txt

cp -r service package/
cp lambda_function.py package/
cp logging.conf package/
cd package
zip -9 -r ../package.zip .
cd ..
rm -r package

echo "Updating lambda code..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://package.zip

rm package.zip
