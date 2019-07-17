# Nictiz-Snowstorm
Modified docker build package for building and deploying snowstorm and elasticsearch containers

# Running snowstorm and elasticsearch from scratch
In the project root, run docker-compose
[docker-compose up snowstorm]
This will build the snowstorm container from the IHTSDO GitHub repository. Edit the dockerfile in ./snowstorm to reflect the desired version available on GitHub.

    * [IMPORTANT] Requirements: 
    docker machine with 4gb memory
    this docker-compose file will create a folder ./elastic containing the indices for elasticsearch. This folder can be backed up or reused.
    
# Snowstorm ingest
The snowstorm ingest image will take several command line options to quickly add or update codesystems in snowstorm.
For testing purposes and example only! This script has not been thoroughly tested, and does not contain any error handling.
Remember to start your snowstorm service with read only disabled! [./docker-compose.yml]

1) Download all release files you want to use in this folder.
2) cd into the ingest folder ./ingest

3) You can either use the prebuilt docker image available on the docker repository, or build your own.
3a) Use the prebuilt image nictiz/snowstorm-ingest:latest
3b) Build your own from source:
    docker build -f Dockerfile-ingest -t nictiz/snowstorm-ingest .

4.1) Run headless, only receives output after finishing:
    docker run --rm --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest "[BRANCHPATH]" "[SHORTNAME]" "[FILENAME]" [SERVERURL:PORT] [IMPORT-TYPE]

4.2) Run interactive, with output to command line:
    docker run --rm -it --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest "[BRANCHPATH]" "[SHORTNAME]" "[FILENAME]" [SERVERURL:PORT] [IMPORT-TYPE]

    * Replace:
    [BRANCHPATH] -> ie. MAIN
    [SHORTNAME] -> ie. SNOMEDCT
    [FILENAME] -> filename of the release, ie. SnomedCT_GMDNMapRelease_Production_20190331T120000Z.zip
    [SERVERURL:PORT] -> ie. your.server.com:8080
    [IMPORT-TYPE] -> SNAPSHOT / DELTA / FULL
    * For more in-depth explanation of each variable, we would like to refer you to the IHTSDO snowstorm GitHub documentation.