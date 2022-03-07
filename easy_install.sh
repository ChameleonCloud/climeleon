#!/usr/bin/env bash

version="${1:-master}"
tmp_dir="$(mktemp -d)"
repo="https://github.com/ChameleonCloud/climeleon"
install_dir="${CHI_INSTALL_PATH:-/usr/local/bin}"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

pushd "$tmp_dir" >/dev/null
curl -sL "$repo/archive/$version.tar.gz" \
  | tar -xz --strip-components=1
echo "Copying scripts to $install_dir"
cp bin/* "$install_dir/"
popd >/dev/null

printf "Do you store your Chameleon password in a CLI-enabled password manager? [y/N] "
read answer </dev/tty
echo
if [[ "$answer" =~ [Yy] ]]; then
  echo "I'm glad to hear that! Follow the instructions here to set up your"
  echo "CLI credentials: https://github.com/ChameleonCloud/climeleon#credentials"
  echo
else
  echo "Ah, that's too bad. I'll need to set up a shell alias to pass your "
  echo "credentials to climeleon. This will mean that your password will be"
  echo "stored in plaintext in your home directory."
  echo
  echo "If you want, you can set this up yourself by doing:"
  echo
  echo "  chameleon_password() {"
  echo "    echo \$MY_PASSWORD"
  echo "  }"
  echo "  export -f chameleon_password"
  echo
  echo "... somewhere in your login profile."
  echo
  echo "To set this up automatically, enter your Chameleon password."
  printf "Leave empty to skip: "
  read -s password </dev/tty
  if [[ -n "$password" ]]; then
    cat >>~/.bash_profile <<EOF

# AUTO-GENERATED BY CLIMELEON
chameleon_password() {
  echo "$password"
}
export -f chameleon_password
# /AUTO-GENERATED BY CLIMELEON
EOF
    echo "Password installed to ~/.bash_profile. You will need to log out and"
    echo "back in for your shell to be updated, or alternatively, do:"
    echo
    echo "  source ~/.bash_profile"
    echo
  fi
fi

echo "Done!"
