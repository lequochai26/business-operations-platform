# Chức năng 05 – Tạo và đăng mẫu mới

## Mục đích
Mỗi khi có một mẫu nail mới, app tự làm hết các việc: chỉnh ảnh, làm poster, viết content, đăng Page và đăng group. Chủ tiệm chỉ **duyệt một lần ở cuối**. Phần việc của chủ tiệm giảm từ khoảng 15 phút xuống khoảng 1–2 phút.

## Liên quan
- Nhận ảnh từ thợ: `02-technician-channel.md`, mục 5
- Lưu kết quả: `06-content-library.md`
- Đăng group bằng trình duyệt tự động, phanh an toàn: `01-group-auto-comment.md`, mục 8
- Gemini, cách render poster: `../04-technical.md`

---

## 1. Luồng

1. **Nhận mẫu mới.** Gồm ảnh gốc (1 hoặc nhiều ảnh), mô tả của thợ (tên mẫu, chi tiết) và giá. Đến từ một trong hai nguồn:
   - Messenger (thợ hoặc chủ tiệm gửi);
   - tải lên trên web app.
2. **Chuẩn bị thông tin mẫu bằng AI:**
   - **tên mẫu ngắn** để làm tiêu đề poster;
   - **mô tả 1 dòng**;
   - **tag**: tông màu, kỹ thuật (thạch, mắt mèo, tráng gương, French, vẽ, đính đá…), form móng, mùa hoặc dịp.

   Mô tả của thợ là nguồn chính. AI chỉ bổ sung những gì nhìn thấy rõ trong ảnh và không được mâu thuẫn với lời thợ.
3. **Chỉnh ảnh bằng AI** (mục 2).
4. **Làm poster** từ mẫu poster có sẵn (mục 3).
5. **Viết gói content** (mục 4).
6. **Đưa vào hàng chờ duyệt** và báo chủ tiệm.
7. **Chủ tiệm duyệt một lần** (mục 5).
8. **Đăng tự động:** đăng Page (mục 6), đăng group (mục 7).
9. **Lưu toàn bộ vào kho content** (chức năng 06), kể cả khi chủ tiệm chỉ duyệt mà chưa đăng.

Các bước 2 đến 5 chạy nền. Lỗi ở bước nào thì bước đó được đánh dấu lỗi, các phần đã làm được vẫn được giữ, và chủ tiệm có thể bấm làm lại riêng phần lỗi.

---

## 2. Chỉnh ảnh

### Nhà cung cấp
- Mặc định: **Google Gemini, model Nano Banana 2.1, ảnh 2K**, gọi qua API trả phí.
- Ước tính khoảng 0,05 USD mỗi ảnh, khoảng 6 USD/tháng nếu chỉnh 4 ảnh/ngày.

### Prompt
- Dùng **bộ prompt chỉnh ảnh của tiệm**. Chủ tiệm đang lưu bộ này ở nơi dùng chung và sẽ nhập vào app.
- Bộ prompt có các style:
  - studio tối giản nền sage;
  - lụa + hoa + ngọc trai;
  - lifestyle ánh nắng + ly latte;
  - macro editorial;
  - tối kiểu quảng cáo nước hoa.
- Mỗi style là một mục trong cài đặt. Chủ tiệm chọn **style mặc định**.
- Mọi prompt luôn được ghép thêm **các ràng buộc bắt buộc**:
  - giữ nguyên mẫu, form và màu móng;
  - giải phẫu bàn tay đúng, không thừa hoặc thiếu ngón;
  - không thêm chữ hay watermark.

### Số bản
- Mặc định tạo **1 bản** mỗi ảnh gốc.
- Ở bước duyệt, chủ tiệm bấm "tạo lại", có thể kèm đổi style, để có thêm bản. Mỗi lần bấm là một lần tính phí.

### Ảnh gốc
- Sửa chiều ảnh theo EXIF trước khi gửi đi chỉnh.
- Lưu ảnh gốc song song với ảnh đã chỉnh.

### Dự phòng
- Khi Gemini lỗi hoặc hết hạn mức:
  - app tạo sẵn prompt;
  - chủ tiệm bấm "sao chép prompt", tự chỉnh ảnh ở công cụ khác (app Gemini, ChatGPT…), rồi **tải ảnh đã chỉnh lên**.
- Chủ tiệm cũng có thể **bỏ qua bước chỉnh** và dùng ảnh gốc.

### Thay nhà cung cấp
- Code phải tách bước chỉnh ảnh thành một khâu thay được nhà cung cấp, để sau này đổi sang API khác hoặc model chạy local mà không sửa luồng.

---

## 3. Làm poster

### Cách làm
- App có **bộ mẫu poster riêng**, viết bằng HTML/CSS và chuyển ra ảnh PNG. Đây không phải ảnh do AI vẽ, nên chữ, giá và nhận diện **luôn đúng tuyệt đối**.
- Các mẫu poster đầu tiên được **chuyển từ các poster hiện có trên canvas Claude Design**. Ưu tiên ba kiểu:
  - poster 1 mẫu tiêu chuẩn (kiểu Poster 6 / 12 / 14);
  - "vé hẹn" có lịch (kiểu Poster 10 / 13);
  - "Bìa tạp chí MIO".

  Chủ tiệm cung cấp các file poster hoặc cho phép đọc từ canvas (xem `06-open-issues-and-assumptions.md`).

### Nhận diện bắt buộc
- Khổ **1080×1350px**.
- Màu: sage `#8FA284`, kem `#FAF7F0`, xanh nhấn `#4E6045`.
- Font: Playfair Display (tiêu đề), Dancing Script (chữ viết tay), Be Vietnam Pro (nội dung).

