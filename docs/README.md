# QSCAT Documentation

This directory contains the Sphinx documentation for QSCAT.

## Building the Documentation

### Prerequisites

- Python 3.6 or later
- pip

### Installation

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Building

From the `docs/` directory:

1. Build the HTML documentation:

   ```bash
   make html
   ```

2. The built documentation will be in `build/html/`. Open `build/html/index.html` in your browser to view it.

### Other Build Options

- `make clean`: Remove the build directory
- `make help`: Show available targets

### Read the Docs

The documentation is automatically built and hosted on Read the Docs. Configuration is in `.readthedocs.yaml`.
