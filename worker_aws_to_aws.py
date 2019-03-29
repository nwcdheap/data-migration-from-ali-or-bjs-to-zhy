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




#sqs = aws_session.resource('sqs')

client = aws_session.client('sqs')

#queue=sqs.get_queue_by_name(QueueName="bucket_migration_0"+ str(random.randint(1, 5)))

auth =oss2.Auth('','')
bucket=oss2.Bucket(auth,'http://oss-cn-hangzhou.aliyuncs.com','seimutig')

s3 = boto3.resource('s3')
#s3.Bucket(config['target_bucket_aws']).upload_file('/tmp/hello.txt', 'hello.txt')

while True:
    #random_url= 'https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0' + str(random.randint(1, 5))
    random_url = 'https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0' + str(4)
    response = client.receive_message(QueueUrl = random_url)
    print(response)



    if 'Messages' in response:
        body=response['Messages'][0]['Body']
        handle=response['Messages'][0]['ReceiptHandle']
        list=json.loads(body)
        print(type(list))
        print(list)
        for key in list["KEYS"]:
            copy_source = {
                'Bucket': config['source_bucket_aws'],
                'Key': key
            }
            bucket = s3.Bucket(config['target_bucket_aws'])
            bucket.copy(copy_source, key)
        response=client.delete_message(
            QueueUrl=random_url, ReceiptHandle=handle
        )


    else:
        logging.info('no message')
