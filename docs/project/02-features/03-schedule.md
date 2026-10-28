# Chức năng 03 – Lịch làm của thợ

## Mục đích
Lịch trong app là **nguồn sự thật duy nhất** về thời gian của thợ. Mọi chỗ cần biết "còn trống không" đều đọc từ đây: comment loại 2 và 3, trả lời khách trong inbox, tóm tắt lịch cho thợ. Nhờ vậy không còn chuyện chủ tiệm và thợ mỗi người nắm một lịch khác nhau.

## Liên quan
- Đọc lịch: `01-group-auto-comment.md`, `04-page-inbox.md`
- Duyệt / hủy / dời qua Messenger: `02-technician-channel.md`
- Màn hình lịch: `07-screens-and-settings.md`

---

## 1. Các thành phần của lịch

### Giờ làm việc theo tuần
- Thợ hoặc chủ tiệm khai báo giờ nhận khách cho từng ngày trong tuần. Ví dụ: T2–T6 9:00–21:00, T7–CN 8:00–21:30.
- Một ngày có thể có nhiều khoảng, ví dụ nghỉ trưa ở giữa.
- **Hiện chưa có giờ nhận khách chính thức.** Đây là thông tin bắt buộc phải nhập trước khi bật comment loại 2 (xem `06-open-issues-and-assumptions.md`).

### Ngày đặc biệt
- Ghi đè giờ làm của một ngày cụ thể: nghỉ cả ngày, hoặc làm theo giờ khác (lễ, Tết).

### Khung bận
- Khoảng thời gian thợ tự khóa vì việc riêng. Tạo trên web hoặc nhắn qua Messenger.

### Lịch hẹn
- Một khoảng thời gian thợ làm cho một khách, xem mục 2.

### Thời lượng
- **Thời lượng mặc định** một lượt làm: 2,5 giờ, chỉnh được.
- Lịch hẹn có thể có thời lượng riêng, ví dụ mẫu đơn giản 1,5 giờ hoặc mẫu cầu kỳ 3 giờ.
- **Thời gian đệm** giữa hai lịch, ví dụ dọn dẹp: mặc định 15 phút, chỉnh được (quyết định của người viết).

---

## 2. Lịch hẹn

### Thông tin
- khách (liên kết tới hồ sơ khách trong inbox, nếu có);
- ngày, giờ bắt đầu, thời lượng;
- mẫu hoặc dịch vụ, nếu biết;
- ghi chú;
- nguồn: inbox Page, thợ tạo, chủ tiệm tạo;
- trạng thái và lịch sử thay đổi (ai đổi, lúc nào, qua kênh nào).

### Các trạng thái
- **Chưa duyệt:** app ghi nhận khi khách xin đặt qua inbox. **Tạm giữ chỗ**, nên khung này không được mời khách khác.
- **Đã chốt:** thợ (hoặc chủ tiệm) đã duyệt sau khi chốt với khách.
- **Đã làm xong:** thợ báo khách đã đến và làm xong. Khách được tính là "xong" (xem chức năng 04).
- **Khách không đến.**
- **Đã hủy:** kèm lý do, nếu có.
- *(Dời lịch không phải một trạng thái riêng.)* Dời lịch là đổi thời gian của lịch đó, kèm chốt luôn. Lịch sử giữ lại thời gian cũ.

### Chuyển trạng thái
- Chưa duyệt → **Đã chốt**: thợ bấm Duyệt.
- Chưa duyệt hoặc Đã chốt → **Đã chốt với giờ mới**: thợ Dời và báo giờ mới.
- Chưa duyệt hoặc Đã chốt → **Đã hủy**.
- Đã chốt → **Đã làm xong** hoặc **Khách không đến**.
- Ai được làm: thợ và chủ tiệm, trên web hoặc qua Messenger.

### Lịch "chưa duyệt" bị bỏ quên
- Sau **2 giờ** chưa được xử lý, app nhắc thợ.
- Nếu tới sát giờ hẹn (mặc định trước 3 giờ) mà vẫn chưa duyệt, app báo cả thợ và chủ tiệm.
- App **không tự hủy** (quyết định của người viết).

---

## 3. Tìm khung trống

Đây là phép tính dùng chung cho mọi chức năng.

**Đầu vào:**
- ngày;
- buổi hoặc khoảng giờ mong muốn, nếu có;
- thời lượng (mặc định lấy thời lượng mặc định).

**Một khung được coi là trống khi:**
- nằm trong giờ làm của ngày đó (đã tính ngày đặc biệt);
- không chồng lên khung bận;
- không chồng lên lịch hẹn ở trạng thái **chưa duyệt** hoặc **đã chốt**, kể cả thời gian đệm;
- giờ bắt đầu cách hiện tại ít nhất **N giờ** (mặc định 2 giờ), để không mời khách vào khung sắp diễn ra.

**Giờ bắt đầu đề xuất** làm tròn theo bước 30 phút (chỉnh được).

**Quy ước buổi** (quyết định của người viết, chỉnh được):
- sáng: 8:00–12:00
- chiều: 12:00–17:00
- tối: 17:00–21:30

**Khung trống gần nhất:**
- Khi khung khách hỏi không còn trống, tìm các khung trống gần nhất tính theo khoảng cách thời gian.
- Ưu tiên cùng ngày, sau đó các ngày kế tiếp, trong tối đa N ngày (mặc định 7).
- Trả về tối đa K khung (mặc định 3). Các khung nên trải ra các buổi khác nhau, không trả ba khung liền nhau trong cùng một buổi.

**Cách diễn đạt:** khi trả lời khách hoặc comment, app có thể nói theo khung rộng, ví dụ "chiều T3 còn slot từ 14h". Nhưng **mọi giờ nói ra phải nằm trong khung trống thật**.

---

## 4. Chống trùng lịch

- Tạo hoặc dời lịch phải được kiểm tra trống **ngay tại thời điểm ghi** vào cơ sở dữ liệu, trong cùng một giao dịch, để hai thao tác cùng lúc không tạo ra hai lịch chồng nhau.
- Mọi luồng tự động (inbox giữ chỗ, đề xuất khung) **luôn bị chặn cứng** khi trùng.
- Chỉ thao tác ép chọn của thợ hoặc chủ tiệm mới vượt qua được kiểm tra này. Lịch ép chọn mang cờ "ép chọn" và hiện cảnh báo trên lịch.
- Gợi ý cách làm: ràng buộc loại trừ trong PostgreSQL, áp dụng cho các lịch không có cờ ép chọn.
- Thợ dời lịch sang một khung không trống:
  - app báo khung đó đang bị chiếm bởi gì;
  - đề xuất khung gần nhất;
  - và vẫn cho thợ **ép chọn** nếu thợ xác nhận (thợ là người quyết định cuối cùng).

---

## 5. Hiển thị

- **Lịch theo ngày và theo tuần**, dễ xem trên điện thoại.
- Màu sắc khác nhau cho chưa duyệt, đã chốt, khung bận.
- Bấm vào một lịch để xem chi tiết, đổi trạng thái, mở cuộc trò chuyện với khách.
- Xem chi tiết ở `07-screens-and-settings.md`.
