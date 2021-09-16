npm init
npm install --save serverless-python-requirements

docker build test-alpaca .
docker run -it --rm -p 9000:8080 test-alpaca:latest handler.lambda_handler
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"test": "value"}'