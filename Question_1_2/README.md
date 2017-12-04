# Question 1

> *DBs:* testing DBs, Linux/CLI, general terminal/scripting, etc: load simple user data and metadata into the following, making sure each DB is “properly” set up:
>
>   1.1. SQL: choose between MySQL or PostgreSQL.
>
>   1.2. NoSQL: choose between MongoDB, Redis.
>
>   1.3. Graph: choose between Neo4J, OrientDB.
>
>   1.4. Basic data and metadata to be loaded to each one of the DBs above: User Data and Metadata: username, passwd, selected keywords (name, last name, list of colors).
>
>   In addition to the above, add the below data and metadata to each of the chosen DBs (1 SQL, 1 NoSQL, 1 Graph) above:
>
>        - Create a DB to accumulate different family events: DB name == 'events'
>        - Using the 'events' DB, create a field to accumulate different types
>            of events: Thanksgiving , Potluck , Birthday .
>        - Each event should should contain the following relevant fields:
>            Name , Food , Confirmed , Sign Up Date .
>        - Data to be added to each field:
>            Names: John Jay; Sandy Ess; Tom Tee; Tina Tee.
>            Foods: Casserole; Key Lime Tarts; BBQ; Salad.
>            Confirmed: Yes; No. (Pick at random.)
>            Sign Up Date: pick as desired.

## Solution

*If I had a smidge more time, I would have had the python scripts running in their own containers, sharing same network as DB.*

Commands for all DB's:

```pip install -r requirements.txt``` to ensure all libraries exist 

```python generate_events.py > events.json``` to generate the event data

### Postgres

- Created explicit columns for metadata.
- Considered keyword search as indexes.

Two versions: Half normalized (only event types and colors, did not bother names, foods, etc. due to time .. realize in fully normalized world they would be) and anther using metadata and JSONB for the user data. See DDL sql.

  - On the JSONB version, created one GIN index on event->name. Had trouble doing the same on last_name.
    - ```SELECT event -> 'name' FROM public.events_json;```
  - Also debated splitting name beforehand, but left it as 1 string as requirements seemed explicit.

```
docker run --name q1postgres -p 5432:5432 -e POSTGRES_PASSWORD=myR00Tpw -d postgres
docker cp events_ddl.sql q1postres:/tmp   #Copy our DDL script
docker exec -it q1postgres bash
    psql -U postgres -c "CREATE USER usr_question1 WITH PASSWORD 'goGO99';"
    psql -U postgres -d postgres -c "CREATE DATABASE events";
    psql -U postgres -d postgres -c "GRANT ALL ON DATABASE events to usr_question1";
    psql -U postgres -d events < /tmp/events_ddl.sql

python postgres_load.py
```

### Mongo

Choosing to store our events in a collection.

- Metadata keys will begin with at least one '_'
- Adding non-unique indexes to our 3 keyword fields, which I used '__' as prefix for those keywords/metadata

```
docker run --name q1mongo -p 27017:27017 -d mongo
#Struggled with auth (rootadmin couldn't create oter users), need to go deeper another day
docker exec -it q1mongo mongo admin
    #db.createUser({ user: 'rootadmin', pwd: '!goGO99', roles: [ { role: "dbOwner", db: "admin" } ]})
    use events
    #db.createUser({ user: 'usr_question1', pwd: 'goGO99', roles: [ { role: "readWrite", db: "events" } ] })

python mongo_load.py
```

### Neo4J

Ended up walking through Movies tutorial first.

Planning (Must be a better way without making a cycle):
  - Name -->attends--> Event
        props: [Confirmed, Brought]
  - Name -->brings--> Food
        props: [SignUp Date, Attended]


Couldn't figure out best way to create keywords/metadata so added as properties on appropriate Node label

```
docker run --name q1neo4j -p 7474:7474 -p 7687:7687 -d neo4j

#Need to visit http://localhost:7474 and change password

python neo4j_load.py
    # MATCH (n) RETURN n
```

# Question 2

> *Python:* testing Python 3, ORMs, code quality, etc: write ​[Python] ​code to connect to the above DBs and list its contents.
>   *Bonus* for using appropriate ORMs.
>   *Extra Bonus:* using Pandas as backend.
> > In Python, write code to connect with the above DBs, and list its contents. Feel free to use ORMs, Pandas, etc.

## Solution

**Pandas would not install from pip on Windows, need to go via Anaconda and ran out of time :(***

### Postgres

Only handled JSON version for time purposes (skipped normalized)
  - Half-normalized would need to *inner join* to their respective tables to get the value for display.

Code isn't as ORM'y as I would have liked .. ran out of time

```
python postgres_q2.py
```

### Mongo

Leveraged and refactored postgres Q2 solution.. ran out of time

```
python mongo_q2.py
```


### Neo4J

*Default python neo4j-driver does not seem to work on Windows.  Switched to restclient library instead.*

There are probably some better ways to traverse entire tree

```
python neo4j_q2.py
```
