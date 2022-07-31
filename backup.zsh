#! /usr/bin/env zsh

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


local backup_file="$(date '+%Y-%m-%d.%s').tar.bz2"

echo ""
echo "Backing up files..."
echo ""
tar --dereference --create --verbose --bzip2 --exclude '.directory' --file ${backup_file} ${passwords_file} --directory ${HOME} Documents Pictures
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
