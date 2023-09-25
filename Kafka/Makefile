topic_name?=example_topic
topic_partition?=1
bootstrap-server?=localhost:9092
group_id?=consumer_1

run-kafka:
	docker-compose up

create-topic:
	docker exec --interactive --tty broker \
    kafka-topics --create \
    --topic $(topic_name) \
    --bootstrap-server $(bootstrap-server) \
    --replication-factor 1 \
    --partitions $(topic_partition)

create-producer:
	docker exec --interactive --tty broker \
	kafka-console-producer --bootstrap-server $(bootstrap-server) \
	--topic $(topic_name)

create-consumer:
	docker exec --interactive --tty broker \
	kafka-console-consumer --bootstrap-server $(bootstrap-server) \
	--group $(group_id) \
	--topic $(topic_name) \
	--from-beginning
