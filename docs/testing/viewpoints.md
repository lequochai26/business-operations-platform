# Bảng khía cạnh test

Mọi lần `/test-case-design` phải xét đủ các khía cạnh dưới đây. Khía cạnh không áp dụng cho một tính năng thì ghi lý do trong file test case.

Phạm vi manual test: mọi thứ con người làm được bằng tay qua trình duyệt, DB, cookie, Facebook, Messenger, thiết bị thật. Không gồm việc can thiệp vào luồng xử lý của code.

## 1. Hiển thị

### Câu hỏi gợi ý
- Màn hình có khớp mockup ở mọi trạng thái đã thiết kế (trống, đang tải, có dữ liệu, lỗi, không có quyền)?
- Dữ liệu hiển thị có đúng với bản ghi trong DB không (số, giá, ngày giờ, trạng thái, tên)?
- Chữ tiếng Việt có dấu, tên Facebook có emoji, chuỗi rất dài có bị vỡ dòng, tràn khung, cắt mất chữ không?
- Ở bề ngang điện thoại (iPhone của chủ tiệm, Android của thợ) và máy tính, bố cục có dùng được bằng ngón cái, không cuộn ngang không?
- Ngày giờ có hiển thị theo giờ Việt Nam và đúng định dạng thống nhất (thứ, ngày/tháng, 24h) không?
- Màu và nhãn trạng thái có phân biệt rõ (chưa duyệt / đã chốt / khung bận, chạy / tạm dừng / bị dừng)?
- Ảnh (ảnh gốc, ảnh đã chỉnh, poster, ảnh thu nhỏ) có đúng ảnh, đúng chiều, không méo không?
- Đánh giá bằng mắt: poster đúng nhận diện (khổ 1080×1350, màu, font), chữ không đè lên vùng móng, giọng văn đúng giọng tiệm?

### Ví dụ
- Trang chính: số comment hôm nay so với giới hạn (ví dụ 7/15) khớp số bản ghi đã gửi trong DB; chu kỳ quét thực tế hiển thị đúng.
- Lịch tuần trên iPhone: lịch ép chọn mang cảnh báo rõ, lịch chưa duyệt và đã chốt khác màu.
- Màn hình duyệt mẫu mới: ảnh gốc và ảnh đã chỉnh đặt cạnh nhau để so; poster ghi "99k trọn bộ" chỉ khi đã xác nhận trọn bộ.
- Danh sách khách: tên Facebook dài có emoji, tin nhắn gần nhất nhiều dòng vẫn hiển thị gọn.

## 2. Kiểm tra dữ liệu nhập

### Câu hỏi gợi ý
- Trường bắt buộc để trống, chỉ có dấu cách thì sao?
- Giá trị ngay dưới, bằng, ngay trên giới hạn dưới và trên?
- Sai kiểu (chữ vào ô số, số âm, số thập phân)?
- Sai định dạng (URL, số điện thoại, giờ)?
- Trùng với bản ghi đã có?
- Chuỗi rất dài, emoji, tiếng Việt có dấu tổ hợp?
- Dán nội dung có ký tự xuống dòng hoặc khoảng trắng đầu/cuối?
- Tải lên file sai loại, quá lớn, ảnh xoay theo EXIF?

### Ví dụ
- Cài đặt group: dán link `facebook.com/groups/abc?ref=share`, dán ID số, dán link không phải group, dán lại group đã có.
- Giới hạn comment/ngày: 0, 1, 15, 16, -1, `abc`, `2.5`.
- Giờ làm việc: giờ kết thúc trước giờ bắt đầu, hai khoảng giờ chồng nhau trong cùng ngày; khoảng giờ buổi sáng/chiều/tối chồng nhau.
- Danh sách từ cấm và từ khóa lọc: nhập có dấu và không dấu, trùng từ, từ chỉ có dấu cách.

## 3. Logic nghiệp vụ

