# Networking_tool
# Networking Monitoring Tool

A comprehensive Python-based network monitoring tool for tracking network performance, connectivity, and system resources.

## Overview

This tool provides real-time monitoring and diagnostics for network infrastructure, including ping monitoring, DNS resolution checking, traceroute analysis, and system resource tracking. Perfect for network administrators, DevOps engineers, and anyone needing to maintain visibility into their network health.

## Features

- **Ping Monitor**: Track network latency and availability of hosts
- **DNS Checker**: Verify DNS resolution and query response times
- **Traceroute Monitor**: Analyze network paths and identify routing issues
- **Resource Monitor**: Track system CPU, memory, and network usage
- **Configurable Alerts**: Set thresholds for automated notifications
- **YAML Configuration**: Easy-to-manage configuration files

## Prerequisites

- Python 3.7 or higher
- Administrator/root privileges (required for ICMP operations)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Networking_tool
```

2. Install required dependencies:
```bash
pip install -r requiremnts.txt
```

## Dependencies

- `ping3` - ICMP ping functionality
- `psutil` - System and network resource monitoring
- `PyYAML` - Configuration file parsing
- `dnspython` - DNS query operations

## Configuration

Edit the `config/config.yml` file to customize monitoring parameters:

```yaml
# Example configuration
hosts:
  - google.com
  - 8.8.8.8
  
dns_servers:
  - 8.8.8.8
  - 1.1.1.1

ping_interval: 60
alert_threshold: 100
```

## Usage

Run the monitoring tool:

```bash
python main.py
```

### Running with elevated privileges

On Linux/Mac:
```bash
sudo python main.py
```

On Windows (run as Administrator):
```bash
python main.py
```

## Project Structure

```
Networking_tool/
├── config/
│   └── config.yml          # Configuration file
├── core/
│   ├── dns_checker.py      # DNS resolution monitoring
│   ├── ping_monitor.py     # Ping/latency monitoring
│   ├── resource_monitor.py # System resource tracking
│   ├── traceroute_monitor.py # Route path analysis
│   └── utils.py            # Helper utilities
├── tests/
│   └── test_ping_monitor.py # Unit tests
├── main.py                  # Main application entry point
├── requiremnts.txt          # Python dependencies
└── README.md               # This file
```

## Features in Development

- [ ] Web dashboard for real-time monitoring
- [ ] Alert notifications (email, Slack, etc.)
- [ ] Historical data logging and visualization
- [ ] Network bandwidth testing
- [ ] Port scanning capabilities
- [ ] Export reports (CSV, JSON, PDF)

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

<Feel free to use this tool for personal or commercial projects. Just please don’t redistribute or modify it without asking first!>

## Support

For issues, questions, or contributions, please open an issue in the repository.

## Roadmap

- **Phase 1**: Core monitoring features (ping, DNS, traceroute)
- **Phase 2**: Resource monitoring and alerting
- **Phase 3**: Web interface and data visualization
- **Phase 4**: Advanced analytics and reporting

## Troubleshooting

**Permission Errors**: Ensure you're running with administrator/root privileges, as ICMP operations require elevated permissions.

**Module Not Found**: Verify all dependencies are installed with `pip install -r requiremnts.txt`

## Author

Souf

## Acknowledgments

- Built with Python and open-source libraries
- Inspired by network monitoring best practices
