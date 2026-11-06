#!/bin/bash
# Gera dist/gnome-claude-usage_<versão>_all.deb
set -euo pipefail
cd "$(dirname "$0")"

VERSION="${1:-1.0.0}"
MAINTAINER="Thiago Adriano <thiago.adriano@portergroup.com.br>"
BUILD=build
rm -rf "$BUILD" && mkdir -p "$BUILD" dist
# ---------- Uso do Claude ----------
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
Description: Uso do plano Claude (5 h e semanal) na barra do GNOME
 Mostra a porcentagem usada dos limites de sessão (5 h) e semanal do Claude,
 com cores e notificações a partir de 80% e 90%. Usa o login do app Claude
 em ~/.claude/.credentials.json.
EOF
cat > "$P/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
echo "Habilite com: gnome-extensions enable claude-usage@local  (e reinicie o GNOME Shell)"
EOF
chmod 755 "$P/DEBIAN/postinst"

# Permissões padrão de pacote: 755 pastas/executáveis, 644 demais arquivos
chmod -R u=rwX,go=rX "$BUILD"

dpkg-deb --root-owner-group --build "$BUILD/gnome-claude-usage" "dist/gnome-claude-usage_${VERSION}_all.deb"
rm -rf "$BUILD"
