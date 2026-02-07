"""
Promotion Engine cơ bản – có print timeline từng bước
Mục tiêu: chạy code là THẤY NGAY quy trình POS → Engine → POS
"""

from typing import List, Dict
from dataclasses import dataclass

# ====== Data models ======

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
    member_level: str  # NONE | SILVER | GOLD
    channel: str       # DINE_IN | TAKE_AWAY
    time: str          # ISO datetime string

@dataclass
class PromotionResult:
    total_discount: float
    item_discounts: Dict[str, float]
    final_amount: float
    applied_promotions: List[str]


# ====== Promotion Engine ======

class PromotionEngine:
    """
    Promotion Engine chỉ làm 1 việc:
    Nhận context từ POS -> trả kết quả áp khuyến mãi
    """

    def calculate(self, context: BillContext) -> PromotionResult:
        print("\n[ENGINE] Nhận context từ POS")
        print(f"[ENGINE] Bill ID: {context.bill_id}")

        # Step 1: tính tổng tiền gốc
        total_amount = sum(i.price * i.qty for i in context.items)
        print(f"[ENGINE] Tổng tiền gốc (chưa KM): {total_amount}")
        print(f"[PROMOTION ENGINE] Bắt đầu áp dụng khuyến mãi...")
        print(f"================================")        

        item_discounts = {}
        applied_promotions = []
        total_discount = 0.0

        # Step 2: áp promotion theo member
        print("[ENGINE] Kiểm tra promotion theo member")
        if context.member_level == "GOLD":
            discount = total_amount * 0.10
            total_discount += discount
            applied_promotions.append("MEMBER_GOLD_10_PERCENT")
            print(f"[ENGINE] Áp MEMBER_GOLD_10_PERCENT: -{discount}")
        else:
            print("[ENGINE] Không có promotion theo member")

        # Step 3: áp promotion theo item
        print("[ENGINE] Kiểm tra promotion theo item")
        for item in context.items:
            if item.qty >= 2:
                d = item.price * item.qty * 0.05
                item_discounts[item.id] = d
                total_discount += d
                applied_promotions.append(f"BULK_{item.id}_5_PERCENT")
                print(f"[ENGINE] Áp BULK cho {item.name}: -{d}")
            else:
                print(f"[ENGINE] Item {item.name} không đủ điều kiện bulk")

        print(f"================================")     
        print(f"[PROMOTION ENGINE] Kết thúc áp dụng khuyến mãi.") 
        
        # Step 4: tính tiền cuối cùng
        final_amount = max(total_amount - total_discount, 0)
        print(f"[ENGINE] Tổng giảm giá: {total_discount}")
        print(f"[ENGINE] Số tiền POS cần thu: {final_amount}")

        # Step 5: trả kết quả cho POS
        print("[ENGINE] Trả kết quả về cho POS\n")

        return PromotionResult(
            total_discount=round(total_discount, 2),
            item_discounts=item_discounts,
            final_amount=round(final_amount, 2),
            applied_promotions=list(set(applied_promotions))
        )


# ====== Giả lập POS ======

if __name__ == "__main__":
    print("[POS] Tạo bill và chuẩn bị gọi Promotion Engine")

    bill = BillContext(
        bill_id="BILL_001",
        member_level="GOLD",
        channel="DINE_IN",
        time="2025-01-01T12:00:00",
        items=[
            Item(id="CF01", name="Coffee", price=30000, qty=2),
            Item(id="CK01", name="Cake", price=40000, qty=1),
        ]
    )

    engine = PromotionEngine()

    print("[POS] Gọi Promotion Engine.calculate()")
    result = engine.calculate(bill)

    print("[POS] Nhận kết quả từ Promotion Engine")
    print(f"[POS] Tổng giảm giá: {result.total_discount}")
    for item_id, discount in result.item_discounts.items():
        print(f"[POS] Giảm giá cho item {item_id}: {discount}")
    print(f"[POS] Tổng tiền phải thu: {result.final_amount}")
    print(f"[POS] Promotion đã áp: {result.applied_promotions}")
