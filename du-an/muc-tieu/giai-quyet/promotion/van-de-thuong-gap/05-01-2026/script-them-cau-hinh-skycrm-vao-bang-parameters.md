# timeline
- 15-01-2026: sửa skycloud=>skycrm bổ sung thêm port skycrm vào parameter
- 05-01-2026: xóa tham số discount group id, không cần thiết lập discount group id vì trong discount đã có rồi 
- 31-12-2025: thêm các thông tin về key Organization Id/DiscountGroups Id thay vì dùng theo key name khó kiểm tra
- 29-12-2025: thêm các thông tin về server/Organization Name/ApiSuffixCRM/ApiSuffixMasterData

# thêm cấu hình skycrm vào bảng parameters

## mục tiêu

chỉ lưu **1 tham số cần dùng** để gọi skycrm:

* server
* ~~access token ~~ (không lưu xem vấn đề bên dưới)

không thêm các key auth khác vì **hiện không dùng**.

---

## key dùng trong code

```csharp
#region SkyCRM
//longterm
public const string SkyCRMServer = "SkyCRMServer";
public const string SkyCRMPort = "SkyCRMPort";
//api suffix
public const string SkyCRMApiSuffixCRM = "SkyCRMApiSuffixCRM";
public const string SkyCRMApiSuffixMasterData = "SkyCRMApiSuffixMasterData";

//shortterm
public const string SkyCRMOrganizationId = "SkyCRMOrganizationId";
//tạo mới discount group
public const string SkyCRMDiscountGroupCode = "SkyCRMDiscountGroupCode";
public const string SkyCRMDiscountGroupName = "SkyCRMDiscountGroupName";
#endregion
```

---

## script insert
- cần tùy chỉnh SkyCRMOrganizationId và SkyCRMDiscountGroupId phù hợp với môi trường
```sql
INSERT INTO Parameters (name, status, parentId, description, paramName, intVal, strVal)
VALUES
-- core
(N'Sky CRM Server', 4, 0, NULL, 'SkyCRMServer', 0, 'https://api-dev.dcorp.com.vn'),
(N'Sky CRM Port', 4, 0, NULL, 'SkyCRMPort', NULL, NULL),

-- organization
(N'Sky CRM Organization Id', 4, 0, NULL, 'SkyCRMOrganizationId', 8582, NULL),

-- api suffix
(N'Sky CRM Api Suffix CRM', 4, 0, NULL, 'SkyCRMApiSuffixCRM', 0, 'crm/'),
(N'Sky CRM Api Suffix MasterData', 4, 0, NULL, 'SkyCRMApiSuffixMasterData', 0, 'masterdata/'),

-- discount group runtime
(N'Sky CRM Discount Group Name', 4, 0, NULL, 'SkyCRMDiscountGroupName', 0, '[dev] open discount'),
(N'Sky CRM Discount Group Code', 4, 0, NULL, 'SkyCRMDiscountGroupCode', 0, 'devop')
```

---

## ghi chú

* `status = 4`: tham số đang sử dụng
* `paramName`: map trực tiếp với constant trong code
* Token hết hạn → cập nhật `strVal`, **không đổi cấu trúc**

---

## kết luận

* chỉ 2 key → **đủ chạy, không thừa**
* khi nào dùng oauth / refresh token → **mở rộng sau**

## vấn đề thường gặp
### access token ~6000 ký tự 
**không nên** nhét vào chỗ thiết kế cho 256 ký tự.

---

#### vấn đề cốt lõi

* jwt dài ~4–6kb là **bình thường**
* cột `strval (varchar(256))` là **không phù hợp về mặt thiết kế**
* cắt chuỗi / truncate token = lỗi ngầm, rất khó debug

không phải *có lưu được không*, mà là *có nên không*.

---

#### 3 hướng xử lý (đi thẳng, không vòng vo)

##### 1. chuẩn chỉnh nhất (khuyên dùng)

**không lưu access token vào `parameters`**

* chỉ lưu:

  * `skycrmserver`
  * thông tin để **lấy token** (client / secret / endpoint)
* token:

  * lưu in-memory / cache (redis, memorycache)
  * hết hạn thì refresh

→ đúng kiến trúc, đúng bảo mật, đúng đời dài.

---

##### 2. chấp nhận thực tế, sửa db

nếu **bắt buộc lưu token**:

* đổi `strval` → `nvarchar(max)` hoặc `text`
* hoặc thêm cột riêng:

  * `longstrval`
  * `jsonval`

→ ít đụng code, nhưng phải chấp nhận rủi ro bảo mật.

---

##### 3. tạm thời, chữa cháy (không khuyến khích)

* encode / split token
* lưu nhiều dòng parameters

→ mùi hack, về sau chính bạn quay lại chửi mình.

---

#### quyết định nhanh theo 20/80

* token **6000 ký tự** + **có hạn sử dụng**
  → **không nên** coi là “parameter cấu hình”

> parameter là thứ **ổn định – ngắn – lâu dài**
> token là thứ **tạm thời – dài – dễ chết**

---

#### câu chốt để nói với team

> *access token không phải config. nó là runtime data.
> bảng parameters không nên gánh trách nhiệm đó.*

nói xong là hết tranh luận.


