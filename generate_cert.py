#!/usr/bin/env python3
"""
Generate self-signed SSL certificate for HTTPS server
"""

import os
import sys
from datetime import datetime, timedelta

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("❌ Error: cryptography library not found")
    print("\nInstalling required dependency...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    print("\n✓ Dependency installed. Please run this script again.")
    sys.exit(0)


def generate_self_signed_cert(
    cert_file="cert.pem",
    key_file="key.pem",
    hostname="localhost",
    days_valid=365
):
    """
    Generate a self-signed SSL certificate

    Args:
        cert_file: Path to save certificate file
        key_file: Path to save private key file
        hostname: Hostname for the certificate
        days_valid: Number of days the certificate is valid
    """
    print("\n" + "=" * 70)
    print("🔐 SSL Certificate Generator")
    print("=" * 70)

    # Generate private key
    print("\n[1/4] Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    print("✓ Private key generated")

    # Generate certificate
    print("\n[2/4] Generating certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Ollama Voice Assistant"),
        x509.NameAttribute(NameOID.COMMON_NAME, hostname),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=days_valid)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(hostname),
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    print("✓ Certificate generated")

    # Save private key
    print(f"\n[3/4] Saving private key to {key_file}...")
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"✓ Private key saved")

    # Save certificate
    print(f"\n[4/4] Saving certificate to {cert_file}...")
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"✓ Certificate saved")

    print("\n" + "=" * 70)
    print("✓ SSL Certificate Generation Complete!")
    print("=" * 70)
    print(f"\nCertificate: {cert_file}")
    print(f"Private Key: {key_file}")
    print(f"Valid for:   {days_valid} days")
    print(f"Hostname:    {hostname}")
    print("\n⚠️  This is a self-signed certificate for development/local use only.")
    print("    Browsers will show a security warning - this is expected.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import ipaddress

    # Check if files already exist
    if os.path.exists("cert.pem") or os.path.exists("key.pem"):
        print("\n⚠️  Warning: Certificate files already exist!")
        response = input("Do you want to overwrite them? [y/N]: ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)

    # Get hostname
    print("\n" + "=" * 70)
    print("SSL Certificate Configuration")
    print("=" * 70)

    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"\nDetected local IP: {local_ip}")
    except:
        local_ip = "127.0.0.1"

    print("\nEnter hostname for certificate (press Enter for localhost):")
    print(f"  Suggestions: localhost, {local_ip}, or your domain name")
    hostname = input("\nHostname: ").strip() or "localhost"

    # Get validity period
    print("\nEnter number of days the certificate should be valid (default: 365):")
    days_str = input("Days: ").strip()
    days_valid = int(days_str) if days_str else 365

    # Generate certificate
    generate_self_signed_cert(
        cert_file="cert.pem",
        key_file="key.pem",
        hostname=hostname,
        days_valid=days_valid
    )
