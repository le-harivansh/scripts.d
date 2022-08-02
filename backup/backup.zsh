#! /usr/bin/env zsh

set -e

echo "Sourcing environment variables..."
set -a
source "${0:a:h}/.env"
set +a

[ -z ${BACKUP_GPG_ENCRYPTION_PASSPHRASE} ] && echo "The BACKUP_GPG_ENCRYPTION_PASSPHRASE variable should be set." && exit 1

local working_directory="$(mktemp -d)"

echo "Going into ${working_directory}..."
pushd ${working_directory}

local password_store_location="${HOME}/.password-store"
local passwords_file="passwords.txt"

echo "Decrypting passwords..."
for password_file_path in ${password_store_location}/**/*.gpg
do
  local username="$(echo ${password_file_path} | sed --expression "s#${password_store_location}/##g" --expression 's#\.gpg##g')"

  echo "${username} $(pass ${username})" >> ${passwords_file}
done

local backup_file="$(date '+%Y-%m-%d.%s').tar.bz2"

echo "Backing up files:"
tar --dereference --create --verbose --bzip2 --exclude '.directory' --file ${backup_file} ${passwords_file} --directory ${HOME} Documents Pictures

echo "Encrypting backup file..."
gpg --sign --symmetric --no-symkey-cache --batch --pinentry-mode loopback --passphrase "${BACKUP_GPG_ENCRYPTION_PASSPHRASE}" ${backup_file}

local encrypted_backup_file="${backup_file}.gpg"

echo "Going back to the previous working directory..."
popd

echo "Moving ${working_directory}/${encrypted_backup_file} to $(pwd)..."
mv "${working_directory}/${encrypted_backup_file}" .

echo "Cleaning up..."
rm -rf ${working_directory}

echo "Backup complete."
