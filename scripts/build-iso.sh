#!/bin/bash
# AOS Build Script — Phase 1 Week 4
# Base: Ubuntu 24.04 LTS (Noble)
# Desktop: Cinnamon 6.0.4
set -e

AOS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$AOS_ROOT/aos-build"
PACKAGES_DIR="$AOS_ROOT/packages"
DEB_REPO_DIR="$AOS_ROOT/repo"

NOBLE="$BUILD_DIR/noble"
SQUASH="$BUILD_DIR/squashfs.root"
ISO="$BUILD_DIR/aos-$(date +%Y%m%d).iso"

echo "=== AOS ISO Build ==="
echo "Build root: $BUILD_DIR"
echo "Output ISO: $ISO"

# ── Step 1: Base system via debootstrap ──
if [ ! -d "$NOBLE" ]; then
    echo "[1/6] Running debootstrap (Ubuntu 24.04 noble)..."
    sudo debootstrap --arch amd64 noble "$NOBLE" \
        http://mirrors.tuna.tsinghua.edu.cn/ubuntu
else
    echo "[1/6] Base system exists, skipping debootstrap."
fi

# ── Step 2: Install core packages ──
echo "[2/6] Installing core packages..."
sudo chroot "$NOBLE" /bin/bash -c "
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
    cinnamon \
    wine \
    fcitx5 fcitx5-rime fcitx5-chinese-addons \
    locales language-pack-zh-hans \
    linux-generic linux-firmware \
    grub-pc grub2-common \
    squashfs-tools xorriso \
    debootstrap \
    sudo nano curl wget git \
    network-manager \
    gdm3 \
    gnome-terminal \
    nautilus \
    && apt-get clean
"

# ── Step 3: Install AOS custom packages ──
echo "[3/6] Installing AOS packages..."
if [ -d "$PACKAGES_DIR" ]; then
    sudo chroot "$NOBLE" /bin/bash -c "
        dpkg -i /packages/*.deb || apt-get install -f -y
    "
fi

# ── Step 4: AOS customizations ──
echo "[4/6] Applying AOS customizations..."
sudo chroot "$NOBLE" /bin/bash -c "
    # Set locale
    locale-gen zh_CN.UTF-8 en_US.UTF-8

    # Configure Fcitx5 as default IME
    im-config -n fcitx5
    mkdir -p /etc/skel/.config/fcitx5
    cp -r /usr/share/fcitx5/rime /etc/skel/.config/fcitx5/

    # Set default display manager to GDM (branded)
    echo '/usr/sbin/gdm3' > /etc/X11/default-display-manager

    # Enable autologin (for demo/testing only)
    mkdir -p /etc/gdm3/custom.conf.d/
    cat > /etc/gdm3/custom.conf.d/01-aos.conf << 'GDM'
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=aos
GDM

    # AOS branding
    mkdir -p /usr/share/aos
    echo 'AOS_VERSION=1.0.0-alpha' > /usr/share/aos/version
"

# ── Step 5: Build squashfs ──
echo "[5/6] Building squashfs..."
sudo rm -rf "$SQUASH"
sudo mkdir -p "$SQUASH"
sudo rsync -a "$NOBLE/" "$SQUASH/"
sudo mksquashfs "$SQUASH" "$BUILD_DIR/aos.squashfs" \
    -comp xz -b 1M -no-xattrs

# ── Step 6: Build ISO ──
echo "[6/6] Building ISO..."
mkdir -p "$BUILD_DIR/iso"
sudo xorriso \
    -as mkisofs \
    -R -J -A 'AOS 1.0' \
    -b isolinux.bin -c boot.cat \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
    -isohybrid-mbr /usr/lib/syslinux/bios/mbr.bin \
    -o "$ISO" "$BUILD_DIR/iso/"

echo "=== Build complete: $ISO ==="
ls -lh "$ISO"
