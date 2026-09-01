import socket
import sys
from urllib.parse import urlparse

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


CHECK_URLS = {
    "PyPI": "https://pypi.org",
    "Amazon Bedrock Runtime": "https://bedrock-runtime.us-east-1.amazonaws.com",
}


def check_python():
    print(f"[INFO] Python: {sys.version.split()[0]}")

    if sys.version_info < (3, 11):
        print("[FAIL] Python 3.11+ is recommended.")
        return False

    print("[OK] Python version")
    return True


def check_dependencies():
    dependencies = [
        "boto3",
        "faiss",
        "numpy",
        "streamlit",
        "dotenv",
    ]

    success = True

    for package in dependencies:
        try:
            __import__(package)
            print(f"[OK] Dependency: {package}")
        except ImportError:
            print(f"[FAIL] Missing dependency: {package}")
            success = False

    return success


def check_dns(url):
    hostname = urlparse(url).hostname

    try:
        ip = socket.gethostbyname(hostname)
        print(f"[OK] DNS: {hostname} -> {ip}")
        return True
    except socket.gaierror as error:
        print(f"[FAIL] DNS resolution failed for {hostname}: {error}")
        return False


def check_https(name, url):
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
        )

        # Bedrock root commonly returns 404.
        # Any HTTP response proves that the endpoint was reachable.
        print(
            f"[OK] HTTPS: {name} reachable "
            f"(HTTP {response.status_code})"
        )

        return True

    except requests.RequestException as error:
        print(f"[FAIL] HTTPS: {name} unreachable")
        print(f"       {error}")
        return False


def check_aws_identity():
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()

        print(
            f"[OK] AWS authentication: "
            f"Account {identity['Account']}"
        )

        return True

    except (BotoCoreError, ClientError) as error:
        print("[FAIL] AWS authentication failed")
        print(f"       {error}")
        return False


def main():
    print("\nKB AI DevOps Study Buddy - Preflight Check")
    print("=" * 50)

    checks = []

    checks.append(check_python())
    checks.append(check_dependencies())

    for name, url in CHECK_URLS.items():
        checks.append(check_dns(url))
        checks.append(check_https(name, url))

    checks.append(check_aws_identity())

    print("=" * 50)

    if all(checks):
        print("\n✅ All preflight checks passed.")
        print("Application is ready to start.")
        return 0

    print("\n❌ One or more preflight checks failed.")
    print("Resolve the failures before starting the application.")
    return 1


if __name__ == "__main__":
    sys.exit(main())