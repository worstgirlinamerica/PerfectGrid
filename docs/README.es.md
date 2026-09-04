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
  <a href="docs/README.zh.md">Chino</a> &nbsp;|&nbsp;
  <a href="docs/README.pt.md">Portugués</a> &nbsp;|&nbsp;
  <a href="docs/README.es.md">Español</a> &nbsp;|&nbsp;
  <a href="docs/README.ja.md">Japonés</a> &nbsp;|&nbsp;
  <a href="docs/README.fr.md">Francés</a> &nbsp;|&nbsp;
  <a href="docs/README.de.md">Alemán</a> &nbsp;|&nbsp;
  <a href="docs/README.ko.md">한국어</a> &nbsp;|&nbsp;
  <a href="docs/README.ar.md">العربية</a>
</p>

Perfect Grid es una aplicación de escritorio gratuita y de código abierto para crear hojas de contacto de vídeo y vistas previas en miniatura a partir de archivos de vídeo locales. Arrastra un vídeo, elige tu diseño y exporta una hoja de contacto en formato PNG de alta calidad.

Diseñada para editores, coleccionistas, archiveros y cualquier persona que desee un resumen visual rápido de un vídeo.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Ejemplo de hoja de vista previa creada con Perfect Grid">
  <br>
  <em>Ejemplo de hoja de contacto generada con Perfect Grid.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="Descargar para macOS">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Descargar para Windows">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Descargar para Linux">
  </a>
</p>

## Características

- Genera hojas de contacto de alta calidad con visualización avanzada de metadatos de vídeo (resolución, códecs, duración, tamaño de archivo, etc.)
- Diseños de cuadrícula totalmente personalizables
- Superposición opcional de códigos de tiempo
- Selección inteligente de fotogramas con **Refine Picks**
- Guarda y reutiliza ajustes preestablecidos personalizados
- Procesamiento por lotes
- Funciona en Windows, macOS y Linux
> Si experimentas __cualquier__ error, algo no funciona o tienes alguna pregunta, por favor, crea un [incidente](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) para informarnos.

## Uso básico

1. Abre Perfect Grid.
2. Arrastra un vídeo a la ventana.
3. Ajusta el diseño y el estilo de la cuadrícula. Si cambias el diseño, haz clic en **Actualizar vista previa** para volver a generar las miniaturas.
4. Las vistas previas son de menor calidad a propósito; las exportaciones siempre utilizan la configuración de calidad que hayas seleccionado.
5. (Opcional) En la pestaña **Rango**, utiliza **Perfeccionar selección** para una selección de fotogramas más inteligente.
6. Elige una calidad de exportación en **Rango**: **Rápida (1080p)**, **Detallada (1440p)** o **Máxima (4K)**.
7. Haz clic en **Exportar PNG**.

## Instalación

Descarga la última versión para tu sistema operativo desde la página [Versiones](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest).

### macOS

1. Descarga `PerfectGrid-v0.1.2-macos-universal.zip`.
2. Haz doble clic para extraerlo y, a continuación, arrastra Perfect Grid a la carpeta Aplicaciones.
3. Abre `Perfect Grid.app`.

> macOS bloqueará la aplicación al iniciarla por primera vez, ya que no está firmada. Haz clic con el botón derecho → **Abrir** → **Abrir** para superar este bloqueo. Si sigue sin abrirse, ejecuta esto en la Terminal: `xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. Descarga `PerfectGrid-v0.1.2-Windows-x86_64.zip`.
2. Haz clic con el botón derecho → **Extraer todo** y, a continuación, abre la carpeta.
3. Haz doble clic en «Perfect Grid.exe».

> Es posible que Windows SmartScreen te muestre una advertencia, ya que la aplicación no está firmada. Haz clic en **Más información** → **Ejecutar de todos modos**.

### Linux

1. Descarga `PerfectGrid-v0.1.2-Linux-x86_64.AppImage`.
2. Hazlo ejecutable y ejecútalo:
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

No es necesaria ninguna instalación: FFmpeg y todas las dependencias están incluidas. Funciona en la mayoría de distribuciones x86_64 (Ubuntu 22.04 y posteriores, Fedora, Arch, etc.).

> Si aparece un error de FUSE: `sudo apt install fuse` (Debian/Ubuntu) o `sudo dnf install fuse` (Fedora).

## Privacidad

Todo se ejecuta localmente. Sin análisis, sin telemetría, sin subidas de archivos. FFmpeg y FFprobe están incluidos.

## Localización

La interfaz de usuario de la aplicación está disponible en 8 idiomas. La representación de los nombres de archivo en la hoja es un sistema independiente: dibuja los nombres de archivo como píxeles en el PNG exportado, lo que requiere un manejo de fuentes específico para el script.

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
- Las compilaciones para macOS no están firmadas; consulta la nota de instalación anterior.

<details>
<summary>Para desarrolladores</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Para obtener compatibilidad completa con nombres de archivo en árabe/RTL al compilar desde el código fuente:

```bash
pip install arabic-reshaper python-bidi
```

Los scripts de compilación se encuentran en `scripts/`. GitHub Actions compila automáticamente las versiones para Windows y Linux al enviar cambios etiquetados. La versión para macOS se compila manualmente.

</details>

## Colaborar

Si detectas algún fallo o error, háznoslo saber creando una [incidencia](https://github.com/worstgirlinamerica/PerfectGrid/issues/new). 
La información más útil que puedes incluir es tu sistema operativo, el formato de vídeo y si el problema se produjo en la vista previa, el refinado, la exportación o el procesamiento por lotes.

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para obtener más información.

## Licencia

MIT. Consulta [LICENSE](LICENSE).
