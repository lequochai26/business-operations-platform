# 06 – Vấn đề mở và giả định

Mục này gồm hai phần:
- **thông tin còn thiếu hoặc chưa chốt**, cần chủ tiệm bổ sung;
- **các quyết định do người viết tự đưa ra**, chủ tiệm cần rà lại.

---

## 1. Thông tin còn thiếu (cần trước khi bật tính năng liên quan)

### Cần cho lịch và comment loại 2 (giai đoạn 2)
- **Giờ nhận khách chính thức** theo từng ngày trong tuần, và ngày nghỉ.
- **Thời lượng mặc định** một lượt làm. Tài liệu tạm dùng 2,5 giờ.

### Cần cho bộ thông tin của tiệm (giai đoạn 3)
- Địa chỉ đầy đủ, mô tả đường đi.
- SĐT 0911 897 965 có dùng Zalo không.
- Phí phá gel / tháo móng cũ. Có báo trước không, và bao nhiêu.
- Giá 99k/110k của các mẫu móng dài đã gồm nối móng chưa.
- Chính sách cọc, hủy, bảo hành.
- Danh sách dịch vụ và chất liệu.
- Chỗ gửi xe, nếu có.

### Cần cho poster (giai đoạn 4)
- Quyền truy cập các file poster `.dc.html` trên canvas Claude Design (artifact `03808feb-165b-432a-a5a2-a5ad1111f8da`), để chuyển thành mẫu poster HTML.
- Bộ prompt chỉnh ảnh hiện đang lưu ở nơi dùng chung.
- Tên hiển thị Page đã chốt chưa. Phương án đang dẫn đầu là "Tiệm Nhà Mio – Nail".

### Cần cho nhập dữ liệu cũ (tùy chọn)
- File Excel lịch sử content.

### Sau này
- **Bảng giá chính thức** (chủ tiệm sẽ bổ sung), để làm phần gợi ý giá tự động.

---

## 2. Câu hỏi chờ chủ tiệm quyết định

- **Tài khoản vận hành dùng thật là tài khoản nào?** Sau khi thử bằng tài khoản phụ: chuyển sang tài khoản Huỳnh Mio, hay tiếp tục dùng tài khoản phụ (đã nuôi, đã tham gia các group)?
- **App có tự nói mình là trợ lý tự động khi khách hỏi không?** Tài liệu tạm đặt: không tự nói ra, nhưng nếu khách hỏi thẳng thì trả lời thật.
- **Có chấp nhận gửi tin nhắn của khách qua gói miễn phí của Gemini không?** Với gói này, Google có thể dùng dữ liệu để cải thiện sản phẩm. Nếu không chấp nhận, phần đọc tin nhắn khách sẽ chuyển sang project trả phí. Chi phí rất nhỏ ở quy mô của tiệm, nhưng không còn miễn phí.
- **Tài khoản nào chạy worker inbox?** Dùng chung tài khoản vận hành của group, hay một tài khoản riêng để tách rủi ro? Tài khoản này cần được thêm vào Page với quyền nhắn tin. Không nên dùng tài khoản đang sở hữu Page (xem `04-technical.md`, mục 4.3).
- **Tên miền:** dùng tên miền phụ miễn phí (DuckDNS), hay mua tên miền riêng?

## 2b. Đã chốt trong vòng hỏi cuối (28/10/2026)
- Tiệm **chưa có giấy phép kinh doanh**. Inbox khách dùng **trình duyệt tự động** trên Meta Business Suite (phương án b). Không xin App Review.
- Hiện theo dõi **6 group** (có thể tăng), khoảng **50–100 bài mới mỗi ngày**.
- Chủ tiệm dùng **iPhone**, thợ dùng **Android**.
- Tên file tài liệu bằng tiếng Anh.

---

## 3. Quyết định do người viết tự đưa ra

Các quyết định dưới đây đều chỉnh được trong cài đặt, trừ khi có ghi khác.

### Comment group (chức năng 01)
- Chu kỳ quét: 10 phút trong giờ vàng, 30 phút ngoài giờ vàng. Giờ nghỉ 23:30–07:00. Xáo thứ tự group mỗi lượt.
- Chỉ xét bài trong vòng 24 giờ. Bài đã quá 3 giờ thì comment bằng giọng hướng tới người lướt xem.
- Bài vừa hỏi thời gian vừa có ảnh xin báo giá được xếp loại 3, và vẫn kiểm tra lịch.
- Bài không nhắc khu vực vẫn comment. Bài chỉ nhắc khu vực ngoài danh sách thì bỏ qua.
- Loại 1: AI viết lại nhẹ mỗi lần gửi để tránh lặp y hệt. Tắt được theo từng bộ content.
- Loại 2: không còn khung trống nào trong 7 ngày thì không comment. Kiểm tra lại lịch ngay trước khi gửi.
- Loại 3:
  - nhắc thợ sau 45 phút, bỏ bài sau 3 giờ;
  - tùy chọn comment "ib báo giá" khi hết thời gian chờ (mặc định tắt);
  - với mẫu móng dài hoặc nhọn mà thợ không nói rõ, ghi "chưa gồm nối móng";
  - bài nhiều mẫu: gửi tối đa 4 ảnh, thợ có thể báo giá theo khoảng.
