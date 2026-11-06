#!/bin/bash
# Builds dist/gnome-claude-usage_<version>_all.deb
set -euo pipefail
cd "$(dirname "$0")"

VERSION="${1:-1.0.0}"
MAINTAINER="Thiago Adriano <thiago.adriano@portergroup.com.br>"
BUILD=build
rm -rf "$BUILD" && mkdir -p "$BUILD" dist
# ---------- Claude usage ----------
P="$BUILD/gnome-claude-usage"
install -Dm755 claude_usage.py "$P/usr/bin/claude-usage"
mkdir -p "$P/usr/share/gnome-shell/extensions"
cp -r claude-usage@local "$P/usr/share/gnome-shell/extensions/"
mkdir -p "$P/DEBIAN"
cat > "$P/DEBIAN/control" <<EOF
Package: gnome-claude-usage
Version: $VERSION
Architecture: all
Maintainer: $MAINTAINER
Depends: python3, gnome-shell (>= 45)
Section: gnome
Priority: optional
Description: Claude plan usage (5-hour and weekly) in the GNOME top bar
 Shows the percentage used of Claude's session (5-hour) and weekly limits,
 with colors and notifications from 80% and 90%. Uses the Claude app login
 in ~/.claude/.credentials.json.
EOF
cat > "$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
echo "Enable with: gnome-extensions enable claude-usage@local  (then restart GNOME Shell)"
EOF
chmod 755 "$P/DEBIAN/postinst"

# Standard package permissions: 755 dirs/executables, 644 other files
chmod -R u=rwX,go=rX "$BUILD"

dpkg-deb --root-owner-group --build "$BUILD/gnome-claude-usage" "dist/gnome-claude-usage_${VERSION}_all.deb"
rm -rf "$BUILD"
