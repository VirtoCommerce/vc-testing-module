# Dataset cheat sheet

Quick reference for notable product and location states in the test dataset.

## Product IDs out of stock

All fulfillment centers hold zero quantity for these products.

- `smartphone-apple-iphone-17-256gb-lavender`
- `smartphone-apple-iphone-17-512gb-mist-blue`
- `smartphone-apple-iphone-17-pro-256gb-deep-blue`
- `smartphone-apple-iphone-17-pro-256gb-silver`
- `smartphone-apple-iphone-17-pro-512gb-deep-blue`
- `smartphone-samsung-galaxy-a37-5g-awesome-lavender`
- `smartphone-samsung-galaxy-s26-ultra-black`

## Not active pickup locations

- `pickup-location-acme-transeuro-logistics-node` — TransEuro Logistics Node
- `pickup-location-acme-union-square-greenmarket` — Union Square Greenmarket

## Product IDs with sale price

Both USD and EUR pricelists carry a `sale` price for these products.

- `smartphone-apple-iphone-17-256gb-black`
- `smartphone-apple-iphone-17-256gb-lavender`
- `smartphone-apple-iphone-17-256gb-mist-blue`
- `smartphone-apple-iphone-17-256gb-sage`
- `smartphone-apple-iphone-17-256gb-white`
- `smartphone-apple-iphone-17-pro-256gb-cosmic-orange`
- `smartphone-apple-iphone-17-pro-256gb-deep-blue`
- `smartphone-apple-iphone-17-pro-256gb-silver`

## Product IDs with promotions

- `smartphone-samsung-galaxy-a57-5g` — $50 off (promotion `promotion-acme-50-off-smartphone-samsung-galaxy-a57-5g`)
- `smartphone-samsung-galaxy-a17-5g-black` — free gift when cart has 20+ items (promotion `promotion-acme-gift-for-20-cart-items`)

### Cart-level promotions (not tied to a product)

- `promotion-acme-100-off-for-cart-subtotal` — $100 off when cart subtotal ≥ $4000
- `promotion-acme-100-off-for-cart-subtotal-by-coupon` — $100 off with coupon
