# Convierte a Markdown

Herramienta web local para convertir documentos de cualquier formato a Markdown. Funciona completamente offline, sin necesidad de cuenta ni conexión a internet (excepto para convertir URLs).

## ¿Qué hace?

Convierte los siguientes formatos a Markdown fiel al original:

| Formato | Extensión |
|---|---|
| PDF (texto y escaneados con OCR) | `.pdf` |
| Word | `.docx`, `.doc` |
| Excel (todas las hojas) | `.xlsx`, `.xls` |
| PowerPoint | `.pptx`, `.ppt` |
| HTML | `.html`, `.htm` |
| CSV | `.csv` |
| JSON | `.json` |
| XML / RSS | `.xml` |
| ZIP (convierte el contenido) | `.zip` |
| EPUB | `.epub` |
| Jupyter Notebook | `.ipynb` |
| Outlook | `.msg` |
| Imágenes (metadatos EXIF) | `.jpg`, `.png`, `.gif`… |
| URLs: páginas web, Wikipedia, YouTube (transcripción) | — |

---

## Ejecutable (Windows)

### Dónde está el ejecutable

```
dist\
└── ConverteAMarkdown\                ← 📁 ESTA ES LA CARPETA QUE USAS
    ├── ConverteAMarkdown.exe         ← ▶️  ESTE ES EL ARCHIVO QUE EJECUTAS
    └── _internal\                    ← ⚠️  NO TOCAR (dependencias internas)
```

### Reglas importantes

| | Qué hacer |
|---|---|
| 📁 Carpeta `ConverteAMarkdown\` | **Puedes moverla** a donde quieras: Escritorio, Documentos, `C:\Programas`… |
| ▶️ `ConverteAMarkdown.exe` | **Nunca lo saques** de su carpeta. Siempre debe estar junto a `_internal\` |
| ⚠️ Carpeta `_internal\` | **Nunca la borres ni muevas** por separado. Contiene todas las librerías que necesita el exe para funcionar |

> Si mueves la aplicación, mueve **siempre la carpeta `ConverteAMarkdown\` completa**, no solo el `.exe`.

### Cómo ejecutarla

1. Abre la carpeta `dist\ConverteAMarkdown\`
2. Doble clic en **`ConverteAMarkdown.exe`**
3. El navegador se abre automáticamente en `http://127.0.0.1:5000`
4. Para cerrar: botón **Cerrar** en la esquina superior derecha de la app

### Acceso directo en el escritorio (recomendado)

Para no tener que buscar la carpeta cada vez:

1. Clic derecho sobre `ConverteAMarkdown.exe`
2. → *Enviar a* → *Escritorio (crear acceso directo)*

El acceso directo apunta al exe original — la carpeta puede quedarse donde esté.

---

## ⚠️ OCR para PDFs escaneados (requisito previo)

Si necesitas convertir PDFs que son imágenes (documentos escaneados, multas, expedientes, facturas escaneadas, etc.) necesitas instalar **Tesseract OCR** antes de usar la app.

Sin Tesseract, los PDFs con texto real se convierten correctamente. Solo los PDFs escaneados (sin capa de texto) necesitan OCR.

### Instalación de Tesseract en Windows

1. Descarga el instalador desde la página oficial de UB Mannheim:
   **https://github.com/UB-Mannheim/tesseract/wiki**
   → Archivo: `tesseract-ocr-w64-setup-5.x.x.exe` (elegir la versión más reciente)

2. Ejecuta el instalador. En el paso **"Additional language data (download)"** despliega la lista y marca:
   - ✅ **Spanish** (para documentos en español)
   - ✅ English ya viene seleccionado por defecto

3. Instala en la ruta por defecto:
   ```
   C:\Program Files\Tesseract-OCR\
   ```

4. La aplicación detecta Tesseract automáticamente en esa ruta. No hace falta configurar nada más.

5. Reinicia `ConverteAMarkdown.exe` si ya estaba abierto.

---

## Ejecutar en modo desarrollo

### Requisitos

- Python 3.10 o superior

### Instalación

```bash
git clone https://github.com/IgnacioAC1/markitdown.git
cd markitdown
pip install -r requirements.txt
```

### Arrancar el servidor

```bash
python app.py
```

Abre el navegador en `http://localhost:5000`

### Dependencias principales

```
flask>=3.0.0
markitdown[pdf,docx,xlsx,xls,pptx,outlook,youtube-transcription]>=0.1.0
pymupdf        # renderizado de PDF para OCR
pytesseract    # interfaz Python para Tesseract OCR
```

---

## Generar el ejecutable

Para regenerar el `.exe` tras modificar el código:

```bash
pip install pyinstaller
pyinstaller -y --noconsole --onedir --name "ConverteAMarkdown" \
  --add-data "templates;templates" \
  --collect-all magika \
  --collect-all markitdown \
  --hidden-import=fitz \
  --hidden-import=pytesseract \
  --hidden-import=PIL \
  launcher.py
```

El resultado queda en `dist/ConverteAMarkdown/`.

---

## Estructura del proyecto

```
markitdown/
├── app.py                        # servidor Flask + lógica de conversión y OCR
├── launcher.py                   # punto de entrada para el ejecutable
├── requirements.txt              # dependencias Python
├── templates/
│   └── index.html                # interfaz web completa
├── dist/
│   └── ConverteAMarkdown/
│       ├── ConverteAMarkdown.exe # ejecutable Windows
│       └── _internal/            # dependencias del exe (no borrar)
└── packages/
    └── markitdown/               # librería MarkItDown (Microsoft, fork)
```

---

## Basado en

[MarkItDown](https://github.com/microsoft/markitdown) — herramienta open source de Microsoft para convertir documentos a Markdown.
