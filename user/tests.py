import logging
import sys
from datetime import datetime

import logstash
import pika
from elasticsearch import Elasticsearch


class TestEs:
    def __init__(self):
        self.es = Elasticsearch(['localhost'], http_auth=('elastic', '123456'), timeout=3600)

    def test_es(self):
        doc = {
            'author': 'kimchy',
            'text': 'Elasticsearch: cool. bonsai cool.',
            'timestamp': datetime.now(),
        }
        res = self.es.index(index="test-index", id=1, body=doc)
        print(res['result'])

        res = self.es.get(index="test-index", id=1)
        print(res['_source'])

        self.es.indices.refresh(index="test-index")

        res = self.es.search(index="test-index", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


class TestLogstash:

    def test_log(self):
        host = 'localhost'

        test_logger = logging.getLogger('python-logstash-logger')
        test_logger.setLevel(logging.INFO)
        test_logger.addHandler(logstash.LogstashHandler(host, 5044, version=1))
        # test_logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

        test_logger.error('python-logstash: test logstash error message.')
        test_logger.info('python-logstash: test logstash info message.')
        test_logger.warning('python-logstash: test logstash warning message.')

        # add extra field to logstash message
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
        test_logger.info('python-logstash: test extra fields', extra=extra)


class TestRabbitmq:
    def __init__(self):
        credentials = pika.PlainCredentials('root', '123456')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.0.105 ', port=5672, virtual_host='/test', credentials=credentials))

    def test_rb_c(self):
        channel = self.connection.channel()
        m = channel.basic_publish(exchange='test', routing_key='test',
                              body=b'Test message.')
        self.connection.close()

    def test_rb_r(self):
        channel = self.connection.channel()

        for method_frame, properties, body in channel.consume('test'):
            # Display the message parts and acknowledge the message
            print(method_frame, properties, body)
            channel.basic_ack(method_frame.delivery_tag)

            # Escape out of the loop after 10 messages
            if method_frame.delivery_tag == 10:
                break

        # Cancel the consumer and return any pending messages
        requeued_messages = channel.cancel()
        print('Requeued %i messages' % requeued_messages)
        self.connection.close()


if __name__ == '__main__':
    # test = TestEs()
    # test.test_es()

    # test = TestLogstash()
    # test.test_log()

    test = TestRabbitmq()
    # test.test_rb_c()
    test.test_rb_r()
