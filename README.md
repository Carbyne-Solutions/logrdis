# What does it do?
This script is a log munger and redirector; it receives a deterministic input string via a configurable socket and munges the input string based on a pre-determined configurable.

The outcome is a transfer system that takes a standardized input stream, matches it with a regular expression pattern and stores it in a database.

It's original use-case is to convert Squid access_logs, streamed via TCP, into a PostgreSQL database. Via the extendable YAML configuration gimmick, this script can be adapted to similar, but different, use cases. Reference the [Squid LogModules Documentation](https://wiki.squid-cache.org/Features/LogModules) for more information.

# How do I use it?
## Microservice Architecture
Logrdis is designed to be used as a micro service. As such, it is best used in combination with a docker container cluster, consisting of the service with streaming output and a database container. An example docker-compose.yml configuration file:
```yaml
version: "3"

services:
  db:
    image: postgres
    volumes:
      - dbdata:/var/lib/postgresql/data:rw
    environment:
      - POSTGRES_PASSWORD=default
      - POSTGRES_USER=squid
      - POSTGRES_DB=squidb

  squid:
    image: carbyne/squid
    links:
      - db
    depends_on:
      - db
    environment:
      - PGPASSWORD=default
    ports:
      - 3128:3128
      - 3129:3129
    volumes:
      - squiddata:/etc/squid:rw

  logrdis:
    image: carbyne/logrdis
    links:
      - squid
      - db
    depends_on:
      - squid
      - db
    volumes:
      - logrdisetc:/etc/logrdis:rw
      - logrdisdb:/var/lib/logrdis/logrdis.sql:rw
    environment:
      - DB_PROTO='postgresql'
      - DB_HOST='db'
      - DB_USER='squid'
      - DB_PASS='default'
      - DB_NAME='squidb'

volumes:
  dbdata:
  squiddata:
  logrdisetc:
  logrdisdb:
```

## Configuration
Logrdis uses a YAML file to configure the stream redirector. There are a few key configuration options:

### Top Level
* engine *(str.)*: defines the SQL backend engine to use. Valid keys: reference [the SQLAlchemy Engines reference page](http://docs.sqlalchemy.org/en/latest/core/engines.html).
* socket *(str.)*: the protocol of the socket on which the stream redirector should listen. Valid keys: `tcp` or `udp`.
* listen_host *(str.)*: the canonical IP address on which the stream redirector listens for packet streams; if blank indicates 0.0.0.0.
* listen_port *(int.)*: the canonical port number on which the stream redirector listens for packet streams.

### Stream definitions
* ingest: *(list.)*: defines the streams which are to match. Each key defines the stream's internal reference (within the logrdis framework) and can then be referenced from the process section. In fact, each key **should** have a corresponding process section in order to process the stream. If a process key entry is not given, the default action is for the stream to be dropped.
 * Each stream is defined by a single line, separated by a newline character. Within the stream, each match must be clearly marked using the named groups feature in the Python regular expression matching engine.
 * For instance, to line up a match of **id** that should be stored in the **id** column of the backend database, identify the regular expression matching group accordingly: `(?P<id>\d+)`. The preceeding example demonstrates a match of 1 or more digits, whose match group can later be identified by the **id** string.
* process: *(dict.)*: defines the RDBMS schema of the resultant database; each **key** identifies a key in the **ingest** section (described above).
 * Each schema row should have an identical match in the *ingest* list.
 * action *(str.)*: *required*; identifies the action of each section. Can either be **store** or **drop**. When set to **store** the system will redirect the log into the database table. When set to **drop** the stream is dropped.
 * tablename *(str.)*: *required*; identifies the resultant name of the table.
 * pk *(str.)*: *required*; identifies the *primary key* of the table schema. This **must** identify one of the column names as the primary key of the table.

## YAML Configuration Example
```yaml
---
engine: 'sqlite:///test.sql'
socket: 'tcp'
listen_host: ''
listen_port: 4444

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
    action: drop%

```

Read the [License](LICENSE)