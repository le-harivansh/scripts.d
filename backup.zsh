#! /usr/bin/env zsh

if [ "${#}" -gt 0 ]
then
  case ${1} in

    -h | --help | *)
      echo ""
      echo "NAME"
      echo -e "\t${0} - A script to back up files on the system."
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


echo ""
echo "Decrypting passwords..."
echo ""

local password_store_location="${HOME}/.password-store"
local passwords_file=$(mktemp "passwords.XXXXXXXX.txt")

for password_file_path in ${password_store_location}/**/*.gpg
do
  local username="$(echo ${password_file_path} | sed --expression "s#${password_store_location}/##g" --expression 's#\.gpg##g')"

  echo "${username} $(pass ${username})" >> ${passwords_file}
done

echo ""
echo ""


local backup_file="backup.$(date +%s).tar.bz2"

echo ""
echo "Backing up files..."
echo ""
tar --dereference --create --verbose --bzip2 --exclude '.directory' --file ${backup_file} ${passwords_file} --directory ${HOME} .vimrc .zshenv .zshrc Documents Pictures
echo ""
echo ""


echo ""
echo "Encrypting backup file..."
echo ""
gpg --symmetric ${backup_file}
echo ""
echo ""


echo ""
echo "Cleaning up..."
echo ""
rm ${backup_file}
rm ${passwords_file}
echo ""
echo ""


echo ""
echo "Backup complete."
echo ""
echo ""
