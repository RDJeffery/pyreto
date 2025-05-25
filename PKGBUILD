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
source=("$pyreto-0.1.0.tar.gz")
sha256sums=('e37fabf3154b0421533f6fd324f8b5a1d193b1254e3263582d4b6d37eae858e8')  # Replace with actual checksum after creating the tarball

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir/" --optimize=1
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
} 