
# Apache Kafka Installation and Setup Guide

This guide outlines the steps to install and set up Apache Kafka on a virtual machine, along with creating topics, starting Zookeeper and Kafka servers, and configuring producers and consumers.

## Step 1: Creating Virtual Machine

- Create the virtual machines and add an RSA key pair to access the VM through SSH. 
- After successful creation of the VM, obtain the connection code to connect to your VM.

## Step 2: Editing Security Group

- Edit the inbound rules to enable all traffic for testing purposes, allowing all ports to communicate with the machine through its public internet address.

## Step 3: Installing Apache Kafka

- Download Apache Kafka version 2.12-3.6.2 from the official website.
`wget https://downloads.apache.org/kafka/3.6.2/kafka_2.12-3.6.2.tgz`

- Unzip the downloaded Kafka package.
`tar -xvf kafka_2.12-3.6.2.tgz`

## Step 4: Installing Java

- Check the installed Java version.
`java -version`

- Install Java version 1.8 if not already installed.
`sudo yum install java-1.8*`

- Verify the installed Java version.
`java -version`

## Step 5: Starting Zookeeper

- Navigate to the Kafka directory.
`cd kafka_2.12-3.6.2`

- Start Zookeeper server.
`bin/zookeeper-server-start.sh config/zookeeper.properties`

## Step 6: Starting Kafka Server

- Open a new terminal and connect to the VM.
- Navigate to the Kafka directory.
`cd kafka_2.12-3.6.2`

- Set Kafka heap options.
`export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"`

- Start Kafka server.
`bin/kafka-server-start.sh config/server.properties`

- Modify `server.properties` to use the public IP.
`sudo nano config/server.properties`
 
`advertised.listeners=PLAINTEXT://<PUBLIC_IP>:9092`

## Step 7: Creating Topics

- Duplicate the session and enter a new console.
- Navigate to the Kafka directory.
`cd kafka_2.12-3.6.2`

- Create Kafka topics for each website name, as spiders will use them as topics.
`bin/kafka-topics.sh --create --topic website1 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1`
`bin/kafka-topics.sh --create --topic website2 --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1`

Add more topics for each website as needed

## Step 8: Start Producer
- Make sure your zookeepr and kafka broker are running
-  the spider which will be triggered periodically (e.g., every week). Or you can run them manually by starting any spider through the main.py file( they will act as a producer)

## Step 9: Start Consumer

- Keep the consumer running on the same VM if desired.
- The consumer code is provided .The ENV file has to be configured(Necessary template has been given).

Make sure all the above steps are followed and the broker and the zookeper are running
Also dont miss to change the server.properties file as said

This README provides a basic setup guide for installing and configuring Apache Kafka. Adjustments may be necessary based on specific requirements and configurations. Make sure to replace `<public_IP>` with the actual public IP of your VM.
