# DOCKER

## CREATE CONTAINER

```
sudo docker run --name test-mysql -p 3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
```

## STOP CONTAINER

```
sudo docker stop test-mysql
```

## START CONTAINER

```
sudo docker start test-mysql
```

## COMMANDS USEFUL

```
sudo docker container ps
sudo docker container ps -a
sudo docker images
```

# MYSQL

```
sudo apt install mysql-server
mysql -P $PORTNUMBER --protocol=tcp -u root -p
```

## CREATE AND UPDATE DATABASE WITH A SCRIPT

```
sudo mysql --local-infile=1 -P 49154 --protocol=tcp -u root -p < ../db.sql
```
