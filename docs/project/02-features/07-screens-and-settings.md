# Chức năng 07 – Màn hình quản lý và cấu hình

## Mục đích
Đây là web app dành cho chủ tiệm và thợ:
- xem tình hình;
- duyệt những gì cần duyệt;
- quản lý lịch, khách và kho;
- cài đặt mọi tham số của app.

Phần lớn thời gian app tự chạy. Màn hình chủ yếu dùng để **duyệt, xử lý ngoại lệ và chỉnh cài đặt**.

## Yêu cầu chung
- **Ưu tiên điện thoại.** Mọi màn hình dùng tốt trên màn hình nhỏ, chạm bằng ngón cái. Máy tính là phụ.
- **Cài được ra màn hình chính** (PWA) và nhận **thông báo đẩy** (web push). Đây là kênh dự phòng khi Messenger không gửi được (chức năng 02, mục 7).
  - **Chủ tiệm dùng iPhone:** web push trên iPhone chỉ chạy khi web app đã được thêm vào màn hình chính (iOS 16.4 trở lên), và kém ổn định hơn Android. App cần có trang hướng dẫn cài đặt cho iPhone.
  - **Thợ dùng Android:** web push hoạt động bình thường trên Chrome.
- **Email cho thông báo khẩn** (quyết định của người viết):
  - Các thông báo khẩn (tài khoản bị dừng, worker inbox dừng, lỗi hệ thống nghiêm trọng) được gửi **thêm qua email** cho chủ tiệm.
  - Email không phụ thuộc vào cửa sổ 24 giờ của Messenger hay độ ổn định của web push trên iPhone.
  - Dùng SMTP miễn phí, ví dụ Gmail với mật khẩu ứng dụng.
- Giao diện tiếng Việt. Dùng tông màu nhận diện của tiệm cho giao diện (quyết định của người viết).
- **Đăng nhập:**
  - Có hai vai trò: **Quản lý** (chủ tiệm) và **Thợ**.
  - Mỗi người một tài khoản, đăng nhập bằng tên đăng nhập và mật khẩu.
  - Giữ đăng nhập lâu dài trên điện thoại.
- Truy cập qua HTTPS. App không công khai, chỉ ai có tài khoản mới vào được.

---

## 1. Danh sách màn hình

### 1.1 Trang chính (Hôm nay)
- **Việc cần làm ngay**, mỗi việc bấm vào là tới nơi xử lý:
  - khách đang chờ người thật;
  - lịch chưa duyệt;
  - mẫu mới chờ duyệt;
  - comment hoặc bài đăng chờ duyệt;
  - yêu cầu báo giá đang chờ thợ.
- **Trạng thái tự động hóa:**
  - tài khoản vận hành đang chạy, tạm dừng hay bị dừng vì bất thường (kèm lý do);
  - lượt quét gần nhất;
  - số comment hôm nay so với giới hạn.
- **Nút dừng khẩn cấp** và nút **chạy lại**.
- **Lịch hôm nay** dạng rút gọn.
- **Số liệu nhanh:** hôm nay và 7 ngày qua, gồm số bài phù hợp, số comment, số tin nhắn mới, số lịch đặt, số khách đã xong.

### 1.2 Bài trong group
- Danh sách bài app đã xét, lọc theo trạng thái, loại bài, group, ngày.
- Mỗi bài hiện:
  - nội dung rút gọn, link;
  - kết quả phân loại và lý do;
  - comment đã gửi hoặc đề xuất;
  - thời gian từ lúc bài được đăng đến lúc comment.
- Hành động: duyệt / sửa / bỏ (khi đang chờ duyệt), đánh dấu **"phân loại sai"**, comment lại (khi thất bại).

### 1.3 Báo giá
- Các yêu cầu báo giá: đang chờ thợ, đã có giá, đã bỏ, hết hạn.
- Chủ tiệm hoặc thợ có thể nhập giá trực tiếp ở đây, thay vì qua Messenger.

### 1.4 Lịch
- Xem theo ngày và theo tuần.
- Tạo, sửa, duyệt, dời, hủy lịch hẹn. Đánh dấu đã làm xong hoặc khách không đến.
- Tạo khung bận. Sửa giờ làm việc theo tuần và ngày đặc biệt.

### 1.5 Khách (inbox)
- Danh sách khách theo trạng thái (chức năng 04, mục 6).
- Xem cuộc trò chuyện. Bật/tắt tự trả lời cho từng cuộc.
- **Gợi ý trả lời**, rồi gửi tin trực tiếp từ web app (gửi qua Page).
- Ghi chú về khách, liên kết với lịch hẹn.

