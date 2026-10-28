# Chức năng 04 – Inbox Page: tự trả lời khách và theo dõi khách

## Mục đích
- Trả lời ngay các câu hỏi có thông tin cố định, thay cho thợ và chủ tiệm.
- Ghi nhận yêu cầu đặt lịch thành lịch "chưa duyệt" để thợ chốt.
- Khi không trả lời được thì nhờ khách chờ một cách thân thiện và gọi người thật vào.
- Cho chủ tiệm thấy rõ khách nào đang ở bước nào và khách nào đã xong.

**Cách kết nối (đã chốt với chủ tiệm):** tiệm chưa có giấy phép kinh doanh, nên không qua được bước xác minh doanh nghiệp mà Meta yêu cầu để app nhắn tin với khách thật qua đường chính thức. Vì vậy, inbox khách được đọc và trả lời bằng **trình duyệt tự động** (Playwright mở inbox Page trên Meta Business Suite), giống cách làm với group. Rủi ro và cách giảm rủi ro xem `../04-technical.md`, mục 4.3.

Kênh thợ (chức năng 02) vẫn dùng đường chính thức, vì thợ và chủ tiệm được thêm làm tester của Meta app.

## Liên quan
- Lịch: `03-schedule.md`
- Hỏi thợ: `02-technician-channel.md`
- Cách kết nối inbox bằng trình duyệt và rủi ro: `../04-technical.md`, mục 4.3

---

## 1. Bộ thông tin của tiệm

Đây là nguồn kiến thức **duy nhất** app được dùng để trả lời khách.

- Chủ tiệm nhập trên web app, dưới dạng danh sách các mục thông tin. Ví dụ:
  - địa chỉ đầy đủ;
  - mô tả đường đi ("Quận 11 mà khúc nào");
  - giờ nhận khách (lấy từ lịch, xem chức năng 03);
  - SĐT và có dùng Zalo không;
  - khoảng giá mẫu hiện tại;
  - phí phá gel, tháo móng cũ;
  - giá đã gồm nối móng chưa;
  - chất liệu;
  - chỗ gửi xe;
  - chính sách cọc, hủy, bảo hành;
  - …
- Mỗi mục có trạng thái **đã xác nhận / chưa xác nhận**. App **chỉ dùng mục đã xác nhận**.
- Câu hỏi rơi vào mục chưa có hoặc chưa xác nhận thì app **chuyển cho người thật**, không tự trả lời.
- Hiện nhiều mục vẫn còn trống, ví dụ địa chỉ, giờ, chính sách cọc (xem `06-open-issues-and-assumptions.md`). App vẫn chạy được, chỉ là sẽ chuyển cho người thật nhiều hơn.

---

## 2. Cách app xử lý một tin nhắn của khách

1. **Phát hiện tin nhắn mới.**
   - Worker trình duyệt của inbox kiểm tra inbox Page theo chu kỳ: mặc định mỗi 1 phút trong giờ hoạt động, mỗi 5 phút trong giờ nghỉ (chỉnh được).
   - Mở các cuộc trò chuyện có tin chưa đọc, rồi đọc các tin mới.
   - Mục tiêu: khách nhận được câu trả lời trong khoảng 2–3 phút.
   - **Bỏ qua cuộc trò chuyện của thợ và chủ tiệm.** Hai cuộc này đã được kênh thợ xử lý qua webhook.
   - Gửi tin trả lời cũng bằng trình duyệt, với nhịp gõ giống người.
2. **Kiểm tra có được tự trả lời không.** Không trả lời nếu:
   - cuộc trò chuyện đang ở chế độ **"người thật đang trả lời"** (mục 5);
   - người nhắn là thợ hoặc chủ tiệm (chức năng 02);
   - tự trả lời đang bị tắt.
3. **Hiểu ý khách bằng AI.** AI đọc vài tin gần nhất của cuộc trò chuyện và xếp tin nhắn vào một trong các nhóm:
   - **Hỏi thông tin cố định:** địa chỉ, khúc nào, giờ, giá chung, phí phá gel…
   - **Hỏi lịch hoặc muốn đặt lịch:** "ngày này giờ này em qua được không?"
   - **Hỏi giá một mẫu cụ thể:** thường kèm ảnh.
   - **Chọn mẫu từ poster:** "em muốn làm mẫu mắt mèo nâu".
   - **Chào hỏi hoặc câu xã giao.**
   - **Khác hoặc không chắc:** khiếu nại, hỏi ngoài lề, tin nhắn mơ hồ…
4. **Trả lời theo từng nhóm** (mục 3).
5. **Cập nhật trạng thái khách** (mục 6).

Một tin nhắn có thể chứa nhiều ý, ví dụ vừa hỏi địa chỉ vừa hỏi lịch. App trả lời phần nào trả lời được, phần còn lại chuyển cho người thật.

