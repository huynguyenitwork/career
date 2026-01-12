# test case
## sales receipt sync api

## total sales data sync api

# thời điểm golive
- 12/12 (dự kiến 1/11)
	
# yêu cầu cần xử lý
2 - tích hợp saledata	
	2.1	sales transaction
	2.2	sales line
		thực hiện **gởi dữ liệu bán hàng cuối ngày sau khi đóng ca** (thực hiện đồng bộ dữ liệu bán hàng qua api)
	2.3	eod
		thực hiện **tổng hợp số liệu từ chi tiết để gởi về erp**
		
# các mục đang xử lý
1 - tích hợp masterdata	
	1.1	menu (item / combo)
	1.2	price
	1.3	store

**2 - tích hợp saledata	**
	2.1	**sales transaction**
	2.2	**sales line**
	2.3	**eod**

5 - promotion	
	5.1	tích hợp nhận promotion từ taptap
	5.2	xử lý tính toán giá trị giảm giá
	5.3	áp dụng promotion trên pos
	
# giai đoạn phần mềm
1. kick-off
2. workshop
3. phân tích và thiết kế hệ thống
4. development
5. sit
6. uat
7. go-live