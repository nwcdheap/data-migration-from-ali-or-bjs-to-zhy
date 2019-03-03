FROM basic:latest

#RUN apt-get update && apt-get install -y python3 python3-pip python3-dev
COPY . /opt
WORKDIR /opt
#RUN pip3 install oss2 boto3

#RUN source /etc/profile

#RUN export LC_ALL="en_US.UTF-8" 



#ENTRYPOINT ["bash", "run.sh"]
#RUN cat /proc/version

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

#RUN locale 


#UN locale-gen en_US.UTF-8

#RUN echo "LC_ALL=en_US.UTF8 " >  /etc/default/locale

CMD ["python3", "worker_ali_to_aws.py"]
