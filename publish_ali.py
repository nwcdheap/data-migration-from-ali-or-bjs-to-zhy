import oss2
import sys,os

#from itertools import islice

import boto3

import json

import logging

import random


file = open('config.json','r',encoding='utf-8')
config = json.load(file)



aws_session=boto3.session.Session(aws_access_key_id=config['aws_access_key_id'],
                                  aws_secret_access_key=config['aws_secret_access_key'])


#client = aws_session.client('sqs')

sqs = aws_session.resource('sqs')

auth =oss2.Auth('','')
firstbucket=oss2.Bucket(auth,'http://oss-cn-hangzhou.aliyuncs.com','seimutig')


msg=[]

for obj in oss2.ObjectIterator(firstbucket):
    c = obj.key
    if c[-1:] == '/':
        #os.mkdir("/Volumes/4T/mnt/"+ c)
        pass

    else:
        msg.append(c)
        # firstbucket.get_object_to_file(c,"/mnt/"+c)


#print(msg[:])

for i in range(0,len(msg),3):
    message=msg[i:i+3]
    print(message)
    Message={
        "SOURCE_BUCKET": config['source_bucket_ali'],
        "TARGET_BUCKET": config['target_bucket_aws'],
        "KEYS": message }

    #queue = sqs.get_queue_by_name(QueueName="bucket_migration_0" + str(4))
    queue=sqs.get_queue_by_name(QueueName="bucket_migration_0"+ str(random.randint(1, 5)))
    response = queue.send_message(MessageBody=json.dumps(Message))
    print(response.get('MessageId'))
