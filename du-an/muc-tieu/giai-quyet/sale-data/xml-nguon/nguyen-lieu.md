# SaleTransaction
## nguồn
SP_GetIDOCHeader (SELECT)
SP_GetTransaction| RK7_CHECKS
SP_GetTransactionEx| RK7_CHECKS
SP_GetLineItem| RK7_CHECKS, RK7_DISHES, RK7_TAXES
SP_GetLineItemEx| RK7_CHECKS, RK7_DISHES
SP_GetLineItemDisc| RK7_CHECKS, RK7_DISHES, RK7_DISCS
SP_GetLineItemTax| RK7_CHECKS, RK7_DISHES, RK7_TAXES
SP_GetPayment| RK7_CHECKS, RK7_PAYMENTS, CARD_TRANSACTIONS
SP_GetCreditCard| RK7_CHECKS, RK7_PAYMENTS, CARD_TRANSACTIONS

## mô tả
### kết quả đầu ra
- hệ thống **rk7** khi xuất dữ liệu bán hàng (sale) sang sap phải dựng ra một cấu trúc xml khá phức tạp: header → transaction → line item → chiết khấu → thuế → payment → credit card.
- những stored procedure này chính là “đường ống” rút dữ liệu từ các bảng rk7 để ghép thành xml.
### store procedure

#### 1. SP_GetIDOCHeader

Bảng: Không lấy bảng RK7, chỉ SELECT tham số
Đây là cái “khung sườn”, kiểu giấy khai sinh của gói XML.
Nó tạo metadata cần cho SAP: mã hệ thống, thời gian tạo, số tài liệu, kiểu interface.
Nếu ví hóa đơn là một lá thư thì cái này chính là phần “header của phong bì”.

#### 2. SP_GetTransaction / SP_GetTransactionEx

Bảng dùng: RK7_CHECKS

Hai thằng này giống nhau 80%, khác 20% là “Ex” thường trả thêm chi tiết mở rộng.
Công dụng: lấy thông tin một bill bán hàng ở mức tổng quát.

Những thứ như:
• Số hóa đơn
• Thời điểm mở – đóng bill
• Tổng tiền
• Nhân viên, bàn, ca làm việc
• Các flag liên quan đến trạng thái bill

Tóm gọn: “đây là dữ liệu cấp hóa đơn”.

#### 3. SP_GetLineItem

Bảng: RK7_CHECKS, RK7_DISHES, RK7_TAXES

Đây là “linh hồn chính”—lấy danh sách món trong hóa đơn.
Từ món ăn, số lượng, đơn giá, thành tiền, thuế của từng món.
Bảng Dishes là món; Taxes là thuế theo từng dòng.

Tóm gọn: “dòng món ăn có thuế”.

#### 4. SP_GetLineItemEx

Bảng: RK7_CHECKS, RK7_DISHES

Bản rút gọn không tính thuế, chỉ lấy dữ liệu món & số lượng.
Dùng khi hệ thống chỉ cần output món nhưng không quan tâm thuế theo item.

Tóm gọn: “dòng món ăn không thuế”.

#### 5. SP_GetLineItemDisc

Bảng: RK7_CHECKS, RK7_DISHES, RK7_DISCS

Lấy chiết khấu trên từng món.
Ví dụ: giảm giá 10%, combo, voucher tác động vào món, v.v.

Tóm gọn: “chiết khấu từng món”.

#### 6. SP_GetLineItemTax

Bảng: RK7_CHECKS, RK7_DISHES, RK7_TAXES

Dùng khi hệ thống cần bóc riêng phần thuế của từng món.
Một số interface cần thuế tách dòng.

Tóm gọn: “thuế từng món”.

#### 7. SP_GetPayment

Bảng: RK7_CHECKS, RK7_PAYMENTS, CARD_TRANSACTIONS

Lấy thông tin thanh toán của hóa đơn:
• Tiền mặt
• Momo
• Thẻ
• Voucher
• Trả lại tiền thừa

Khi thanh toán có thẻ, nó join thêm bảng CARD_TRANSACTIONS để lấy mã giao dịch.

Tóm gọn: “tất cả thông tin thanh toán”.

#### 8. SP_GetCreditCard

Bảng: RK7_CHECKS, RK7_PAYMENTS, CARD_TRANSACTIONS

Giống Payment nhưng lọc riêng thanh toán bằng thẻ, lấy chi tiết như:
• BIN, issuer
• Số tham chiếu ngân hàng
• Mã giao dịch POS

Tóm gọn: “chi tiết chuyên sâu thẻ ngân hàng”.

### tổng kết

Một hóa đơn bán hàng → phải ghép thành XML với 6 lớp thông tin.
Mỗi SP giải quyết một lớp.

Nếu ví cả hệ thống là một bộ phim, thì:

• IDOCHeader = opening scene
• Transaction = hồ sơ nhân vật chính
• LineItem = diễn viên
• Discount/Tax = đạo cụ
• Payment = phân cảnh kết thúc
• CreditCard = đoạn hậu trường cho giao dịch thẻ

Nhìn đúng 20%, ta hiểu được toàn bộ 80% luồng xử lý dữ liệu hóa đơn.

Hệ thống RK7 dùng cách **modular** này vì **SAP thích dữ liệu tách lớp**, rõ ràng, truy vết được.