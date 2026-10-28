# Chức năng 02 – Kênh làm việc với thợ (Messenger)

## Mục đích
Thợ chỉ cần biết **một kênh duy nhất là Messenger**. Mọi việc app cần thợ làm (báo giá, chốt lịch, gửi mẫu mới, báo khách đã xong) đều đi qua cuộc trò chuyện giữa **Page** và **tài khoản Facebook cá nhân của thợ**. Thợ trả lời bằng câu ngắn hoặc bấm nút, không phải mở app.

Trong phần này, chủ tiệm cũng nhận thông báo qua Messenger theo cùng cách (mục 6).

## Liên quan
- Báo giá cho bài loại 3: `01-group-auto-comment.md`
- Lịch hẹn và các trạng thái: `03-schedule.md`
- Lịch hẹn sinh ra từ inbox: `04-page-inbox.md`
- Mẫu mới: `05-new-design-publishing.md`
- Giới hạn của Messenger Platform: `../04-technical.md`

---

## 1. Nhận diện thợ và chủ tiệm

- Trong cài đặt, chủ tiệm gán **cuộc trò chuyện nào trên Page là của thợ** và **cuộc nào là của mình**.
  - *Gợi ý cách làm:* thợ nhắn một mã ghép nối do app tạo, ví dụ "MIO-THO-4821", vào Page. App nhận mã và ghi nhớ người đó là thợ.
- Tin nhắn từ thợ hoặc chủ tiệm **không bao giờ** được xử lý như tin của khách. App không tự trả lời họ kiểu chăm sóc khách hàng.

---

## 2. App gửi gì cho thợ

Mọi tin nhắn gửi thợ đều ngắn, đọc lướt được trong vài giây, và có **nút bấm nhanh** (quick reply) khi phù hợp.
Mỗi yêu cầu có một **mã ngắn** để ghép với câu trả lời, ví dụ `#G12` cho báo giá hoặc `#L07` cho lịch hẹn.

### 2.1 Hỏi giá (bài loại 3)
- Gồm:
  - ảnh mẫu (tối đa 4 ảnh);
  - mô tả 1 dòng do AI viết;
  - thời gian khách hỏi, nếu có, kèm tình trạng lịch ngày đó;
  - link bài;
  - mã yêu cầu.
- Ví dụ:
  > 💅 #G12 Khách hỏi giá mẫu này
  > Mô tả: Thạch hồng, French tráng gương, đính bi bạc, form bầu
  > Khách hỏi: mai (T4) – mình còn trống 9h, 14h
  > Trả lời giá (vd "99k"), hoặc "mô tả mới + giá", hoặc "bỏ".
- Nút nhanh, *gợi ý của người viết*: "Bỏ".

### 2.2 Lịch hẹn mới chờ duyệt (từ inbox Page)
- Gồm:
  - tên khách;
  - ngày giờ khách muốn;
  - mẫu hoặc dịch vụ, nếu biết;
  - link cuộc trò chuyện;
  - mã lịch.
- Nút nhanh: **Duyệt**, **Hủy**, **Dời**.
- Bấm **Dời** thì app hỏi "Dời sang lúc nào?" và thợ trả lời bằng chữ.

### 2.3 Hỏi khách đã làm xong chưa
- Sau giờ kết thúc dự kiến của một lịch đã chốt (mặc định 30 phút sau), app hỏi:
  > Khách [tên] lịch 14h đã làm xong chưa?
- Nút nhanh: **Xong**, **Khách không đến**, **Chưa**. Bấm "Chưa" thì app hỏi lại sau 1 giờ.

(Quyết định của người viết: app chủ động hỏi để thợ không phải nhớ báo.)

### 2.4 Nhắc chờ
- Yêu cầu báo giá hoặc lịch chờ duyệt quá lâu thì app nhắc một lần. Thời gian chờ chỉnh được, xem chức năng 01 và 04.

### 2.5 Xác nhận lại mọi thay đổi
- Mỗi lần app hiểu và thực hiện xong một câu trả lời của thợ, app nhắn lại một dòng xác nhận. Ví dụ: "✅ Đã duyệt lịch chị Lan 14h T3", "✅ #G12 giá 99k, đã comment".
- Nhờ vậy, nếu app hiểu sai thì thợ thấy ngay để sửa.

### 2.6 Tóm tắt lịch đầu ngày (tùy chọn, mặc định bật)
- Mỗi sáng, ví dụ lúc 8:00, app gửi danh sách lịch hẹn trong ngày và các yêu cầu còn chờ thợ.

---

## 3. Thợ có thể nhắn gì cho app

App dùng AI để đọc câu trả lời tự do của thợ. AI đổi câu đó thành một **ý định** có cấu trúc. Nếu không hiểu chắc chắn, app **hỏi lại**, không đoán.

- **Báo giá:** "99k", "120k nha", "110-130k tùy form".
  - Một khoảng giá được giữ nguyên là khoảng giá trong comment.
- **Mô tả mới + giá:** "thạch hồng mắt mèo không đính đá 99k".
- **Từ chối báo giá:** "bỏ", "không làm được mẫu này".
- **Duyệt / hủy / dời lịch:** bấm nút, hoặc nhắn "duyệt", "hủy lịch chị Lan", "dời sang 15h thứ 7".
- **Báo khách đã xong:** bấm nút, hoặc "khách 14h xong rồi".
- **Khóa giờ bận:** "chiều mai mình bận", "T7 nghỉ".
  - App tạo khung bận tương ứng và xác nhận lại. Nếu khung đó đang có lịch hẹn thì app báo cho thợ chứ không tự hủy lịch.
