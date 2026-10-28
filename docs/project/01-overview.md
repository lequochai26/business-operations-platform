# 01 – Tổng quan

- **Dự án:** Web app nội bộ vận hành marketing cho Tiệm Nhà Mio
- **Ngày viết:** 28/10/2026
- **Nguồn:** `GeneralSpec.xlsx` (danh sách khó khăn), `BusinessContext.md` (bối cảnh tiệm), buổi trao đổi với chủ tiệm ngày 27–28/10/2026
- **Quy ước:** những chỗ ghi "(quyết định của người viết)" là đề xuất của người viết tài liệu, chủ tiệm chưa xác nhận. Danh sách đầy đủ nằm ở `06-open-issues-and-assumptions.md`.

---

## 1. Bối cảnh

### Về tiệm
- Tiệm nail nhỏ ở Quận 11, TP.HCM. Chỉ có **1 thợ**. Giai đoạn này chủ yếu **nhận khách mẫu** với giá 89k–150k.
- Một số mẫu mất 2,5–3 tiếng mỗi khách, nên lịch rất dễ bị dồn.
- Khách liên hệ qua **inbox Facebook Page** và SĐT 0911 897 965.
- **Kênh tìm khách chính:** comment vào các bài "tìm mẫu nail / tuyển mẫu nail" trong các group Facebook về nail, kèm poster, để kéo khách về inbox Page. Page có nhiệm vụ tạo niềm tin khi khách bấm vào xem.
- Hiện có hai người vận hành:
  - **Chủ tiệm (người chạy ad):** tìm khách, làm poster và content, đăng bài, trả lời khách khi thợ bận. Đây là người dùng chính của app.
  - **Thợ:** làm móng và chốt lịch với khách. Thợ luôn bận tay nên chỉ trả lời tin nhắn được trong những lúc ngắn giữa hai lượt khách.

### Các khó khăn hiện tại (từ GeneralSpec)
- Không có thời gian đăng bài và đi comment.
- Mỗi mẫu nail mới mất khoảng **15 phút**: tải ảnh thợ gửi, nhờ ChatGPT chỉnh ảnh theo prompt có sẵn, kiểm tra ảnh, nhờ Claude làm poster và content, lưu lại, đăng Page, đăng group. Mỗi lần đăng tối đa 3 group, nên phải đăng ít nhất 3 lần.
- Không có thời gian chạy đều đặn luồng đi comment:
  - lướt từng group để tìm bài (bước **tốn thời gian nhất**);
  - chọn content và poster phù hợp, phải mò lại file Excel lịch sử content;
  - viết comment.
- Gặp bài cần báo giá thì chủ tiệm không đủ chuyên môn để ước giá. Phải nhắn thợ, thợ bận nên trả lời rất chậm, và trong lúc chờ thì bài đã trôi mất. Comment trong 30 phút đầu sau khi bài được đăng là quan trọng nhất.
- Mất thời gian nghĩ câu trả lời cho khách. Khó theo dõi khách nào đã xử lý xong, khách nào chưa.
- Lịch giữa chủ tiệm và thợ không thống nhất.
- Content cũ dùng lại được, nhưng mỗi lần cần lại phải mò file để tìm.

---

## 2. Mục đích của app

App gánh phần lớn công việc marketing lặp đi lặp lại, để chủ tiệm chỉ còn **duyệt và quyết định**, và thợ chỉ cần **trả lời ngắn qua Messenger**.

Cụ thể, app sẽ:
- Tự lướt các group nail, nhận ra bài đang tìm thợ hoặc tìm mẫu, và tự comment đúng nội dung, đúng ngày giờ, đúng giá.
- Hỏi giá thợ thay chủ tiệm. Thợ chỉ cần trả lời một con số.
- Giữ **một lịch làm duy nhất** của thợ, dùng chung cho việc comment, trả lời khách và đặt lịch.
- Tự trả lời các câu hỏi thông tin cố định trong inbox Page. Câu nào không trả lời được thì nhờ khách chờ và gọi người thật.
- Rút luồng làm mẫu mới từ 15 phút xuống còn **một lần duyệt**.
- Lưu mọi poster và content vào một kho dễ tìm.

