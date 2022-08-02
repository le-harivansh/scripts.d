#! /usr/bin/env zsh

set -e

# Bleachbit
echo "Cleaning the system-space using bleachbit..."
sudo bleachbit --clean $(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')
echo ""

echo "Cleaning the user-space using bleachbit..."
bleachbit --clean $(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')
echo ""

# System
echo "Cleaning journalctl..."
sudo journalctl --vacuum-time=30days --vacuum-size=50M
echo ""

# Pacman
echo "Removing orphan packages..."
sudo pacman --remove --nosave --recursive $(pacman --query --unrequired --deps --quiet)
echo ""

echo "Clearing pacman's cache..."
sudo pacman --sync --clean --clean
echo ""

local docker_utilities_script="docker.zsh"

# docker
echo "Cleaning docker..."
"${0:a:h}/${docker_utilities_script}" purge
echo ""

echo "Cleanup complete."
