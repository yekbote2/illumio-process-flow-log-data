import sys
import csv

# Reference: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
def get_protocol(protocol_id: int):
    id_protocol_map = {
        6: "tcp",
        17: "udp"
    }

    if protocol_id not in id_protocol_map:
        print(f"Protocol with id: {protocol_id} not found. Set to default unknown.")

    return id_protocol_map.get(protocol_id, "unknown").lower()


def parse_logs(log_path: str) -> dict:
    port_protocol_count = {}
    try:
        with open(log_path, 'r') as logs:
            for log in logs:
                log = log.strip()
                parts = log.split(' ')

                dstport = int(parts[6])
                protocol_id = int(parts[7])
                protocol = get_protocol(protocol_id)
                
                key = (dstport, protocol)
                port_protocol_count[key] = port_protocol_count.get(key, 0) + 1
    except Exception as e:
        print(f"Error reading logs: {e}")
        
    return port_protocol_count


def get_lookup_table(lookup_table_path: str) -> dict:
    lookup_table = {}
    try:
        with open(lookup_table_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dstport = int(row['dstport'])
                protocol = row['protocol'].lower()

                key = (dstport, protocol)

                lookup_table[key] = row['tag'].strip()
    except Exception as e:
        print(f"Error reading lookup table: {e}")

    return lookup_table


def count_tags(port_protocol_count: dict, lookup_table: dict) -> dict:
    tag_count = {}
    for key, count in port_protocol_count.items():
        tag = lookup_table.get(key, "Untagged")
        tag_count[tag] = tag_count.get(tag, 0) + count

    return tag_count


def output_results(port_protocol_count: dict, tag_count: dict, output_path: str):
    try:
        with open(output_path, mode='w') as file:
            file.write("Tag Counts:\n")
            file.write("Tag, Count\n")
            for tag, count in tag_count.items():
                file.write(f"{tag}, {count}\n")
                
            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Port, Protocol, Count\n")
            for (port, protocol), count in port_protocol_count.items():
                file.write(f"{port}, {protocol}, {count}\n")
    except Exception as e:
        print(f"Error writing output: {e}")


def main(log_path: str, lookup_table_path: str, output_path: str):
    port_protocol_count = parse_logs(log_path)
    if port_protocol_count is None or len(port_protocol_count) == 0:
        print("No logs found. Please check if log file exists and is not empty.")
        return

    lookup_table = get_lookup_table(lookup_table_path)
    if lookup_table is None or len(lookup_table) == 0:
        print("Empty lookup table. All combinations marked as Untagged.")

    tag_count = count_tags(port_protocol_count, lookup_table)

    output_results(port_protocol_count, tag_count, output_path)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception("Usage: python3 process_flow_logs.py <log_path> <lookup_table_path> <output_path>")
    
    log_path = sys.argv[1]
    lookup_table_path = sys.argv[2]
    output_path = sys.argv[3]

    main(log_path, lookup_table_path, output_path)
