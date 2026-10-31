<!-- src-section: 0b0fa0b228 5fcde9686011 -->
# Mockup – Đổi mật khẩu (`/account/password`)

**Tóm tắt.** Mockup màn hình Đổi mật khẩu của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Đổi mật khẩu" trong `docs/phases/phase-0/design/auth.md`.

<!-- src-section: 2df8c1fb05 225d010866ea -->
## Trạng thái đã vẽ

**Tóm tắt.** Mockup vẽ form trống, hộp thoại xác nhận, trạng thái đang lưu, thành công, các lỗi nhập liệu và các banner lỗi. Một số trạng thái không vẽ vì không áp dụng hoặc đã vẽ ở màn hình khác.

**Các trạng thái đã vẽ**
- `normal.html`: form trống gồm ô Mật khẩu hiện tại, ô Mật khẩu mới có gợi ý "Ít nhất 8 ký tự", ô Nhập lại mật khẩu mới và nút "Đổi mật khẩu". Mục "Đổi mật khẩu" ở khối tài khoản đang được chọn.
- `confirm-dialog.html` (R-AUT-34): hộp thoại "Đổi mật khẩu" có các nút sau:
  - "Đổi và đăng xuất thiết bị khác": nút primary, được focus sẵn;
  - "Chỉ đổi mật khẩu": nút secondary;
  - "Hủy": nút ghost.
- `loading.html`: người dùng đã bấm "Đổi và đăng xuất thiết bị khác". Nút đó hiện "Đang lưu…", hai nút còn lại không bấm được.
- `success.html` (R-AUT-23): form được xoá trắng và hiện toast success "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất." Nếu người dùng chọn "Chỉ đổi mật khẩu", toast là "Đã đổi mật khẩu."
- `validation-error.html`: cả ba ô trống. Các lỗi là R-AUT-19 "Nhập mật khẩu hiện tại", R-AUT-21 "Nhập mật khẩu mới" và R-AUT-22 "Nhập lại mật khẩu mới".
- `validation-error-format.html`: các lỗi là R-AUT-19 "Mật khẩu tối đa 128 ký tự", R-AUT-21 "Mật khẩu mới phải từ 8 đến 128 ký tự" và R-AUT-22 "Mật khẩu nhập lại không khớp".
- `validation-error-username.html`: lỗi R-AUT-21 "Mật khẩu không được trùng tên đăng nhập". Ví dụ vẽ cảnh Thợ `ngocanh.nail` nhập `NgocAnh.Nail`, ô đang hiện ký tự.
- `validation-error-current.html`: lỗi R-AUT-20 "Mật khẩu hiện tại không đúng" do API trả về. Hộp thoại đã đóng và form giữ dữ liệu.
- `validation-error-same.html`: lỗi R-AUT-21 "Mật khẩu mới phải khác mật khẩu hiện tại" do API trả về.
- `locked.html` (R-AUT-20, R-AUT-06): banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." Form giữ dữ liệu. Thời gian chờ còn đủ 15 phút vì lần sai thứ 5 vừa làm khoá.
- `system-error.html`: banner danger "Lỗi hệ thống, vui lòng thử lại sau", form giữ dữ liệu. Khi mất mạng, banner nằm ở cùng chỗ với câu "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."

**Không vẽ**
- `empty`: form không có dữ liệu để rỗng. Trạng thái ban đầu chính là `normal`.
- `forbidden`: cả Quản lý và Thợ đều dùng được màn hình này, vì mỗi người đổi mật khẩu của mình.
- Phiên bị xoá trong lúc gửi (R-AUT-24, R-AUT-31): app chuyển tới `/login` kèm banner. Trạng thái này đã vẽ ở `docs/design/ui/login/session-expired.html`.

<!-- src-section: 34e57f188d 5c7f13d2d516 -->
## Luồng thao tác

**Tóm tắt.** Web kiểm tra dữ liệu trước, sau đó hỏi xác nhận bằng hộp thoại rồi mới gửi. Kết quả hiện thành toast, lỗi dưới ô hoặc banner.

1. Bấm "Đổi mật khẩu" ở khối tài khoản. Màn hình hiện `normal`.
2. Bấm nút "Đổi mật khẩu". Web kiểm tra dữ liệu theo R-AUT-19, ba ý đầu của R-AUT-21 và R-AUT-22.
   - Nếu có lỗi, màn hình hiện một trong các trạng thái `validation-error*` và không mở hộp thoại.
   - Nếu hợp lệ, màn hình hiện `confirm-dialog`.
3. Trong hộp thoại, nhấn Esc, bấm ra ngoài hoặc bấm "Hủy" thì hộp thoại đóng và form giữ dữ liệu. Bấm một trong hai nút đổi thì màn hình chuyển sang `loading`.
4. Nếu thành công, màn hình hiện `success`. Nếu lỗi, hộp thoại đóng:
   - lỗi theo trường hiện dưới ô (`validation-error-current`, `validation-error-same`);
   - `LOGIN_LOCKED` và các lỗi khác hiện thành banner (`locked`, `system-error`).

<!-- src-section: 955f8ca0fb d2d86a5e6ee7 -->
## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): dùng với `active="/account/password"`.
- `<mio-password-field>` (`docs/design/components/password-field.md`): dùng cho cả ba ô. Mỗi ô có nút Hiện/Ẩn riêng.
- Các component cơ bản (nút, thẻ, banner, toast, hộp thoại) được dùng qua `docs/design/ui/mockup-base.css`.

<!-- src-section: 67d26e4976 520a4d694771 -->
## Khác với thiết kế chi tiết

**Tóm tắt.** Mockup đổi vị trí banner và câu thông báo khoá so với thiết kế chi tiết. Các thay đổi này đã được cập nhật vào tài liệu thiết kế.

- Vùng thông báo (banner) đặt ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu", giống màn Đăng nhập.
- Thông báo `LOGIN_LOCKED` đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
- Hai thay đổi trên đã được cập nhật vào thiết kế chi tiết, `api/users.md` và `openapi.yaml` ngày 2026-10-31.

<!-- src-section: 80b54c0db6 ea608720b937 -->
## Lịch sử thay đổi

- 2026-10-31: tạo mới.
- 2026-10-31: theo góp ý khi duyệt UI, chuyển banner xuống sau ô Nhập lại mật khẩu mới và đổi câu thông báo khoá.
