# Question 3

> *Data Lake on AWS:* testing Data Warehousing, Data Pipelining, AWS.
>
>   3.1. What kinds of AWS services would you use to build a Data Lake on AWS? A high-level overview of the server-side architecture will suffice.
>   For example: Cognito, API Gateway, Lambda, DynamoDB, ElasticSearch, S3 buckets — explain what is a Data Lake, why deploy one on AWS, and give a basic description of each of the AWS services you'd use to deploy one on AWS. If you are able to refine your original proposal, making it more sophisticated, please, go ahead and describe its architecture and the AWS services you'd use.
>   *Bonus* for using a CloudFormation Script. 
>   *Extra Bonus* for deploying on a free AWS tier.

## Solution

### Background
Data Lakes are a more recent, modern architectural pattern for the purposes of storing vast amounts of data for later processing, analysis, and analytics, where the results of any transformations are also preserved.  A key characteristic of the Lake, as compared to Data Warehouses and Data Marts of the past, is the data is stored in its original, raw format: it doesn't matter if its structured, semi-structured, unstructured or binary - the lake will take it. This is a big difference to the former design, which required skilled resources to actually translate/transform the data into a fixed schema before being ingested into the Warehouse; consequently, fields that were not needed were dropped and possibly lost forever. Now with a Lake, the original data is retained so that if an analysis query later needs another field, it would be available immediately instead of needing to go back to source and hoping it was preserved upstream.

Another analogy to visualize a Lake is: streams & rivers (different ingress points) feeding water (data) into the body of the lake (centralized data store), with potentially streams flowing out (analytics, visualizations, etc.)

Finally, to layout the different components of a Data Lake:

- **Acquisition**
  - **Data Submission Endpoints** - How the data gets in:  batch file copy, data streams, event queues/topics, web services, etc.
  - **Ingestion Processing** - Initial validation, indexing, extraction of metadata, etc.
- **Management**
  - **Dataset Management** - Storage and management of the big data itself
  - **Search** - Keeping any indexes any metadata up-to-date
  - **Dataset Analysis** - Sorts, Joins, Transformations, Aggregations, Analysis of data
- **Access**
  - **Publishing** - Making analyzed data available in structured form
  - **Visualization** - Preparing data for visual analysis

### AWS
AWS, like any other cloud provider such as Azure or GCP, has a set of services for building and managing a company's data lake. Some of the reasons one would choose to go the cloud route for hosting it include:

- Multiple tools available in the cloud suite for compute & processing, storage, ad-hoc & predictive analysis/analytics, real-time streaming, MI and AI.
  - Services provisioned immediately as opposed to waiting for traditional on-prem
  - Can use right tool for the job instead of what company may have licensed
- Savings for the vast amount of compute & storage needed
- Security out of the box (roles, subnets, etc.)
- Choose locations/regions where the business is actually located (*ie: IoT use case - ability to place services where customers actually are*)
- Disaster Recovery inherently built-in

#### AWS Services

- **S3** Simple Storage Service: Storage of any object into buckets, which can be retrieved from anywhere. *One of key foundations*
  - Storing extracts/batch files/snapshots in buckets for ingestion into lake
  - Storage of actual lake data which is indexed/inventoried across ES
  - Saving data (*ie: after ingestion processing*) before being loaded elsewhere
  - Saving analyzed extracts of data from the lake for later analytics/visualizations
  - **S3 Events** trigger alerts that new/processed data is available
  - **Athena** Analyze data in S3 with query-like syntax, very fast

- **EC2** Elastic Compute Service: Scalable and resizable servers for computing type function.. basically a virtual server with limitations.
  - Hosting any web services / microservices (could be exposed in API Gateway)
  - Compute container for hosting auxiliary tools in lake management and processing (ie: Spark)

- **API Gateway** Front door to APIs - functions to create, publish, maintain & monitor & secure
  - Expose EC2 services for ingress of data into lake
  - Exposing Lambda services for ingress of data and intermediary processing

- **Lambda** FaaS (Function As A Service) / Serverless for running code without needing a server
  - Building services for injesting data, exposed in API Gateway
  - Accept event notifications from S3 buckets
  - Hosting functions in a pipeline during later analysis of data in lake (ie: parse metadata or indexes)

