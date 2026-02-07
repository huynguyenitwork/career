"""
PROMOTION DECISION SERVICE – DEMO 12 CASES
Mục tiêu:
- Chạy code → thấy rõ timeline
- Mỗi promotion là 1 decision độc lập
- Không sync, không lưu state
"""

from dataclasses import dataclass
from typing import List, Dict

# ========= MODELS =========

@dataclass
class Item:
    id: str
    name: str
    price: float
    qty: int

@dataclass
class BillContext:
    bill_id: str
    items: List[Item]
    member_level: str
    channel: str
    hour: int
    voucher: str | None = None

@dataclass
class PromotionResult:
    total_discount: float
    final_amount: float
    applied: List[str]


# ========= ENGINE =========

class PromotionEngine:

    def calculate(self, ctx: BillContext) -> PromotionResult:
        print(f"\n[ENGINE] ===== START BILL {ctx.bill_id} =====")

        total = sum(i.price * i.qty for i in ctx.items)
        discount = 0
        applied = []

        print(f"[ENGINE] Base total: {total}")

        # ---- BILL LEVEL (1–4) ----

        # 1. % bill discount
        if total >= 200_000:
            d = total * 0.05
            discount += d
            applied.append("BILL_5_PERCENT")
            print(f"[CASE 1] Bill >=200k → -{d}")

        # 2. Fixed bill discount
        if total >= 300_000:
            discount += 20_000
            applied.append("BILL_MINUS_20K")
            print("[CASE 2] Bill >=300k → -20000")

        # 3. Member discount
        if ctx.member_level == "GOLD":
            d = total * 0.1
            discount += d
            applied.append("MEMBER_GOLD_10_PERCENT")
            print(f"[CASE 3] GOLD member → -{d}")

        # 4. Happy hour
        if 14 <= ctx.hour <= 16:
            discount += 15_000
            applied.append("HAPPY_HOUR")
            print("[CASE 4] Happy hour → -15000")

        # ---- ITEM LEVEL (5–8) ----

        for item in ctx.items:
            # 5. Buy X discount
            if item.qty >= 2:
                d = item.price * item.qty * 0.05
                discount += d
                applied.append(f"BULK_{item.id}")
                print(f"[CASE 5] Buy >=2 {item.name} → -{d}")

            # 6. Buy N discount
            if item.qty >= 3:
                discount += 10_000
                applied.append(f"BUY3_{item.id}")
                print(f"[CASE 6] Buy 3 {item.name} → -10000")

            # 7. Buy X Get Y
            if item.qty >= 2:
                discount += item.price
                applied.append(f"BUY1GET1_{item.id}")
                print(f"[CASE 7] Buy1Get1 {item.name} → -{item.price}")

        # 8. Combo
        ids = {i.id for i in ctx.items}
        if {"CF", "CK"}.issubset(ids):
            discount += 25_000
            applied.append("COMBO_CF_CK")
            print("[CASE 8] Combo Coffee+Cake → -25000")

        # ---- ADVANCED (9–12) ----

        # 9. Channel
        if ctx.channel == "TAKE_AWAY":
            discount += 10_000
            applied.append("TAKE_AWAY")
            print("[CASE 9] Take-away → -10000")

        # 10. Segment
        if ctx.member_level in ["GOLD", "PLATINUM"]:
            discount += 5_000
            applied.append("LOYAL_SEGMENT")
            print("[CASE 10] Loyal segment → -5000")

        # 11. Bill count (giả lập)
        if ctx.bill_id.endswith("5"):
            discount += 15_000
            applied.append("5TH_BILL")
            print("[CASE 11] 5th bill → -15000")

        # 12. Voucher
        if ctx.voucher == "PROMO50":
            discount += 50_000
            applied.append("VOUCHER_PROMO50")
            print("[CASE 12] Voucher PROMO50 → -50000")

        final = max(total - discount, 0)

        print(f"[ENGINE] Total discount: {discount}")
        print(f"[ENGINE] Final amount: {final}")
        print(f"[ENGINE] Applied promotions: {applied}")
        print(f"[ENGINE] ===== END BILL {ctx.bill_id} =====\n")

        return PromotionResult(discount, final, applied)


# ========= SIMULATE POS =========

if __name__ == "__main__":
    engine = PromotionEngine()

    bills = [
        # CASE 1: % bill discount
        BillContext(
            bill_id="BILL_201",
            member_level="NONE",
            channel="DINE_IN",
            hour=10,
            items=[Item("CF", "Coffee", 50000, 4)],
        ),

        # CASE 2: fixed bill discount
        BillContext(
            bill_id="BILL_202",
            member_level="NONE",
            channel="DINE_IN",
            hour=11,
            items=[Item("CK", "Cake", 100000, 3)],
        ),

        # CASE 3: member discount
        BillContext(
            bill_id="BILL_203",
            member_level="GOLD",
            channel="DINE_IN",
            hour=12,
            items=[Item("CF", "Coffee", 40000, 2)],
        ),

        # CASE 4: happy hour
        BillContext(
            bill_id="BILL_204",
            member_level="NONE",
            channel="DINE_IN",
            hour=15,
            items=[Item("CF", "Coffee", 30000, 2)],
        ),

        # CASE 5: bulk item
        BillContext(
            bill_id="BILL_205",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 2)],
        ),

        # CASE 6: buy N
        BillContext(
            bill_id="BILL_206",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 3)],
        ),

        # CASE 7: buy X get Y
        BillContext(
            bill_id="BILL_207",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 2)],
        ),

        # CASE 8: combo
        BillContext(
            bill_id="BILL_208",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            items=[
                Item("CF", "Coffee", 30000, 1),
                Item("CK", "Cake", 40000, 1),
            ],
        ),

        # CASE 9: channel
        BillContext(
            bill_id="BILL_209",
            member_level="NONE",
            channel="TAKE_AWAY",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 1)],
        ),

        # CASE 10: segment
        BillContext(
            bill_id="BILL_210",
            member_level="PLATINUM",
            channel="DINE_IN",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 1)],
        ),

        # CASE 11: bill count (giả lập)
        BillContext(
            bill_id="BILL_215",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            items=[Item("CF", "Coffee", 30000, 1)],
        ),

        # CASE 12: voucher
        BillContext(
            bill_id="BILL_216",
            member_level="NONE",
            channel="DINE_IN",
            hour=13,
            voucher="PROMO50",
            items=[Item("CF", "Coffee", 80000, 1)],
        ),
    ]

    print("[POS] Bắt đầu checkout 12 bills → gọi Promotion Engine")

    for bill in bills:
        print(f"[POS] Checkout {bill.bill_id}")
        engine.calculate(bill)
