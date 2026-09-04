<p align="center">
  <img src="assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid" alt="Lançamento no GitHub">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="Downloads">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="Licença">
</p>

<p align="center">
  <a href="docs/README.zh.md">Chinês</a> &nbsp;|&nbsp;
  <a href="docs/README.pt.md">Português</a> &nbsp;|&nbsp;
  <a href="docs/README.es.md">Espanhol</a> &nbsp;|&nbsp;
  <a href="docs/README.ja.md">Japonês</a> &nbsp;|&nbsp;
  <a href="docs/README.fr.md">Francês</a> &nbsp;|&nbsp;
  <a href="docs/README.de.md">Alemão</a> &nbsp;|&nbsp;
  <a href="docs/README.ko.md">Coreano</a> &nbsp;|&nbsp;
  <a href="docs/README.ar.md">Árabe</a>
</p>

O Perfect Grid é uma aplicação de secretária gratuita e de código aberto para criar folhas de contacto de vídeo e miniaturas de pré-visualização a partir de ficheiros de vídeo locais. Basta arrastar um vídeo, escolher o layout e exportar uma folha de contacto em PNG de alta qualidade.

Concebido para editores, colecionadores, arquivistas e qualquer pessoa que pretenda um resumo visual rápido de um vídeo.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Exemplo de folha de pré-visualização criada com o Perfect Grid">
  <br>
  <em>Exemplo de folha de contacto gerada com o Perfect Grid.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="Descarregar para macOS">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Descarregar para Windows">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Descarregar para Linux">
  </a>
</p>

## Funcionalidades

- Crie folhas de contacto de alta qualidade com apresentação avançada de metadados de vídeo (resolução, codecs, duração, tamanho do ficheiro, etc.)
- Layouts de grelha totalmente personalizáveis
- Sobreposições opcionais de código temporal
- Seleção inteligente de fotogramas com **Refine Picks**
- Guarde e reutilize predefinições personalizadas
- Processamento em lote
- Funciona no Windows, macOS e Linux
> Se encontrar __qualquer__ erro, se algo não funcionar ou se tiver dúvidas, crie um [Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) para o comunicar.

## Localização

A interface do utilizador da aplicação está disponível em 8 idiomas. A representação dos nomes dos ficheiros das folhas é um sistema separado — desenha os nomes dos ficheiros como píxeis no PNG exportado, o que requer um tratamento de tipos de letra específico do script.

| Idioma | IU | Na folha |
|---|---|---|
| Inglês | Sim | Sim |
| Chinês (中文) | Sim | Sim (macOS, Windows) |
| Português (PT) | Sim | Sim |
| Espanhol (ES) | Sim | Sim |
| Japonês (JA) | Sim | Sim (macOS, Windows) |
| Francês (FR) | Sim | Sim |
| Alemão (DE) | Sim | Sim |
| Coreano (KO) | Sim | Sim (macOS, Windows) |
| Árabe / RTL | — | Sim |
| Hebraico | — | — |
| Tailandês | — | — |
| Devanagari (hindi, etc.) | — | — |

> A renderização de nomes de ficheiros não ASCII no Linux não é atualmente suportada — os nomes de ficheiros em alfabetos não latinos serão apresentados como caixas. Isto será corrigido na próxima versão!

## Utilização básica

1. Abra o Perfect Grid.
2. Arraste um vídeo para dentro da janela.
3. Ajuste o layout e o estilo da grelha. Se alterar o layout, clique em **Atualizar pré-visualização** para regenerar as miniaturas.
4. As pré-visualizações têm uma qualidade inferior de forma intencional — as exportações utilizam sempre a configuração de qualidade selecionada.
5. (Opcional) No separador **Intervalo**, utilize **Aperfeiçoar Seleções** para uma seleção mais inteligente de fotogramas.
6. Escolha uma qualidade de exportação em **Intervalo**: **Rápido (1080p)**, **Detalhe (1440p)** ou **Máximo (4K)**.
7. Clique em **Exportar PNG**.

## Instalação

Descarregue a versão mais recente para o seu sistema operativo a partir da página [Versões](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest).

### macOS

1. Descarregue `PerfectGrid-v0.1.2-macos-universal.zip`.
2. Clique duas vezes para extrair e, em seguida, arraste o Perfect Grid para a pasta «Aplicações».
3. Abra `Perfect Grid.app`.

> O macOS irá bloquear a aplicação na primeira vez que for iniciada, uma vez que não está assinada. Clique com o botão direito do rato → **Abrir** → **Abrir** para contornar este bloqueio. Se ainda assim não abrir, execute este comando no Terminal: `xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. Descarregue o ficheiro `PerfectGrid-v0.1.2-Windows-x86_64.zip`.
2. Clique com o botão direito do rato → **Extrair tudo** e, em seguida, abra a pasta.
3. Clique duas vezes em `Perfect Grid.exe`.

> O Windows SmartScreen poderá apresentar um aviso, uma vez que a aplicação não possui assinatura de código. Clique em **Mais informações** → **Executar na mesma**.

### Linux

1. Descarregue `PerfectGrid-v0.1.2-Linux-x86_64.AppImage`.
2. Torne-o executável e execute-o:
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

Não é necessária qualquer instalação — o FFmpeg e todas as dependências estão incluídos. Funciona na maioria das distribuições x86_64 (Ubuntu 22.04+, Fedora, Arch, etc.).

> Se receber um erro FUSE: `sudo apt install fuse` (Debian/Ubuntu) ou `sudo dnf install fuse` (Fedora).

## Privacidade

Tudo é executado localmente. Sem análises, sem telemetria, sem envios. O FFmpeg e o FFprobe estão incluídos.

## Notas

- Suporta MP4, MOV, MKV, AVI, WebM e qualquer formato que o FFmpeg consiga ler.
- A descodificação de AV1 e VP9 pode ser lenta em hardware mais antigo.
- As compilações para macOS não estão assinadas — consulte a nota de instalação acima.

<details>
<summary>Para programadores</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Para suporte completo a nomes de ficheiros em árabe/RTL ao compilar a partir do código-fonte:

```bash
pip install arabic-reshaper python-bidi
```

Os scripts de compilação encontram-se em `scripts/`. O GitHub Actions compila automaticamente as versões para Windows e Linux quando são enviadas alterações marcadas. A versão para macOS é compilada manualmente.

</details>

## Contribuir

Por favor, informe-nos se encontrar algum bug ou erro, criando um [Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) 
As informações mais úteis a incluir são o seu sistema operativo, o formato de vídeo e se o problema ocorreu na pré-visualização, no refinamento, na exportação ou no processamento em lote.

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para mais informações.

## Licença

MIT. Consulte [LICENSE](LICENSE).
