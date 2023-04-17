# ReservationService
(다른 서비스랑 돌아가는지 확인x)

## Run container
```
# cd into directory
cd ReservationService/
# build image
sudo docker build . -t reservation
# run container
sudo docker run --name ReservationService -p 8000:8000 reservation 
# try curling localhost
curl localhost:8000 ## "hello from Reservation"
```

## Stop container
```
# check name of the container
sudo docker ps 
# stop and remove container
sudo docker stop ReservationService
sudo docker rm ReservationService
# ... or just force remove directly
sudo docker rm ReservationService -f
```

## sample automap data
- Table 관련 문서: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table
```json
{'columns': [Column('id', INTEGER(display_width=11), table=<User>, primary_key=True, nullable=False),
             Column('createdAt', TIMESTAMP(), table=<User>, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2925e10>, for_update=False)),
             Column('updatedAt', TIMESTAMP(), table=<User>, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2926950>, for_update=False)),
             Column('username', VARCHAR(length=20), table=<User>),
             Column('password', VARCHAR(length=128), table=<User>),
             Column('email', VARCHAR(length=50), table=<User>, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2926b90>, for_update=False)),
             Column('userType', INTEGER(display_width=11), table=<User>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2926cb0>, for_update=False)),
             Column('isAdmin', TINYINT(display_width=1), table=<User>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2926dd0>, for_update=False)),
             Column('noShowCount', INTEGER(display_width=11), table=<User>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2926ef0>, for_update=False)),
             Column('isBanned', INTEGER(display_width=11), table=<User>, nullable=False, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x7f0fa2927010>, for_update=False))],
 'description': 'User',
 'foreign_key_constraints': set(),
 'foreign_keys': set(),
 'indexes': set(),
 'info': {},
 'key': 'User',
 'primary_key': PrimaryKeyConstraint(Column('id', INTEGER(display_width=11), table=<User>, primary_key=True, nullable=False)),
 'schema': None}
```