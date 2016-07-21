# Entropy Scripts
Scripts for extracting historical info on the top 500 rankings from alexa.com as they've changed since 2009. The scripts will populate two collections in a mongodb: ** sites, handlers. **


Every url that's ever appeared on a top 500 ranking on alexa.com will have a document in the **sites** collection containing a list of snapshots each of which will have a timestamp and historical info such as the IPs and a meta tag description. For every distinct ip in **sites** there will be a handler in the **handlers** collection to which it belong. Every handler document will keep info on name, org, associated IPs in **sites** and the range of address that it currently controls. 
