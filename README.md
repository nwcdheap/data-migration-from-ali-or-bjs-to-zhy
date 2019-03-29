# data-migration-from-ali-or-bjs-to-zhy

## 免责说明
建议测试过程中使用此方案，生产环境使用请自行考虑评估。 </br>
当您对方案需要进一步的沟通和反馈后，可以联系 nwcd_labs@nwcdcloud.cn 获得更进一步的支持。</br>
欢迎联系参与方案共建和提交方案需求, 也欢迎在 github 项目issue中留言反馈bugs。</br>

## 项目介绍
通过使用队列机制及灵活扩展的docker，提升了大规模数据复制的可靠性及高并发性。   
项目适用于：
- 数据从阿里oss向aws S3迁移；
- 数据在aws北京区域和宁夏区域之间的迁移。  

## 建议  </br>
本项目仅用于对搬迁原理进行示例，以便您更好的定制自己的搬迁方案。如果你需要一个稳定的经过生产环境验证的aws北京和宁夏区域间迁移方案，请移步nwcdlabs/s3-migration-solution-from-patsnap

## 从阿里oss迁移到aws s3 </br>
1. 设置相关开发环境。以ubuntu为例：
```
apt-get update && apt-get install -y python3 python3-pip python3-dev
pip3 install oss2 boto3
```

2. git clone本项目文件夹。

3. 修改config.json文件，将您的阿里云密钥、aws密钥、阿里源桶名、aws目标桶名输入并保存。

4. 创建消息队列  

您可以选择在任何地方(本地，虚机，docker)运行sqs_init.py代码，该代码将为你创建5个队列和1个死信队列。  
（队列的数量、队列的属性参数您可以根据实际需要自行修改代码，进行硬编码或传参。本项目仅为示例代码。）

5. 将阿里oss桶里的文件信息打到消息队列中   

您可以选择在任何地方(本地，虚机，docker)运行publish_ali.py代码，该代码将需要搬迁的文件名作为消息随机的打入5个队列中的一个。  
您也可以选择稍微修改代码（参见被注释掉的行）,使其将消息全部打入某1条队列中.    

6. 开始搬迁工作   
为了满足大规模的数据搬迁场景，我们建议您在这一步使用docker进行工作。
- 使用basic文件夹下的Dockerfile构建docker基础镜像basic:latest

- 为简单起见，每个worker永远只监视一条队列的消息。因此，需要您打开worker_ali_to_aws.py，修改第66行代码，指定监控哪条队列。  


- 使用当前文件夹下的Dockerfile构建worker1镜像. 重复上条步骤，依次构建worker2/3/4/5/dead镜像（如果您有5个队列和1个死信队列的话）。

- 现在，您可以根据实际情况，选择使用ECS,swarm,kubernetes等容器编排引擎组织并启动您的容器们了。比如，你可以启动101个docker，其中20个使用worker1的image，20个使用worker2的image，20个使用worker3的image，20个使用worker4的image，20个使用worker5的image，1个使用workerdead的image。    

7. 当所有队列（包括死信队列）里面的消息都为空时，表示数据迁移完成。


## 从aws北京区域S3桶迁移到aws宁夏区域S3桶 </br>
1. 设置相关开发环境。以ubuntu为例：
```
apt-get update && apt-get install -y python3 python3-pip python3-dev
pip3 install  boto3
```

2. git clone本项目文件夹。

3. 修改config.json文件，将您的aws密钥、aws源桶名、aws目标桶名输入并保存。

4. 创建消息队列  

您可以选择在任何地方(本地，虚机，docker)运行sqs_init.py代码，该代码将为你创建5个队列和1个死信队列。  
（队列的数量、队列的属性参数您可以根据实际需要自行修改代码，进行硬编码或传参。本项目仅为示例代码。）

5. 将源桶里的文件信息打到消息队列中  

您可以选择在任何地方(本地，虚机，docker)运行publish_aws.py代码，该代码将需要搬迁的文件名作为消息随机的打入5个队列中的一个。
您也可以选择稍微修改代码（参见被注释掉的行）,使其将消息全部打入某1条队列中    

6. 开始搬迁工作   
为了满足大规模的数据搬迁场景，我们建议您在这一步使用docker进行工作。
- 使用basic文件夹下的Dockerfile构建docker基础镜像basic:latest

- 为简单起见，每个worker永远只监视一条队列的消息。因此，需要您打开worker_ali_to_aws.py，修改第40行代码，指定监控哪条队列。  

- 修改当前文件夹下的dockerfile，将最后一行 worker_ali_to_aws 改为 worker_aws_to_aws。 </br>
- 使用当前文件夹下的Dockerfile构建worker1镜像. 重复上条步骤，依次构建worker2/3/4/5/dead镜像（如果您有5个队列和1个死信队列的话）。

- 现在，您可以根据实际情况，选择使用ECS,swarm,kubernetes等容器编排引擎组织并启动您的容器们了。比如，你可以启动101个docker，其中20个使用worker1的image，20个使用worker2的image，20个使用worker3的image，20个使用worker4的image，20个使用worker5的image，1个使用workerdead的image。

7. 当所有队列（包括死信队列）里面的消息都为空时，表示数据迁移完成。


## 注意事项
- 阿里云向aws的迁移过程中，每个文件需要在本地做中转，但一旦传输完成后立马删掉。因此，一个worker需要的磁盘空间为您的最大的单个文件的大小。  
- aws区域间迁移不在本地落盘，因此无需为worker预留太多的instance store空间。

## todo-list
   -增加ECS/Kubernetes快速启动模板。  
   -优化log输出。  
   -通过客户的使用反馈，进一步封装，便于客户快速上手。  
   
