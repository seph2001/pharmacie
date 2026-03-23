import os
import io
import requests
import pytesseract
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
from . import db
from .models import Product, Prescription, Notification

bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@bp.route("/")
def index():
    products = Product.query.order_by(Product.name).all()
    return render_template("index.html", products=products)


@bp.route("/health")
def health():
    return {"status": "ok", "service": "app"}, 200


@bp.route("/ordonnance", methods=["POST"])
def ordonnance():
    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    items_text = request.form.get("items_text", "").strip()
    file = request.files.get("file")

    if not customer_name or not items_text:
        flash("Veuillez renseigner votre nom et les produits demandés.")
        return redirect(url_for("main.index"))

    saved_path = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        saved_path = filename
        file_path_full = os.path.join(upload_dir, filename)
        file.save(file_path_full)
        
        # OCR : Lecture du texte dans l'image de l'ordonnance
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                ocr_text = pytesseract.image_to_string(Image.open(file_path_full))
                if ocr_text.strip():
                    # On ajoute le texte lu à la liste des produits demandés
                    clean_ocr = ocr_text.replace("\n", ", ")
                    items_text = f"{items_text}, {clean_ocr}"
            except Exception as e:
                print(f"Erreur OCR: {e}")

    presc = Prescription(
        customer_name=customer_name,
        phone=phone,
        email=email,
        items_text=items_text,
        file_path=saved_path,
        status="pending",
    )
    db.session.add(presc)
    db.session.commit()

    requested = [x.strip().lower() for x in items_text.split(",") if x.strip()]
    products = Product.query.all()
    stock_map = {p.name.lower(): p for p in products}

    unavailable = []
    for item in requested:
        p = stock_map.get(item)
        if p is None or p.quantity <= 0:
            unavailable.append(item)

    if unavailable:
        status = "unavailable"
        message = f"Indisponible: {', '.join(unavailable)}. Nous vous recontactons dès réapprovisionnement."
    else:
        status = "available"
        message = "Votre ordonnance est disponible à la pharmacie."
        for item in requested:
            p = stock_map.get(item)
            if p:
                p.quantity = max(0, p.quantity - 1)
        db.session.commit()

    presc.status = status
    db.session.commit()

    notify_success = send_notification(phone or "", email or "", message)
    notif = Notification(
        prescription_id=presc.id,
        channel="email" if email else "sms",
        message=message,
        success=notify_success,
    )
    db.session.add(notif)
    db.session.commit()

    return render_template(
        "ordonnance_result.html",
        prescription=presc,
        unavailable=unavailable,
        available=(len(unavailable) == 0),
        message=message,
    )


def send_notification(phone: str, email: str, message: str) -> bool:
    notifier_url = os.getenv("NOTIFIER_URL", "http://notifier:5001/notify")
    payload = {"phone": phone, "email": email, "message": message}
    try:
        resp = requests.post(notifier_url, json=payload, timeout=3)
        return 200 <= resp.status_code < 300
    except Exception:
        return False


@bp.route("/logo", methods=["GET", "POST"])
def logo():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not allowed_file(file.filename):
            flash("Veuillez envoyer une image (.png/.jpg/.jpeg).")
            return redirect(url_for("main.logo"))
        filename = "pharma.png"
        static_dir = current_app.static_folder
        os.makedirs(static_dir, exist_ok=True)
        save_path = os.path.join(static_dir, filename)
        file_stream = file.stream.read()
        with open(save_path, "wb") as f:
            f.write(file_stream)
        flash("Logo mis à jour.")
        return redirect(url_for("main.index"))
    return render_template("upload_logo.html")


@bp.route("/hero", methods=["GET", "POST"])
def hero():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not allowed_file(file.filename):
            flash("Veuillez envoyer une image (.png/.jpg/.jpeg).")
            return redirect(url_for("main.hero"))
        filename = "2.jpg"
        static_dir = current_app.static_folder
        os.makedirs(static_dir, exist_ok=True)
        save_path = os.path.join(static_dir, filename)
        file_stream = file.stream.read()
        with open(save_path, "wb") as f:
            f.write(file_stream)
        flash("Bannière mise à jour.")
        return redirect(url_for("main.index"))
    return render_template("upload_hero.html")
