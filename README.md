This service is designed to run as a Google Cloud function and then scheduled with GCS Scheduler to run every hour or so. 

It just dumps the data from the Burk into firebase for the dashboard page to do what is needed with.

Cost to run just this cron service and store the data with about 3 months of data polled hourly has been aprox 0.03-0.05$ CAD per month.

Tested on:

Arc Plus Touch FW Version: 	5.0.17.3