---

## 3. Mục tiêu

- **Đi comment hoàn toàn tự động.** Chủ tiệm chọn một trong hai chế độ: app tự gửi, hoặc app chuẩn bị sẵn để chủ tiệm duyệt.
- **Comment nhanh:** bài phù hợp được comment trong vòng 30 phút kể từ lúc bài được đăng, nếu app quét kịp và không bị chờ báo giá.
- **Báo giá nhanh:** thợ có thể báo giá bằng một tin nhắn ngắn, không phải mở app.
- **Không trùng lịch:**
  - App **không bao giờ tự tạo** hai lịch hẹn chồng nhau, và không bao giờ mời khách vào khung đã kín.
  - Lịch chồng nhau chỉ có thể xuất hiện khi thợ **cố ý ép chọn** sau khi đã được cảnh báo. Lịch đó được đánh dấu rõ (xem `02-features/03-schedule.md`, mục 4).
- **Inbox:** câu hỏi thông tin cố định được trả lời gần như ngay lập tức. Mọi khách đều có trạng thái rõ ràng.
- **Mẫu mới:** phần việc của chủ tiệm giảm từ khoảng 15 phút xuống khoảng 1–2 phút duyệt.
- **Content tìm lại được** trong vài giây, theo tên mẫu, tông màu, kiểu, giá hoặc mùa.

---

## 4. Những gì không làm (ở phiên bản này)

- **Không tự ước tính giá.** Giá luôn do thợ báo. Khi chủ tiệm chốt bảng giá thì sẽ bổ sung phần gợi ý giá ở một bản sau.
- Không quản lý tiền: không thu cọc, không thanh toán, không làm sổ sách.
- Không chạy quảng cáo trả phí (Facebook Ads).
- Không làm cho kênh khác: TikTok, Instagram, Zalo.
- Không quản lý nhiều tiệm hay nhiều thợ. App làm cho đúng 1 tiệm và 1 thợ (quyết định của người viết: nên đặt dữ liệu lịch theo "thợ" để sau này mở rộng được, nhưng không làm giao diện nhiều thợ).
- Không thay thế canvas Claude Design hiện có. App có bộ mẫu poster riêng. Canvas vẫn dùng như cũ khi chủ tiệm muốn làm poster đặc biệt.
- Không tự ước giá cho bài loại 3 khi thợ không trả lời.

---

## 5. Những điều tuyệt đối không được xảy ra

Nếu xảy ra một trong các điều sau, app coi như thất bại, dù về kỹ thuật vẫn chạy:

- **Nói sai với khách:** sai giá, sai ngày giờ trống, sai địa chỉ, hoặc tự bịa ra thông tin chưa có (địa chỉ cụ thể, giờ mở cửa, khuyến mãi, số lượng khách, chính sách cọc…).
- **Nhận trùng lịch:** hứa với hai khách cùng một khung giờ.
- **Comment giống spam:** lặp y hệt câu chữ, comment hai lần vào cùng một bài, comment vào bài không liên quan, comment dồn dập.
- **Làm mất kênh tìm khách:** tài khoản Facebook dùng để tìm khách hoặc trả lời inbox bị khóa mà không có cảnh báo hay cơ chế dừng. Tệ hơn nữa là làm mất quyền quản lý Page.
- **Ảnh chỉnh sai mẫu:** ảnh sau khi AI chỉnh khác mẫu móng thật (sai màu, sai form, thừa ngón), hoặc ghi "ảnh thật tại tiệm" cho ảnh đã chỉnh.
- **Vi phạm nguyên tắc minh bạch của tiệm:** viết review giả, dùng các từ tuyệt đối như "tốt nhất", "rẻ nhất", "đẹp nhất", hoặc ghi "trọn bộ như hình" khi chưa rõ đã gồm nối móng hay chưa.
- **Chen ngang:** app trả lời khách trong khi thợ hoặc chủ tiệm đang nói chuyện với khách đó.

---

## 6. Người dùng

