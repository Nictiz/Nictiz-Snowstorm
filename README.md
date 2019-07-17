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
For testing purposes and example only! This script has not been thoroughly tested, and does not contain any error handling or safety measures.
Remember to start your snowstorm service with read only disabled! [edit in ./docker-compose.yml]

1) Download all release files you want to use in this folder (./ingest).

2) cd into the ingest folder ./ingest

3) You can either use the prebuilt docker image available on the docker repository, or build your own.

    3a) Use the prebuilt image nictiz/snowstorm-ingest:latest

    3b) Build your own from source:
    docker build -f Dockerfile-ingest -t nictiz/snowstorm-ingest .

4) Run the docker container in one of two ways:

    A) Import all release files in the ./ingest folder, or;

    B) Specify the specific release filename and codebase

    For A, continue to step 5, for B, continue to step 6.

5)  Import all files in the folder

    A) Run headless, only receives output after finishing:
    docker run --rm --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest [SERVERURL:PORT] [IMPORT-TYPE]

    B) Run interactive, with output to command line:
    docker run --rm -it --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest [SERVERURL:PORT] [IMPORT-TYPE]

    This will import all .zip release files in the ./ingest folder to snowstorm/elasticsearch in the same codebase. This tool has been developed to provide a way to quickly launch an up-to-date snowstorm server, if you wish to use the codebase and versioning options of snowstorm, feel free to use this script as an example for your usecase.

    * Replace:
    [SERVERURL:PORT] -> ie. your.server.com:8080
    [IMPORT-TYPE] -> SNAPSHOT / DELTA / FULL
    * For more in-depth explanation of each option, we would like to refer you to the IHTSDO snowstorm GitHub documentation.

6) Specify the release files to be imported

    A) Run headless, only receives output after finishing:
    docker run --rm --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest [SERVERURL:PORT] [IMPORT-TYPE] "[FILENAME]" [CODEBASE] [SHORTNAME]

    B) Run interactive, with output to command line:
    docker run --rm -it --mount src=$(pwd),target=/app/,type=bind nictiz/snowstorm-ingest [SERVERURL:PORT] [IMPORT-TYPE] "[FILENAME]" [CODEBASE] [SHORTNAME]

    This will import the specified .zip release file in the ./ingest folder to snowstorm/elasticsearch in the specified codebase. This tool has been developed to provide a way to quickly launch an up-to-date snowstorm server, if you wish to use the versioning options of snowstorm, feel free to use this script as an example for your usecase.

    * Replace:
    [SERVERURL:PORT] -> ie. your.server.com:8080
    [IMPORT-TYPE] -> SNAPSHOT / DELTA / FULL
    [FILENAME] -> Release filename .zip
    [CODEBASE] -> CODEBASE for your import, ie. MAIN
    [SHORTNAME] -> SHORTNAME for your codebase, ie. SNOMEDCT
    * For more in-depth explanation of each option, we would like to refer you to the IHTSDO snowstorm GitHub documentation.