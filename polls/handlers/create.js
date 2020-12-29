"use strict";

const AWS = require("aws-sdk");

AWS.config.update({ region: "us-west-2" });

const dynamo = new AWS.DynamoDB.DocumentClient();

function makeid(length) {
  var result = "";
  var characters = "abcdefghijklmnopqrstuvwxyz0123456789";
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

module.exports.handler = async (event) => {
  console.log("Creating new poll ...");

  const item = JSON.parse(event.body);

  item.id = makeid(10);

  const result = await dynamo
    .put({
      TableName: "polls",
      Item: item,
    })
    .promise();

  return {
    statusCode: 201,
    body: JSON.stringify(
      {
        result: item,
      },
      null,
      2
    ),
  };
};