### 1.6 Mẫu mới
- Hàng chờ các mẫu đang xử lý hoặc chờ duyệt.
- Màn hình duyệt (chức năng 05, mục 5).
- Nút tải lên một mẫu mới.

### 1.7 Kho content
- Như chức năng 06, mục 3.

### 1.8 Nhật ký đăng bài
- Các lần đăng Page và đăng group, kèm trạng thái và link.

### Quyền của vai trò Thợ (quyết định của người viết)
- **Được:**
  - xem và thao tác trên Trang chính, Lịch, Báo giá, Khách (đọc trò chuyện, gửi tin, ghi chú);
  - tải mẫu mới lên;
  - xem kho content.
- **Không được:**
  - duyệt hoặc sửa comment và bài đăng group;
  - duyệt mẫu mới;
  - nút dừng khẩn cấp và chạy lại;
  - Cài đặt, Nhật ký hệ thống.

### 1.9 Cài đặt (chỉ Quản lý)
Xem mục 2.

### 1.10 Nhật ký hệ thống (chỉ Quản lý)
- Lỗi, các lần tự dừng (có ảnh màn hình), mức dùng Gemini (số lượt, chi phí ước tính trong tháng).

---

## 2. Cài đặt

### Tài khoản vận hành Facebook (cho group)
- Trạng thái phiên đăng nhập.
- Hướng dẫn và nút **đăng nhập lại** (xem cách đăng nhập trên máy chủ ở `../04-technical.md`).

### Group
- Thêm hoặc xóa group (dán link hoặc ID).
- Mỗi group: bật quét, cho phép comment, cho phép đăng bài, giới hạn riêng, ghi chú luật group.

### Quét và comment
- Lịch quét: các khung giờ vàng, chu kỳ trong và ngoài giờ vàng, giờ nghỉ.
- Tuổi tối đa của bài, ngưỡng "bài cũ" (đổi giọng comment).
- Khu vực nhận khách.
- Ngưỡng độ tin cậy khi phân loại.
- Chế độ **tự gửi / duyệt trước**: cho toàn app và cho từng loại bài.
- **Phanh an toàn:**
  - giới hạn comment mỗi ngày và mỗi group;
  - giãn cách giữa các comment;
  - số lần lỗi liên tiếp thì tự dừng.
- Loại 3:
  - thời gian chờ thợ trước khi nhắc, thời gian chờ tối đa;
  - có comment "ib báo giá" khi hết thời gian chờ hay không.

### Đăng group
- Số group mỗi đợt, giãn cách giữa các đợt, số bài tối đa mỗi ngày.
- Số ngày không đăng lại cùng một mẫu vào cùng một group.

### Lịch
- Giờ làm theo tuần.
- Thời lượng mặc định, thời gian đệm, bước làm tròn.
- Khoảng giờ của sáng / chiều / tối.
- Khoảng cách tối thiểu tính từ hiện tại.
- Số ngày tìm khung trống, số khung đề xuất.

### Inbox
- Bật/tắt tự trả lời.
- Bộ thông tin của tiệm, với trạng thái đã xác nhận / chưa xác nhận.
- Các tin nhắn nhờ chờ.
- Ai nhận thông báo khi chuyển cho người thật, thời gian nhắc lại.
- Thời gian tạm dừng khi người thật đã trả lời.
- Có tự nói là trợ lý tự động khi khách hỏi hay không.
- Có dùng lại luồng báo giá cho khách trong inbox hay không.
- Xin feedback sau khi khách xong (bật/tắt).

### Kênh thợ
- Ghép nối Messenger của thợ và của chủ tiệm (mã ghép nối).
- Bật/tắt tóm tắt lịch đầu ngày và giờ gửi.
- Bật/tắt từng loại thông báo.

### Content và nhận diện
- Giọng tiệm (đoạn mô tả ngắn đưa vào mọi prompt viết content).
- Câu mở đầu comment.
- Hashtag.
- Danh sách từ cấm.
- Lịch dịp lễ và mùa.
- Bộ prompt chỉnh ảnh (các style, style mặc định).
- Các mẫu poster đang bật.

### AI
- Model dùng cho phần chữ và cho phần chỉnh ảnh.
- Hạn mức chi tiêu tháng cho phần chỉnh ảnh: **vượt hạn mức thì app tự chuyển sang dự phòng tải ảnh lên tay**.

### Người dùng
- Đổi mật khẩu.
- Quản lý tài khoản thợ.
