# Perfect Grid

[![GitHub Release](https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![Downloads](https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total?)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![License](https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid?)](LICENSE)

Perfect Grid es una app de escritorio gratuita y de código abierto para crear hojas de contacto y miniaturas de vídeo a partir de archivos locales.

Arrastra un vídeo, elige tu diseño y exporta un PNG de alta calidad. Hecha para editores, coleccionistas, archivistas y cualquiera que quiera un resumen visual rápido de un vídeo.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Ejemplo de hoja de contacto generada con Perfect Grid">
  <br>
  <em>Ejemplo de hoja de contacto generada con Perfect Grid.</em>
</p>

<p align="center">
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="Descargar para macOS">
</a>
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-Windows.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?style=for-the-badge&logo=windows21&logoColor=white" alt="Descargar para Windows">
</a>
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-x86_64.AppImage">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?style=for-the-badge&logo=linux&logoColor=white" alt="Descargar para Linux">
</a>
</p>

## Funciones

- Genera hojas de contacto PNG de alta calidad
- Diseños de cuadrícula totalmente personalizables
- Superposición de código de tiempo opcional
- Metadatos del vídeo (resolución, códecs, duración, tamaño, etc.)
- Selección inteligente de fotogramas con **Refinar selección**
- Guarda y reutiliza presets personalizados
- Procesamiento por lotes
- Interfaz disponible en inglés, chino, portugués, español, japonés, francés, alemán y coreano
- Renderizado correcto de nombres de archivo en árabe, CJK y otros scripts no latinos
- Disponible para Windows, macOS y Linux

## Uso básico

1. Abre Perfect Grid.
2. Arrastra un vídeo a la ventana.
3. Ajusta el diseño de cuadrícula y el estilo. Si cambias el diseño, haz clic en **Actualizar vista previa**.
4. Las vistas previas son de menor calidad a propósito — las exportaciones siempre usan la calidad que hayas seleccionado.
5. (Opcional) En la pestaña **Rango**, usa **Refinar selección** para una selección de fotogramas más inteligente.
6. Elige la calidad de exportación en **Rango**: **Rápido (1080p)**, **Detalle (1440p)** o **Máximo (4K)**.
7. Haz clic en **Exportar PNG**.

## Descargar e instalar

Descarga la última versión para tu sistema desde la página de [Releases](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest).

### macOS

1. Descarga `PerfectGrid-v0.1.2-macos-universal.zip`.
2. Descomprime y arrastra Perfect Grid a Aplicaciones.
3. Si macOS bloquea la app al abrirla por primera vez, ejecuta esto en la Terminal:

```bash
xattr -cr "/Applications/Perfect Grid.app"
```

### Windows

1. Descarga `Perfect-Grid-Windows.zip`.
2. Descomprime en cualquier carpeta.
3. Ejecuta `Perfect Grid.exe`.

### Linux

1. Descarga `Perfect-Grid-x86_64.AppImage`.
2. Hazlo ejecutable y ábrelo:

```bash
chmod +x Perfect-Grid-x86_64.AppImage
./Perfect-Grid-x86_64.AppImage
```

FFmpeg está incluido — no necesitas instalarlo por separado.

## Licencia

MIT. Consulta [LICENSE](../LICENSE).