---

## 3. Trả lời theo từng nhóm

### Hỏi thông tin cố định
- Trả lời từ bộ thông tin của tiệm, đúng giọng tiệm (mục 4).
- Không có thông tin thì chuyển cho người thật.

### Hỏi lịch hoặc muốn đặt lịch
- Trích ra ngày, giờ, mẫu hoặc dịch vụ (nếu có), rồi tra lịch (chức năng 03).
- **Khách hỏi một thời điểm cụ thể và khung đó còn trống:**
  - Trả lời là còn trống.
  - Tạo lịch **"chưa duyệt"** để giữ chỗ.
  - Báo khách: "mình giữ tạm slot cho bạn rồi nè, chút xíu thợ nhắn xác nhận lại với bạn nha 💕".
  - Gửi yêu cầu duyệt cho thợ (chức năng 02, mục 2.2).
- **Khung đó không còn trống:** đề xuất các khung gần nhất còn trống (tối đa 3) và để khách chọn. Khi khách chọn một khung thì làm như trường hợp còn trống.
- **Khách chỉ hỏi chung** ("tuần này còn slot không"): liệt kê vài khung trống, chưa tạo lịch.
- **Thiếu thông tin** (chỉ có ngày mà không có giờ): hỏi lại khách và đưa sẵn lựa chọn sáng / chiều / tối kèm khung trống. Chủ tiệm thích cách này.
- **Mỗi khách chỉ có tối đa 1 lịch "chưa duyệt"** tại một thời điểm. Khách đổi ý thì cập nhật lịch đó, không tạo thêm (quyết định của người viết).
- Khách muốn đi 2 người: chuyển cho người thật, vì cần hẹn lệch giờ theo cách thợ hay xử lý.

### Hỏi giá một mẫu cụ thể
- Gửi cho thợ giống luồng báo giá loại 3: ảnh, mô tả 1 dòng do AI viết, và tên khách thay cho link bài.
- Nhắn khách chờ một chút (mục 4).
- Thợ trả lời giá thì app gửi giá cho khách theo giọng tiệm, kèm các lưu ý minh bạch (nối móng, phá gel).
- Thợ không trả lời trong 30 phút (chỉnh được) thì báo chủ tiệm.

(Quyết định của người viết: dùng lại luồng báo giá. Chủ tiệm có thể tắt để thợ tự nhắn giá cho khách.)

### Chọn mẫu từ poster
- Tra kho content (chức năng 06) theo tên hoặc mô tả để lấy giá đã công bố trên poster, rồi trả lời và gợi ý đặt lịch.
- Không tìm thấy mẫu thì chuyển cho người thật.

### Chào hỏi hoặc câu xã giao
- Chào lại ngắn gọn và hỏi khách cần gì. Có thể gửi kèm poster tổng ("Bìa tạp chí MIO") nếu chủ tiệm bật.

### Khác hoặc không chắc
- Chuyển cho người thật.

---

## 4. Giọng và nguyên tắc khi trả lời

- Tiếng Việt, thân thiện, gần gũi, nữ tính. Xưng "mình", gọi "bạn" hoặc "nàng", có emoji vừa phải. Câu ngắn.
- **Tuyệt đối không bịa:** giá, giờ, địa chỉ, khuyến mãi, chính sách, số khách. Mọi thông tin phải lấy từ bộ thông tin tiệm, lịch, kho content hoặc câu trả lời của thợ.
- Không dùng từ tuyệt đối như "tốt nhất", "rẻ nhất", "đẹp nhất".
- Khi không đáp ứng được, ưu tiên đưa giải pháp khác (mẫu khác, giờ khác) thay vì từ chối thẳng. Đây là thói quen của tiệm.
- **Tin nhắn nhờ chờ khi chuyển cho người thật** phải thật thân thiện, có nhiều biến thể và xoay vòng. Ví dụ:
  - "Dạ câu này để thợ nhà Mio trả lời bạn cho chuẩn nha 💕 bạn đợi mình xíu xiu, thợ đang làm dở bộ móng cho khách, xong là nhắn bạn liền ạ 🥰"
  - "Ui câu này mình cần hỏi lại thợ cho chắc nè, nàng chờ mình vài phút nha, mình không để nàng đợi lâu đâu 💅✨"
  - Chủ tiệm sửa và thêm được các biến thể này trên web app.
- App hiển thị trạng thái "đang soạn tin" trước khi gửi, để cuộc trò chuyện tự nhiên hơn.
- **Có tự nói mình là trợ lý tự động hay không:** mặc định là không tự nói ra, nhưng nếu khách hỏi thì trả lời thật. Đây là cài đặt chủ tiệm chọn (xem `06-open-issues-and-assumptions.md`).

