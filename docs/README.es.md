<p align="center">
  <img src="https://raw.githubusercontent.com/worstgirlinamerica/PerfectGrid/main/assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?color=E95420" alt="Lanzamiento en GitHub">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="Descargas">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="Licencia">
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.zh.md">Chino</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.pt.md">Portugués</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.es.md)">Español</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ja.md">Japonés</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.fr.md">Français</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.de.md">Deutsch</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ko.md">한국어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ar.md">العربية</a>
</p>

Perfect Grid es una aplicación de escritorio gratuita y de código abierto para crear hojas de contacto de vídeo y miniaturas de vista previa a partir de archivos de vídeo locales. Arrastra y suelta un vídeo, elige tu diseño y exporta una hoja de contacto en formato PNG de alta calidad.

Diseñada para editores, coleccionistas, archiveros y cualquier persona que desee un resumen visual rápido de un vídeo.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Ejemplo de hoja de vista previa creada con Perfect Grid">
  <br>
  <em>Ejemplo de hoja de contacto generada con Perfect Grid.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="Descargar para macOS">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Descargar para Windows">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Descargar para Linux">
  </a>
</p>
<p align="center"><sub>Las insignias enlazan con la última versión: descarga el archivo que se ajuste a tu sistema operativo (y a tu chip, en el caso de macOS).</sub></p>

## Características

- Genera hojas de contacto de alta calidad con visualización avanzada de metadatos de vídeo (resolución, códecs, duración, tamaño de archivo, etc.)
- Diseños de cuadrícula totalmente personalizables, con una barra lateral redimensionable para disponer de más espacio de trabajo
- Superposición opcional de códigos de tiempo
- Selección inteligente de fotogramas con **Refine Picks**
- Motor de extracción basado en PyAV con generación de vistas previas adaptada al hardware, para que las vistas previas sigan siendo rápidas en diferentes CPU y arquitecturas
- Calidad de la pasada de extracción inicial ajustable en «Configuración»
- Guarda y reutiliza ajustes preestablecidos personalizados
- Procesamiento por lotes
- Funciona en Windows, macOS y Linux
> Si experimentas __cualquier__ error, algo no funciona o tienes alguna pregunta, por favor, crea un [tema](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) para informarnos.

## Uso básico

1. Abre Perfect Grid.
2. Arrastra un vídeo a la ventana.
3. Ajusta la disposición y el estilo de la cuadrícula. Si cambias la disposición, haz clic en **Actualizar vista previa** para volver a generar las miniaturas.
4. Las vistas previas tienen una calidad inferior a propósito; las exportaciones siempre utilizan la configuración de calidad que hayas seleccionado.
5. (Opcional) En la pestaña **Rango**, utiliza **Perfeccionar selección** para una selección de fotogramas más inteligente.
6. Elige una calidad de exportación en **Rango**: **Rápida (1080p)**, **Detallada (1440p)** o **Máxima (4K)**.
7. Haz clic en **Exportar PNG**.

## Instalación

Descarga la última versión para tu sistema operativo desde la página [Versiones](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest).

### macOS

1. Descarga la versión para tu chip: `PerfectGrid-<versión>-macOS-arm64.zip` (Apple Silicon) o `PerfectGrid-<versión>-macOS-x86_64.zip` (Intel). ¿No sabes cuál tienes? Menú Apple → **Acerca de este Mac**.
2. Haz doble clic para descomprimir el archivo y, a continuación, arrastra Perfect Grid a la carpeta «Aplicaciones».
3. Abre `Perfect Grid.app`.

> macOS bloqueará la aplicación al iniciarla por primera vez, ya que no está firmada. Haz clic con el botón derecho → **Abrir** → **Abrir** para superar este bloqueo. Si aún así no se abre, ejecuta esto en Terminal: `xattr -cr "/Aplicaciones/Perfect Grid.app"`

### Windows

1. Descarga `PerfectGrid-<versión>-Windows-x86_64.zip`.
2. Haz clic con el botón derecho → **Extraer todo** y, a continuación, abre la carpeta.
3. Haz doble clic en `Perfect Grid.exe`.

> Es posible que Windows SmartScreen te avise, ya que la aplicación no está firmada digitalmente. Haz clic en **Más información** → **Ejecutar de todos modos**.

### Linux

1. Descarga `PerfectGrid-<versión>-Linux-x86_64.AppImage`.
2. Hazlo ejecutable y ejecútalo:
```bash
chmod +x PerfectGrid-<versión>-Linux-x86_64.AppImage
./PerfectGrid-<versión>-Linux-x86_64.AppImage
```

No es necesaria ninguna instalación: FFmpeg y todas las dependencias están incluidas. Funciona en la mayoría de distribuciones x86_64 (Ubuntu 22.04+, Fedora, Arch, etc.).

> Si aparece un error de FUSE: `sudo apt install fuse` (Debian/Ubuntu) o `sudo dnf install fuse` (Fedora).

## Privacidad

Todo se ejecuta localmente. Sin análisis, sin telemetría, sin subidas de archivos. FFmpeg y FFprobe están incluidos.

## Localización

La interfaz de usuario de la aplicación está disponible en 8 idiomas. La representación de los nombres de archivo en las hojas es un sistema independiente: dibuja los nombres de archivo como píxeles en el PNG exportado, lo que requiere un manejo de fuentes específico para el script.

| Idioma | IU | En la hoja |
|---|---|---|
| Inglés | Sí | Sí |
| Chino (中文) | Sí | Sí (macOS, Windows) |
| Portugués (PT) | Sí | Sí |
| Español (ES) | Sí | Sí |
| Japonés (JA) | Sí | Sí (macOS, Windows) |
| Francés (FR) | Sí | Sí |
| Alemán (DE) | Sí | Sí |
| Coreano (KO) | Sí | Sí (macOS, Windows) |
| Árabe / RTL | — | Sí |
| Hebreo | — | — |
| Tailandés | — | — |
| Devanagari (hindi, etc.) | — | — |

> Actualmente no se admite la visualización de nombres de archivo no ASCII en Linux; los nombres de archivo en alfabetos no latinos aparecerán como cuadros. ¡Esto se solucionará en la próxima versión!

## Notas

- Admite MP4, MOV, MKV, AVI, WebM y cualquier formato que FFmpeg pueda leer.
- La decodificación de AV1 y VP9 puede resultar lenta en equipos antiguos.
- Las versiones para macOS no están firmadas; consulta la nota de instalación anterior.

<details>
<summary>Para desarrolladores</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Para obtener compatibilidad completa con nombres de archivo en árabe/RTL al ejecutarlo desde el código fuente:

```bash
pip install arabic-reshaper python-bidi
```

Los scripts de compilación se encuentran en `scripts/`. GitHub Actions compila automáticamente versiones para Windows, Linux y macOS (arm64 + x86_64) al realizar envíos etiquetados.

</details>

## Cómo contribuir

Si detectas algún fallo o error, avísanos creando una [incidencia](https://github.com/worstgirlinamerica/PerfectGrid/issues/new). 
La información más útil que puedes incluir es tu sistema operativo, el formato de vídeo y si el problema se produjo en la vista previa, el refinado, la exportación o el procesamiento por lotes.

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para obtener más información.

## Licencia

MIT. Consulta [LICENSE](LICENSE).
