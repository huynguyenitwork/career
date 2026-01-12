# đặt vấn đề

về task promotion engine, đối với các Scheme hiện có trên BDD phần sync promotion như hôm 23/12 3 anh em trao đổi thì dữ liệu ecom sẽ nên đẩy qua bên cloud cụ thể là sky restro để phục vụ POS lấy danh sách discount và verify/calculate cho order
- hiện tại khi thêm trường hợp ecom gởi open discount thì promotion engine dùng với skytransfer để chuyển trực tiếp sang rk7 để sử dụng, em đang triển khai phần này
tuy nhiên, để dễ quản lý vận hành và không tách nhánh quá nhiều và ảnh hưởng tới skytransfer, anh Trường có yêu cầu em chuyển dữ liệu ecom trong trường hợp trên qua sky restro quản lý và điều phối cùng với các scheme hiện có
Vấn đề là em chưa rõ flow hoạt động nếu trong trường hợp promotion engine này sẽ xử lý thế nào
- đầu tiên là api để ECOM gởi dữ liệu sang vẫn sẽ triển khai trên skytransfer để store-and-forward cho rk7/pos hay là api này sẽ đặt để ở skyrestro và bên mình cung cấp api mới cho ECOM
- thứ 2 nếu api đặt để ở skyrestro thì việc store-and-forward trên skyrestro có gặp rủi ro gì trong trường hợp cần sync lại từ transfer qua rk7/pos

# thảo luận

Anh Tính cho em xin ý kiến để **thống nhất luồng đồng bộ promotion** cho task *Promotion Engine* ạ.

Theo các **Scheme hiện có trên BDD** và buổi trao đổi ngày **23/12** giữa anh em mình, thì:

* Dữ liệu promotion từ **ECOM** sẽ được **đẩy lên Cloud**, cụ thể là **SkyRestro**,
* POS sẽ cần lấy danh sách discount và **verify / calculate** các discount khả dụng cho order.

Hiện tại, với **trường hợp ECOM gửi Open Discount**, Promotion Engine đang:

* Dùng **SkyTransfer** để **chuyển trực tiếp sang RK7/POS** sử dụng => Phần này em đang triển khai theo cách đó.

Tuy nhiên, để:

* Dễ quản lý vận hành,
* Tránh tách nhánh logic quá nhiều,
* Hạn chế ảnh hưởng đến SkyTransfer,

thì **anh Trường có đề xuất**:
👉 Chuyển dữ liệu ECOM (case Open Discount) **qua SkyRestro quản lý**, và điều phối **chung với các Scheme hiện có**.

Vấn đề hiện tại là em **chưa rõ flow xử lý cuối cùng của Promotion Engine** trong (case Open Discount) để tiếp tục, nên em muốn hỏi để chốt hướng:

1. **API ECOM gửi dữ liệu**

   * ECOM vẫn gọi API đặt ở **SkyTransfer** (đóng vai trò store-and-forward), sau đó sync tiếp sang RK7/POS?
   * Hay API này sẽ **đặt trực tiếp ở SkyRestro**, và bên mình sẽ **cung cấp API mới cho ECOM**?

2. **Trường hợp API đặt ở SkyRestro**

   * Việc **store-and-forward trên SkyRestro** có rủi ro gì không, đặc biệt trong các tình huống cần **sync lại dữ liệu** từ SkyRestro → RK7/POS (retry, recovery, replay data)?

Em muốn chốt rõ 2 điểm này để **triển khai cho phù hợp**, tránh phải điều chỉnh lại flow sau này
