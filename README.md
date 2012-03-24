Browser request workflow:

    1. A request comes.
    2. Identify which channel the request comes from.
    3. Get data if available, or wait for data.
    4. Response.

Web event update workflow

    1. Web generates event data.
    2. Identify which users should get the data.
    3. Push to every channel belonging to these users.

The Comet System
-------------------

A channel is identified by `user_id` and `location`, where location is the
complete URL of the current page. We represent a channel in Redis using a sorted
set:

    Key: channel:<user_id>:<location>
    Type: sorted set
    Value: <sequence id>
    Score: Creation Time
          (after TTL the item will be garbage collected by a separate process)

The sequence ID records the index of the actual data (a JSON object) stored in
a Redis hash structure:

    Key: channel_data:<user_id>:<location>
    Field: <sequence id>
    Value: JSON string (gzipped to reduce memory footprint)

Since we are using separate garbage collectors to cleanup these Redis keys, we
do not need connections to keep track of open connections anymore.
