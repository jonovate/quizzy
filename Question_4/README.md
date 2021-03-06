# Question 4
>
> *Streaming Data:* testing Kafka, Spark, Hadoop, HDFS.
>
>   4.1. *Kafka* Quickstart , <https://kafka.apache.org/quickstart>:
>
>       4.1.1. High level explanation of Kafka’s structure:
>			4.1.1.1. *Concepts:* Explain the following Kafka concepts: "Kafka is run as a cluster on one or more servers" ; "The Kafka cluster stores streams of records in categories called topics" ; "Each record consists of a key, a value, and a timestamp".
>			4.1.1.2. Kafka has four core *APIs*, explain each one of them: "Producer API" ; "Consumer API" ; "Streams API" ; "Connector API".
>		4.1.2. Deploy a bare bones Kafka/Zookeeper server:
>           4.1.2.1. Create a topic; Send some sample messages; Dump the messages on standard output (consumer); Use Connect to import/export data.
>           4.1.2.2. *Bonus:* run the WordCountDemo, <https://kafka.apache.org/10/documentation/streams/quickstart>.
>
>   4.2. *Spark, Hadoop, HDFS:* quickstart:
>
>		4.2.1. Deploy Spark in standalone mode, and run a couple of examples through your newly deployed Spark server: <https://mbonaci.github.io/mbo-spark/> ;<https://spark.apache.org/docs/latest/spark-standalone.html>.

## Solution

### Kafka

Very fast (high throughput, low latency) distributed transaction log for real-time streams of data, akin to pub/sub due to use of Topics.
Producers feed data into Topics that hold the Records (key, value, timestamp), which for performance reasons can be split across partitions; consumers then query the record data from the topic's partition.
Brokers are responsible for fault tolerance and ensuring Records are replicated appropriately.

Topics are basically partitioned logs where Records are written in an append-only fashion, which helps with patterns such as Event Sourcing. A Record is assigned an offset, aka ID, which identifies itself in a certain partition of a topic. This means records within' a partition are ordered.

In addition to choosing which Topic, Producers can either choose to allow data to be written in a Round Robin or define a partition key function to decide where data goes, similar to the idea of sharding a DB.  This allows similar groups of data to end up on same partition which also helps when order matters.

Other facts:

- Open-Source Apache project from LinkedIn which spun business out into Confluent for overseeing and owning Enterprise offerings.
- Tightly coupled with ZooKeeper
- Written in Java and Scala
- Finally hit v1.0 in November 2017
- AWS Kinesis is similar


#### Answers

> *"Kafka is run as a cluster on one or more servers"*

An instance of Kafka can run by itself or within a group (cluster) where data is reliably backed up across each server.

Kafka can have 1 or more Topics. Topics can have 1 or more Partitions. Records are appended to the Topic which may end up on any partition (*see above*). 
Brokers are then responsible for replicating Partitions across the other servers in the cluster. Zookeeper ensures one is elected as Leader whereas the remaining are Followers.


> *"The Kafka cluster stores streams of records in categories called topics"*

Topics are channels/feeds which contain a logical group of Records, which Producers write to and Consumers read from. Like in Pub/Sub, any number of consumers can read from them ("Consumer Groups").
Topics are then split up across 1 or more Partitions which guarantee ordering of Records within that partition, but not across Topic.  Once a record is written to a Topic's partition, it cannot be changed (immutable). Zookeeper keeps track of the last offset that was read by consumer to ensure it is not read again; Kafka can also be configured to purge records after a certain amount of time or size.


> *"Each record consists of a key, a value, and a timestamp"*

This definition makes reference to the underlying protocol for Records. The value is the payload, the key can optionally be assigned by the Producer to help decide which partition the record should end up on, and the timestamp can be assigned by the client to state the time the record was created, else will be assigned by Producer API depending on system settings (Producer Times versus AppendTime, etc.)

> *"Explain 4 Core APIs"*

Kafka provides various language wrappers around the functions for interacting with the Cluster.

- **Producer API** - Interface for allowing apps/clients to add records to Partitions/Topic(s)
- **Consumer API** - Interface for allowing apps/clients to read and process records from the Partitions/Topic(s)
- **Streams API** - Interface which allows an application to read from input stream, process data and write back to an output stream. Can easily scale solution without much changes to handle bigger loads by deploying horizontally. Some overlap with Storm, Spark, etc.
- **Connector API** - Interface for reliably connecting Kafka with external systems, for both in and out. Can basically ingest all data from external systems and make it available as Topics.

