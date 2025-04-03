This is a Python application that downloads a file from a URL and uploads it to an Amazon S3 bucket. The source URL, S3 bucket name, and S3 file path are all configured via environment variables.

## Prerequisites

- Python 3.11 or higher (for non-container usage)
- AWS credentials with S3 write access
- Podman (for container usage)

## Setup Without Container

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd download-and-push-to-s3
```

2. Install Poetry:
```bash
pip install poetry
```

3. Install dependencies:
```bash
poetry install
```

### Configuration

Set the required environment variables:
```bash
export FILE_URL="https://example.com/file.ext"         # URL to download from
export S3_BUCKET="my-bucket"                           # S3 bucket name
export S3_FILE_PATH="path/file.ext"                    # S3 destination path
export AWS_ACCESS_KEY_ID="your-access-key"             # AWS access key
export AWS_SECRET_ACCESS_KEY="your-secret-key"         # AWS secret key
```

### Running

Execute the script:
```bash
poetry run python download-and-push-to-s3.py
```

## Setup With Container

### Building the Container Image

1. Clone this repository:
```bash
git clone <repository-url>
cd download-and-push-to-s3
```

2. Build the Podman image:
```bash
podman build -t download-and-push-to-s3 .
```

### Running the Container

Run the container with environment variables:
```bash
podman run \
  -e FILE_URL="https://example.com/file.ext" \
  -e S3_BUCKET="my-bucket" \
  -e S3_FILE_PATH="path/file.ext" \
  -e AWS_ACCESS_KEY_ID="your-access-key" \
  -e AWS_SECRET_ACCESS_KEY="your-secret-key" \
  download-and-push-to-s3
```

## Notes

- The script uses `requests` for downloading and `boto3` for S3 upload
- The Podman image uses a distroless Python base for minimal size and security
- Ensure your AWS credentials have appropriate permissions for the target S3 bucket
- The script includes error handling and cleanup of temporary files

## Troubleshooting

- Verify all environment variables are set correctly
- Check AWS credentials and bucket permissions
- Ensure the source URL is accessible
- For container usage, confirm Podman is running properly

The instructions assume a Unix-like environment, but they can be adapted for Windows by changing the environment variable syntax to use `set` instead of `export`.
