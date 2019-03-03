#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import oss2
import sys,os,io

#from itertools import islice

import boto3

import json

import logging

import random


import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print(sys.stdout.encoding)

#def setup_io():
 #   sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
  #  sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

#setup_io()


file = open('config.json','r',encoding='utf-8')
config = json.load(file)



aws_session=boto3.session.Session(aws_access_key_id=config['aws_access_key_id'],
                                  aws_secret_access_key=config['aws_secret_access_key'],region_name='cn-northwest-1')




#sqs = aws_session.resource('sqs')

client = aws_session.client('sqs')

#queue=sqs.get_queue_by_name(QueueName="bucket_migration_0"+ str(random.randint(1, 5)))

auth =oss2.Auth('','')
bucket=oss2.Bucket(auth,'http://oss-cn-hangzhou.aliyuncs.com','seimutig')

s3 = aws_session.resource('s3')
#s3.Bucket(config['target_bucket_aws']).upload_file('/tmp/hello.txt', 'hello.txt')

for obj in oss2.ObjectIterator(bucket):
    c = obj.key
    if c[-1:] == '/':
        os.mkdir("/opt/" + c)

    else:
        pass



while True:
    # random_url= 'https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0' + str(random.randint(1, 5))
    random_url = 'https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0' + str(4)
    response = client.receive_message(QueueUrl=random_url)
    #print(response)



    if 'Messages' in response:
        body=response['Messages'][0]['Body']
        handle = response['Messages'][0]['ReceiptHandle']
        list=json.loads(body,encoding='utf-8')
    #    print(type(list))
        print(list)
        for key in list["KEYS"]:
            print(key)
            print(type(key))
            bucket.get_object_to_file(key, "/opt/"+ key)
            s3.Bucket(config['target_bucket_aws']).upload_file("/opt/" + key, key)
            os.remove("/opt/" + key)
        response = client.delete_message(
            QueueUrl=random_url, ReceiptHandle=handle
        )

    else:
        logging.info('no message')


#QueueUrl='https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0' + str(
            #random.randint(1, 5)))


#response = client.receive_message(QueueUrl='https://cn-northwest-1.queue.amazonaws.com.cn/258616830098/bucket_migration_0'+str(random.randint(1, 5)))




#print(json.loads(response['Messages'][0]['Body']))

#print(len(json.loads(response['Messages'][0]['Body'])['KEYS']))
#print(json.loads(response['Messages'][0]['Body'])['KEYS'])


