# gnome-claude-usage

Extensão do GNOME Shell que mostra na barra superior quanto do plano Claude já foi usado: o limite de 5 horas e o semanal (`5h 12% · 7d 40%`).

- Cada valor fica laranja a partir de 80% e vermelho a partir de 90%, com notificação ao cruzar cada limite (uma vez por período).
- O menu mostra quando cada limite reinicia.
- Atualiza a cada 5 minutos. Sem conexão ou com o login vencido, mostra o último valor conhecido esmaecido.

## Como funciona

O script `claude_usage.py` (instalado como `claude-usage`) lê o login que o app Claude / Claude Code mantém em `~/.claude/.credentials.json` e consulta o mesmo endpoint usado pelo comando `/usage`. O token nunca é renovado nem impresso pelo script; quem renova é o próprio app.

> O endpoint não é documentado e pode mudar sem aviso.

## Instalação

```bash
./build-deb.sh            # gera dist/gnome-claude-usage_1.0.0_all.deb
sudo apt install ./dist/gnome-claude-usage_1.0.0_all.deb
gnome-extensions enable claude-usage@local
```

Reinicie o GNOME Shell (X11: Alt+F2, `r`, Enter; Wayland: sair e entrar de novo).

Para outra versão: `./build-deb.sh 1.1.0`.

## Requisitos

- GNOME Shell 45 a 49
- Python 3
- Login feito no app Claude ou no Claude Code
