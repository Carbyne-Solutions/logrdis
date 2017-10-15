# What does it do?
This script is a log munger; it receives a deterministic input string via a configurable socket and munges the input string based on a pre-determined configurable.

The outcome is a transfer system that takes a standardized input stream, matches it with a regular expression pattern and stores it in a database.

It's original use-case is to convert Squid access_logs, streamed via TCP, into a PostgreSQL database. Via the extendable YAML configuration gimmick, this script can be adapted to similar, but different, use cases.

# How do I use it?
## Create the YAML configuration directive
```
---
engine: 'sqlite:///:memory:'
socket: 'udp'
listen: '4444'

ingest:
  # Example of space separated log output
  data: 'L(?P<id>\S+)\s+(?P<time>\S+)\s+(?P<time_response>\S+)\s+(?P<mac_source>\S+)\s+(?P<ip_source>\S+)\s+(?P<squid_request_status>\S+)\s+(?P<http_status_code>\S+)\s+(?P<http_reply_size>\S+)\s+(?P<http_request_method>\S+)\s+(?P<http_request_url>\S+)\s+(?P<user_name>\S+)\s+(?P<squid_hier_code>\S+)\s+(?P<ip_destination>\S+)\s+(?P<http_content_type>\S+)'
  rotate: 'R'
  truncate: 'T'
  reopen: 'O'
  flush: 'F'
  rotatecount: 'r(\d+)'
  bufferoutput: 'b(\d)'

process:
  data:
    action: store
    tablename: access_logs
    pk: id
    schema:
      id: Integer
      time: String
      time_response: String
      mac_source: String
      ip_source: String
      squid_request_status: String
      http_status_code: String
      http_reply_size: Integer
      http_request_method: String
      http_request_url: String
      user_name: String
      squid_hier_code: String
      ip_destination: String
      http_content_type: String
  rotate:
    action: drop
  truncate:
    action: drop
  reopen:
    action: drop
  flush:
    action: drop
  rotatecount:
    action: drop
  bufferoutput:
    action: drop
```

* Configure the engine to match your system configuration. For more information, reference [SQLAlchemy Engines](http://docs.sqlalchemy.org/en/latest/core/engines.html).
* Configure the listener socket to be of `socket` type ('udp' or 'tcp') and `listen` on port 4444.
* The ingest key specifies the intake regular expressions. Each regular expression should define match groups that correspond to the table columns.
* Table columns are defined under the `process` key. Here the table metadata and columns are defined. The keys are self-explanatory. Reference: https://github.com/paranormal/blooper#squid-configuration for more information on the origin of the table column definitions in this sample file. 
* The script will declare the database fields on the fly during startup.