
#### Cruise control - Kafka Administrative component
Cruise control works based on kafka metrics to generate plans to guarantee kafka cluster health with best practices

* adding or removing broker
* leadership partition rebalance



##### working with cruise control
```sh
#describe cruise control plan
kubectl describe kafkarebalance edh-kafka-rebalance -n ingestion

#aprove the plan
kubectl annotate kafkarebalance edh-kafka-rebalance strimzi.io/rebalance=approve -n ingestion

#refresh to see the newest plan or info
kubectl annotate kafkarebalance edh-kafka-rebalance strimzi.io/rebalance=refresh -n ingestion

```
