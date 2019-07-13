CREATE KEYSPACE IF NOT EXISTS eddb_db
WITH replication = {'class':'NetworkTopologyStrategy', 'datacenter1' : 1};

CREATE TABLE IF NOT EXISTS eddb_db.eddb_data(
    id text PRIMARY KEY,
    schemaRef text,
    header text,
    message text
    );

COPY eddb_db.eddb_data (id,
    schemaRef,
    header,
    message)
FROM './tmp/cass_csv_data.csv' WITH DELIMITER=',' and HEADER=TRUE;
