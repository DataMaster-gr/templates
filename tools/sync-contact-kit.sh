#!/usr/bin/env bash
# Copies the master contact kit (contact-kit/dm-contact) into every template
# (single-page sites in websites/ and multi-page sites in multipage/).
# Run it after changing anything in contact-kit/dm-contact/.
set -euo pipefail
cd "$(dirname "$0")/.."
for t in websites/*/ multipage/*/; do
    rm -rf "${t}dm-contact"
    cp -R contact-kit/dm-contact "${t}dm-contact"
    echo "updated ${t}dm-contact"
done
