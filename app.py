import io
import os
import sys
from flask import Flask, render_template, request, jsonify
from markitdown import MarkItDown, StreamInfo, UnsupportedFormatException, FileConversionException, MissingDependencyException

# Ruta base: sys._MEIPASS cuando corre como exe, directorio del script en dev
BASE_DIR = os.environ.get(
    'APP_BASE_DIR',
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB

md_converter = MarkItDown(enable_plugins=False)

# Ruta a Tesseract en Windows (instalador UB Mannheim)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    try:
        # Conversión desde URL
        if request.is_json:
            data = request.get_json()
            url = (data or {}).get("url", "").strip()
            if not url:
                return jsonify({"error": "URL vacía"}), 400
            result = md_converter.convert_uri(url)
            filename = _filename_from_url(url)
            return jsonify({
                "markdown": result.markdown,
                "title": result.title or filename,
                "filename": filename,
            })

        # Conversión desde archivo subido
        file = request.files.get("file")
        if not file or file.filename == "":
            return jsonify({"error": "No se recibió ningún archivo"}), 400

        original_name = file.filename
        extension = os.path.splitext(original_name)[1].lower()
        file_bytes = file.read()

        stream = io.BytesIO(file_bytes)
        stream_info = StreamInfo(filename=original_name, extension=extension)
        result = md_converter.convert_stream(stream, stream_info=stream_info)

        markdown = result.markdown or ""

        # Si el PDF devuelve vacío o casi vacío, intentar OCR
        if extension == ".pdf" and len(markdown.strip()) < 50:
            markdown = _ocr_pdf(file_bytes)
            if not markdown:
                return jsonify({"error": (
                    "Este PDF es un documento escaneado y no se pudo leer con OCR. "
                    "Asegúrate de tener Tesseract instalado con el idioma español."
                )}), 422

        md_filename = os.path.splitext(original_name)[0] + ".md"
        return jsonify({
            "markdown": markdown,
            "title": result.title or original_name,
            "filename": md_filename,
        })

    except UnsupportedFormatException:
        return jsonify({"error": "Formato no soportado. Prueba con PDF, Word, Excel, PowerPoint, HTML, CSV, imágenes, audio o una URL."}), 422
    except MissingDependencyException as e:
        return jsonify({"error": f"Dependencia faltante: {e}. Instala con: pip install 'markitdown[all]'"}), 500
    except FileConversionException as e:
        return jsonify({"error": f"Error al convertir: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500


def _ocr_pdf(file_bytes: bytes) -> str:
    """Extrae texto de un PDF escaneado usando PyMuPDF + Tesseract."""
    try:
        import fitz  # PyMuPDF
        import pytesseract
        from PIL import Image

        # Configurar ruta a Tesseract si existe
        if os.path.exists(TESSERACT_PATH):
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = []

        for i, page in enumerate(doc, 1):
            # Renderizar página a 200 DPI (factor 2 sobre los 96 DPI base)
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
            img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang="spa+eng", config="--psm 1")
            if text.strip():
                header = f"## Página {i}\n\n" if len(doc) > 1 else ""
                pages.append(f"{header}{text.strip()}")

        doc.close()
        return "\n\n---\n\n".join(pages)

    except ImportError:
        raise Exception("PyMuPDF o pytesseract no están instalados.")
    except Exception as e:
        raise Exception(f"OCR fallido: {e}")


@app.route("/shutdown", methods=["POST"])
def shutdown():
    import threading
    def _stop():
        import time
        time.sleep(0.4)
        os.kill(os.getpid(), 9)
    threading.Thread(target=_stop, daemon=True).start()
    return jsonify({"status": "ok"})


def _filename_from_url(url: str) -> str:
    from urllib.parse import urlparse
    path = urlparse(url).path.rstrip("/")
    base = os.path.basename(path) or "documento"
    name = os.path.splitext(base)[0] or "documento"
    return name + ".md"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
