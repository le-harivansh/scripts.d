#! /usr/bin/env zsh

# Bleachbit

echo ""
echo "Cleaning the system-space using bleachbit..."
echo ""
sudo bleachbit --clean $(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')
echo ""
echo ""

echo ""
echo "Cleaning the user-space using bleachbit..."
echo ""
bleachbit --clean $(bleachbit --list-cleaners | sed --expression '/system\.memory/d' --expression '/system\.free_disk_space/d')
echo ""
echo ""


# System

echo ""
echo "Cleaning journalctl..."
echo ""
sudo journalctl --vacuum-time=30days --vacuum-size=50M
echo ""
echo ""


# Pacman

echo ""
echo "Removing orphan packages..."
echo ""
sudo pacman --remove --nosave --recursive $(pacman --query --unrequired --deps --quiet)
echo ""
echo ""

echo ""
echo "Clearing pacman's cache..."
echo ""
sudo pacman --sync --clean --clean
echo ""
echo ""


echo ""
echo "Cleanup complete."
echo ""
echo ""