- **Gửi mẫu mới:** ảnh móng kèm mô tả, xem mục 5.
- **Hỏi lịch:** "mai còn trống không", "lịch hôm nay". App trả lời từ lịch.
- **Không thuộc các loại trên:** app trả lời "Mình chưa hiểu ý bạn 🥺" kèm danh sách nút gợi ý, và lưu tin nhắn để chủ tiệm xem.

---

## 4. Ghép câu trả lời với đúng yêu cầu

Thứ tự ưu tiên:
1. Thợ **trả lời trực tiếp vào tin nhắn** của app (vuốt để trả lời): dùng tin nhắn được trả lời để xác định yêu cầu.
2. Thợ **bấm nút nhanh**: nút đã mang sẵn mã yêu cầu.
3. Câu trả lời **có chứa mã**, ví dụ "#G12 99k".
4. **Chỉ có một yêu cầu cùng loại đang chờ:** gán cho yêu cầu đó.
5. **Có nhiều yêu cầu cùng loại đang chờ:** app hỏi lại "Giá 99k này cho mẫu nào?" kèm nút cho từng yêu cầu, nút hiện mô tả ngắn.

Câu trả lời cho một yêu cầu đã đóng (đã hết hạn, đã bị bỏ) không được áp dụng. App báo lại cho thợ biết.

---

## 5. Thợ gửi ảnh mẫu mới

- Ảnh thợ gửi mà **không phải để trả lời một yêu cầu báo giá** được hiểu là có thể là mẫu mới. App hỏi:
  > Đây là mẫu mới để đăng bài phải không?
  > [Mẫu mới] [Không]
- Messenger gửi ảnh và chữ thành nhiều tin riêng. App gom các ảnh và chữ thợ gửi trong vòng **2 phút** thành một gói "mẫu mới".
  - Chữ đi kèm được coi là **mô tả của thợ**, có thể có tên mẫu và giá.
- Thiếu giá thì app hỏi "Mẫu này giá bao nhiêu?". Thiếu mô tả thì AI tự viết mô tả từ ảnh (mô tả 1 dòng như loại 3), rồi chủ tiệm duyệt ở bước cuối.
- Sau khi nhận đủ, app xác nhận "✅ Đã nhận mẫu mới, đang làm poster" và chuyển sang chức năng 05.
- Chủ tiệm cũng có thể gửi mẫu mới theo cách này, hoặc tải ảnh lên trực tiếp trên web app.

---

## 6. Thông báo cho chủ tiệm

Chủ tiệm nhận qua Messenger (cùng cơ chế trên) những thông báo sau:
- App đã tự dừng vì tài khoản vận hành có dấu hiệu bất thường (**khẩn**).
- Có khách cần người thật trả lời, xem chức năng 04.
- Thợ chậm trả lời yêu cầu báo giá hoặc duyệt lịch.
- Mẫu mới đã sẵn sàng để duyệt.
- Có comment hoặc bài đăng đang chờ duyệt, nếu đang ở chế độ duyệt trước. Gửi gộp, tối đa mỗi 30 phút một lần (quyết định của người viết).
- Lỗi hệ thống: Gemini lỗi, hết hạn mức, ổ đĩa đầy…

Mỗi loại thông báo bật/tắt được.

---

## 7. Giới hạn "cửa sổ 24 giờ" của Messenger và cách xử lý

- Theo quy định của Messenger Platform, Page chỉ được chủ động nhắn cho một người **trong vòng 24 giờ kể từ tin nhắn gần nhất người đó gửi cho Page**. Quá 24 giờ thì Page không gửi tin tự động thường được nữa.
- Cách xử lý:
  - **Giữ cửa sổ luôn mở:** khi còn khoảng 2 giờ là hết 24 giờ, app gửi cho thợ (hoặc chủ tiệm) một tin kèm nút "👍 OK". Thợ bấm là cửa sổ mở thêm 24 giờ. Tóm tắt lịch đầu ngày (2.6) cũng có nút để thợ bấm.
  - **Kênh dự phòng:** web app có **thông báo đẩy** trên điện thoại (web push, cài web app ra màn hình chính). Khi cửa sổ Messenger đã đóng, thông báo đi qua kênh này. Thợ mở app để xử lý.
  - **Ghi nhận trạng thái cửa sổ:** app hiển thị cửa sổ Messenger của thợ và chủ tiệm còn mở hay đã đóng.
- Đây là quyết định của người viết. Người code cần kiểm tra lại quy định hiện hành của Meta, xem `04-technical.md`.

---

## 8. Trường hợp đặc biệt

- **Thợ trả lời bằng tin nhắn thoại:** app báo "Mình chưa nghe được tin thoại, bạn nhắn chữ giúp mình nha" (quyết định của người viết: phiên bản này không xử lý giọng nói).
- **Thợ trả lời một yêu cầu đã có người xử lý trên web:** báo lại là đã xử lý rồi, kèm kết quả.
- **Hai người cùng thao tác một lịch** (thợ nhắn Messenger, chủ tiệm bấm trên web): thao tác đến trước được áp dụng. Thao tác sau nhận thông báo "lịch đã thay đổi".
