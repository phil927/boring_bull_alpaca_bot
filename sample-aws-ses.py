# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Simple Notification
Service (Amazon SNS) to create notification topics, add subscribers, and publish
messages.
"""

import json
import logging
import time
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, sns_resource):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource = sns_resource


    def publish_text_message(self, phone_number, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.

        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
            logger.info("Published message to %s.", phone_number)
            print("Success")
        except ClientError:
            logger.exception("Couldn't publish message to %s.", phone_number)
            raise
        else:
            return message_id
    
if __name__ == "__main__":
    Sns = SnsWrapper(boto3.resource('sns', region_name='us-east-1'))
    print("Message ID: ", Sns.publish_text_message("+14047316031", "Hello from Phillip"))