### Câu hỏi gợi ý
- Mỗi quy tắc `R-<ABC>-<nn>` trong thiết kế có ít nhất một case cho nhánh đúng và một case cho nhánh sai không?
- Quy tắc nhiều điều kiện (bảng quyết định) đã đủ tổ hợp chưa, kể cả tổ hợp "không điều kiện nào thỏa"?
- Tham số cài đặt có thật sự được dùng không: đổi giá trị trên web thì hành vi có đổi theo?
- Mọi thông tin app nói với khách (giá, giờ, địa chỉ, chính sách) có truy được về nguồn (bộ thông tin tiệm đã xác nhận, lịch, kho, câu trả lời của thợ) không?
- Khi thiếu dữ liệu đầu vào (chưa có giờ làm, chưa bật bộ content, mục thông tin chưa xác nhận), app dừng đúng chỗ và báo đúng người chưa?
- Nội dung app sinh ra có tránh từ tuyệt đối, "trọn bộ như hình", "ảnh thật tại tiệm" khi không đúng không?
- Xoay vòng, giới hạn và giãn cách có tính đúng theo phạm vi (toàn tài khoản, từng group, từng ngày) không?

### Ví dụ
- Phân loại bài: bài loại 1, 2, 3, bài vừa hỏi giờ vừa có ảnh (phải là loại 3), bài bán hàng tiệm khác, bài tuyển nhân viên, bài tìm thợ mi.
- Lọc khu vực: bài không nhắc khu vực, bài nhắc Quận 11, bài chỉ nhắc khu vực ngoài danh sách.
- Comment loại 2: ngày khách hỏi còn trống, không còn trống (đề xuất tối đa 3 khung trải khác buổi), không có khung nào trong 7 ngày (không comment, ghi lý do).
- Inbox: khách hỏi chính sách cọc khi mục đó chưa xác nhận → chuyển cho người thật, không tự trả lời.

## 4. Chuyển trạng thái

### Câu hỏi gợi ý
- Mọi chuyển trạng thái hợp lệ trong sơ đồ đã có case chưa?
- Chuyển không hợp lệ (ví dụ từ trạng thái cuối quay lại) có bị chặn và báo rõ không?
- Thao tác trên bản ghi đã ở trạng thái cuối (đã hủy, đã hết hạn, đã bỏ) thì sao?
- Trạng thái liên quan có cập nhật theo không (lịch hẹn → trạng thái khách, báo giá → trạng thái bài)?
- Lịch sử thay đổi có ghi đủ ai đổi, lúc nào, qua kênh nào, giá trị cũ không?
- Cùng một chuyển trạng thái làm qua web và qua Messenger có cho kết quả giống nhau không?

### Ví dụ
- Lịch hẹn: chưa duyệt → đã chốt → đã làm xong; chưa duyệt → đã hủy; thử đánh dấu "đã làm xong" cho lịch chưa duyệt (phải bị chặn).
- Bài trong group: chờ báo giá → thợ báo "bỏ" → bỏ qua; chờ duyệt → quá tuổi tối đa → tự hết hạn; thất bại → comment lại.
- Khách: mới → đang trao đổi → đã giữ chỗ → đã chốt lịch → đã xong; đang trao đổi 3 ngày không có tin → ngừng trao đổi.
- Yêu cầu báo giá đã hết hạn: thợ trả lời "99k" → không áp dụng, app báo lại cho thợ.

## 5. Phân quyền

### Câu hỏi gợi ý
- Vai trò Thợ có thấy hoặc bấm được những gì chỉ Quản lý được làm không (cả nút trên màn hình lẫn gõ thẳng URL)?
- Gọi thẳng API của chức năng chỉ dành cho Quản lý bằng phiên Thợ thì nhận lỗi gì?
- Chưa đăng nhập mà mở URL bên trong app thì sao?
- Trên Messenger, người lạ (không phải thợ, không phải chủ tiệm) nhắn mã ghép nối hoặc lệnh của thợ thì sao?
- Tin nhắn từ thợ hoặc chủ tiệm có bao giờ bị xử lý như tin của khách không?
- Tài khoản thợ bị chủ tiệm khóa/xóa thì phiên đang mở còn dùng được không?

### Ví dụ
- Đăng nhập vai trò Thợ, mở URL `/settings`, bấm nút dừng khẩn cấp, gọi API duyệt comment: đều phải bị chặn.
- Thợ được thao tác Lịch, Báo giá, Khách, tải mẫu mới; không được duyệt mẫu mới, không sửa comment group.
- Khách nhắn "duyệt" hoặc "#G12 99k" vào Page: không được tính là thợ báo giá hay duyệt lịch.

## 6. Phiên đăng nhập và cookie

