#! /usr/bin/env zsh

if [ "${#}" -gt 0 ]
then
  case ${1} in

    -h | --help | *)
      echo ""
      echo "NAME"
      echo -e "\t${0} - A script to clean the system."
      echo ""
      echo "SYNOPSIS"
      echo -e "\t${0} [OPTIONS]"
      echo ""
      echo "OPTIONS"
      echo -e "\t-h | --help : Print this help message."
      echo ""

      exit 0
      ;;

  esac
fi


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
