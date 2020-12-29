"use strict";

const AWS = require("aws-sdk");

AWS.config.update({ region: "us-west-2" });

const dynamo = new AWS.DynamoDB.DocumentClient();

module.exports.handler = async (event) => {
  const { pollId } = event.pathParameters;

  console.log(`Finding the specified poll: '${pollId}'`);

  const params = {
    TableName: "polls",
    Key: {
      id: pollId,
    },
  };
  const result = await dynamo.get(params).promise();
  const poll = result.Item;

  return {
    statusCode: 200,
    body: JSON.stringify(poll),
  };
};
