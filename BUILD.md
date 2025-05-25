# Building Pyreto for Arch Linux

This guide explains how to build the Pyreto package for Arch Linux using a PKGBUILD and a local tarball.

## Prerequisites
- Arch Linux or compatible distribution
- `base-devel` group installed (for `makepkg`)
- Python 3.8+
- Required Python packages: `textual`, `pyperclip`, `setuptools` (these will be installed as dependencies)

## Steps

### 1. Prepare the Source Tarball

The PKGBUILD expects a tarball named `pyreto-0.1.0.tar.gz` containing a directory `pyreto-0.1.0` with all project files inside.

```bash
cd ..
cp -r pyreto pyreto-0.1.0
# Remove any unwanted files (e.g., venv, .git, __pycache__)
tar --exclude='.git' --exclude='venv' --exclude='__pycache__' -czvf pyreto-0.1.0.tar.gz pyreto-0.1.0
mv pyreto-0.1.0.tar.gz pyreto/
cd pyreto
```

### 2. Update PKGBUILD

- Set the `source` line to:
  ```
  source=("pyreto-0.1.0.tar.gz")
  ```
- Update the `sha256sums` line with the checksum from:
  ```
  sha256sum pyreto-0.1.0.tar.gz
  ```

### 3. Build the Package

```bash
makepkg -f
```

This will create a file like `pyreto-0.1.0-1-any.pkg.tar.zst`.

### 4. Install the Package

```bash
sudo pacman -U pyreto-0.1.0-1-any.pkg.tar.zst
```

### 5. Run Pyreto

After installation, run:
```bash
pyreto
```

---

## Notes
- If you want to submit to the AUR, follow the [AUR guidelines](https://wiki.archlinux.org/title/Arch_User_Repository#AUR_submission_guidelines).
- Make sure to update the version numbers in PKGBUILD and tarball as you release new versions. 