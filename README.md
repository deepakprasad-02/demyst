# Parse fixed width file
Your beautiful parser that generates test data and converts to csv for your use!


## Details of processing files in this repo
- `main.py` is the starting point of the program 
- `fixed_width_generator.py` implements the fixed width encoding logic that generates an encoded file in the input_data folder
- `csv_generator.py` implements a parser that will parse the fixed width file and generate a delimited csv file.
- `file_processor.py` contains an abstract class that provides the skelton for above files
- `spec.py` is used to objectify the spec.json in the program
- `entry.sh` is the entry point to the dockerfile 

## Assumptions
- You have docker installed.

## To run, you need to:
- run `docker build -t my-app .`
- once successful, to run the main program `docker run \
  -v $(pwd)/src/sol_one/input_data:/app/input_data \
  -v $(pwd)/src/sol_one/output_data:/app/output_data \
  --rm my-app main`
- To run the test, `docker run --rm my-app test``

## Results
After you finish above two steps, you should be able to see `input_data` and `output_data` folders under `src/sol_one/`

## What i learnt
- loads of pytesting and docker
- It was a fun project

## Challenges
- Most of python development was in notebooks, this task helped to learn pure python dev
- Docker is fun

## Future improvements
- Easily accommodate more parsing types
- Include more test cases like integration tests.







