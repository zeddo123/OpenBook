# Basic P2P network protocol
## Discovering peers

The discovering process is done by ussing a seed server.
After the initial handshake,The seed server will send a list of active nodes in this manner:
    
    {
    'information_type': 'post_peers',
    'nodeid': 'SeedServer',
    'number_queue': self.number_queue,
    'known_peers': {'number in queue': UUID:IP:PORT},
    }
    

## Connecting to peers
Using exponential uuid distance referencing, the node will connect to the 
_number in queue_ + 2^x