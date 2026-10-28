# 03 – Dữ liệu cần lưu

Đây là mô tả ở **mức nghiệp vụ**: app cần nhớ những gì và chúng liên quan với nhau thế nào. Tên bảng, kiểu cột và chỉ mục do người code quyết định. Cơ sở dữ liệu dùng PostgreSQL (xem `04-technical.md`).

**Quy ước chung:**
- Mọi thời điểm lưu theo UTC.
- Hiển thị và tính toán theo giờ Việt Nam (Asia/Ho_Chi_Minh).
- Mọi bản ghi có thời điểm tạo và thời điểm cập nhật.

---

## 1. Người dùng và cài đặt

### Người dùng
- tên đăng nhập, mật khẩu (đã băm), vai trò (Quản lý / Thợ), tên hiển thị;
- liên kết Messenger: mã người dùng của Facebook theo Page (PSID), nếu đã ghép nối;
- thời điểm tin nhắn Messenger gần nhất (để tính cửa sổ 24 giờ);
- đăng ký thông báo đẩy.

### Cài đặt
- Tất cả tham số chỉnh được trong `02-features/07-screens-and-settings.md`, mục 2.
- Lưu trong cơ sở dữ liệu để đổi được trên web mà không cần khởi động lại.
- Các khóa bí mật (token Facebook, khóa Gemini) **không** lưu ở đây, mà lưu trong biến môi trường.

### Bộ thông tin của tiệm
- Mỗi mục gồm: tên mục, nội dung, trạng thái đã xác nhận / chưa xác nhận, ghi chú.

---

## 2. Group và bài trong group

### Group
- định danh khai báo (slug hoặc ID), Group ID dạng số, tên;
- các công tắc: quét, comment, đăng bài; giới hạn riêng; ghi chú luật;
- trạng thái truy cập, lần quét gần nhất.

### Bài trong group
Kế thừa mô hình `Post` của POC: `postId`, `groupId`, url, tác giả, nội dung, thời điểm đăng, đính kèm, tương tác, `firstSeenAt`, `lastSeenAt`. Thêm các thông tin sau:
- **kết quả phân loại:** có phù hợp không, loại 1/2/3, độ tin cậy, thời gian khách hỏi (đã quy đổi ra ngày giờ), khu vực, dịch vụ, lý do;
- trạng thái xử lý: mới / không phù hợp / bỏ qua / chờ báo giá / chờ duyệt / đã comment / thất bại, kèm lý do;
- đánh dấu "phân loại sai" do chủ tiệm đặt.

### Comment
- bài, nội dung, poster và bộ content đã dùng;
- chế độ (tự gửi hay đã duyệt), người duyệt;
- trạng thái (chờ duyệt / chờ gửi / đã gửi / thất bại / hết hạn), thời điểm gửi, link hoặc ID comment;
- lỗi và ảnh màn hình nếu thất bại.

### Yêu cầu báo giá
- mã ngắn;
- nguồn: bài trong group, hoặc cuộc trò chuyện inbox;
- ảnh, mô tả 1 dòng của AI;
- câu trả lời của thợ: mô tả của thợ, giá (một con số hoặc một khoảng), hoặc từ chối;
- trạng thái: chờ / đã có giá / đã bỏ / hết hạn;
- các mốc thời gian: gửi, nhắc, trả lời;
- ID tin nhắn Messenger đã gửi, để ghép khi thợ vuốt trả lời.

---

## 3. Lịch

- **Giờ làm theo tuần:** mỗi thứ trong tuần có một hoặc nhiều khoảng giờ.
- **Ngày đặc biệt:** ngày; nghỉ hoặc các khoảng giờ riêng; ghi chú.
- **Khung bận:** bắt đầu, kết thúc, lý do, người tạo.
- **Lịch hẹn:**
  - mã ngắn;
  - khách (liên kết), bắt đầu, thời lượng;
  - mẫu hoặc dịch vụ, ghi chú;
  - nguồn;
  - trạng thái (chưa duyệt / đã chốt / đã làm xong / khách không đến / đã hủy);
  - lịch sử thay đổi: ai, lúc nào, kênh nào, thay đổi gì.
