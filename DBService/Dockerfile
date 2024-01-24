FROM mariadb:11.0-rc-jammy


COPY ./maria-init.sql /docker-entrypoint-initdb.d/maria-init.sql

HEALTHCHECK --start-period=5m \
    CMD mariadb -e 'SELECT @@datadir;' || exit 1

EXPOSE 3306

CMD ["mariadbd"]

