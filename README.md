# Family Feud - Serverless

This is a simple serverless web api that runs on the AWS ecosystem. It leverages lambda functions, DynamoDB, and AWS API Gateway.

## Architecture

API Client -> API Gateway -> Lambda -> DynamoDB

(Convert this to a fancy diagram)

## Documentation

## Deployment

[Serverless](https://www.serverless.com/framework/docs/providers/aws/guide/installation/)

```bash
npm install -g serverless
serverless deploy
```

## Cleanup

To remove all the AWS resources for the application.

```bash
serverless remove
```