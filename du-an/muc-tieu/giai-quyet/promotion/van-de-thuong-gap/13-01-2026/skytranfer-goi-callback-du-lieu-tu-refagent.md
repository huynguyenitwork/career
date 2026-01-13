# sketch flow
1. service skytransfer
-> call api service refagent để setdata 
	=> nhận request-id khi thành công (success **true**)
	=> báo lỗi khi thất bại (success false)
		~> buildfail(400) → notsupported(400) → argex(400) → invalidop(503) → ex(500)
		
	
2. service refagent
-> inbound dữ liệu từ call api setdata
-> queue job và handler
	=> phản hồi dữ liệu sau cud discount
		~> thành công: trả success(response) với successmenuitem=true (không lỗi) + results[]
		~> thất bại: failure("lỗi") hoặc successmenuitem=false (có errormessage trong results)
	=> **phản hồi callback url, request-id và kèm dữ liệu**

	
mong muốn:
- skytransfer muốn nhận phản hồi từ callback url với request-id nhận được thì làm thế nào?
- xử lý trực tiếp từ flow 1 hay tách riêng
