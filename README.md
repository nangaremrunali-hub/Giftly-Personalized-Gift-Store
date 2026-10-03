# Giftly — Personalized Gift Store

This version includes 80 products across Birthday, Couple, Friendship, Personalized, and Decor.

## Product photography
Product cards now use **product-specific real-photo searches** rather than one generic category photo. Each SKU has its own search tags, so examples include birthday cards for card products, books for memory books, keychains for keychains, mugs for mug sets, wall clocks for clocks, door/name signs for house signs, botanical prints for botanical decor, and so on.

The product photography uses remote real-photo URLs and therefore requires an internet connection while viewing the site. The original local SVG product art remains in `static/images/products` as a fallback/source asset.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
