# CSE138_Assignment3

A replicated, fault-tolerant, and causally consistent *key-value store*, running as a collection of three *replicas*. These replicas can make requests and broadcast state changes to each other. When they update the local store or show a (causally, consistent) view of the store to clients, the causal order of events is preserved Also, if a replica crashes, the store is still up since the other replicas are up. No data is lost due to replication, but the local copy of the store is lost. Additionally, replicas provide and receive causal metadata to and from clients, ensuring that clients have a causally consistent view of the store.

The store supports view operations (manages which replicas are part of the cluster) and key-value operations (works the key-value store), which are handled at the endpoints `/view` and `/kvs`, respectively.

## Mechanism Description

### Causal Dependencies

(put it here)

### Replica Down Detection

When a KVS request is broadcasted from a replica, it would work as expected as long
as the replicas are up. However, if a request exception is thrown, then that means the
receiving replica is *down*, in which case that replica is removed from all replicas'
VIEW.

## Acknowledgements

N/A

## Citations

- [Python os Module](https://docs.python.org/3/library/os.html)

## Team Contributions

### Hunter:

- Dockerfile and enviroment/codebase setup
- Coded backend of KVS
- Implemented KVS in app
- Implemented KVS broadcast functionality
- Implemented startup, causal metadata and consistency

### David:

- Coded backend of VIEW
- Implmented "replica down" detection for VIEW
- Templated the README

### Alan:

- Implemented VIEW in app
- Implemented "replica added" detection for VIEW
- Implemented KVS update when "replica added"
