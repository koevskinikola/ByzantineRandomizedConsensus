# Byzantine Randomized Consensus

A Byzantine Randomized Consensus is a Byzantine Fault Tolerant consensus protocol. Randomization in consensus protocols is used to overcome the problem of termination in asynchronous systems (no deterministic algorithm solves consensus
in asynchronous systems).

Hence, a randomized consensus protocol is able to function efficiently in an asynchronous environments like p2p networks.

This version of the protocol implements a Byzantine Randomized Broadcast protocol for the broadcast abstraction.

There is a script for testing the implementation locally at: *byzantinerandomizedconsensus/test/brb_test.py*

## License
MIT