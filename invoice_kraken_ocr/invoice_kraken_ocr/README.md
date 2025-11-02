
# Invoice Kraken OCR (ERPNext v15)

**Goal:** High-accuracy OCR for **handwritten Arabic invoices** on ERPNext, with **incremental learning**.

## Features
- Uses **Kraken** (SOTA for handwriting) with Arabic model.
- **Extract** items from photos (phone camera friendly pre-processing).
- **Review & Correct** inside ERPNext; corrections become **training samples**.
- **Retrain** (transfer learning) from a base Arabic model — manual button or daily schedule.
- Auto-post to **Purchase/Sales Invoice**.

## Requirements
- System packages:
  - `sudo apt-get install -y tesseract-ocr` (optional, not used by Kraken but handy for tools)
  - `sudo apt-get install -y libxml2 libxslt1.1 libgl1` (OpenCV headless deps may vary)
- Python deps are handled by this app: `kraken`, `Pillow`, `numpy`, `opencv-python-headless`, `rapidfuzz`.
- Put a base Arabic **Kraken model** (e.g., `arabic-handwriting.mlmodel`) under:
  - `<site>/private/files/kraken_models/base.mlmodel` (configurable in **OCR Model Settings**).

## Install
```bash
cd ~/frappe-bench
bench get-app local /path/to/invoice_kraken_ocr
bench --site your.site install-app invoice_kraken_ocr
bench migrate
bench clear-cache
```

## DocTypes
- **OCR Model Settings**: where models live and if scheduler is enabled.
- **OCR Invoice Import** (parent) + **OCR Invoice Item** (child): review & post.
- **OCR Training Sample**: image crop + correct label stored for retraining.

## Flow
1. Upload invoice image in **OCR Invoice Import** → **Extract with Kraken**.
2. Fix any line text, qty, price → click **Learn Now** to store training samples.
3. **Retrain Model** (button) or wait for daily job (if enabled).
4. **Create Purchase/Sales Invoice**.