---

## 5. Chuyển cho người thật và không chen ngang

### Khi chuyển cho người thật
- App gửi tin nhờ chờ (mục 4).
- Cuộc trò chuyện chuyển sang trạng thái **"chờ người thật"**.
- App báo cho thợ, và báo cả chủ tiệm (cài đặt được: chỉ thợ, chỉ chủ tiệm, hay cả hai). Thông báo gồm câu hỏi của khách và link mở cuộc trò chuyện.
- Không ai trả lời trong 15 phút (chỉnh được) thì nhắc thêm một lần.

### Không chen ngang
- Khi phát hiện **người thật vừa trả lời** khách từ Page, app **tạm dừng tự trả lời** trong cuộc đó.
  - Cách nhận ra: tin gửi từ phía Page mà **không khớp** với tin nào trong nhật ký tin app đã gửi (so nội dung và thời điểm). Mặc định dừng 12 giờ kể từ tin nhắn gần nhất của người thật (quyết định của người viết).
- Trên web app có công tắc bật/tắt tự trả lời cho từng cuộc trò chuyện.
- Trong thời gian tạm dừng, app vẫn đọc tin để cập nhật trạng thái khách và gợi ý câu trả lời trên web, nhưng không tự gửi.

### Gợi ý câu trả lời cho người thật
- Trên web app, ở mỗi cuộc trò chuyện, có nút **"gợi ý trả lời"**. App soạn 2–3 phương án (bản ngắn, bản chi tiết…) dựa trên bộ thông tin tiệm và lịch. Người thật chọn, sửa, rồi gửi.
- Đây là phần giải quyết khó khăn "mất thời gian nghĩ tin nhắn phản hồi khách". Gợi ý cũng gồm các mẫu tin chủ tiệm hay dùng:
  - hẹn lại sang hôm sau, có quà nhỏ;
  - giải thích thời gian chờ vì chỉ có 1 thợ;
  - khách gửi mẫu quá phức tạp hoặc quá giá thì gợi ý mẫu đơn giản hơn.

---

## 6. Theo dõi khách

### Trạng thái của khách
- **Mới:** vừa nhắn lần đầu.
- **Đang trao đổi:** app hoặc người thật đang trả lời, chưa có lịch.
- **Chờ người thật:** đã chuyển, đang chờ thợ hoặc chủ tiệm.
- **Đã giữ chỗ:** có lịch chưa duyệt.
- **Đã chốt lịch:** có lịch đã chốt.
- **Đã xong:** lịch đã chốt **và** thợ đã báo làm xong. Đây là định nghĩa "xong" của chủ tiệm.
- **Không đến / Đã hủy.**
- **Ngừng trao đổi:** không có tin mới trong 3 ngày (chỉnh được) mà chưa có lịch.

Trạng thái được tính tự động từ cuộc trò chuyện và lịch hẹn. Chủ tiệm có thể sửa tay.

### Danh sách khách trên web app
- Lọc theo trạng thái. **Mặc định hiện những khách "cần làm gì đó"**: chờ người thật, đã giữ chỗ, đang trao đổi.
- Mỗi khách có:
  - tên Facebook;
  - tin nhắn gần nhất;
  - trạng thái;
  - lịch hẹn liên quan;
  - số lần đã đến làm;
  - ghi chú (ví dụ "thích tông nude", "hay đi cùng bạn").

### Xin feedback (tùy chọn, mặc định tắt)
- Sau khi khách "đã xong", app có thể gửi tin mẫu xin feedback hoặc ảnh, đúng nguyên tắc "nhắn khách thật xin review". Chỉ gửi trong vòng 24 giờ sau khi khách làm xong.
- Đây là quyết định của người viết, để chủ tiệm bật khi muốn.

---

## 7. Trường hợp đặc biệt

- **Khách gửi tin thoại hoặc video:** chuyển cho người thật.
- **Khách nhắn ngoài giờ nhận khách:** app vẫn trả lời thông tin và giữ chỗ. Tin nhờ chờ thì nói rõ "sáng mai thợ nhắn bạn liền nha".
- **Khách hủy qua tin nhắn:** app hiểu ý, nhắn xác nhận, và báo thợ. Thợ hủy lịch bằng một nút. App không tự hủy lịch đã chốt (quyết định của người viết).
- **Khách cũ quay lại:** app dùng ghi chú và lịch sử để chào thân hơn, ví dụ "lâu rồi mới gặp nàng".
- **Tin nhắn spam hoặc quảng cáo:** không trả lời, đánh dấu spam.
- **Worker inbox bị dừng** (checkpoint, hết phiên đăng nhập): báo khẩn cho chủ tiệm. Thợ và chủ tiệm tự trả lời khách như trước khi có app, cho tới khi worker chạy lại.
