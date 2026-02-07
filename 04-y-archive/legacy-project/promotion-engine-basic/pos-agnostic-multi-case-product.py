"""
PROMOTION DECISION SERVICE – 12 CASES
- Mỗi BILL = 1 case promotion
- Engine xử lý BillContext (decision snapshot)
- Chạy file để xem TIMELINE + LOG
"""

from dataclasses import dataclass
from typing import List, Optional

# ========= CORE MODELS =========

@dataclass
class Item:
    sku: str
    name: str
    price: int
    qty: int

@dataclass
class BillContext:
    bill_id: str
    items: List[Item]
    order_amount: int
    shipping_fee: int
    channel: str
    member_level: Optional[str] = None
    voucher: Optional[str] = None


# ========= PROMOTION ENGINE =========

class PromotionEngine:

    def evaluate(self, ctx: BillContext):
        print(f"\n[ENGINE] ===== START {ctx.bill_id} =====")
        discount = 0

        # CASE 01 – Product discount %
        if ctx.bill_id == "CASE-01":
            print("[CASE-01] PRODUCT % DISCOUNT")
            d = int(ctx.items[0].price * 0.2)
            discount += d
            print(f" → Giảm {d}")

        # CASE 02 – Product discount amount
        elif ctx.bill_id == "CASE-02":
            print("[CASE-02] PRODUCT AMOUNT DISCOUNT")
            discount += 50_000
            print(" → Giảm 50000")

        # CASE 03 – Combo discount
        elif ctx.bill_id == "CASE-03":
            print("[CASE-03] COMBO DISCOUNT")
            discount += 70_000
            print(" → Giảm combo 70000")

        # CASE 04 – Order % discount
        elif ctx.bill_id == "CASE-04":
            print("[CASE-04] ORDER % DISCOUNT")
            d = int(ctx.order_amount * 0.15)
            discount += d
            print(f" → Giảm {d}")

        # CASE 05 – Order amount threshold
        elif ctx.bill_id == "CASE-05":
            print("[CASE-05] ORDER AMOUNT THRESHOLD")
            if ctx.order_amount >= 1_000_000:
                discount += 100_000
                print(" → Giảm 100000")

        # CASE 06 – Order % with cap
        elif ctx.bill_id == "CASE-06":
            print("[CASE-06] ORDER % WITH CAP")
            d = min(int(ctx.order_amount * 0.3), 100_000)
            discount += d
            print(f" → Giảm {d}")

        # CASE 07 – Buy X get Y (gift)
        elif ctx.bill_id == "CASE-07":
            print("[CASE-07] BUY X GET Y")
            print(" → Tặng khoai tây chiên")

        # CASE 08 – Buy variant get variant
        elif ctx.bill_id == "CASE-08":
            print("[CASE-08] BUY VARIANT GET VARIANT")
            print(" → Mua size L tặng size S")

        # CASE 09 – Same item BOGO
        elif ctx.bill_id == "CASE-09":
            print("[CASE-09] BUY SAME GET SAME")
            print(" → Mua 1 tặng 1")

        # CASE 10 – Channel promotion
        elif ctx.bill_id == "CASE-10":
            print("[CASE-10] CHANNEL DISCOUNT")
            if ctx.channel == "DELIVERY":
                discount += 30_000
                print(" → Giảm 30000 cho delivery")

        # CASE 11 – Shipping % discount
        elif ctx.bill_id == "CASE-11":
            print("[CASE-11] SHIPPING % DISCOUNT")
            d = min(int(ctx.shipping_fee * 0.5), 20_000)
            discount += d
            print(f" → Giảm ship {d}")

        # CASE 12 – Voucher
        elif ctx.bill_id == "CASE-12":
            print("[CASE-12] VOUCHER")
            if ctx.voucher == "PROMO50":
                discount += 50_000
                print(" → Giảm voucher 50000")

        final_pay = ctx.order_amount + ctx.shipping_fee - discount

        print(f"[ENGINE] TOTAL DISCOUNT: {discount}")
        print(f"[ENGINE] FINAL PAY: {final_pay}")
        print(f"[ENGINE] ===== END {ctx.bill_id} =====")


# ========= SIMULATE POS (12 BILLS) =========

if __name__ == "__main__":

    engine = PromotionEngine()

    bills = [
        BillContext("CASE-01", [Item("CF", "Coffee", 50_000, 1)], 50_000, 0, "DINE_IN"),
        BillContext("CASE-02", [Item("CK", "Cake", 120_000, 1)], 120_000, 0, "DINE_IN"),
        BillContext("CASE-03", [Item("CB", "Combo", 300_000, 1)], 300_000, 0, "DINE_IN"),
        BillContext("CASE-04", [Item("CF", "Coffee", 200_000, 2)], 400_000, 0, "DINE_IN"),
        BillContext("CASE-05", [Item("ST", "Steak", 1_000_000, 1)], 1_000_000, 0, "DINE_IN"),
        BillContext("CASE-06", [Item("ST", "Steak", 500_000, 2)], 1_000_000, 0, "DINE_IN"),
        BillContext("CASE-07", [Item("CF", "Coffee", 150_000, 2)], 300_000, 0, "DINE_IN"),
        BillContext("CASE-08", [Item("PZ", "Pizza L", 250_000, 1)], 250_000, 0, "DINE_IN"),
        BillContext("CASE-09", [Item("PZ", "Pizza", 200_000, 2)], 400_000, 0, "DINE_IN"),
        BillContext("CASE-10", [Item("CF", "Coffee", 100_000, 1)], 100_000, 20_000, "DELIVERY"),
        BillContext("CASE-11", [Item("CF", "Coffee", 80_000, 1)], 80_000, 40_000, "DELIVERY"),
        BillContext("CASE-12", [Item("CF", "Coffee", 100_000, 1)], 100_000, 0, "DINE_IN", voucher="PROMO50"),
    ]

    print("[POS] START CHECKOUT 12 BILLS")

    for bill in bills:
        print(f"\n[POS] Checkout {bill.bill_id}")
        engine.evaluate(bill)