- **Ràng buộc:** không được có hai lịch hẹn ở trạng thái chưa duyệt hoặc đã chốt mà chồng thời gian lên nhau (kể cả thời gian đệm), trừ trường hợp thợ đã ép chọn và được ghi rõ.

---

## 4. Khách và tin nhắn

### Khách
- định danh khách lấy từ Meta Business Suite (ID cuộc trò chuyện hoặc ID người dùng, xem `04-technical.md` mục 4.3), tên Facebook, ảnh đại diện (nếu lấy được);
- trạng thái (chức năng 04, mục 6), ghi chú;
- số lần đã đến làm, lần nhắn gần nhất.

### Cuộc trò chuyện
- khách;
- tự trả lời: bật hoặc tắt;
- tạm dừng tới thời điểm nào (khi người thật đã trả lời);
- trạng thái "chờ người thật" từ lúc nào.

### Tin nhắn
- ID tin nhắn (của Messenger với kênh thợ, hoặc lấy từ Business Suite với inbox khách);
- chiều (khách gửi tới / Page gửi đi);
- người gửi từ phía Page: app, hay người thật;
- nội dung, đính kèm;
- ý định do AI xác định (với tin của khách);
- thời điểm.

### Tin nhắn trong kênh thợ
- Dùng chung cấu trúc trên, kèm liên kết tới yêu cầu (báo giá, lịch hẹn, mẫu mới) mà tin đó thuộc về, và ý định đã hiểu.

---

## 5. Mẫu nail, poster và content

### Mẫu nail
- ảnh gốc (một hoặc nhiều), ảnh đã chỉnh (nhiều bản, có đánh dấu bản được chọn);
- tên, mô tả 1 dòng, mô tả của thợ;
- giá, giá có gồm nối móng không;
- tag;
- trạng thái (đang xử lý / chờ duyệt / đã duyệt / đang nhận làm / ngừng);
- nguồn.

### Mẫu poster
- tên, các trường điền được, bật/tắt, phiên bản.

### Poster
- file PNG, ảnh thu nhỏ;
- mẫu poster đã dùng, giá trị đã điền;
- mẫu nail (nếu có);
- nhãn, hạn dùng.

### Nội dung chữ
- loại (bài Page / bài group dài, ngắn, kể chuyện / comment mẫu / tin nhắn mẫu);
- nội dung, mẫu nail (nếu có), tag, hạn dùng;
- trạng thái (đang dùng / lưu trữ).

### Danh sách poster dùng khi báo giá
- 1–3 poster chung được đánh dấu để xoay vòng trong comment loại 3. Chữ của comment loại 3 do AI viết riêng cho từng bài, nên không cần bộ content.

### Bộ content
- nội dung chữ + poster;
- dùng cho: loại 1 / loại 2;
- bật/tắt;
- cho phép AI viết lại nhẹ.

### Lịch sử sử dụng
- mục đã dùng (nội dung, poster, bộ content);
- nơi dùng (comment / bài Page / bài group, kèm group);
- thời điểm, link.

### Lần chỉnh ảnh
- ảnh gốc, style, prompt đầy đủ, nhà cung cấp, model;
- kết quả, chi phí ước tính, lỗi (nếu có).

---

## 6. Đăng bài

- **Bài đăng:**
  - mẫu nail, nội dung, poster;
  - nơi đăng (Page / group nào), đợt đăng;
  - hẹn giờ;
  - trạng thái (chờ / đang đăng / đã đăng / chờ admin duyệt / thất bại);
  - link, lỗi.

---

## 7. Vận hành

- **Lượt quét:** thời điểm, từng group, thống kê như `GroupCrawlStats` của POC, lý do dừng, lỗi.
- **Sự kiện tự dừng:** thời điểm, lý do, ảnh màn hình và HTML lúc lỗi, người bấm chạy lại và lúc nào.
- **Mức dùng AI:** theo ngày, theo model, số lượt, chi phí ước tính.
- **Thông báo đã gửi:** người nhận, loại, kênh (Messenger / web push), trạng thái.
