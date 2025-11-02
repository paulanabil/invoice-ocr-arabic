
app_name = "invoice_kraken_ocr"
app_title = "Invoice Kraken OCR"
app_publisher = "You"
app_description = "Handwritten Arabic OCR with Kraken, incremental learning, ERPNext integration"
app_email = "you@example.com"
app_license = "MIT"

# Desk items (optional)

# Scheduler: daily retrain (can be disabled in settings)
scheduler_events = {
    "daily": [
        "invoice_kraken_ocr.train.schedule_daily_retrain"
    ]
}
