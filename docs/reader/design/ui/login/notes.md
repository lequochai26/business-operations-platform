> Bản đọc sinh từ docs/design/ui/login/notes.md (phiên bản 43e3010, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Mockup – Đăng nhập (`/login`)

**Tóm tắt.** Mockup màn hình Đăng nhập của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Đăng nhập" trong `docs/phases/phase-0/design/auth.md`.

<a id="s-2df8c1fb05"></a>

## Trạng thái đã vẽ

**Tóm tắt.** Mockup vẽ form ở trạng thái thường, đang gửi, các lỗi nhập liệu, các lỗi khi gửi và các banner thông tin. Một số trạng thái chuẩn không vẽ vì không áp dụng cho màn hình này.

**Các trạng thái đã vẽ**
- `normal.html`: form trống. Form gồm logo "Mio", tiêu đề "Đăng nhập", ô Tên đăng nhập, ô Mật khẩu có nút Hiện/Ẩn, nút "Đăng nhập" và dòng "Quên mật khẩu? Nhờ người quản trị app đặt lại."
- `loading.html`: form đang gửi. Nút hiện "Đang đăng nhập…" kèm vòng xoay và không bấm được.
- `validation-error.html`: lỗi [R-AUT-01](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)* "Nhập tên đăng nhập" và lỗi [R-AUT-03](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)* "Nhập mật khẩu".
- `validation-error-length.html`: lỗi [R-AUT-02](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)* "Tên đăng nhập tối đa 32 ký tự" khi nhập 33 ký tự, và lỗi [R-AUT-04](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)* "Mật khẩu tối đa 128 ký tự".
- `invalid-credentials.html` ([R-AUT-05](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập không tồn tại hoặc mật khẩu sai") *(Tên đăng nhập không tồn tại hoặc mật khẩu sai)*): banner danger "Tên đăng nhập hoặc mật khẩu không đúng". Form giữ tên đăng nhập và xoá ô mật khẩu.
- `locked.html` ([R-AUT-06](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*): banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 12 phút."
- `system-error.html`: lỗi `INTERNAL_ERROR`, banner danger "Lỗi hệ thống, vui lòng thử lại sau".
- `network-error.html`: mất mạng, banner danger "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại." Form giữ nguyên cả hai ô.
- `invalid-origin.html` ([R-AUT-17](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*): banner danger "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000". Địa chỉ trong ví dụ là `PUBLIC_URL` của máy local.
- `cookie-blocked.html`: banner danger "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại."
- `session-expired.html` ([R-AUT-31](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)*): banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Banner này hiện khi phiên hết hạn, khi người dùng bị đăng xuất từ thiết bị khác hoặc khi tài khoản bị xoá.
- `signed-out.html` ([R-AUT-32](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")*): banner info "Bạn đã đăng xuất".

**Không vẽ**
- `empty`: form không có dữ liệu để rỗng. Trạng thái ban đầu chính là `normal`.
- `forbidden`: đây là trang công khai. Người đã đăng nhập mà mở `/login` thì được chuyển về `/` ([R-AUT-28](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*), nên không có màn hình riêng.

<a id="s-34e57f188d"></a>

## Luồng thao tác

**Tóm tắt.** Người chưa đăng nhập được đưa tới form. Web kiểm tra dữ liệu trước khi gửi, sau đó chuyển trang khi thành công hoặc hiện banner khi lỗi.

1. Mở một trang cần đăng nhập khi chưa đăng nhập. App chuyển tới `/login?next=…` ([R-AUT-28](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*) và hiện trạng thái `normal`.
2. Bấm "Đăng nhập" khi thiếu dữ liệu. Web kiểm tra ngay và hiện `validation-error` hoặc `validation-error-length`, không gửi API.
3. Khi dữ liệu hợp lệ, form chuyển sang `loading`.
   - Nếu thành công, app chuyển tới trang trong `next`, hoặc về `/`.
   - Nếu lỗi, form hiện banner tương ứng: `invalid-credentials`, `locked`, `system-error`, `network-error`, `invalid-origin` hoặc `cookie-blocked`.
4. Bấm "Hiện" ở ô Mật khẩu. Ô hiện ký tự và nút đổi thành "Ẩn".
5. Khi người dùng bị đẩy ra vì phiên không còn dùng được, màn hình hiện `session-expired`. Khi bấm "Đăng xuất" thành công, màn hình hiện `signed-out`. Nếu đăng xuất lỗi, màn hình hiện `normal` và không có banner.

**Chi tiết kỹ thuật**
- Web kiểm tra dữ liệu bằng `loginInputSchema`.

<a id="s-955f8ca0fb"></a>

## Component dùng

- `<mio-password-field>` (`docs/design/components/password-field.md`): dùng cho ô Mật khẩu.
- Các component cơ bản (ô nhập, nút, banner, thẻ) được dùng qua `docs/design/ui/mockup-base.css`.

<a id="s-67d26e4976"></a>

## Khác với thiết kế chi tiết

**Tóm tắt.** Mockup đổi vị trí banner và câu thông báo khoá so với thiết kế chi tiết. Các thay đổi này đã được cập nhật vào tài liệu thiết kế.

**Thay đổi**
- Vùng thông báo (banner) đặt ngay sau ô Mật khẩu, trước nút "Đăng nhập".
- Thông báo `LOGIN_LOCKED` đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
- Hai thay đổi trên đã được cập nhật vào thiết kế chi tiết, `api/sessions.md` và `openapi.yaml` ngày 2026-10-31.

**Ghi chú vẽ**
- Logo "Mio" và dòng phụ "Tiệm Nhà Mio · vận hành" đặt trên thẻ form, giống thanh điều hướng.
- Ô nhập không đặt `maxlength` để lỗi [R-AUT-02](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)* và [R-AUT-04](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)* hiện được.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-31: tạo mới.
- 2026-10-31: theo góp ý khi duyệt UI, chuyển banner xuống sau ô Mật khẩu và đổi câu thông báo khoá.
- 2026-10-31: qua `/design-review auth`, điểm RV-12 đổi câu banner `session-expired` thành "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Điểm RV-10 quy định đăng xuất lỗi thì không có banner.
