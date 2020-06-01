class AppConfig:
    sql_add_item = ("INSERT INTO Item "
                    "(site, id, price, name, description, nickname, start_time) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    db_connection_params = {
        'host': 'db',
        'user': 'carlos',
        'password': '1234',
        'database': 'melidb'
    }
    api_base_url = 'https://api.mercadolibre.com'
    file_line_separator = ','
    file_encoding = 'utf8'
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    log_file_name = 'logs.txt'
    info = 'Task done. Check: /logs for problems encountered'
