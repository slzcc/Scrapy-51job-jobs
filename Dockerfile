FROM registry.aliyuncs.com/slzcc/python:3
RUN git clone -b elasticsearch https://github.com/slzcc/Scrapy-51job-jobs.git && \
    cd Scrapy-51job-jobs && \
    pip install -r package.txt

ENV REDIS_DB_HOST=127.0.0.1 \
    REDIS_DB_PORT=6379 \
    ELASTICSEARCH_DB_SERVER=http://localhost:9200 \
    ELASTICSEARCH_DATA_INDEX=scrapy-51job \
    ELASTICSEARCH_DATA_TYPE=item \

WORKDIR /Scrapy-51job-jobs

CMD ["python", "main.py"]