### Câu hỏi gợi ý
- Xóa cookie phiên web app giữa chừng rồi thao tác tiếp thì sao, dữ liệu đang nhập có mất âm thầm không?
- Đăng nhập sai nhiều lần có bị giới hạn không?
- Đăng nhập lâu dài trên điện thoại có giữ được qua tắt mở PWA, khởi động lại máy không?
- Đổi mật khẩu thì các phiên cũ ở thiết bị khác ra sao?
- Phiên Facebook của tài khoản vận hành hết hạn (xóa cookie trong profile, đăng xuất từ thiết bị khác) thì app có tự dừng và báo khẩn không?
- Phiên Meta Business Suite của tài khoản inbox hết hạn thì worker inbox có dừng và báo không, có gửi nhầm gì cho khách không?
- Sau khi đăng nhập lại qua noVNC, bấm "chạy lại" thì app có hoạt động lại đúng không?

### Ví dụ
- Đăng xuất tài khoản vận hành khỏi Facebook từ điện thoại khác → lượt quét kế tiếp phát hiện hết phiên, tắt toàn bộ tác vụ tự động, lưu ảnh màn hình, báo chủ tiệm qua Messenger và email.
- Xóa cookie web app khi đang sửa comment chờ duyệt → bấm lưu thì được đưa về trang đăng nhập, không lưu nửa vời.
- Đăng nhập sai mật khẩu liên tiếp vượt giới hạn → bị khóa tạm, thông báo rõ.

## 7. Thao tác đồng thời

### Câu hỏi gợi ý
- Bấm gửi/duyệt hai lần liên tiếp thì có tạo hai bản ghi hoặc gửi hai lần không?
- Hai tab (hoặc hai người) cùng sửa một bản ghi thì ai thắng, người kia có được báo không?
- Thợ thao tác qua Messenger đúng lúc chủ tiệm thao tác cùng bản ghi trên web thì sao?
- Hai luồng tự động cùng muốn chiếm một khung giờ (hai khách inbox cùng xin một slot) thì sao?
- Người thật trả lời khách từ Page đúng lúc app chuẩn bị gửi tin tự động thì sao?
- Bấm Back, tải lại trang giữa lúc đang xử lý thì kết quả có nhất quán không?

### Ví dụ
- Hai khách nhắn gần như cùng lúc xin 14h thứ Ba: chỉ một khách được giữ chỗ, khách kia được đề xuất khung khác.
- Thợ bấm "Duyệt" trên Messenger trong khi chủ tiệm bấm "Hủy" trên web cho cùng lịch: thao tác đến trước được áp dụng, thao tác sau nhận "lịch đã thay đổi".
- Chủ tiệm bấm "Duyệt" comment hai lần nhanh: chỉ một comment được gửi lên bài.
- Hai tab cùng sửa giờ làm việc tuần rồi lưu: không mất dữ liệu âm thầm.

## 8. Dữ liệu bất thường trong DB

### Câu hỏi gợi ý
- Bản ghi liên quan bị xóa (bộ content, poster, group, khách) thì màn hình và luồng tự động phản ứng thế nào?
- Trường không bắt buộc bị để NULL, chuỗi rỗng thì có lỗi hiển thị hay lỗi xử lý không?
- Dữ liệu ở trạng thái "lạ" mà UI không tạo ra được (lịch chồng nhau không có cờ ép chọn, trạng thái không khớp lịch sử) thì app có crash không?
- Sửa thời điểm trong DB để giả lập thời gian trôi qua thì job hẹn giờ có chạy đúng không?
- Dữ liệu cũ đã "lưu trữ" có còn liên kết được từ lịch sử comment, bài đăng không?
- Số lượng lớn (hàng nghìn bài, hàng trăm khách) thì danh sách, lọc, tìm kiếm có còn dùng được không?

### Ví dụ
- Xóa poster đang được bộ content loại 1 dùng → lượt comment kế tiếp không gửi comment thiếu ảnh, báo chủ tiệm.
- Sửa `created_at` của lịch chưa duyệt lùi 2 giờ → app nhắc thợ.
- Chèn tay hai lịch đã chốt chồng nhau (không có cờ ép chọn) → màn hình lịch vẫn mở được và cảnh báo.
- Mục thông tin tiệm đã xác nhận bị đổi về "chưa xác nhận" → inbox không dùng mục đó nữa.

## 9. Phía Facebook và Messenger

