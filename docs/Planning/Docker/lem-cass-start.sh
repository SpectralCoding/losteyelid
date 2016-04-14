#!/bin/bash
docker run --detach --name lem_cassandra -p 7000-7001:7000-7001 -p 7199:7199 -p 9042:9042 -p 9160:9160 --volume /content/losteyelid/master/cassandra:/var/lib/cassandra cassandra:latest
