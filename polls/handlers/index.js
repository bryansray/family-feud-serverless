"use strict";

const AWS = require("aws-sdk");

AWS.config.update({ region: "us-west-2" });

const dynamo = new AWS.DynamoDB.DocumentClient();

module.exports.handler = async (event) => {
  console.log(`Listing available polls ...`);

  const params = {
    TableName: "polls",
    ProjectionExpression: "id, #txt",
    ExpressionAttributeNames: { "#txt": "text" }
  };
  const result = await dynamo.scan(params).promise();

  return {
    statusCode: 200,
    body: JSON.stringify(result.Items),
  };
};