### Câu hỏi gợi ý
- Bài gốc bị xóa, tắt comment, chuyển riêng tư trước khi app comment thì sao?
- Tài khoản vận hành rời group, bị kick, group bị khóa hoặc chuyển sang duyệt bài thì sao?
- Facebook bắt checkpoint, chặn comment, báo spam thì app có tự dừng toàn bộ và báo khẩn không?
- Người thật trả lời khách từ Page (Business Suite, app Messenger) thì app có nhận ra và ngừng tự trả lời không?
- Thợ trả lời sai cú pháp, trả lời mơ hồ, trả lời yêu cầu đã hết hạn, gửi tin thoại, ảnh không kèm chữ thì sao?
- Thợ vuốt để trả lời đúng tin, bấm nút nhanh, nhắn có mã, nhắn không mã khi có nhiều yêu cầu cùng chờ: có ghép đúng yêu cầu không?
- Cửa sổ 24 giờ của Messenger đã đóng thì thông báo có đi qua web push và email không?
- Comment, bài đăng thật trên Facebook có hiện đúng chữ, đúng poster, đúng group, không bị lặp không?

### Ví dụ
- Xóa bài trong group riêng tư thử sau khi app đã đưa comment vào hàng đợi → comment không gửi, bài đánh dấu bỏ qua.
- Hai yêu cầu báo giá `#G12` và `#G13` cùng chờ, thợ nhắn "99k" không mã → app hỏi lại "Giá 99k này cho mẫu nào?" kèm nút.
- Chủ tiệm nhắn khách từ Meta Business Suite → app tạm dừng tự trả lời cuộc đó 12 giờ, không chen ngang.
- Thợ gửi tin thoại → app trả lời "Mình chưa nghe được tin thoại, bạn nhắn chữ giúp mình nha".

## 10. Thời gian

### Câu hỏi gợi ý
- Thao tác rơi đúng mốc biên (bắt đầu/kết thúc giờ nghỉ, giờ vàng, giờ làm, nửa đêm) thì sao?
- Ngày tương đối ("mai", "thứ 3", "tối nay") có quy đổi theo thời điểm bài/tin được đăng, không theo lúc app xử lý không? Bài đăng lúc 23:50 ghi "mai" thì sao?
- Các hạn chờ (nhắc thợ, hết hạn báo giá, comment chờ duyệt quá tuổi, lịch chưa duyệt bị bỏ quên) có kích hoạt đúng lúc và chỉ một lần không?
- Nội dung, nhãn, bộ content có hạn dùng (ví dụ Halloween hết hạn sau 31/10) có tự tắt đúng ngày không?
- Mọi giờ hiển thị và lưu có đúng múi giờ `Asia/Ho_Chi_Minh` khi máy chủ ở Singapore, điện thoại để múi giờ khác không?
- Khung trống có tôn trọng khoảng cách tối thiểu tính từ hiện tại (mặc định 2 giờ) không?
- Ngày đặc biệt (nghỉ Tết, làm giờ khác) có ghi đè giờ làm tuần đúng không?
- Chạy thật dài ngày: sau nhiều ngày liên tục, giới hạn theo ngày có reset đúng lúc 00:00 giờ Việt Nam không?

### Ví dụ
- Giờ nghỉ 23:30–07:00: comment đến lượt gửi lúc 23:29 và 23:31; không quét, không gửi trong giờ nghỉ.
- Bài đăng tối thứ Hai ghi "mai tuyển mẫu", app quét sáng thứ Ba → "mai" vẫn là thứ Ba.
- Sửa DB lùi thời điểm gửi yêu cầu báo giá 45 phút → app nhắc thợ một lần và báo chủ tiệm; lùi 3 giờ → bỏ qua bài.
- Lịch hẹn kết thúc 16:30 → khoảng 17:00 app hỏi thợ "Khách … lịch 14h đã làm xong chưa?".

## 11. Lỗi mạng và lỗi hệ thống bên ngoài

