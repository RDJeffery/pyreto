#!/bin/bash

# Create a tarball of the current directory
tar -czvf pyreto-0.1.0.tar.gz --exclude=".git" --exclude="venv" --exclude="__pycache__" .

# Calculate the SHA256 checksum of the tarball
checksum=$(sha256sum pyreto-0.1.0.tar.gz | cut -d ' ' -f 1)

# Update the PKGBUILD with the correct checksum
sed -i "s/sha256sums=('SKIP')/sha256sums=('$checksum')/" PKGBUILD

echo "Tarball created: pyreto-0.1.0.tar.gz"
echo "PKGBUILD updated with checksum: $checksum" 