### Chủ tiệm (vai trò "Quản lý")
- Dùng app trên điện thoại và máy tính, phần lớn là điện thoại.
- Cài đặt app: danh sách group, các bộ content, bộ thông tin của tiệm, giới hạn an toàn, chế độ tự gửi hay duyệt trước.
- Duyệt mẫu mới, theo dõi kết quả, xử lý khi app báo cần người.
- Được làm mọi thứ thợ làm được.

### Thợ (vai trò "Thợ")
- Chủ yếu làm việc qua **Messenger** với Page: báo giá, duyệt/hủy/dời lịch, gửi ảnh mẫu mới, báo khách đã làm xong.
- Khi cần thì mở web app để xem và sửa lịch, khóa những khung mình bận.
- Không cần học thêm công cụ nào khác ngoài Messenger.

### Khách
- Không dùng app. Khách chỉ thấy comment trong group và tin nhắn từ Page.
- Với khách, mọi tin nhắn đều phải giống người của tiệm đang nhắn: giọng thân thiện, xưng "mình", gọi "bạn/nàng", có emoji.

---

## 7. Thế nào là thành công

(Các con số là đề xuất của người viết, chủ tiệm có thể chỉnh.)

- Sau 2 tuần chạy thật:
  - Chủ tiệm không còn phải tự lướt group.
  - Mỗi ngày app comment được khoảng 10–15 bài phù hợp (theo kinh nghiệm của tiệm) mà tài khoản không bị khóa.
- Mọi comment loại 2 đều khớp với lịch thật của thợ. Không có ca trùng lịch nào.
- Thời gian từ lúc phát hiện bài loại 3 đến lúc comment chỉ còn phụ thuộc vào tốc độ trả lời của thợ, không phụ thuộc chủ tiệm.
- Một mẫu mới đi từ lúc thợ gửi ảnh đến lúc đăng lên Page mà chủ tiệm chỉ phải bấm duyệt.
- Có số liệu theo ngày (số comment, số tin nhắn mới, số lịch đặt) để áp dụng bài học "theo dõi ít nhất 1 tuần trước khi kết luận content không hiệu quả".

---

## 8. Các từ dùng trong tài liệu

- **Page:** Facebook Page "Tiệm Nhà Mio".
- **Tài khoản vận hành:** tài khoản Facebook cá nhân mà app dùng (qua trình duyệt tự động) để lướt group, comment và đăng bài group. Chủ tiệm sẽ thử bằng tài khoản phụ (clone) trước.
- **Tài khoản inbox:** tài khoản Facebook có quyền nhắn tin trên Page, mà app dùng (qua trình duyệt tự động trên Meta Business Suite) để đọc và trả lời khách. Có thể dùng chung với tài khoản vận hành.
- **Group:** group Facebook về nail mà tài khoản vận hành đã tham gia và chủ tiệm đã khai báo trong app.
- **Bài loại 1 / 2 / 3:** ba loại bài tìm mẫu được mô tả trong `02-features/01-group-auto-comment.md`.
- **Bộ content:** một nội dung chữ kèm một ảnh poster, dùng để comment hoặc đăng bài.
- **Kho content:** nơi lưu mọi poster, bộ content, comment mẫu và bài đăng.
- **Mẫu nail:** một mẫu móng thợ đã làm, có ảnh gốc, ảnh đã chỉnh, mô tả, giá và các poster/content đi kèm.
- **Lịch hẹn:** một khoảng thời gian thợ làm cho một khách, có trạng thái (xem `03-schedule.md`).
- **Khung bận:** khoảng thời gian thợ tự khóa vì việc riêng.
- **Kênh thợ:** cuộc trò chuyện Messenger giữa Page và thợ, nơi app hỏi và thợ trả lời.
- **Phanh an toàn:** các giới hạn giúp tài khoản vận hành ít bị Facebook phát hiện là bot (giới hạn số lượng, giãn cách, giờ nghỉ, tự dừng).
- **Chế độ tự gửi / duyệt trước:** công tắc quyết định app tự comment/đăng, hay chờ chủ tiệm bấm duyệt.
- **Chuyển cho người thật:** khi app không trả lời được khách, app nhắn khách chờ và báo cho thợ cùng chủ tiệm vào trả lời.