- **Kinesis** Ingest and buffering of real-time stream data and events. A managed Kafka offering.  **Firehose** then lets you direct data into other AWS Services.
  - Handling stream of data as ingress, store data in S3 for example.
  - **Kinesis Data Analytics** - Run SQL-like querying against Kinesis stream for selective analytics

- **SQS / SNS** Simple Queue Service / Simple Notification Service: Queuing and Topics for decoupling and building distributed applications
  - Allow other apps in landscape to place data in queue/topic for ingestion into lake
  - Accept event notifications from S3 buckets

- **ES** ElasticSearch Service - Managed ES instance for search, analytics, monitoring, etc.
  - Storing metadata of processed data; cataloging
  - Search for specific data across Lake
  - Lake performance/infrastructure analytics and push to Kibana

- **DynamoDB** Very fast (and flexible) document and key-value NoSQL store
  - Storing data in Lake and indexing/tagging alongside ES
  - Leverage Triggers to activate AWS Lambda functions when data changes

- **EMR** ElasticMapReduce Service - Managed HDFS/Hive / Spark type activity
  - ETL activity on data for analysis

- **Redshift** Data Warehouse (based on postgres but columnar) Storing data in fixed format
  - Store processed lake data in fixed formats for analysts with SQL skills and other tools

- **QuickSight** - Easy to use for building visualizations of data, ad-hoc analysis and insights
  - Hook into data in lake (ie: Redshift) to produce visualizations, etc.
  - Could alternatively use *Kibana* to hook into for visualizations

- **Cognito** Security/Management for Authentication of Solutions and Apps
  - Authentication for services allowing ingestion into lake
  - Managing who can see data in the lake
- **IAM** Identity and Access Management: Control and manage access to resources in AWS
  - Managing users and roles for adding/changing data in lake
  - Managing who can operate AWS Services, change infrastructure components, etc.
- **VPC** Virtual Private Cloud: Isolate and protect services in compartments, VPN, etc.
  - Protect and isolate data for security, separate ingestion from storage


#### Templates & Solution
Ran out of time to build my own, would have used one of these as foundations though:

- <https://s3.amazonaws.com/quickstart-reference/datalake/F47lining/latest/templates/data-lake-master.template>
- <https://s3.amazonaws.com/solutions-reference/data-lake-solution/latest/data-lake-deploy.template>

What it would have looked like:

**Data Acquisition** (depending on infrastructure):
1. Ingest S3 bucket for batch/file copy
2. API Gateway in front of web services/microservices on EC2/Lambda for receiving requests
    * Depending on size, would place request in S3 bucket or consider SQS/SNS
3. Kinesis for ingesting streams of data, using Firehose to route data into an S3 bucket
4. *SQS/SNS if integration into existing landscape*  Lambda then puts it into S3 bucket

All 4 would feed the data into S3, which notifies Lambda to perform processing (validation, indexing & extraction metadata, etc.). Would need to further look into using Kinesis/SQS/SNS here as well for throttling/rate limiting depending on volume.

**Management**
1. Combination of DynamoDB (key/value) and S3 Buckets for Storage of data - system of record
    * ES indexes location of data (Dynamo vs S3) based on metadata, highlights latest versions, etc.
2. RedShift for any processing where we end up with more structure
3. EMR and/or Lambda and/or other services in EC2 (ie: Spark) for ETL/Aggregations/etc into 1 or 2

**Access**
1. Can perform further analysis in data in RedShift
2. Use QuickSight or Kibana to build visualizations

### References:
- <https://aws.amazon.com/big-data/data-lake-on-aws/>
- <https://aws.amazon.com/blogs/big-data/introducing-the-data-lake-solution-on-aws/>
- <https://aws.amazon.com/quickstart/#bigdata>
- <https://en.wikipedia.org/wiki/Data_lake>
- <https://www.blue-granite.com/blog/bid/402596/top-five-differences-between-data-lakes-and-data-warehouses>
- <http://resources.idgenterprise.com/original/AST-0163853_how-to-build-an-enterprise-data-lake.pdf>
- <https://www.slideshare.net/AmazonWebServices/best-practices-for-building-a-data-lake-on-aws>
