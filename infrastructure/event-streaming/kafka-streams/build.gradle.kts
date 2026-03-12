// Kafka Streams サンプル（UEP v5.0）
// 補強スキル: イベント駆動（Kafka Streams）
plugins {
    java
    application
}

application {
    mainClass.set("uep.EventCountStream")
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.apache.kafka:kafka-streams:3.6.0")
    implementation("org.slf4j:slf4j-simple:2.0.9")
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

tasks.jar {
    manifest {
        attributes["Main-Class"] = "uep.EventCountStream"
    }
}
