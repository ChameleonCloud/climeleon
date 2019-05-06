#!/usr/bin/env bash

version="${1:-master}"
tmp_dir="$(mktemp -d)"
repo="https://github.com/ChameleonCloud/climeleon"
install_dir="${CC_INSTALL_PATH:-/usr/local/bin}"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

printf "GitHub username: "
read username </dev/tty
printf "GitHub password (OR Access Token if you're using 2FA): "
read -s password </dev/tty
echo

pushd "$tmp_dir" >/dev/null
curl -u "$username:$password" -sL "$repo/archive/$version.tar.gz" \
  | tar -x --strip-components=1 \
  || {
    echo "Error pulling repository from GitHub. Make sure your username and"
    echo "password are correct, and that you have access to the repo!"
    exit 1
  }
echo "Copying scripts to $install_dir"
cp bin/* "$install_dir/"
popd >/dev/null
