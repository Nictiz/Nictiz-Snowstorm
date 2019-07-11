FROM openjdk:8-jdk-alpine
LABEL maintainer="SNOMED International <tooling@snomed.org>"

ARG SNOWSTORM_VERSION=3.0.3

ARG SUID=1042
ARG SGID=1042

VOLUME /tmp

# Create a working directory
RUN mkdir /app
WORKDIR /app

RUN mkdir /snomed-drools-rules

# Copy necessary files
#ADD target/snowstorm-*.jar snowstorm.jar

# Download specified release
RUN wget https://github.com/IHTSDO/snowstorm/releases/download/${SNOWSTORM_VERSION}/snowstorm-${SNOWSTORM_VERSION}.jar
RUN mv snowstorm-${SNOWSTORM_VERSION}.jar snowstorm.jar

# Create the snowstorm user
RUN addgroup -g $SGID snowstorm && \
    adduser -D -u $SUID -G snowstorm snowstorm

# Change permissions.
RUN chown -R snowstorm:snowstorm /app

# Run as the snowstorm user.
USER snowstorm

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","snowstorm.jar"]