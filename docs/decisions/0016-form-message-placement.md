# 0016 – Vị trí và câu chữ thông báo trên màn hình

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan: docs/design/ui-style.md mục "Vị trí thông báo"; ADR 0008-ui-style-direction; tính năng `auth` (phase-0) – góp ý duyệt UI màn Đăng nhập, Đổi mật khẩu; skill `ui-design`, `design-review`

## Bối cảnh

- `ui-style.md` đã có kiểu banner, toast và vị trí lỗi theo trường (dưới ô), nhưng chưa quy định **thông báo cấp form** đặt ở đâu: lỗi nghiệp vụ (sai mật khẩu, bị khóa), lỗi hệ thống, mất mạng, thông báo info khi vừa chuyển tới trang.
- Mockup `auth` lần đầu đặt banner ở đầu form. Khi duyệt, người dùng muốn banner nằm sau ô nhập cuối, ngay trên nút gửi: người dùng đang nhìn vào nút vừa bấm, banner ở đầu form dễ bị bỏ qua, nhất là form dài phải cuộn.
- Cùng lần duyệt lộ ra vấn đề câu chữ: thông báo `LOGIN_LOCKED` "Đăng nhập sai quá nhiều lần…" dùng chung cho màn Đăng nhập và Đổi mật khẩu, đặt ở màn Đổi mật khẩu thì khó hiểu. Đã đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
- Phần lớn màn hình của các giai đoạn sau là form cài đặt dài và hộp thoại xác nhận, nên cần một quy ước chung để không lặp lại hai vấn đề trên ở từng tính năng.

## Các phương án

### A. Banner ở đầu form
- Ưu: kiểu phổ biến; người dùng thấy ngay khi trang vừa mở (hợp với thông báo info khi chuyển trang tới).
- Nhược: sau khi bấm gửi, mắt người dùng đang ở nút, phải nhìn ngược lên mới thấy; form dài cuộn thì banner nằm ngoài khung nhìn; tách xa nút làm người dùng tưởng chưa có gì xảy ra.

### B. Banner ngay trên hàng nút gửi (vùng thông báo của form)
- Ưu: kết quả hiện ngay cạnh chỗ vừa bấm; form dài vẫn thấy vì nút luôn ở trong khung nhìn lúc bấm; một vị trí cố định cho mọi loại thông báo cấp form, kể cả trong hộp thoại.
- Nhược: thông báo info khi vừa mở trang (ví dụ "Bạn đã đăng xuất") nằm dưới các ô, kém nổi hơn đặt ở đầu; form rất dài thì người vừa mở trang có thể chưa thấy ngay.

### C. Chỉ dùng toast cho mọi thông báo cấp form
- Ưu: không chiếm chỗ trong form, không làm form nhảy bố cục.
- Nhược: toast tự ẩn, không hợp với lỗi cần đọc kỹ (bị khóa bao nhiêu phút, sai địa chỉ app); toast ở góc dưới phải xa form; lẫn với toast kết quả thao tác khác.

## Quyết định

Chọn B (người dùng chốt khi duyệt UI `auth` ngày 2026-10-31) vì thông báo cấp form là phản hồi của thao tác gửi, nên đặt ở nơi người dùng vừa thao tác. Kèm các quy tắc (chi tiết ở `ui-style.md` mục "Vị trí thông báo"):

- Lỗi theo trường: dưới ô, thay chỗ gợi ý (giữ như cũ).
- Thông báo cấp form: một vùng thông báo duy nhất, ngay sau trường cuối cùng, trước hàng nút gửi.
  - Hiện mọi thông báo còn đúng, mỗi thông báo một banner, xếp theo mức độ danger → warning → info.
  - Mỗi lần bấm gửi: xóa hết banner cũ trước khi hiện kết quả mới.
  - Không lặp: cùng nội dung chỉ một banner.
- Hộp thoại: cùng quy tắc, vùng thông báo ngay trên hàng nút. Gửi lỗi mà hộp thoại đã đóng thì thông báo về vùng thông báo của form gốc.
- Thông báo cấp trang (trạng thái hệ thống, không gắn với form nào, ví dụ "Đã tự dừng"): dưới đầu trang, trên nội dung.
- Thành công: toast; không dùng banner success trong form, trừ khi thông báo phải ở lại trên trang.
- Câu chữ: một thông báo dùng chung cho nhiều màn hình hoặc nhiều endpoint phải đúng nghĩa ở mọi chỗ nó hiện; không đúng thì viết câu trung tính hoặc tách câu riêng.

## Hệ quả

- Được:
  - mọi form có cùng một chỗ đọc kết quả, người dùng không phải đi tìm;
  - `ui-design` và `design-review` có tiêu chí cụ thể để kiểm, không phụ thuộc trí nhớ người duyệt;
  - code web chỉ cần một component vùng thông báo cho form và hộp thoại.
- Mất / rủi ro:
  - thông báo info khi vừa chuyển tới trang (ví dụ "Phiên đăng nhập đã hết hạn…") kém nổi hơn đặt ở đầu form; chấp nhận vì các form có thông báo này đều ngắn;
  - vùng thông báo xuất hiện làm nút gửi dịch xuống; người dùng bấm lại ngay có thể trượt (chấp nhận, form không có thao tác bấm liên tiếp);
  - phải sửa lại các mockup đã vẽ trước quy ước nếu có (hiện chỉ có `auth`, đã theo quy ước).
