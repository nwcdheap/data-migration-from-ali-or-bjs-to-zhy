import boto3

import json

import logging


file = open('config.json','r',encoding='utf-8')
config = json.load(file)



aws_session=boto3.session.Session(aws_access_key_id=config['aws_access_key_id'],
                                  aws_secret_access_key=config['aws_secret_access_key'])


#client = aws_session.client('sqs')

sqs = aws_session.resource('sqs')

deadqueue = sqs.create_queue(QueueName='dead_queue',
                            Attributes={
                    'ReceiveMessageWaitTimeSeconds': '20',
                    'VisibilityTimeout': '1800'}
                            )
dead_queue_arn =deadqueue.attributes.get('QueueArn')

#print(deadqueue.url)
#print(deadqueue.attributes.get('QueueArn'))

for i in range(1, 6):
    queue_name = "bucket_migration_0"+ str(i)
    logging.info('Create queue {}'.format(queue_name))
    sqs.create_queue(QueueName=queue_name,
                    Attributes={
                        'ReceiveMessageWaitTimeSeconds': "20",
                        'VisibilityTimeout': "1800",
                        'RedrivePolicy': json.dumps({
                        'deadLetterTargetArn': dead_queue_arn,
                        'maxReceiveCount': '3'
                        })})




