import boto3

import json

import logging

import random

file = open('config.json','r',encoding='utf-8')
config = json.load(file)



aws_session=boto3.session.Session(aws_access_key_id=config['aws_access_key_id'],
                                  aws_secret_access_key=config['aws_secret_access_key'])


sqs = aws_session.resource('sqs')

client = aws_session.client('s3')


def list_objects( max_keys=10, ctoken=None):
    p = {
        'Bucket': config['source_bucket_aws'],
        'MaxKeys': max_keys,
    }

    if ctoken:
        p['ContinuationToken'] = ctoken
    return client.list_objects_v2(**p)

def list_objects_all():
    ctoken = None
    has_next = True
    while has_next:
        res = list_objects(ctoken=ctoken)
        if 'IsTruncated' in res and res['IsTruncated']:
            ctoken = res['NextContinuationToken']
        else:
            has_next = False
        yield res['Contents']
    return





def message_gen():

    for batch in list_objects_all():
        msg = []
        for content in batch:
            msg.append(content['Key'])

        yield msg





#mia=list_objects_all()

#for n in mia:
 #  print(n)

mia2=message_gen()

for n in mia2:
    Message = {
        "SOURCE_BUCKET": config['source_bucket_ali'],
        "TARGET_BUCKET": config['target_bucket_aws'],
        "KEYS": n}
    #queue=sqs.get_queue_by_name(QueueName="bucket_migration_0"+ str(random.randint(1, 5)))
    queue = sqs.get_queue_by_name(QueueName="bucket_migration_0" + str(4))
    response = queue.send_message(MessageBody=json.dumps(Message))
    print(response.get('MessageId'))





#print(next(mia))

#print(next(mia))