### Câu hỏi gợi ý
- Điện thoại mất mạng giữa lúc gửi form thì người dùng có biết thao tác chưa thành công không, gửi lại có bị trùng không?
- Máy chủ mất mạng khi đang comment, đăng bài, gửi tin cho khách thì sau khi có mạng lại, app thử lại hay đánh dấu thất bại đúng thiết kế?
- Gemini lỗi, sai khóa API hoặc vượt hạn mức chi tiêu tháng thì app có chuyển sang dự phòng (sao chép prompt, tải ảnh lên tay) và báo chủ tiệm không?
- Graph API đăng Page lỗi thì có báo và cho bấm đăng lại không?
- Messenger Send API lỗi, web push không tới được iPhone thì thông báo khẩn có còn tới qua email không?
- Một dịch vụ trong `compose.yml` (Redis, PostgreSQL, browser-worker) dừng rồi chạy lại thì job đang dở có mất hoặc chạy hai lần không?
- Ổ đĩa đầy, sao lưu hằng đêm thất bại thì có cảnh báo không?

### Ví dụ
- Đặt hạn mức chi tiêu chỉnh ảnh rất thấp trong Cài đặt → mẫu mới tiếp theo chuyển sang dự phòng tải ảnh lên tay, chủ tiệm được báo.
- Tắt Wi-Fi điện thoại khi bấm "Duyệt" lịch → báo lỗi rõ; bật lại và bấm lại → lịch chỉ duyệt một lần.
- Dừng container browser-worker khi có comment trong hàng đợi, chạy lại → comment được gửi đúng một lần hoặc đánh dấu thất bại kèm lý do.
- Đổi khóa Gemini trong `.env` thành khóa sai rồi khởi động lại → phân loại bài báo lỗi hệ thống, không comment bừa.

## 12. Regression

### Câu hỏi gợi ý
- Case nào là cốt lõi của tính năng và phải gắn cờ regression?
- Tính năng mới đụng tới phần dùng chung nào (tìm khung trống, phanh an toàn, kênh thợ, bộ thông tin tiệm, kho content)? Case regression của các phần đó đã chạy lại chưa?
- Thay đổi schema DB, migration có làm hỏng dữ liệu của tính năng cũ không?
- Đổi prompt AI có làm phân loại, giọng văn, mô tả mẫu xấu đi trên các bài/ảnh đã từng đúng không?
- Đổi style UI hoặc component dùng chung có làm vỡ màn hình nào khác không?
- Lỗi đã sửa (`P<N>-ISS-<nnn>`) có case test lại và case đó đã gắn cờ regression chưa?

### Ví dụ
- Sửa phép tính khung trống cho inbox → chạy lại case regression comment loại 2 và tóm tắt lịch đầu ngày.
- Thêm loại thông báo mới cho chủ tiệm → kiểm tra lại cửa sổ 24 giờ và kênh dự phòng web push, email.
- Đổi prompt phân loại bài → chạy lại bộ bài mẫu đã biết loại (loại 1, 2, 3, không phù hợp) và so kết quả.
- Đổi màu token trạng thái → xem lại Lịch, Trang chính, Khách trên iPhone.

## Lằn ranh đỏ

- Nói sai với khách: sai giá, sai ngày giờ trống, sai địa chỉ, hoặc tự bịa thông tin chưa có (địa chỉ cụ thể, giờ mở cửa, khuyến mãi, số lượng khách, chính sách cọc…) → giữ bởi khía cạnh 3, 10
- Nhận trùng lịch: hứa với hai khách cùng một khung giờ → giữ bởi khía cạnh 3, 7, 8
- Comment giống spam: lặp y hệt câu chữ, comment hai lần vào cùng một bài, comment vào bài không liên quan, comment dồn dập → giữ bởi khía cạnh 3, 7, 9
- Làm mất kênh tìm khách: tài khoản Facebook tìm khách hoặc trả lời inbox bị khóa mà không có cảnh báo hay cơ chế dừng; tệ hơn là mất quyền quản lý Page → giữ bởi khía cạnh 6, 9, 11
- Ảnh chỉnh sai mẫu: ảnh AI chỉnh khác mẫu móng thật (sai màu, sai form, thừa ngón), hoặc ghi "ảnh thật tại tiệm" cho ảnh đã chỉnh → giữ bởi khía cạnh 1, 3
- Vi phạm nguyên tắc minh bạch: viết review giả, dùng từ tuyệt đối ("tốt nhất", "rẻ nhất", "đẹp nhất"), ghi "trọn bộ như hình" khi chưa rõ đã gồm nối móng → giữ bởi khía cạnh 1, 3
- Chen ngang: app trả lời khách trong khi thợ hoặc chủ tiệm đang nói chuyện với khách đó → giữ bởi khía cạnh 7, 9

## Lịch sử thay đổi

- 2026-10-29: tạo mới
