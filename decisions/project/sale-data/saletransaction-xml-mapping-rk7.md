# saletransaction → xml: mapping rk7
## phạm vi
- chỉ dùng để hiểu và kiểm tra **luồng lấy dữ liệu → ghép xml**
- không phân tích sql, không bàn nghiệp vụ sap

---

## mục tiêu quyết định
- biết **sp nào sinh ra segment nào trong xml**
- khoanh nhanh lỗi thiếu/sai segment khi xml không đạt

---

## nguyên tắc lọc
- mỗi sp = 1 lớp dữ liệu
- sp không map ra segment → loại khỏi phạm vi debug
- chỉ quan tâm thứ tự ghép, không quan tâm chi tiết field

---

## khung xml chuẩn (thứ tự)
- idocheader
- transaction
- lineitem
- lineitemdisc
- lineitemtax
- payment
- creditcard

lệch thứ tự → sap reject

---

## mapping 20/80 theo sp

- sp_getidocheader
  - tạo header xml
  - không lấy rk7 table
  - thiếu sp này → xml không gửi được

- sp_gettransaction / sp_gettransactionex
  - nguồn: rk7_checks
  - sinh segment transaction
  - thiếu → không có cấp hóa đơn

- sp_getlineitem
  - nguồn: rk7_checks, rk7_dishes, rk7_taxes
  - sinh lineitem + thuế theo món
  - dùng khi sap cần thuế gắn item

- sp_getlineitemex
  - nguồn: rk7_checks, rk7_dishes
  - sinh lineitem không thuế
  - dùng khi thuế xử lý cấp tổng

- sp_getlineitemdisc
  - nguồn: rk7_checks, rk7_dishes, rk7_discs
  - sinh discount theo item
  - thiếu → sai tổng tiền

- sp_getlineitemtax
  - nguồn: rk7_checks, rk7_dishes, rk7_taxes
  - sinh tax tách dòng
  - chỉ dùng khi sap yêu cầu bóc thuế

- sp_getpayment
  - nguồn: rk7_checks, rk7_payments, card_transactions
  - sinh payment segment
  - thiếu → hóa đơn coi như chưa thu tiền

- sp_getcreditcard
  - nguồn: rk7_checks, rk7_payments, card_transactions
  - sinh creditcard segment
  - chỉ tồn tại khi payment = card

---

## checklist debug nhanh
- xml thiếu header → check sp_getidocheader
- xml có bill nhưng rỗng món → check getlineitem / getlineitemex
- sai tổng tiền → check lineitemdisc / tax
- sap báo thiếu payment → check sp_getpayment
- lỗi thẻ → chỉ soi sp_getcreditcard

---

## kết luận vận hành
- mỗi sp = một mảnh lego xml
- lỗi xml = lỗi thiếu hoặc sai lego
- debug theo lớp, không debug toàn cục
- hiểu mapping này là đủ kiểm soát 80% lỗi sale xml