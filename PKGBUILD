# Maintainer: RDJeffery <your.email@example.com>

pkgname=pyreto
pkgver=0.1.0
pkgrel=1
pkgdesc="A color palette management tool for Linux"
arch=('any')
url="https://github.com/RDJeffery/pyreto"
license=('MIT')
depends=('python' 'python-textual' 'python-pyperclip')
makedepends=('python-setuptools')
source=("pyreto-0.1.0.tar.gz")
sha256sums=('957fa0710eb1f5d2bdedb9de7c4e898e9ec104a9ad6eb1dcde48fa99997c88e0')  # Replace with actual checksum after creating the tarball

package() {
  cd "$srcdir/$pkgname-$pkgver"
  
  # Install Python package
  python setup.py install --root="$pkgdir/" --optimize=1 --prefix=/usr
  
  # Install license
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  
  # Create a wrapper script that uses the system Python
  mkdir -p "$pkgdir/usr/bin"
  cat > "$pkgdir/usr/bin/pyreto" << 'EOF'
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/usr/lib/python3.13/site-packages/pyreto')))
from main import main
if __name__ == '__main__':
    main()
EOF
  chmod +x "$pkgdir/usr/bin/pyreto"
} 