> Bản đọc sinh từ docs/decisions/0016-form-message-placement.md (phiên bản ac0ed83, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0016 – Vị trí và câu chữ thông báo trên màn hình

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan:
  - docs/design/ui-style.md mục "Vị trí thông báo";
  - [ADR 0008](0008-ui-style-direction.md "Hướng style UI: kem ấm, sage nhấn, thanh điều hướng xanh đậm") *(Hướng style UI: kem ấm, sage nhấn, thanh điều hướng xanh đậm)*-ui-style-direction;
  - tính năng `auth` (phase-0): góp ý duyệt UI màn Đăng nhập, Đổi mật khẩu;
  - skill `ui-design`, `design-review`.

**Tóm tắt.** Thông báo cấp form được đặt trong một vùng thông báo duy nhất, ngay trên hàng nút gửi, vì đó là nơi người dùng vừa thao tác. Kèm theo là quy tắc câu chữ: thông báo dùng chung cho nhiều màn hình phải đúng nghĩa ở mọi chỗ nó hiện.

<a id="s-0bc81167ac"></a>

## Bối cảnh

- `ui-style.md` đã có kiểu banner, toast và vị trí lỗi theo trường (dưới ô). Tài liệu này chưa quy định **thông báo cấp form** đặt ở đâu. Thông báo cấp form gồm lỗi nghiệp vụ (sai mật khẩu, bị khoá), lỗi hệ thống, mất mạng và thông báo info khi vừa chuyển tới trang.
- Mockup `auth` lần đầu đặt banner ở đầu form. Khi duyệt, người dùng muốn banner nằm sau ô nhập cuối, ngay trên nút gửi. Lý do là người dùng đang nhìn vào nút vừa bấm. Banner ở đầu form dễ bị bỏ qua, nhất là với form dài phải cuộn.
- Cùng lần duyệt đó lộ ra một vấn đề về câu chữ. Thông báo `LOGIN_LOCKED` "Đăng nhập sai quá nhiều lần…" dùng chung cho màn Đăng nhập và màn Đổi mật khẩu. Đặt ở màn Đổi mật khẩu thì câu này khó hiểu. Câu đã được đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
- Phần lớn màn hình của các giai đoạn sau là form cài đặt dài và hộp thoại xác nhận. Vì vậy cần một quy ước chung để từng tính năng không lặp lại hai vấn đề trên.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-53b1780f6f"></a>

### A. Banner ở đầu form

**Ưu**

- Là kiểu phổ biến.
- Người dùng thấy ngay khi trang vừa mở, hợp với thông báo info khi chuyển tới trang.

**Nhược**

- Sau khi bấm gửi, mắt người dùng đang ở nút nên phải nhìn ngược lên mới thấy.
- Form dài phải cuộn thì banner nằm ngoài khung nhìn.
- Banner tách xa nút làm người dùng tưởng chưa có gì xảy ra.

<a id="s-68f9c5e896"></a>

### B. Banner ngay trên hàng nút gửi (vùng thông báo của form)

**Ưu**

- Kết quả hiện ngay cạnh chỗ vừa bấm.
- Form dài vẫn thấy, vì lúc bấm thì nút luôn ở trong khung nhìn.
- Mọi loại thông báo cấp form có một vị trí cố định, kể cả trong hộp thoại.

**Nhược**

- Thông báo info khi vừa mở trang (ví dụ "Bạn đã đăng xuất") nằm dưới các ô, nên kém nổi hơn khi đặt ở đầu.
- Với form rất dài, người vừa mở trang có thể chưa thấy thông báo ngay.

<a id="s-a74a23d898"></a>

### C. Chỉ dùng toast cho mọi thông báo cấp form

**Ưu**

- Không chiếm chỗ trong form.
- Không làm form nhảy bố cục.

**Nhược**

- Toast tự ẩn, không hợp với lỗi cần đọc kỹ, ví dụ bị khoá bao nhiêu phút hay sai địa chỉ app.
- Toast nằm ở góc dưới bên phải, xa form.
- Toast dễ lẫn với toast kết quả của thao tác khác.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án B. Người dùng chốt phương án này khi duyệt UI `auth` ngày 2026-10-31.

**Vì sao.** Thông báo cấp form là phản hồi của thao tác gửi. Vì vậy thông báo nên nằm ở nơi người dùng vừa thao tác.

**Quy tắc kèm theo** (chi tiết ở `ui-style.md` mục "Vị trí thông báo")

- Lỗi theo trường: hiện dưới ô, thay chỗ dòng gợi ý, giữ như cũ.
- Thông báo cấp form: có một vùng thông báo duy nhất, ngay sau trường cuối cùng và trước hàng nút gửi.
  - Vùng này hiện mọi thông báo còn đúng, mỗi thông báo một banner. Banner xếp theo mức độ: danger trước, rồi warning, rồi info.
  - Mỗi lần bấm gửi, toàn bộ banner cũ bị xoá trước khi hiện kết quả mới.
  - Không lặp: cùng một nội dung chỉ có một banner.
- Hộp thoại: theo cùng quy tắc, vùng thông báo nằm ngay trên hàng nút. Nếu gửi lỗi mà hộp thoại đã đóng thì thông báo hiện ở vùng thông báo của form gốc.
- Thông báo cấp trang là trạng thái hệ thống, không gắn với form nào, ví dụ "Đã tự dừng". Loại này đặt dưới đầu trang, trên phần nội dung.
- Thành công: dùng toast. Không dùng banner success trong form, trừ khi thông báo phải ở lại trên trang.
- Câu chữ: một thông báo dùng chung cho nhiều màn hình hoặc nhiều endpoint phải đúng nghĩa ở mọi chỗ nó hiện. Nếu không đúng thì viết câu trung tính hoặc tách thành câu riêng.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Mọi form có cùng một chỗ để đọc kết quả, người dùng không phải đi tìm.
- `ui-design` và `design-review` có tiêu chí cụ thể để kiểm tra, không phụ thuộc trí nhớ người duyệt.
- Code web chỉ cần một component vùng thông báo cho cả form và hộp thoại.

**Mất và rủi ro**

- Thông báo info khi vừa chuyển tới trang (ví dụ "Phiên đăng nhập đã hết hạn…") kém nổi hơn khi đặt ở đầu form. Điều này được chấp nhận vì các form có thông báo này đều ngắn.
- Khi vùng thông báo xuất hiện, nút gửi bị đẩy xuống. Người dùng bấm lại ngay có thể bấm trượt. Điều này được chấp nhận vì form không có thao tác bấm liên tiếp.
- Phải sửa lại các mockup đã vẽ trước quy ước, nếu có. Hiện chỉ có mockup `auth`, và mockup này đã theo quy ước.