- **Mặc định khi mới cài: chế độ duyệt trước cho mọi loại bài.**
- Phanh an toàn mặc định:
  - 15 comment/ngày, 3 comment/group/ngày;
  - giãn cách 4–12 phút;
  - tự dừng hoàn toàn khi có dấu hiệu bất thường, chỉ chạy lại khi chủ tiệm bấm.

### Kênh thợ (chức năng 02)
- Ghép nối Messenger bằng mã do app tạo.
- Mỗi yêu cầu có mã ngắn (`#G12`, `#L07`).
- Thứ tự ghép câu trả lời: vuốt trả lời → nút bấm → mã → chỉ còn một yêu cầu đang chờ → hỏi lại.
- App chủ động hỏi "khách đã làm xong chưa" sau giờ kết thúc dự kiến 30 phút.
- Tóm tắt lịch đầu ngày lúc 8:00 (mặc định bật).
- Thợ khóa được giờ bận bằng tin nhắn.
- Cửa sổ 24 giờ: gửi nút "👍 OK" khi cửa sổ còn khoảng 2 giờ. Web push làm dự phòng.
- Chưa xử lý tin nhắn thoại.

### Lịch (chức năng 03)
- Thời gian đệm 15 phút. Làm tròn giờ theo bước 30 phút. Không mời khách vào khung bắt đầu trong vòng 2 giờ tới.
- Buổi sáng 8:00–12:00, chiều 12:00–17:00, tối 17:00–21:30.
- Lịch chưa duyệt giữ chỗ và không tự hủy. Nhắc sau 2 giờ, báo cả hai người khi còn 3 giờ tới giờ hẹn.
- Thợ được ép chọn một khung đang bị chiếm khi dời lịch.
- Dữ liệu lịch gắn với "thợ" để sau này mở rộng được, nhưng giao diện chỉ làm cho 1 thợ.

### Inbox (chức năng 04)
- Mỗi khách có tối đa 1 lịch chưa duyệt.
- Khách muốn đi 2 người thì chuyển cho người thật.
- Dùng lại luồng báo giá của loại 3 cho khách hỏi giá trong inbox. App gửi giá cho khách khi thợ trả lời.
- Người thật trả lời thì app tạm dừng tự trả lời 12 giờ trong cuộc đó.
- Khách không có tin mới 3 ngày mà chưa có lịch thì chuyển sang "ngừng trao đổi".
- Khách hủy qua tin nhắn: app không tự hủy lịch đã chốt, chỉ báo thợ.
- Xin feedback sau khi khách xong: có tính năng, mặc định tắt.

### Mẫu mới (chức năng 05)
- Mỗi ảnh mặc định tạo 1 bản chỉnh. Tạo thêm khi chủ tiệm bấm.
- App có bộ mẫu poster HTML riêng, chuyển từ canvas. Canvas Claude Design vẫn dùng song song khi cần.
- Đăng group: 3 group mỗi đợt, các đợt cách nhau 1–3 giờ, tối đa 6 bài/ngày. Không đăng lại cùng mẫu vào cùng group trong 14 ngày.
- Nhắc duyệt mẫu sau 24 giờ.

### Kho content (chức năng 06)
- Có chức năng nhập dữ liệu cũ một lần (tùy chọn, ở giai đoạn cuối).
- Không xóa cứng mục đã từng được dùng.

### Màn hình (chức năng 07)
- Ưu tiên điện thoại, cài được ra màn hình chính, có web push. Giao diện dùng tông màu của tiệm.

### Kỹ thuật (04)
- Đặt mọi thao tác dùng tài khoản vận hành vào một hàng đợi chạy từng việc một.
- Đăng nhập trên máy chủ bằng Xvfb + noVNC.
- Dùng HTTPS bằng Caddy hoặc Cloudflare Tunnel.
- Hai project Google: một miễn phí, một trả phí.
- Sao lưu hằng đêm lên Oracle Object Storage.
- Giao diện là SPA (ví dụ React + Vite). Người code được chọn framework.
- Mục tiêu độ chính xác phân loại: comment nhầm dưới 2%.
- Worker trình duyệt tách được khỏi máy chủ chính, để có thể chạy ở máy nhà nếu IP Oracle bị chặn.
- Dùng tên miền phụ miễn phí (DuckDNS) + Caddy cho HTTPS, nếu chủ tiệm không mua tên miền riêng.
- Lọc bài bằng từ khóa trước khi gửi cho AI. Có giới hạn số lượt mở group mỗi ngày. Comment được ưu tiên hơn quét.
- Chỉ bật 1 bộ content loại 1 thì vẫn dùng lặp lại, dựa vào bước viết lại nhẹ.
- Lịch ép chọn được phép trùng, nhưng mang cờ và cảnh báo. Mọi luồng tự động bị chặn cứng khi trùng.
- Vai trò Thợ không duyệt comment, bài đăng hay mẫu mới, và không vào được Cài đặt.
- Giai đoạn 2 chỉ lưu ảnh mẫu mới thợ gửi. Xử lý đầy đủ ở giai đoạn 4.
- Worker inbox kiểm tra tin mới mỗi 1 phút trong giờ hoạt động, mỗi 5 phút trong giờ nghỉ. Nếu dùng chung tài khoản với group thì inbox được ưu tiên cao nhất.
- Inbox bắt đầu bằng chế độ "chỉ gợi ý" vài ngày rồi mới bật tự gửi.
- Thông báo khẩn gửi thêm qua email, vì web push trên iPhone kém ổn định.
