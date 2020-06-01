FROM mysql
ENV MYSQL_DATABASE melidb
ENV MYSQL_USER carlos
ENV MYSQL_PASSWORD 1234
ENV MYSQL_ROOT_PASSWORD=supersecret
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/