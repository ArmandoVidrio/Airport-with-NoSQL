# Airport-with-NoSQL
2 models of 2 NoSQL engines (Cassandra and MongoDB) that tell a marketing company whose are the best airports to open a restaurant and when they have to do it.
  ### FOR CASSANDRA

### Setup a python virtual environment with python cassandra installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
virtualenv -p python3 ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r requirements.txt
```

### Launch cassandra container
```
# To start a new container
docker run --name node01 -p 9042:9042 -d cassandra

# If container already exists just start it
docker start node01

```

### If it's your first time running the project, you will need to run the app.py file and then exit to create the tables.
```
python3 app.py

```

### After you ran the app file you will need to create all the data we are going to use 
```
python3 tools/populate.py

```

### Copy data to container
```
docker cp tools/data.cql node01:/root/data.cql
docker exec -it node01 bash -c "cqlsh -u cassandra -p cassandra"
#In cqlsh:
USE investments;
SOURCE '/root/data.cql'
```

### Then you can run the app.py file again and use the program 
```
python3 app.py
```

### If isn't your first time running the program you can run the app file directly
```
python3 app.py
```
