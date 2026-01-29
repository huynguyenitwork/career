## script combo / product

### mục tiêu
- kiểm tra đúng quan hệ combo – product – variant
- reset data test an toàn
- xác nhận mapping sku rk7 ↔ ecom

---

### combo – kiểm tra
- kiểm tra combo + toàn bộ bảng phụ theo comboid
- thiếu 1 bảng → combo sai

```sql
select * from ecomcombo where id in (21,23,24);
select * from ecomcomboexcludeddate where comboid in (21,23,24);
select * from ecomcomboapplicabletime where comboid in (21,23,24);
select * from ecomcombogroup where comboid in (21,23,24);
select * from ecomcomboproduct where combogroupid in (28,29,30,31);
select * from ecomcombovariant where comboid in (21,23,24);
````

---

### combo – xóa data test

* thứ tự bắt buộc: bảng phụ → bảng chính

```sql
delete from ecomcomboexcludeddate where comboid in (23,24);
delete from ecomcomboapplicabletime where comboid in (23,24);
delete from ecomcomboproduct where combogroupid in (28,29,30,31);
delete from ecomcombogroup where comboid in (23,24);
delete from ecomcombovariant where comboid in (23,24);
delete from ecomcombo where id in (23,24);
```

---

### product – kiểm tra

* product lỗi → combo lỗi theo

```sql
select * from ecomproduct where id in (111,112,113);
select * from ecomvariant where productid in (111,112,113);
select * from ecomproductoption where productid in (111,112,113);
```

---

### product – xóa data test

* thứ tự bắt buộc: option → variant → product

```sql
delete from ecomproductoption where productid = 114;
delete from ecomvariant where productid = 114;
delete from ecomproduct where id = 114;
```

---

### mapping sku (điểm chết)

* combo: gensapcomponentmaster (rk7) → combosku (ecom)
* item: gensapcode (rk7) → variantsku (ecom)
* sku lệch → sinh combo sai

---

### data đối chiếu nhanh

* rk7: combo "28999998", item "21001247"
* ecom: combosku / variantsku phải khớp 1–1

---

### regex dùng khi soi log

```regex
(genSAPCODE=")(.+?)(")
```

---

### store procedure dùng để sync

* sp_ecomvariant: lấy variant processstatus = 0
* sp_ecomcombo: lấy combo processstatus = 0
* sp_ecomcombovariant: map combo ↔ variant
* sp trả sai → sync sai

---

### kết luận

* lỗi combo luôn kiểm tra từ sku
* xóa sai thứ tự → vỡ quan hệ
* mapping đúng > logic phức tạp

