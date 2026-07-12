#!/usr/bin/env bash
# License: GPL-2.0-or-later

iso_name="aether-ghost-os"
iso_label="AETHER_GHOST"
iso_publisher="AetherGhost OS Project <https://github.com/AETHERGHOSTOS/ghost-mode>"
iso_application="Aether Ghost Live Security OS"
iso_version="1.0.0"
install_dir="arch"
buildmodes=('iso')
bootmodes=('bios.syslinux.mbr' 'bios.syslinux.eltorito' 'uefi-ia32.grub.esp' 'uefi-x64.grub.esp' 'uefi-ia32.grub.eltorito' 'uefi-x64.grub.eltorito')
arch="x86_64"
pacman_conf="pacman.conf"
file_permissions=(
  ["/etc/shadow"]="0:0:0400"
  ["/etc/gshadow"]="0:0:0400"
  ["/etc/skel/.gnupg"]="0:0:0700"
  ["/usr/local/bin/aether-init.sh"]="0:0:0755"
)
