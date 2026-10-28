# Chức năng 06 – Kho content

## Mục đích
Gom tất cả poster, ảnh, bài đăng và comment mẫu về một chỗ. Chủ tiệm tìm lại được trong vài giây, thay vì mò file Excel lịch sử content. Kho cũng là nguồn nội dung cho các chức năng khác: comment loại 1 và 3, trả lời khách khi khách chọn mẫu, đăng lại.

## Liên quan
- Dùng content để comment: `01-group-auto-comment.md`
- Tạo content mới: `05-new-design-publishing.md`
- Tra mẫu khi khách hỏi: `04-page-inbox.md`

---

## 1. Kho chứa gì

### Mẫu nail
- ảnh gốc, ảnh đã chỉnh;
- tên mẫu, mô tả 1 dòng, giá (và giá có gồm nối móng không), tag;
- ngày tạo;
- trạng thái: **đang nhận làm** hoặc **ngừng**. Mẫu ngừng thì không còn dùng để comment hay trả lời khách.

### Poster
- file ảnh PNG;
- mẫu poster đã dùng;
- mẫu nail liên quan (nếu có);
- nhãn hoặc sticker, **hạn dùng** (nếu có).
- Poster chung không gắn với mẫu nào, ví dụ lưới portfolio, "Bìa tạp chí MIO", poster lịch slot.

### Nội dung chữ
- Mỗi nội dung có một **loại**: bài Page, bài group (dài / ngắn / kể chuyện), comment mẫu, tin nhắn mẫu cho khách.
- Mỗi nội dung có thể có **hạn dùng**, ví dụ content Halloween chỉ dùng tới 31/10.

### Bộ content
- Một cặp **nội dung chữ + poster** dùng làm đơn vị để comment hoặc đăng.

### Lịch sử sử dụng
- Mỗi lần một nội dung, poster hay bộ content được dùng (comment, đăng Page, đăng group), app ghi lại: ở đâu, lúc nào, link.

---

## 2. Cấu hình bộ content cho comment

Phần này là các thiết lập chủ tiệm làm trên web app:

- **Bộ content cho bài loại 1:**
  - Chọn **1 đến 3 bộ** đang bật.
  - Với mỗi bộ, bật/tắt việc "AI viết lại nhẹ trước khi gửi".
- **Bộ content cho bài loại 2:**
  - Tùy chọn. Nếu không chọn thì dùng bộ loại 1 và thay câu về lịch.
- **Poster dùng khi báo giá loại 3:**
  - Chọn 1 đến 3 poster chung, xoay vòng.
- **Tin nhắn mẫu cho người thật:**
  - Các mẫu hay dùng: hẹn lại hôm sau, giải thích thời gian chờ, gợi ý mẫu đơn giản hơn…
  - Dùng cho nút "gợi ý trả lời" ở chức năng 04.

**Cảnh báo:**
- Bộ content đang bật mà đã **hết hạn dùng** thì app tự tắt bộ đó và báo chủ tiệm.
- Không còn bộ nào đang bật cho loại 1 thì app **không comment bài loại 1** và báo chủ tiệm.

---

## 3. Tìm kiếm và duyệt kho

- **Tìm bằng chữ** theo tên mẫu, mô tả, nội dung, tag. Hỗ trợ gõ không dấu, ví dụ gõ "mat meo" vẫn ra "mắt mèo".
- **Lọc** theo:
  - loại (mẫu, poster, bài Page, bài group, comment);
  - tông màu, kỹ thuật, khoảng giá, mùa;
  - còn hạn dùng hay đã hết;
  - đã dùng hay chưa dùng gần đây.
- **Xem dạng lưới ảnh** cho mẫu và poster.
- Mỗi mục có các nút:
  - **sao chép chữ**, **tải ảnh**;
  - **dùng làm bộ content** cho loại 1;
  - **đăng lại** lên Page hoặc group (vào luồng duyệt và đăng của chức năng 05, bước 5 đến 8);
  - **nhân bản để sửa**.
- Hiển thị số lần đã dùng và lần dùng gần nhất. Điều này giúp chủ tiệm không lặp lại content quá dày.

---

## 4. Đưa dữ liệu cũ vào kho

- Chủ tiệm đang có:
  - một **file Excel lịch sử content**;
  - các poster trên **canvas Claude Design**.
- *Đề xuất của người viết:* có một chức năng **nhập một lần**:
  - nhập file Excel (chủ tiệm cung cấp file để xác định các cột);
  - tải lên hàng loạt ảnh poster đã xuất từ canvas, rồi gắn tên mẫu, giá, tag. AI gợi ý tag từ ảnh.
- Phần này thuộc giai đoạn cuối (xem `../05-roadmap.md`), và có thể bỏ nếu chủ tiệm muốn bắt đầu kho mới từ đầu.

---

## 5. Lưu trữ

- Ảnh lưu trên ổ đĩa của máy chủ, có sao lưu (xem `../04-technical.md`).
- Mỗi poster lưu bản PNG đầy đủ và một ảnh thu nhỏ để xem nhanh trên điện thoại.
- Không xóa cứng mục đã từng được dùng. Chỉ đánh dấu "lưu trữ", để lịch sử comment và bài đăng vẫn còn liên kết được.
