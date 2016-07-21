# Entropy Scripts
Scripts for extracting historical info from the top 500 rankings from alexa.com as they've changed since 2009 till today. The scripts will populate two collections in a mongodb: **sites and handlers.**

Every url that has ever appeared on a top 500 ranking on alexa.com will have a document in the **sites** collection containing a list of snapshots, each of which will have a timestamp and fields of historical info such as a list of IPs and a meta tag description. For every distinct ip in **sites** there will be a handler in the **handlers** collection to whom it is currently allocated or assigned. Every handler document will have fields recording name, org, associated IPs in **sites** and the range of addresses presently under its controls. 

In order to run these scripts you must have an instance of a mongodb server running locally with the default settings. If mongo is already installed just run: 
```
mongod
``` 
Then call 
```
python main.py
```
