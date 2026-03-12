FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app
COPY . .
RUN ./gradlew installDist -x test --no-daemon

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/build/install/kafka-streams/ .
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:29092
# トピック作成の伝播を待つ
ENTRYPOINT ["/bin/sh", "-c", "sleep 5 && exec ./bin/kafka-streams"]
