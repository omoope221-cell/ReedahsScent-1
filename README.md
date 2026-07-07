# Reedah's Scent — Django E-commerce Backend

A mini Django e-commerce site for a perfume store. No payment gateway —
customers add items to a cart, fill in their delivery details, and get
redirected straight to WhatsApp with a pre-filled message (order summary +
your bank account details) ready to send.

## Admin Dashboard
A custom, hidden admin dashboard lives at:
- `/admin-login/` — staff-only login (not linked anywhere in the public site)
- `/admin-dashboard/` — overview: total/pending orders, product count, confirmed revenue, low-stock alerts, recent orders
- `/admin-dashboard/products/` — add, edit, delete products
- `/admin-dashboard/categories/` — add/delete categories
- `/admin-dashboard/orders/` — filter by status, view full order details, update status, message the customer on WhatsApp directly from the order page

Only accounts with `is_staff=True` can log in here — create one with `python manage.py createsuperuser`. This is separate from Django's built-in `/admin/`, which still works too if you ever need it, but the dashboard above is the one designed for day-to-day use.

## Apps
- **store** — Categories & Products, product listing/detail pages
- **cart** — session-based shopping bag (no login required to add items)
- **orders** — checkout form, order + order items, builds the WhatsApp message
- **accounts** — simple signup/login/logout (Django's built-in auth)

## How ordering works
1. Customer browses `/shop/`, adds products to their bag.
2. At `/orders/create/` they fill in name, email, phone, and delivery address.
3. On submit, an `Order` + `OrderItem`s are saved, the cart is cleared, and the
   customer is redirected to `https://wa.me/<your number>?text=...` with a
   message like:

   ```
   Hi Reedah's Scent! I would love to get this:

   - Amber Oud x1 — ₦45,000

   Total: ₦45,000

   Name: Jane Doe
   Phone: 08012345678
   Delivery Address: 12 Allen Ave, Ikeja, Lagos

   Please confirm my order. I'll make payment to:
   Account Number: 0123456789
   Bank: Your Bank Name
   Account Name: Reedah's Scent
   ```

4. You confirm the order and payment directly with the customer over WhatsApp,
   then update the order's status from the Django admin.

## Setup (Windows / VS Code)

1. Open this folder in VS Code, then open a terminal **inside this exact
   folder** (the one containing `manage.py`).

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   You should see `(venv)` at the start of your terminal prompt — if you
   don't, the activation didn't work; re-run the second command.

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   If Pillow fails to install (common on newer Python versions like 3.14),
   run:
   ```
   pip install Pillow --only-binary=:all:
   ```

4. Create your `.env` file:
   ```
   copy .env.example .env
   ```
   Then open `.env` and fill in:
   - `SECRET_KEY` — any long random string
   - `WHATSAPP_NUMBER` — your WhatsApp number in international format, no
     `+`, spaces, or leading zero (e.g. `2348012345678`)
   - `STORE_BANK_NAME`, `STORE_ACCOUNT_NUMBER`, `STORE_ACCOUNT_NAME` — the
     bank details you want shown to customers

5. Run migrations and create an admin account:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the dev server:
   ```
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the storefront and
   `http://127.0.0.1:8000/admin/` to add categories, products, and product
   images.

## Adding products
Go to `/admin/` → **Products** → add a name, category, price, description,
fragrance notes, stock, and upload an image. Tick "is featured" to show it
on the homepage.

## Notes
- Currency is displayed in ₦ (Naira) throughout.
- Uses Tailwind via CDN + Cormorant Garamond/Jost fonts for a warm, luxury
  look matching the brand.
- No payment gateway is wired in on purpose — orders are confirmed manually
  via WhatsApp + bank transfer.
