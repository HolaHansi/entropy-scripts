# Entropy Scripts

## Data Extraction
Scripts for extracting historical info from the top 500 rankings from alexa.com as they've changed since 2009 till today. The scripts will populate two collections in a mongodb: **sites and handlers.**

Every url that has ever appeared on a top 500 ranking on alexa.com will have a document in the **sites** collection containing a list of snapshots, each of which will have a timestamp and fields of historical info such as a list of IPs and a meta tag description. For every distinct ip in **sites** there will be a handler in the **handlers** collection to whom it is currently allocated or assigned. Every handler document will have fields recording name, org, associated IPs in **sites** and the range of addresses presently under its control. 

In order to run these scripts you'll need an instance of a mongodb server running locally with the default settings. If mongo is already installed just run mongod in the background: 
```
mongod &
``` 
Make sure you have the dependencies installed
```
pip install -r requirements.txt
```
Now call
```
python main.py
```
The scripts will take hours to terminate as they require a lot of network traffic. 

## Statistics and Analysis
running stats.py will create a stats folder in the working directory with three files: 
```
handlerNumIps.json      ipsPrDate.json          snapshotHandlers.json
```
**handlerNumIps.json** contains a list of all the handlers and the number of IPs they are controlling of all the distinct ips in the sites collection.

**ipsPrDate.json** has for every snapshot date a record of all the IPs belonging to some site on the top 500 alexa ranking of that date. 

**snapshotHandlers.json** has for every snapshot date, a list of handlers, each with a field specifying the number of IPs in the top 500 alexa ranking that they were controlling on the date of the snapshot. 

*note that*: it's probably an issue that all counts are based on distinct ips and not all ips, as it's possible that two sites may share a common IP
