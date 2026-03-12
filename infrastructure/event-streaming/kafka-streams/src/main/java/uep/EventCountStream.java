package uep;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.kstream.Printed;

import java.util.Properties;

/**
 * Kafka Streams サンプル: イベント種別ごとの件数集計
 * 補強スキル: イベント駆動（Kafka Streams）
 */
public class EventCountStream {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "uep-event-count");
        String bootstrap = System.getenv("KAFKA_BOOTSTRAP_SERVERS");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap != null ? bootstrap : "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        // Windows: プロジェクト内の state ディレクトリを使用（ロック・権限問題を回避）
        props.put(StreamsConfig.STATE_DIR_CONFIG, "./build/kafka-streams-state");

        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> source = builder.stream("uep-events");

        source
            .groupBy((key, value) -> "event")  // 簡易: 全件を1キーで集計
            .count(Materialized.as("event-count-store"))
            .toStream()
            .print(Printed.toSysOut());

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
