from flask import Flask, send_from_directory, request, jsonify

from apimanager import MeliApiManager
from filereader import FileProcessor, FileReader, CsvFileFormatter

import config
import db
import logger
import time


app = Flask(__name__)
app.config.from_object(config.AppConfig)
db.db_connection.init_app(app)


@app.route('/process_file', methods=['POST'])
def process_file():
    file_name = request.json['file_name']
    chunk_size = request.json['chunk_size']

    logger.file_logger.init_logger()

    api_manager = MeliApiManager(config.AppConfig.api_base_url)
    formatter = CsvFileFormatter(config.AppConfig.file_line_separator)
    file_reader = FileReader(file_name, formatter, config.AppConfig.file_encoding)

    fp = FileProcessor(file_reader, chunk_size, api_manager)
    st = time.time()
    fp.process()
    print('Total api calls were ' + str(api_manager.api_calls_count))
    total_time = time.time() - st
    print("Time is " + str(total_time))
    logger.file_logger.stop_logger()
    return jsonify({"total_time_seconds": total_time,
                    "http_requests_performed": api_manager.api_calls_count,
                    "more_info": config.AppConfig.info})


@app.route('/')
def hello_world():
    return 'Hello, World! Please check docs!'


@app.route('/logs')
def get_logs():
    return send_from_directory('.', config.AppConfig.log_file_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
