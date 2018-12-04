import os
import tdclient
import time
import argparse
import sys
from tabulate import tabulate

#The first thing we have to do is import the TD API KEY so we can gain access to our database.
apikey = os.getenv("TD_API_KEY")

#In this part we are going to parse the elements out of the command passed.
parser = argparse.ArgumentParser()

#Let's start with optional inputs.
parser.add_argument('--query_engine','-e',default='presto',choices=['presto','hive'], help="The available engines are Presto and Hive. Hint: use -e presto or hive")
parser.add_argument('--format','-f',default='tabular', choices=['csv','tabular'], help="The available export formats are TSV or CSV. Hint: use -f tsv or csv")
parser.add_argument('--columns','-c',default='*', help="Columns can be entered, or by default, all columns will be returned.")
parser.add_argument('--min','-m',default='NULL', help="An optional minimum unix timestamp can be entered, or by default NULL will be entered.")
parser.add_argument('--MAX','-M',default='NULL', help="An optional maximum unix timestamp can be entered, or by default NULL will be entered.")
parser.add_argument('--limit','-l',default='0',help="An optional limit to number of rows returned can defined.")

#Then let's get the required inputs.
parser.add_argument('database', help="A database name is required. Try \"evaluation_mikelafleur\".")
parser.add_argument('table', help="A table name is required. Try \"sampledata\".")

#Here we set arguments to variables, so we can use them in the query.
args= parser.parse_args()
db_name = args.database
table_name = args.table
query_engine = args.query_engine
file_format = args.format
column = args.columns
minimum = args.min
maximum = args.MAX
query_limit = args.limit

set_limit = ""

#We really only have one database, so we have to check to make sure the right one has been entered
if db_name != "evaluation_mikelafleur":
	print "\nERROR: It looks like you didn't use \"evaluation_mikelafleur\" for the database. Unfortunately, that's the only database available to you right now. Please try it again using \"evaluation_mikelafleur\"."
	sys.exit(1)
else:
	print "\n*** Using \""+db_name+"\" as the database.\n"

#We have to do the same for the table name. We only have the one table right now.
if table_name != "sampledata":
	print "ERROR: It looks like you didn't use \"sampledata\" for the table. Unfortunately, that's the only table available to you right now. Please try it again using \"sampledata\"."
	sys.exit(2)
else:
	print "*** Querying the table \""+table_name+"\".\n"

#There are only two choices for query engine, so we have to check that as well.
if query_engine == "presto" or query_engine == "hive":
	print "*** Using \""+query_engine+"\" to execute the query.\n"
else:
	print "ERROR: It looks like you didn't use \"presto\" or \"hive\" for the query engine. Unfortunately, you have to choose between the two, or use the default."
	sys.exit(3)

#There are only two choices for file formats, too, so we have to check them.
if file_format == "csv" or file_format == "tabular":
	print "*** Saving the file to \""+file_format+"\" format.\n"
else:
	print "ERROR: It looks like you didn't use \"csv\" or \"tabular\" for the file format. Unfortunately, you have to choose between the two, or use the default."
	sys.exit(4)

#So, now let's make sure that the columns that have been entered, are actually available.
#This really should be done programatically, but for expediency, let's create a list of the available columns, knowing that we'll come back an do this with a query
available_columns = ['time','id','time_','firstname','lastname','email','gender','ip','state','*']
column_list = [i for i in column.split(',')]

for check in column_list:
	if check not in available_columns:
		print "ERROR: The column \""+check+"\" is not in the table. Available columns are time, id, time_, firstname, lastname, email, gender, ip, state."
		sys.exit(5)
available_columns = "id,time_,firstname,lastname,email,gender,ip,state,time"

#Let's get a timestamp for use in the file name.
timestring = time.strftime("%m%d-%H%M%S")

# Since we are allowing null as input for them, we have to set MIN time and MAX time to UNIX timestamps
if minimum == 'NULL':
	minimum = str(0) #Min Unix timestamp value: January 1, 1970

if maximum == 'NULL':
	maximum = str(253402300799) #Max Unix timestamp value: December 31, 9999

#We have to make sure Min is smaller than Max

if minimum >= maximum:
	print "ERROR: The entered \"minimum\" value, \""+str(minimum)+"\", is not less than the entered \"maximum\" value, \""+str(maximum)+"\". Please enter the appropriate values."
	sys.exit(8)

#We have to handle limits
if query_limit.isdigit():
	if str(query_limit) == "0":
		set_limit = ""
	else:
		set_limit = " LIMIT "+str(query_limit)
else:
	print "ERROR: The limit value \""+str(query_limit)+"\" is not a number. Please enter a number to limit the number of rows returned."
	sys.exit(7)

#We are	using the Arm Treasure Data Python client in order to run the query.
with tdclient.Client(apikey) as client:
	job=client.query(db_name,"SELECT " +column+" FROM "+table_name+" WHERE TD_TIME_RANGE(time,"+minimum+","+maximum+")"+set_limit+"", type=query_engine)
	print "*** Please stand by. The job is "+job.status()+".\n"
	while not job.finished():
		time.sleep(2)
	#Ungraceful catching of no data returned.
	for row in job.result_format("csv"):
		if not row:
			print "END OF JOB: Sorry, but your query returned no records."
			sys.exit(0)
	#Trying to handle errors.
	if job.status() == 'error':
		print "ERROR: It looks like there is an error, and the query has failed. Please ensure arguments were correct, and the database name and table name are correct."
                sys.exit(6)


#Output the results of the query

#First if "csv" was entered
if file_format == "csv":
	if column == "*":
		column = available_columns
	f = open("DataReturned-"+timestring+"."+file_format,"w")
	print column
	f.write(column+"\n")
	for row in job.result_format(file_format):
		print row
		f.write(row+"\n")
		f.close()
		print "END OF JOB: Returned data is in the file \"DataReturned-"+timestring+"."+file_format+"\" on the filesystem."
        	sys.exit(0)

#Second if not "csv", then it is tabular
else:
	if column == "*":
		column = available_columns
	f = open("DataReturned-"+timestring+"."+file_format,"w")
	print(tabulate([list(row) for row in job.result()], headers=column.split(","), tablefmt='grid')+"\n")
	f.write(tabulate([list(row) for row in job.result()], headers=column.split(","), tablefmt='grid'))
	f.close()
	print "END OF JOB: Returned data is in the file \"DataReturned-"+timestring+"."+file_format+"\" on the filesystem."
	sys.exit(0)