#### Examples

```
git config --global core.autocrlf false
git clone https://github.com/wurstmeister/kafka-docker.git
cd kafka-docker

#You may need to edit docker-compose.yml and change KAFKA_ADVERTISED_HOST_NAME to 'kafka' first
#FYI - Auto Create Topics is disabled by default
docker-compose up -d

docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic question4
    #check with:  docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --list --zookeeper zookeeper:2181

Terminal 1 ->
    docker-compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic question4 --from-beginning
Terminal 2 ->
    docker-compose exec kafka /opt/kafka/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic question4
#line1
#line2
#etc
#^C

#Streams Quickstart
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic streams-plaintext-input
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic streams-wordcount-output
Terminal 1 ->
    docker-compose exec kafka /opt/kafka/bin/kafka-run-class.sh org.apache.kafka.streams.examples.wordcount.WordCountDemo
Terminal 2 ->
    docker-compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic streams-wordcount-output --from-beginning     --formatter kafka.tools.DefaultMessageFormatter --property print.key=true --property print.value=true --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
Terminal 3 ->
    docker-compose exec kafka /opt/kafka/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic streams-plaintext-input
        #what a day
        #Consumer: what 1
        #          a    1
        #          day  1
        #day
        #Consumer day  2


#Connect: Setup File In, File Out Connector - uses default topic of connect-test
docker-compose exec kafka /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic connect-test

docker-compose exec kafka sh   #Doesn't seem to work via exec
    cd /opt/kafka/ && ./bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
docker cp google-10000-english.txt kafkadocker_kafka_1:/opt/kafka/test.txt
docker-compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic connect-test --from-beginning
    ##Processed a total of 10000 messages
docker-compose exec kafka cat /opt/kafa/test.sink.txt
    ##wc test.sink.txt == 10000
#(Would then use API on 8083 to keep Connect running long term)
#I also built the Kafka-Connect-Gitub-Source project to feed data into Kafka, but ran out of time to fully set it up
```

### Spark

```
docker pull p7hb/docker-spark:2.2.0

#Jump right to spark shell
docker run -it -p 4040:4040 -p 4080:8080 -p 4081:8081 -h spark --name=spark p7hb/docker-spark:2.2.0 spark-shell
#Console on http://localhost:4040

    spark version
        #> String = 2.2.0

    #Getting started with RDDs
    val nums = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    val numsData = sc.parallelize(no)
    nums.count()
        #> Long = 10
    nums.take(3)
        #> Array[int] = Array(1,2,3)

    #In another terminal
    docker cp google-10000-english.txt spark:/tmp/data.txt
    #
    val googleData = sc.textFile("/tmp/data.txt)
    googleData.cache()
    googleData.count()
        #> Long = 10000
        ## Now available on http://localhost:4000/storage
    val thWords = googleData.filter(line => line.startsWith("th") & line.length() > 5)
    thWords.count()
        #> Long = 63   (63 words beginning with th which are at least 5 chars long)
    thWords.sortBy({K => K}, false).take(5)
        #> Array[String] = Array(thursday, thunder, thumbzilla, thumbs, thumbnails)

    :quit    #Will close docker process

docker rm spark         #It was started with spark-shell command

#Re-Run with default shell
docker run -it -p 4040:4040 -p 4080:8080 -p 4081:8081 -h spark --name=spark p7hb/docker-spark:2.2.0
start-master.sh
#Master Console on http://localhost:4080
start-slave.sh spark://spark:7077
#Worker Console on http://localhost:4081

spark-submit --class org.apache.spark.examples.SparkPi --master spark://spark:7077 $SPARK_HOME/examples/jars/spark-examples*.jar 5
    #> Pi is roughly 3.143478286956574

#To start spark shell with master now
spark-shell --master spark://spark:7077

#More examples here: https://spark.apache.org/examples.html
```

With Hadoop/HDFS Built-in, but older Spark version:

```
docker pull sequenceiq/spark
docker run -it -p 8088:8088 -p 8042:8042 -p 4440:4040 -h sandbox sequenceiq/spark:1.6.0 bash

#Run as YARN Client
spark-submit --class org.apache.spark.examples.SparkPi --master yarn-client --driver-memory 1g --executor-memory 1g --executor-cores 1 $SPARK_HOME/lib/spark-examples-1.6.0-hadoop2.6.0.jar
    #> Pi is roughly 3.143478286956574
```
