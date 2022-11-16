CREATE USER flow WITH CREATEDB PASSWORD 'password';

CREATE DATABASE flow_monitoring
WITH OWNER = flow
    TEMPLATE = template0
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8';