### Các trường điền vào mẫu
- ảnh chính (ảnh đã chỉnh);
- tên mẫu;
- tag mẫu;
- giá ("99k trọn bộ" chỉ khi đã xác nhận trọn bộ);
- sticker hoặc nhãn (tùy chọn, ví dụ "Tone Thu Đông", "Đỏ – màu mùa lễ");
- bật/tắt SĐT;
- màu nhấn (với mẫu có hỗ trợ).

### Chọn mẫu và sticker
- App tự chọn mẫu poster theo luật đơn giản, ví dụ xoay vòng giữa các mẫu đang bật. Chủ tiệm đổi được ở bước duyệt.
- **Nhãn theo mùa hoặc dịp** do AI đề xuất từ lịch dịp lễ. Nhãn nào gắn với một dịp thì có **hạn dùng**, ví dụ nhãn Halloween hết hạn sau 31/10.

### Kiểm tra bố cục
- Chữ hoặc sticker không được đè lên vùng móng.
- *Gợi ý của người viết:* khung ảnh trong mẫu dùng `object-position` chỉnh được ở bước duyệt, và AI gợi ý điểm lấy nét.

---

## 4. Gói content

Giống gói content tiệm đang làm cho mỗi poster:
- **1 bài đăng Page.**
- **2–3 biến thể bài đăng group:** bản dài, bản ngắn, bản kể chuyện.
- **3–5 comment mẫu**, đưa vào kho để chức năng 01 dùng lại. Ví dụ: có thể gắn vào bộ content loại 1, hoặc dùng khi khách hỏi đúng mẫu này.

### Quy tắc viết
- Giọng tiệm (xem chức năng 04, mục 4).
- CTA đơn giản: "ib mình", "nhắn Page", "inbox để giữ slot".
- Hashtag: `#TiemNhaMio #NailQuan11` và các hashtag chủ tiệm cấu hình.
- **Ngữ cảnh thời sự** (thời tiết, dịp lễ, mùa) chỉ dùng khi phù hợp. Content có nhắc tới dịp thì phải ghi **hạn dùng**.
- **Danh sách từ cấm:** "tốt nhất", "rẻ nhất", "đẹp nhất" và các từ chủ tiệm thêm. Kiểm tra tự động trước khi đưa vào hàng chờ duyệt. Có từ cấm thì tự viết lại.
- Không thêm thông tin chưa có: địa chỉ cụ thể, giờ mở cửa, khuyến mãi, số lượng khách.
- Không ghi "ảnh thật tại tiệm" cho ảnh đã chỉnh bằng AI.
- Dòng đầu comment mẫu luôn bắt đầu bằng "Tiệm Nhà Mio nhận làm…".

---

## 5. Màn hình duyệt (một lần, ở cuối)

- Xem được trên điện thoại. Một trang gồm:
  - ảnh gốc và ảnh đã chỉnh đặt cạnh nhau, để so có sai mẫu không;
  - poster;
  - bài Page;
  - các biến thể bài group;
  - comment mẫu;
  - tên mẫu, giá, tag.
- Với từng phần, chủ tiệm có thể:
  - **sửa trực tiếp** (chữ, giá, tên);
  - **tạo lại** (ảnh, poster với mẫu khác, content);
  - **bỏ** (ví dụ không muốn đăng group lần này).
- **Lựa chọn đăng:**
  - đăng Page ngay hoặc hẹn giờ (gợi ý giờ vàng gần nhất);
  - đăng group: bật/tắt, xem trước danh sách group sẽ đăng.
- **Bấm "Duyệt"** là xong. Bấm "Lưu, chưa đăng" để chỉ đưa vào kho.
- Một mẫu chưa được duyệt sau 24 giờ thì app nhắc chủ tiệm một lần.

---

## 6. Đăng Page

- Đăng qua **kết nối chính thức** (Graph API của Page): poster kèm nội dung bài Page.
- Đăng thành công thì lưu link bài. Đăng lỗi thì báo chủ tiệm và cho bấm đăng lại.

---

## 7. Đăng group

- Dùng **trình duyệt tự động** với tài khoản vận hành, cùng phanh an toàn với chức năng 01 (giờ nghỉ, tự dừng khi bất thường, nút dừng khẩn cấp).
- **Chỉ đăng vào group đã bật "cho phép đăng bài".**
- **Chia đợt:**
  - Mỗi đợt tối đa **3 group** (theo cách tiệm đang làm).
  - Các đợt cách nhau ngẫu nhiên, mặc định 1–3 giờ.
  - Tối đa **N bài/ngày** cho toàn tài khoản, mặc định 6.
- **Xoay biến thể:** các group trong cùng một đợt nhận các biến thể content khác nhau. Một group không nhận lại đúng biến thể nó đã nhận trước đây.
- **Không đăng lại cùng một mẫu vào cùng một group** trong vòng N ngày (mặc định 14).
- Mỗi lần đăng được ghi lại: group, thời điểm, link bài (nếu lấy được), trạng thái.
  - Group có duyệt bài thì trạng thái là "chờ admin duyệt", nếu nhận ra được.

---

## 8. Trường hợp đặc biệt

- **Thợ gửi nhiều ảnh của cùng một mẫu:** chọn ảnh rõ nhất làm ảnh chính, các ảnh còn lại dùng cho dải ảnh phụ (với mẫu poster có dải ảnh). Chủ tiệm đổi được.
- **Thợ gửi ảnh nhiều mẫu khác nhau trong một lần:** app hỏi lại "Đây là 1 mẫu hay nhiều mẫu?".
- **Thiếu giá:** không tạo poster có giá. App hỏi thợ trước (chức năng 02).
- **Ảnh có watermark AI** (ví dụ ảnh chỉnh từ công cụ khác rồi tải lên): AI cảnh báo ở bước duyệt.
