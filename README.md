# illumio-process-flow-log-data

### Parse flow logs

- A python program that parses flow logs to count port/protocol combinations and tags associated with them.
- Port/Protocol combinations are matched to tags based on a lookup table.
- Counts are written to a given output file.

### How to run

Requirements:
- A working python environment is required to execute the program

Usage:
- python process_flow_logs.py <logs_path> <lookup_table_path> <output_path>

Program accepts all files as command line arguments

### Tests

Below scenarios have been tested:
- Logs file not found or empty
- Lookup table file not found or empty
- 10MB logs file
- 10,000 mappings in lookup table

### Assumptions/Working

- Protocol keywords are fetched from a csv found here : https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml]
- protocols-numbers-1.csv must be present in the cwd for the program to execute
- Only dstport is considered
- Tag counts are increased by the total number of port/protocol counts found associated with that tag

Example:

Lookup table:

port, protocol, tag
20, tcp, sv_p1

Protocol counts:

port, protocol, count
20,tcp,5

Tag counts:

tag, count
sv_p1, 5

- Tag matches are case-insensitive
- Protocol matches are case-insensitive
- Lookup table file is not malformed
- Logs file is not malformed and follows the version 2 format [Reference: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields]
- Python script is provided. Executable can be created via pyinstaller if needed

### Complexity

n = number of log lines
m = number of lookup table entries

Worst case: each log line corresponds to a unique port/protocol combination

Space: O(n + m) 
Time: O(n + m)

Since, n >> m as log files will generally be huge when compared to a lookup table:

Space: O(n)
Time: O(n)

### Improvements
- Performance can be drastically improved if Map/Reduce is used
