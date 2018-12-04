# TD Technical Challenge

As part of the vetting process, Treasure Data issues a technical challenge to applicants.

This challenge is meant to evaluate technical apptitude, particularly around data access and development tools, including Python, Java, or Ruby--all of which Treasure Data supports with client libraries.

The challenge directs that a command line tool be built that issues a query on Treasure Data to retrieve the values of a specified set of columns in a specified date/time range.

**************************************************

## To Address the Challenge

In response to the challenge, the file "query.py" was created.

**************************************************
## Installation

To install the file, copy the file "query.py" to a directory that you have read/write/execute access to, and ensure that the file has been set to executable. (This step may not be necessary if you will be using Python to invoke the file.)

## Dependencies

The file relies on the Treasure Data API Library for Python, which can be found at https://github.com/treasure-data/td-client-python.

(To install the client, follow the instructions found on the respository. Additional documentation can be found on Arm Treasure Data's Support site: https://support.treasuredata.com/hc/en-us/articles/360001264848-Python-Client)

The Treasure Data client relies on an API Key to get access to the Treasure Data server. It does this by calling the environment variable "TD_API_KEY" during runtime. Ensure that your "TD_API_KEY" has been defined with the appropriate key.

The file also utilizes the "tabulate" library. It can be installed via "pip," and more information can be found at: https://pypi.org/project/tabulate/


## Running the File

The file "query.py" was written on Linux, and in order to support alternative operating systems, the bash command referencing Python has been left out. 

In order to run, Python must be referenced. For example:

     > python ./query.py

### Expected Arguments

query.py expects several arguments to be passed as part of the command. Of these expected values, two are required: a database name and a table name.

For this exercise you must use the following:

     database = evaluation_mikelafleur
     table = sampledata

To return all rows in the table with default query engine and file format, run:

     > python ./query.py evaluation_mikelafleur sampledata

The resulting query, which will have used Presto as the query engine, will return all rows in the table, displaying them on the screen, in a tabular format, as well as writing the query results to the file system in a tabular formatted file, with extention "tabular".

query.py accepts the following, optional, arguments:

     --query_engine, -q followed by either "presto" or "hive"
     --format, -f followed by either "csv" or "tabular"
     --min, -m followed by a unix timestamp
     --MAX, -M followed by a unix timestamp
     --columns, -c followed by column names separated by a comma

          Available columns are:

               time (a Treasure Data unix timestamp, which is referenced above)
               id
               time_ (a transaction timestamp, which is an artifact of the sample data used)
               firstname
               lastname
               email
               gender
               ip 
               state

For example to execute a query that returns the email address, ip address, and state from the table, the following command would be issued:

     > python ./query.py -c email,ip,state evaluation_mikelafleur sampledata

In addition to returning the values to the console, query.py writes a file named "DataReturned-[DATE-TIME].tabular". "DATE-TIME" will be a date and time stamp of the query. If "-f csv" is passed, a file named "DataReturned-[DATE-TIME].csv" will be written.

### Exit Codes

The following exit codes are in use:

     0 - Success
     1 - Invalid database entered
     2 - Invalid table entered
     3 - Invalid query engined entered
     4 - Invalid file format entered
     5 - Column entered does not exist
     6 - Query failed
     7 - Limit set incorrectly
     8 - Min greater than Max
     
## Help
```

usage: query.py [-h] [--query_engine {presto,hive}] [--format {csv,tsv}]
                [--columns COLUMNS] [--min MIN] [--MAX MAX]
                database table

positional arguments:
  database              A database name is required. Try
                        "evaluation_mikelafleur."
  table                 A table name is required. Try "sampledata."

optional arguments:
  -h, --help            show this help message and exit
  --query_engine {presto,hive}, -e {presto,hive}
                        The available engines are Presto and Hive. Hint: use
                        -e presto or hive
  --format {csv,tsv}, -f {csv,tsv}
                        The available export formats are TSV or CSV. Hint: use
                        -f tsv or csv
  --columns COLUMNS, -c COLUMNS
                        Columns can be entered, or by default, all columns
                        will be returned.
  --min MIN, -m MIN     An optional minimum unix timestamp can be entered, or
                        by default NULL will be entered.
  --MAX MAX, -M MAX     An optional maximum unix timestamp can be entered, or
                        by default NULL will be entered.
```
## Test Queries

The file "TestQueries.txt" found in this respository contains descriptions of the text queries run as part of the instructions in the challenge.
