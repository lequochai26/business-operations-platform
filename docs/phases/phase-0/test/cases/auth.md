# Test case – Đăng nhập và phân quyền (`auth`, `AUT`)

- Thiết kế: `docs/phases/phase-0/design/auth.md`
- Mockup: `docs/design/ui/login/`, `docs/design/ui/app-shell/`, `docs/design/ui/change-password/`, `docs/design/ui/forbidden/`, `docs/design/ui/not-found/`
- Cập nhật: 2026-10-31

## Khía cạnh không áp dụng

- 9. Phía Facebook và Messenger: đăng nhập không dùng dịch vụ ngoài (thiết kế mục Tích hợp bên ngoài); ghép nối Messenger của thợ thuộc giai đoạn sau.
- 1. Hiển thị, phần giao diện điện thoại và ngày giờ: giai đoạn 0 chỉ mở qua `127.0.0.1` trên máy tính, chưa thiết kế bố cục điện thoại (thiết kế mục Màn hình); tính năng không hiển thị ngày giờ nào.
- Lằn ranh đỏ: không lằn ranh nào thuộc tính năng này (không nói với khách, không comment, không đụng lịch hay tài khoản Facebook). Case cốt lõi về bảo mật (khóa đăng nhập, phiên, CSRF, không lộ mật khẩu) vẫn gắn `Regression: có`.

## Ghi chú chạy

- Môi trường: hệ thống chạy như P0-SKL-001 bằng `compose.yml`, `.env` có `MIO_PUBLIC_URL=http://localhost:3000`. Web mở bằng Playwright (Chromium) tại `http://localhost:3000`, khung 1440×900. "Context A/B/C" là các browser context riêng (mỗi context = một thiết bị).
- Viết tắt trong các bước:
  - `<api>` = `http://127.0.0.1:3000/api/v1`;
  - `<psql> "<sql>"` = `docker compose exec -T postgres psql -U mio -d mio -c "<sql>"`;
  - `<cli> <lệnh>` = `docker compose exec -T api node dist/cli.js <lệnh>`; mật khẩu đưa qua stdin: `printf '%s\n' '<mật khẩu>' | <cli> …`;
  - `<origin>` = `-H 'Origin: http://localhost:3000'`; `<json>` = `-H 'Content-Type: application/json'`;
  - `<đăng nhập mio>` = `curl -s -i -c mio.jar <origin> <json> -d '{"username":"mio","password":"MioQuanLy#2026"}' <api>/sessions`; tương tự `<đăng nhập ngocanh>` với `ngocanh.jar`;
  - `<log auth>` = `docker compose logs api --since 10m | grep '"event":"auth.'`;
  - `<id mio>` = `(select id from users where username = 'mio')`.
- Dữ liệu mẫu (tạo như P0-AUT-081 nếu chưa có):
  - `mio`: Quản lý, tên hiển thị "Huỳnh Mio", mật khẩu `MioQuanLy#2026`;
  - `ngocanh.nail`: Thợ, tên hiển thị "Ngọc Anh", mật khẩu `NgocAnh#2026`.
  - Case làm đổi mật khẩu của tài khoản mẫu: cuối case đặt lại bằng `printf '%s\n' '<mật khẩu mẫu>' | <cli> reset-password --username <tên>`.
- Trước mỗi case chạy `<psql> "delete from login_throttles"`, trừ khi tiền điều kiện ghi khác.
- Giả lập thời gian trôi qua bằng cách sửa cột thời gian qua SQL theo `now()` của PostgreSQL. Các container dùng chung đồng hồ máy local nên chỉ chênh vài giây; khoảng sai số ghi trong từng bước.
- Mạng chậm: giả lập bằng Chrome DevTools Protocol (`Network.emulateNetworkConditions`, độ trễ 3000 ms) qua Playwright, tương đương chỉnh Network throttling trong DevTools. Mất mạng: `context.setOffline(true)`.
- Case cần tính năng sau (chạy `/manual-test-run` khi chưa có thì case là `bị chặn`, chạy lại sau):
  - cần trang `/settings` (thêm bởi `group-settings`) và `/system-log` (thêm bởi `emergency-stop`): P0-AUT-041, P0-AUT-043;
  - cần ít nhất một endpoint chỉ Quản lý có nút thao tác trên web (`group-settings` hoặc `crawl-settings`): P0-AUT-042, P0-AUT-044.
  - Trước khi có các tính năng đó, Quản lý cũng chỉ thấy mục "Trang chính" (thiết kế mục Khung app: mỗi tính năng tự thêm mục của mình).
- Banner "Phiên đăng nhập đã kết thúc…" dựa vào cờ `mio.hadSession` trong `localStorage` (R-AUT-31): context đã từng vào app thì có cờ; context mới hoặc vừa bấm "Đăng xuất" thì không.
- Phần chỉ kiểm được bằng test tự động (không tạo được bằng thao tác bên ngoài code); `/implementation-plan` phải có test tương ứng:
  - R-AUT-14: route thiếu `@Public()` / `@Roles(...)` làm api thoát mã 1, log "Route chưa khai báo quyền: <METHOD> <path>"; manual chỉ kiểm hệ quả ở P0-AUT-040;
  - R-AUT-24: cả hai nhánh thứ tự (phiên bị xóa trước / sau bước kiểm phiên); manual chỉ kiểm bất biến ở P0-AUT-066;
  - R-AUT-06: transaction khóa dòng của `recordFailure`, `confirmSuccess`; request đúng mật khẩu đã qua `getLock` mà gặp khóa lúc `confirmSuccess` → 429, không tạo phiên; manual kiểm hệ quả ở P0-AUT-023;
  - R-AUT-23, R-AUT-26: đổi mật khẩu và `reset-password` khóa dòng `users`; lần đổi thứ hai chạy sau, kiểm mật khẩu hiện tại trên chuỗi băm mới; manual kiểm hệ quả ở P0-AUT-066;
  - R-AUT-30: CLI không mở được `/proc/1/fd/1` thì ghi log ra stderr;
  - R-AUT-05: tên không tồn tại vẫn gọi `verify` trên chuỗi băm giả; manual chỉ đo thời gian ở P0-AUT-013;
  - R-AUT-30: danh sách `redact` ở độ sâu 1 đến 3.

## P0-AUT-001 Quản lý đăng nhập từ trang cần đăng nhập
- Thiết kế: R-AUT-08, R-AUT-09, R-AUT-28; mục Khung app
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: có tài khoản `mio`; `<psql> "delete from user_sessions"`; context mới, không có cookie
- Các bước:
  1. Mở `http://localhost:3000/` → màn hình chờ rồi chuyển `/login?next=%2F`, form Đăng nhập trống [evidence]
  2. Nhập `mio` / `MioQuanLy#2026`, bấm "Đăng nhập" → `POST /api/v1/sessions` trả 201, thân `{"user":{"id":"<uuid>","username":"mio","displayName":"Huỳnh Mio","role":"manager"}}`; chuyển `/`, tiêu đề "Hôm nay", mục "Trang chính" đang chọn [evidence]
  3. Xem khối tài khoản cuối thanh điều hướng → "Huỳnh Mio", badge "Quản lý", "Đổi mật khẩu", "Đăng xuất" [evidence]
  4. `<psql> "select expires_at - now() as con_lai from user_sessions where user_id = <id mio>"` → đúng 1 dòng, `con_lai` ≈ 90 ngày (sai số 1 phút) [evidence]
  5. Tải lại trang → vẫn ở `/`, không quay về `/login`
  6. Chạy `localStorage.getItem('mio.hadSession')` trong trang → khác `null` (R-AUT-31)

## P0-AUT-002 Thợ đăng nhập, thanh điều hướng chỉ có mục của Thợ
- Thiết kế: R-AUT-08, R-AUT-29; mục Khung app
- Khía cạnh: Phân quyền
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: có tài khoản `ngocanh.nail`; context mới
- Các bước:
  1. Mở `/login`, đăng nhập `ngocanh.nail` / `NgocAnh#2026` → chuyển `/`, tiêu đề "Hôm nay"
  2. Xem thanh điều hướng → chỉ có "Trang chính"; không có "Cài đặt", "Nhật ký hệ thống", không có đường kẻ nhóm Quản lý [evidence]
  3. Xem khối tài khoản → "Ngọc Anh", badge "Thợ", "Đổi mật khẩu", "Đăng xuất" [evidence]

## P0-AUT-003 Màn hình Đăng nhập và khung app khớp mockup
- Thiết kế: mục Màn hình Đăng nhập, Khung app; mockup `login/`, `app-shell/`
- Khía cạnh: Hiển thị
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: người
- Tiền điều kiện: đã có ảnh evidence của P0-AUT-001, 002, 005, 007, 008, 012, 014, 028, 030, 034, 047, 053, 068, 069, 071
- Các bước:
  1. Đặt từng ảnh evidence cạnh ảnh mockup cùng trạng thái trong `docs/design/ui/login/screenshots/` → bố cục, màu, chữ, nút khớp; banner nằm ngay sau ô Mật khẩu, trước nút "Đăng nhập"; chữ tiếng Việt có dấu hiển thị đủ, không vỡ font [evidence]
  2. So ảnh Trang chính của Quản lý, Thợ, màn hình chờ, màn hình lỗi nạp phiên với `docs/design/ui/app-shell/screenshots/` → khớp; badge vai trò dễ đọc trên nền thanh điều hướng [evidence]

## P0-AUT-004 Thuộc tính ô nhập và nút Hiện/Ẩn trên màn Đăng nhập
- Thiết kế: mục Màn hình Đăng nhập; component `password-field`
- Khía cạnh: Hiển thị
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Đọc DOM → ô Tên đăng nhập có `autocomplete="username"`, `autocapitalize="none"`; ô Mật khẩu `type="password"`, `autocomplete="current-password"`; không ô nào có `maxlength`
  2. Gõ `abc 123` vào ô Mật khẩu, bấm "Hiện" → ô hiện `abc 123`, nút đổi thành "Ẩn" (`aria-label` "Ẩn mật khẩu"); bấm "Ẩn" → ẩn lại, giá trị không đổi [evidence]
  3. Tab tới nút Hiện/Ẩn, nhấn Enter rồi Space → chỉ đổi hiện/ẩn; tab Network không có request `POST /api/v1/sessions`
  4. Đặt con trỏ trong ô Mật khẩu, nhấn Enter → form được gửi (có một request `POST /api/v1/sessions`)

## P0-AUT-005 Bỏ trống cả hai ô khi đăng nhập
- Thiết kế: R-AUT-01, R-AUT-03
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Bấm "Đăng nhập" khi hai ô trống → dưới ô Tên đăng nhập "Nhập tên đăng nhập", dưới ô Mật khẩu "Nhập mật khẩu"; không có banner; không có request `POST /api/v1/sessions` [evidence]
  2. Nhập `mio` vào Tên đăng nhập, bấm lại → chỉ còn lỗi "Nhập mật khẩu"

## P0-AUT-006 Ô chỉ có khoảng trắng
- Thiết kế: R-AUT-01, R-AUT-03, R-AUT-07
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Tên đăng nhập 3 khoảng trắng, mật khẩu `x`, bấm "Đăng nhập" → "Nhập tên đăng nhập" dưới ô; không gửi API
  2. Tên `mio`, mật khẩu 3 khoảng trắng → không có lỗi theo trường; API trả 401, banner danger "Tên đăng nhập hoặc mật khẩu không đúng" [evidence]
  3. `<psql> "select failed_count from login_throttles where username = 'mio'"` → `1`

## P0-AUT-007 Tên đăng nhập 32 và 33 ký tự
- Thiết kế: R-AUT-02, R-AUT-07 (độ dài theo code point, đo sau khi chuẩn hóa)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`; mật khẩu nhập `x`
- Các bước:
  1. Tên `a` × 32 → không có lỗi theo trường, banner "Tên đăng nhập hoặc mật khẩu không đúng"
  2. Tên `a` × 33 → "Tên đăng nhập tối đa 32 ký tự" dưới ô, không gửi API [evidence]
  3. Tên gồm 2 khoảng trắng + `a` × 32 + 2 khoảng trắng → như bước 1 (độ dài tính sau khi bỏ khoảng trắng hai đầu)
  4. Tên `ệ` × 32 (chữ dựng sẵn), rồi `😀` × 32 → như bước 1; `ệ` × 33, `😀` × 33 → như bước 2
  5. `curl -s <origin> <json> -d '{"username":"<a × 33>","password":"x"}' <api>/sessions` → 400, `{"code":"VALIDATION_ERROR","message":"Dữ liệu đăng nhập không hợp lệ","fields":{"username":"Tên đăng nhập tối đa 32 ký tự"}}` [evidence]
  6. Tên `İ` × 32 (chữ I hoa có chấm, U+0130; đổi chữ thường thành 2 code point mỗi ký tự) trên web và qua API → "Tên đăng nhập tối đa 32 ký tự" / 400 `VALIDATION_ERROR`, không có 500; `İ` × 16 → 401 bình thường [evidence]

## P0-AUT-008 Mật khẩu đăng nhập 128 và 129 ký tự
- Thiết kế: R-AUT-04 (độ dài theo code point; lỗi 400 không đếm vào R-AUT-06)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`; tên nhập `mio`
- Các bước:
  1. Mật khẩu `x` × 128 → không có lỗi theo trường; API 401, banner "Tên đăng nhập hoặc mật khẩu không đúng"
  2. Mật khẩu `x` × 129 → "Mật khẩu tối đa 128 ký tự" dưới ô, không gửi API [evidence]
  3. Mật khẩu `😀` × 128 (256 đơn vị UTF-16) → như bước 1; `😀` × 129 → như bước 2
  4. Gọi API với mật khẩu `x` × 129 → 400 `VALIDATION_ERROR`, `fields.password` "Mật khẩu tối đa 128 ký tự"
  5. `<psql> "select failed_count from login_throttles where username = 'mio'"` → `2` (chỉ hai lần 401 được đếm)

## P0-AUT-009 Tên đăng nhập được chuẩn hóa, mật khẩu giữ nguyên
- Thiết kế: R-AUT-07
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Tên `  MIO  `, mật khẩu `MioQuanLy#2026` → 201, vào `/` với "Huỳnh Mio" [evidence]
  2. Đăng xuất. Tên `Mio`, mật khẩu `miOQuanLy#2026` (khác hoa thường) → 401, banner "Tên đăng nhập hoặc mật khẩu không đúng"
  3. Tên `mio`, mật khẩu `MioQuanLy#2026 ` (thêm khoảng trắng cuối) → 401; ` MioQuanLy#2026` (khoảng trắng đầu) → 401
  4. `<psql> "select username, failed_count from login_throttles"` → đúng một dòng `mio | 3`

## P0-AUT-010 API đăng nhập: thiếu trường, sai kiểu
- Thiết kế: R-AUT-01 … R-AUT-04 (phần API)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. `curl -s <origin> <json> -d '{}' <api>/sessions` → 400, `{"code":"VALIDATION_ERROR","message":"Dữ liệu đăng nhập không hợp lệ","fields":{"username":"Nhập tên đăng nhập","password":"Nhập mật khẩu"}}` [evidence]
  2. Thân `{"username":123,"password":true}` → như bước 1
  3. Thân `{"username":null,"password":"x"}` → `fields` chỉ có `username` "Nhập tên đăng nhập"
  4. Thân `{"username":"mio","password":""}` → `fields` chỉ có `password` "Nhập mật khẩu"
  5. `<psql> "select count(*) from login_throttles"` → `0`

## P0-AUT-011 Thân request đăng nhập không phải JSON hoặc quá lớn
- Thiết kế: R-SKL-15 (qua `POST /api/v1/sessions`, `docs/design/api/sessions.md`)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. `curl -s <origin> <json> -d 'username=mio' <api>/sessions` → 400 `INVALID_JSON`, "Dữ liệu gửi lên không đúng định dạng JSON"
  2. Thân JSON 1,1 MB (`password` dài 1.100.000 ký tự) → 413 `PAYLOAD_TOO_LARGE`, "Dữ liệu gửi lên quá lớn"
  3. `<psql> "select count(*) from login_throttles"` → `0`

## P0-AUT-012 Sai mật khẩu và tên không tồn tại trả giống hệt nhau
- Thiết kế: R-AUT-05; mục Màn hình Đăng nhập (vùng thông báo)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Nhập `mio` / `sai-mat-khau`, bấm "Hiện" ở ô Mật khẩu, bấm "Đăng nhập" → banner danger "Tên đăng nhập hoặc mật khẩu không đúng" ngay sau ô Mật khẩu, trước nút "Đăng nhập"; ô Tên giữ `mio`; ô Mật khẩu trống và về trạng thái ẩn (nút "Hiện") [evidence]
  2. Nhập lại mật khẩu sai, gửi lần nữa → vẫn chỉ một banner trên form
  3. Nhập `khongco` / `sai-mat-khau` → banner y hệt bước 1
  4. `curl -s -i` cho hai trường hợp → cả hai 401, thân `{"code":"INVALID_CREDENTIALS","message":"Tên đăng nhập hoặc mật khẩu không đúng"}` giống hệt; không có `Set-Cookie` [evidence]

## P0-AUT-013 Thời gian phản hồi tên không tồn tại và sai mật khẩu tương đương
- Thiết kế: R-AUT-05
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. Lặp 10 vòng: `<psql> "delete from login_throttles"`, gửi `mio` / `sai-mat-khau` rồi `khongco` / `sai-mat-khau` bằng `curl -s -o /dev/null -w '%{http_code} %{time_total}\n'` → 20 kết quả đều `401`
  2. Tính trung vị thời gian của nhóm `mio` và nhóm `khongco` → chênh nhau không quá 20% [evidence]

## P0-AUT-014 Lần sai thứ 5 khóa tên đăng nhập 15 phút
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập, mở `/login`
- Các bước:
  1. Đăng nhập `mio` sai 4 lần → mỗi lần banner "Tên đăng nhập hoặc mật khẩu không đúng"; `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"` → `4`, rỗng
  2. Sai lần 5 → banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút."; response 429 `LOGIN_LOCKED`, header `Retry-After: 900` [evidence]
  3. Chạy lại SQL bước 1 → `failed_count` 0, `locked_until` ≈ now() + 15 phút (sai số 1 phút) [evidence]
  4. Nhập mật khẩu đúng `MioQuanLy#2026` → vẫn 429 cùng câu "Thử lại sau 15 phút.", ở lại `/login`, response không có `Set-Cookie` [evidence]

## P0-AUT-015 Đang khóa: không đếm thêm, không kéo dài khóa
- Thiết kế: R-AUT-06, R-AUT-30
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `mio` vừa bị khóa như P0-AUT-014; ghi lại `locked_until`
- Các bước:
  1. Gửi thêm 3 lần sai qua API → 3 × 429 `LOGIN_LOCKED`, `Retry-After` không tăng giữa các lần
  2. `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"` → `failed_count` 0, `locked_until` bằng đúng giá trị đã ghi lại
  3. `<log auth>` → mỗi lần ở bước 1 có đúng một dòng `auth.login.failed` mức warn, `"reason":"locked"`, có `lockedUntil`, không có `failedCount`; không có thêm dòng `auth.lock.started` [evidence]

## P0-AUT-016 Số phút còn lại làm tròn lên, tối thiểu 1
- Thiết kế: R-AUT-06
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `mio` đang bị khóa như P0-AUT-014; context mở `/login`
- Các bước:
  1. `<psql> "update login_throttles set locked_until = now() + interval '150 seconds' where username = 'mio'"`, gửi ngay đăng nhập trên web → banner "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 3 phút."; `Retry-After` trong 140–150 [evidence]
  2. Đặt `locked_until = now() + interval '30 seconds'`, gửi ngay → "Thử lại sau 1 phút."; `Retry-After` trong 20–30
  3. Đặt `locked_until = now() + interval '3 seconds'`, gửi ngay qua API → "Thử lại sau 1 phút."; `Retry-After` trong 1–3 (không bao giờ 0)

## P0-AUT-017 Hết khóa: đăng nhập lại được, bộ đếm bắt đầu từ 0
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai
- Khía cạnh: Thời gian
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `mio` đang bị khóa như P0-AUT-014
- Các bước:
  1. `<psql> "update login_throttles set locked_until = now() - interval '1 second' where username = 'mio'"`; đăng nhập đúng → 201, vào app [evidence]
  2. `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"` → không còn dòng, hoặc `0` và rỗng
  3. Khóa lại bằng 5 lần sai, đặt `locked_until = now() - interval '1 second'`; gửi 1 lần sai → 401 (không phải 429)
  4. SQL bước 2 → `failed_count` 1, `locked_until` rỗng, `window_started_at` ≈ now() [evidence]

## P0-AUT-018 Cửa sổ đếm 15 phút
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai (bước 2)
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. Sai 4 lần với `mio`; `<psql> "update login_throttles set window_started_at = now() - interval '15 minutes 5 seconds' where username = 'mio'"`; sai lần 5 → 401 (không khóa); `failed_count` 1, `window_started_at` ≈ now() [evidence]
  2. Xóa bộ đếm; sai 4 lần; đặt `window_started_at = now() - interval '14 minutes 50 seconds'`; sai lần 5 ngay → 429, khóa 15 phút [evidence]

## P0-AUT-019 Đăng nhập đúng xóa bộ đếm
- Thiết kế: R-AUT-06
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. Sai 4 lần với `mio` → `failed_count` 4
  2. Đăng nhập đúng → 201; dòng `mio` không còn, hoặc `failed_count` 0
  3. Sai 4 lần nữa → cả 4 lần 401; lần 5 → 429

## P0-AUT-020 Giới hạn áp cả tên đăng nhập không tồn tại
- Thiết kế: R-AUT-06, R-AUT-05, R-AUT-30
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không có tài khoản `khongco`
- Các bước:
  1. Đăng nhập `khongco` sai 5 lần trên web → 4 lần banner "Tên đăng nhập hoặc mật khẩu không đúng", lần 5 banner "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." như tài khoản thật [evidence]
  2. `<psql> "select locked_until - now() from login_throttles where username = 'khongco'"` → ≈ 15 phút
  3. `<log auth>` → 5 dòng `auth.login.failed` có `"username":"khongco"`, `"userExists":false`, `"reason":"invalid_credentials"`, 4 dòng đầu có `failedCount` 1 … 4, dòng thứ 5 có `failedCount` 5 và `lockedUntil`; một dòng `auth.lock.started` `"source":"login"`, `"userExists":false`, cùng `requestId` với dòng `failed` thứ 5 [evidence]

## P0-AUT-021 Khóa đăng nhập không ảnh hưởng phiên đang có
- Thiết kế: R-AUT-06 (phiên đang có không bị ảnh hưởng)
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context A đã đăng nhập `mio` trên web
- Các bước:
  1. Context B: đăng nhập `mio` sai 5 lần → khóa
  2. Context A tải lại `/` → vẫn trong app, `GET /api/v1/sessions/current` 200 [evidence]

## P0-AUT-022 Bộ đếm tính theo tên đã chuẩn hóa
- Thiết kế: R-AUT-06, R-AUT-07
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. Gửi sai lần lượt với `mio`, `MIO`, ` Mio`, `mIo `, `MiO` → 4 lần đầu 401, lần 5 → 429 [evidence]
  2. `<psql> "select username from login_throttles"` → đúng một dòng `mio`

## P0-AUT-023 Nhiều lần đăng nhập sai gửi đồng thời
- Thiết kế: R-AUT-06 (đồng thời: kiểm lại khóa trong transaction, không đếm khi đang khóa, không kéo dài khóa)
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. Gửi song song 10 request `mio` / `sai-mat-khau` (`seq 10 | xargs -P 10 -I{} curl -s -o /dev/null -w '%{http_code}\n' …`) → mỗi request 401 hoặc 429, không có 500
  2. Đếm mã trả về → đúng 4 × 401 và 6 × 429 (lần sai được tính tối đa 5; lần thứ 5 làm khóa, 5 request còn lại gặp khóa) [evidence]
  3. `<log auth>` → đúng một dòng `auth.lock.started` cho `mio`; 10 dòng `auth.login.failed`: 5 dòng `invalid_credentials` (`failedCount` 1 … 5), 5 dòng `locked` [evidence]
  4. `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"` → `failed_count` 0, `locked_until` ≈ now() + 15 phút; ghi lại
  5. Gửi song song thêm 5 request (có 1 request đúng mật khẩu) → tất cả 429; `locked_until` bằng giá trị đã ghi lại

## P0-AUT-024 Cookie phiên đúng thuộc tính, token chỉ lưu dạng băm
- Thiết kế: R-AUT-09
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `PUBLIC_URL` là `http://localhost:3000`
- Các bước:
  1. `<đăng nhập mio>` → 201; `Set-Cookie: mio_session=<token>` có `HttpOnly`, `SameSite=Lax`, `Path=/`, `Max-Age` trong 7775990–7776000; không có `Secure` [evidence]
  2. `<token>` dài 43 ký tự, chỉ gồm `A–Z`, `a–z`, `0–9`, `-`, `_`
  3. `printf '%s' '<token>' | sha256sum` → bằng `token_hash` của phiên mới nhất (`<psql> "select token_hash from user_sessions order by created_at desc limit 1"`) [evidence]
  4. `docker compose exec -T postgres pg_dump -U mio mio | grep -c '<token>'` → `0`
  5. Đăng nhập trên web, chạy `document.cookie` trong trang → không chứa `mio_session`

## P0-AUT-025 Cookie có `Secure` khi `PUBLIC_URL` là https
- Thiết kế: R-AUT-09
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: sao lưu `.env`
- Các bước:
  1. Đặt `MIO_PUBLIC_URL=https://localhost:3000`, `docker compose up -d api`, chờ `healthy`
  2. `curl -s -i <json> -H 'Origin: https://localhost:3000' -d '{"username":"mio","password":"MioQuanLy#2026"}' <api>/sessions` → 201, `Set-Cookie` có `Secure` [evidence]
  3. `DELETE <api>/sessions/current` với cookie vừa nhận, cùng `Origin` → 204, `Set-Cookie` xóa cookie cũng có `Secure`
  4. Trả lại `.env`, `docker compose up -d api`; `<đăng nhập mio>` → `Set-Cookie` không có `Secure`

## P0-AUT-026 Một tài khoản đăng nhập trên nhiều thiết bị
- Thiết kế: R-AUT-09, R-AUT-12
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`
- Các bước:
  1. Context A và B cùng đăng nhập `mio` trên web → `<psql> "select count(*) from user_sessions where user_id = <id mio>"` → `2`
  2. Context A bấm "Đăng xuất" → đếm còn `1`; context B tải lại → vẫn trong app [evidence]

## P0-AUT-027 Gia hạn phiên trượt sau 24 giờ
- Thiết kế: R-AUT-10
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; `<đăng nhập mio>`
- Các bước:
  1. `<psql> "update user_sessions set updated_at = now() - interval '23 hours 59 minutes', expires_at = now() + interval '89 days'"`; `curl -s -i -b mio.jar <api>/sessions/current` → 200, không có `Set-Cookie`; `expires_at`, `updated_at` giữ nguyên giá trị vừa đặt [evidence]
  2. Đặt `updated_at = now() - interval '24 hours 1 minute'`, `expires_at = now() + interval '89 days'`; gọi lại → 200 kèm `Set-Cookie` cùng token, `Max-Age` trong 7775990–7776000; `expires_at` ≈ now() + 90 ngày, `updated_at` ≈ now() [evidence]
  3. Gọi lại ngay → 200, không có `Set-Cookie`

## P0-AUT-028 Phiên hết hạn
- Thiết kế: R-AUT-11, R-AUT-28; mục Trạng thái › Phiên
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; web đăng nhập `mio`, đang ở `/`
- Các bước:
  1. `<psql> "update user_sessions set expires_at = now() - interval '1 second' where user_id = <id mio>"`
  2. Tải lại trang → chuyển `/login?next=%2F`, banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" (câu hỏi mở 8) [evidence]
  3. Response `GET /api/v1/sessions/current` → 401, `{"code":"UNAUTHENTICATED","message":"Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn"}`, `Set-Cookie: mio_session=; Max-Age=0` [evidence]
  4. `<psql> "select count(*) from user_sessions where user_id = <id mio>"` → `0`
  5. `<đăng nhập mio>`; đặt `expires_at = now() + interval '5 seconds'`; `curl -b mio.jar <api>/sessions/current` ngay → 200; chờ 6 giây, gọi lại → 401

## P0-AUT-029 Không có cookie hoặc cookie bị sửa
- Thiết kế: R-AUT-11
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`
- Các bước:
  1. `curl -s -i <api>/sessions/current` không cookie → 401 `UNAUTHENTICATED`, không có `Set-Cookie`
  2. `-H 'Cookie: mio_session=abc'` → 401, `Set-Cookie` xóa cookie (`Max-Age=0`) [evidence]
  3. Token hợp lệ trong `mio.jar` đổi ký tự cuối → như bước 2
  4. Web đang đăng nhập: sửa giá trị cookie `mio_session` trong context, tải lại → `/login?next=%2F` kèm banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại"; cookie `mio_session` không còn trong context [evidence]
  5. Tải lại `/login?next=%2F` lần nữa (giờ không còn cookie) → không còn banner

## P0-AUT-030 Mất cookie giữa chừng khi đang đổi mật khẩu
- Thiết kế: R-AUT-31, R-AUT-28
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, mở `/account/password`; ghi lại `password_hash` của `mio`
- Các bước:
  1. Nhập Mật khẩu hiện tại `MioQuanLy#2026`, Mật khẩu mới và Nhập lại `MioMoi#2026x`
  2. Xóa cookie của context (`context.clearCookies()`)
  3. Bấm "Đổi mật khẩu", trong hộp thoại bấm "Đổi và đăng xuất thiết bị khác" → API 401; chuyển `/login?next=%2Faccount%2Fpassword`, banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" [evidence]
  4. `password_hash` của `mio` không đổi; đăng nhập `MioQuanLy#2026` → vào `/account/password`, form trống

## P0-AUT-031 Dùng lại cookie cũ sau khi đăng xuất
- Thiết kế: R-AUT-12; mục Trạng thái › Phiên (chuyển không hợp lệ)
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`; sao chép `mio.jar` thành `old.jar`
- Các bước:
  1. `curl -s -i -X DELETE -b mio.jar <origin> <api>/sessions/current` → 204
  2. `curl -s -i -b old.jar <api>/sessions/current` → 401 `UNAUTHENTICATED`, `Set-Cookie` xóa cookie [evidence]
  3. `curl -s -i -b old.jar <origin> <json> -d '{"currentPassword":"MioQuanLy#2026","newPassword":"MioMoi#2026x","signOutOtherDevices":true}' <api>/users/me/change-password` → 401; mật khẩu không đổi

## P0-AUT-032 Đăng nhập thành công dọn phiên hết hạn
- Thiết kế: R-AUT-13
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `mio`, `ngocanh.nail` đều có một phiên còn hạn (`<đăng nhập mio>`, `<đăng nhập ngocanh>`)
- Các bước:
  1. `<psql> "insert into user_sessions (user_id, token_hash, expires_at) select id, md5(random()::text), now() - interval '1 day' from users"` → mỗi tài khoản thêm một phiên hết hạn
  2. Đăng nhập sai `ngocanh.nail` 1 lần → `<psql> "select count(*) from user_sessions where expires_at <= now()"` vẫn ≥ 2 (đăng nhập sai không dọn phiên)
  3. Đăng nhập đúng `ngocanh.nail` → đếm phiên hết hạn → `0` (cả phiên của `mio`); hai phiên còn hạn ban đầu vẫn còn [evidence]

## P0-AUT-033 Dọn bộ đếm đăng nhập sai đã cũ
- Thiết kế: R-AUT-13
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. Chèn bốn dòng (`window_started_at` = `updated_at`):
     - `a1`: `failed_count` 2, `updated_at` now() − 25 giờ;
     - `a2`: `failed_count` 2, `updated_at` now() − 23 giờ;
     - `a3`: `failed_count` 0, `locked_until` now() + 5 phút, `updated_at` now() − 25 giờ;
     - `a4`: `failed_count` 0, `locked_until` now() − 1 giờ, `updated_at` now() − 25 giờ.
  2. Gửi đăng nhập sai cho `khac` → 401
  3. `<psql> "select username from login_throttles order by username"` → `a2`, `a3`, `khac`; không còn `a1`, `a4` [evidence]

## P0-AUT-034 Đăng xuất từ thanh điều hướng
- Thiết kế: R-AUT-32, R-AUT-12, R-AUT-30
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; web đăng nhập `mio`, ở `/`
- Các bước:
  1. Bấm "Đăng xuất" → `DELETE /api/v1/sessions/current` 204; chuyển `/login`, banner info "Bạn đã đăng xuất" [evidence]
  2. `<psql> "select count(*) from user_sessions where user_id = <id mio>"` → `0`; context không còn cookie `mio_session`; `localStorage.getItem('mio.hadSession')` → `null`
  3. Bấm Back → không hiện nội dung app; chuyển `/login?next=%2F`, form trống, không có banner "Phiên đăng nhập đã kết thúc…" (cookie đã bị xóa khi đăng xuất) [evidence]
  4. `<log auth>` → dòng `auth.logout` có `userId` của `mio`

## P0-AUT-035 Đăng xuất qua API là idempotent
- Thiết kế: R-AUT-12, R-AUT-18
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. `curl -s -i -X DELETE <origin> <api>/sessions/current` không cookie → 204, `Set-Cookie: mio_session=; Max-Age=0`
  2. `<đăng nhập mio>`, đặt `expires_at = now() - interval '1 second'`; DELETE với `mio.jar` → 204, xóa cookie; phiên không còn trong DB
  3. `<đăng nhập mio>`; DELETE hai lần với cùng `mio.jar` (không ghi lại jar) → cả hai 204
  4. Mọi response ở bước 1–3 có `Cache-Control: no-store`

## P0-AUT-036 Đăng xuất khi máy chủ lỗi hoặc mất kết nối
- Thiết kế: R-AUT-32
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/`
- Các bước:
  1. `docker compose stop postgres`; bấm "Đăng xuất" → DELETE trả 500; vẫn chuyển `/login`, form Đăng nhập hiện ra, không có banner "Bạn đã đăng xuất", không có màn hình lỗi [evidence]
  2. `docker compose start postgres`, chờ api `healthy`; mở `/` → vào lại app (phiên và cookie còn, chấp nhận theo thiết kế)
  3. `docker compose stop api`; bấm "Đăng xuất" → vẫn chuyển `/login`, không có banner "Bạn đã đăng xuất"; `docker compose start api`

## P0-AUT-037 Chưa đăng nhập mở đường dẫn bên trong rồi quay lại đúng trang
- Thiết kế: R-AUT-28
- Khía cạnh: Phân quyền
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập
- Các bước:
  1. Mở `/account/password?tu=link` → chuyển `/login?next=%2Faccount%2Fpassword%3Ftu%3Dlink`, không có banner (chưa từng đăng nhập, không có cookie) [evidence]
  2. Đăng nhập `mio` → chuyển `/account/password?tu=link`, trang Đổi mật khẩu [evidence]

## P0-AUT-038 Tham số `next` không an toàn bị bỏ qua
- Thiết kế: R-AUT-28
- Khía cạnh: Phân quyền
- Kỹ thuật: bảng quyết định
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context chưa đăng nhập; giữa các bước bấm "Đăng xuất"
- Các bước:
  1. Mở `/login?next=%2F%2Fevil.example` (`//evil.example`), đăng nhập `mio` → chuyển `http://localhost:3000/`, không rời khỏi app [evidence]
  2. `next=%2F%5Cevil.example` (`/\evil.example`) → `/` [evidence]
  3. `next=https%3A%2F%2Fevil.example` → `/`
  4. `next=evil` (không bắt đầu bằng `/`) → `/`
  5. `next=%2Flogin` → `/`
  6. `next=%2Fkhong-co` → `/khong-co`, màn hình Không tìm thấy trang (đường dẫn hợp lệ dù không có trang)
  7. Không có `next` → `/`
  8. `next=%2F%09%2Fevil.example` (`/` + tab + `/evil.example`), `next=%2F%0A%2Fevil.example` (xuống dòng) → `/`, không rời app [evidence]

## P0-AUT-039 Đã đăng nhập mà mở trang Đăng nhập
- Thiết kế: R-AUT-28
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`
- Các bước:
  1. Gõ `/login` → chuyển `/`, không hiện form Đăng nhập
  2. Gõ `/login?next=%2Faccount%2Fpassword` → chuyển `/`
  3. Từ `/` bấm Back về lịch sử `/login` → lại chuyển `/`

## P0-AUT-040 Quyền của route API khi chưa đăng nhập
- Thiết kế: R-AUT-14, R-AUT-16, R-SKL-14
- Khía cạnh: Phân quyền
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không có cookie
- Các bước:
  1. Gọi mọi operation trong `docs/design/api/openapi.yaml` không kèm cookie, có `<origin>`, thân hợp lệ nếu cần → trả 401 `UNAUTHENTICATED`, trừ ba route công khai `GET /api/v1/health` (200), `POST /api/v1/sessions` (201 với `mio`), `DELETE /api/v1/sessions/current` (204) [evidence]
  2. `GET <api>/khong-co`, `POST <api>/khong-co` → 404 `NOT_FOUND`, "Không tìm thấy địa chỉ yêu cầu" (không phải 401)
  3. `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/` và một file trong `/assets/` → `200`, không cần cookie

## P0-AUT-041 Thợ mở thẳng trang chỉ dành cho Quản lý
- Thiết kế: R-AUT-29; mục Màn hình Không có quyền
- Khía cạnh: Phân quyền
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-settings` (`/settings`) và `emergency-stop` (`/system-log`); web đăng nhập `ngocanh.nail`
- Các bước:
  1. Gõ `/settings` → trong khung app: tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý.", nút "Về Trang chính"; địa chỉ vẫn `/settings`; không mục điều hướng nào được chọn [evidence]
  2. Gõ `/system-log` và một trang con của Cài đặt (ví dụ `/settings/groups`) → như bước 1
  3. Bấm "Về Trang chính" → `/`

## P0-AUT-042 Thợ gọi thẳng API chỉ dành cho Quản lý
- Thiết kế: R-AUT-15, R-AUT-16
- Khía cạnh: Phân quyền
- Kỹ thuật: bảng quyết định
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: có ít nhất một endpoint chỉ Quản lý (của `group-settings` hoặc `crawl-settings`, ví dụ `GET`/`PUT /api/v1/settings/<khóa>`); `<đăng nhập ngocanh>`, `<đăng nhập mio>`
- Các bước:
  1. Thợ `GET` endpoint đó → 403, `{"code":"FORBIDDEN","message":"Bạn không có quyền thực hiện thao tác này"}` [evidence]
  2. Thợ `PUT`/`POST` có `<origin>` với thân sai quy tắc → 403 `FORBIDDEN` (không phải 400, vì kiểm vai trò trước kiểm dữ liệu)
  3. Thợ `PUT`/`POST` với thân hợp lệ → 403; dữ liệu trong DB không đổi [evidence]
  4. Quản lý gọi như bước 1 → 200

## P0-AUT-043 Thanh điều hướng của Quản lý đủ mục
- Thiết kế: R-AUT-29; mục Khung app
- Khía cạnh: Hiển thị
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-AUT-041; web đăng nhập `mio`
- Các bước:
  1. Xem thanh điều hướng → "Trang chính", đường kẻ, "Cài đặt", "Nhật ký hệ thống", rồi khối tài khoản [evidence]
  2. Bấm "Cài đặt" → `/settings`, mục "Cài đặt" đang chọn (`aria-current="page"`)
  3. Đăng nhập `ngocanh.nail` ở context khác → chỉ thấy "Trang chính"

## P0-AUT-044 API trả 403 khi đang thao tác
- Thiết kế: R-AUT-29; `ui-style.md` mục "Vị trí thông báo"
- Khía cạnh: Phân quyền
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-AUT-042; web đăng nhập `mio`, mở một màn hình Cài đặt có form và nút lưu
- Các bước:
  1. `<psql> "update users set role = 'technician' where username = 'mio'"` (không tải lại trang)
  2. Sửa một trường, bấm nút lưu → API 403; banner danger "Bạn không có quyền thực hiện thao tác này" ở vùng thông báo ngay trên hàng nút của form, không phải toast; dữ liệu trên form giữ nguyên [evidence]
  3. Ngay sau đó (không tải lại): thanh điều hướng chỉ còn "Trang chính", khối tài khoản có badge "Thợ"; vùng nội dung chuyển sang màn hình Không có quyền, đường dẫn giữ nguyên [evidence]
  4. Nếu đã có thao tác không có form chỉ dành cho Quản lý (nút trong danh sách, công tắc): làm lại bước 1, bấm thao tác đó → toast danger cùng câu ở góc dưới phải, không tự ẩn, có nút "Đóng"; bấm "Đóng" → toast biến mất. Chưa có thì ghi `không áp dụng` cho bước này
  5. Đặt lại `role = 'manager'`

## P0-AUT-045 Thứ tự kiểm tra: Origin → phiên → dữ liệu
- Thiết kế: R-AUT-15 (thứ tự kiểm tra), R-AUT-17, R-AUT-11, R-SKL-15
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: bảng quyết định
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`
- Các bước (đều gọi `POST <api>/users/me/change-password` với thân `{}`):
  1. `Origin: http://evil.example`, không cookie → 403 `INVALID_ORIGIN` [evidence]
  2. `<origin>`, không cookie → 401 `UNAUTHENTICATED`
  3. `<origin>`, cookie `mio.jar` → 400 `VALIDATION_ERROR`, "Dữ liệu đổi mật khẩu không hợp lệ", `fields` = `{"currentPassword":"Nhập mật khẩu hiện tại","newPassword":"Nhập mật khẩu mới","signOutOtherDevices":"Chọn có đăng xuất các thiết bị khác hay không"}` [evidence]
  4. Không có header `Origin`, cookie `mio.jar` → như bước 3
  5. Phần vai trò → dữ liệu: xem P0-AUT-042 bước 2
  6. `Origin: http://evil.example`, không cookie, thân `{"currentPassword":` (JSON hỏng) → 403 `INVALID_ORIGIN` (kiểm Origin trước khi đọc thân) [evidence]
  7. `<origin>`, không cookie, thân JSON hỏng → 400 `INVALID_JSON` (đọc thân trước khi kiểm phiên)

## P0-AUT-046 Chống CSRF: so origin của request ghi
- Thiết kế: R-AUT-17
- Khía cạnh: Phân quyền
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước (bước 1–3 gọi `POST <api>/sessions` với thân đăng nhập đúng của `mio`):
  1. `Origin: http://evil.example` → 403, `{"code":"INVALID_ORIGIN","message":"Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000"}`; không có `Set-Cookie`, không tạo phiên [evidence]
  2. `Origin: http://localhost:3001` (khác cổng), `https://localhost:3000` (khác scheme), `http://127.0.0.1:3000` (khác host) → đều 403 `INVALID_ORIGIN`
  3. `Origin: http://localhost:3000` → 201; không có header `Origin` → 201
  4. `DELETE <api>/sessions/current` với cookie hợp lệ và `Origin: http://evil.example` → 403; phiên vẫn còn trong DB
  5. `GET <api>/sessions/current` với cookie hợp lệ và `Origin: http://evil.example` → 200 (GET không kiểm)
  6. `<psql> "select count(*) from login_throttles"` → `0` (request bị chặn ở bước 1–2 không được đếm)

## P0-AUT-047 Mở app bằng địa chỉ khác `PUBLIC_URL`
- Thiết kế: R-AUT-17; mục Màn hình Đăng nhập (vùng thông báo)
- Khía cạnh: Phân quyền
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `PUBLIC_URL` là `http://localhost:3000`
- Các bước:
  1. Mở `http://127.0.0.1:3000/login`, đăng nhập `mio` đúng mật khẩu → banner danger "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000"; ô Tên giữ `mio`, ô Mật khẩu bị xóa [evidence]
  2. `<psql> "select count(*) from user_sessions where created_at > now() - interval '1 minute'"` → `0`

## P0-AUT-048 Đăng nhập qua Vite dev server
- Thiết kế: mục `apps/web` (Dev: Vite proxy đặt lại `Origin`), R-AUT-17, R-AUT-32
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: api chạy ở cổng 3000; `pnpm --filter @mio/web dev` (cổng do Vite in ra, mặc định 5173)
- Các bước:
  1. Mở `http://localhost:5173/login`, đăng nhập `mio` → vào `/`, không có banner `INVALID_ORIGIN` [evidence]
  2. Bấm "Đăng xuất" → `/login`, banner "Bạn đã đăng xuất"

## P0-AUT-049 Header bảo mật và chặn nhúng khung
- Thiết kế: R-AUT-18
- Khía cạnh: Phân quyền
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`
- Các bước:
  1. `curl -s -D -` tới `/`, `/assets/<một file>`, `<api>/health`, `<api>/khong-co`, `POST <api>/sessions` sai mật khẩu → mọi response có `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin` [evidence]
  2. Response của `POST <api>/sessions` (201, 400, 401, 429), `GET`/`DELETE <api>/sessions/current` (200, 401, 204), `POST <api>/users/me/change-password` (204, 400) → đều có `Cache-Control: no-store`
  3. Mở bằng Playwright một file HTML cục bộ chứa `<iframe src="http://localhost:3000/login">` → khung không hiển thị trang Đăng nhập; console báo bị chặn do `X-Frame-Options` [evidence]

## P0-AUT-050 Đổi mật khẩu và đăng xuất các thiết bị khác
- Thiết kế: R-AUT-23, R-AUT-34, R-AUT-31, R-AUT-30; mục Màn hình Đổi mật khẩu
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; context A và B đăng nhập `mio`, B đang ở `/account/password`; ghi lại `password_hash` và cookie của A
- Các bước:
  1. A bấm "Đổi mật khẩu" ở khối tài khoản → `/account/password`, mục "Đổi mật khẩu" đang chọn; ba ô trống, dưới ô Mật khẩu mới có gợi ý "Ít nhất 8 ký tự" [evidence]
  2. Nhập `MioQuanLy#2026`, `MioMoi#2026x`, `MioMoi#2026x`, bấm "Đổi mật khẩu" → hộp thoại tiêu đề "Đổi mật khẩu", nội dung "Bạn có muốn đăng xuất khỏi các thiết bị khác đang đăng nhập tài khoản này không? Nên chọn đăng xuất nếu bạn nghi có người khác biết mật khẩu cũ.", ba nút "Đổi và đăng xuất thiết bị khác", "Chỉ đổi mật khẩu", "Hủy"; nút đầu đang được focus [evidence]
  3. Bấm "Đổi và đăng xuất thiết bị khác" → request có `"signOutOtherDevices":true`, response 204 kèm `Set-Cookie` mới; hộp thoại đóng, ba ô trống, ở lại trang, toast success "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất." [evidence]
  4. DB: `password_hash` khác giá trị cũ; `user_sessions` của `mio` còn đúng 1 dòng, `token_hash` = SHA-256 của cookie mới của A; cookie cũ của A gọi `GET <api>/sessions/current` → 401 [evidence]
  5. A tải lại → vẫn trong app
  6. B nhập form hợp lệ, gửi qua hộp thoại → 401; chuyển `/login?next=%2Faccount%2Fpassword`, banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" [evidence]
  7. Đăng nhập `mio` bằng `MioQuanLy#2026` → 401; bằng `MioMoi#2026x` → 201
  8. `<log auth>` → dòng `auth.password.changed` có `userId`, `"signedOutOtherDevices":true`
  9. Đặt lại mật khẩu `mio` về `MioQuanLy#2026`

## P0-AUT-051 Chỉ đổi mật khẩu, giữ phiên thiết bị khác
- Thiết kế: R-AUT-23, R-AUT-34
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-AUT-050; ghi lại `token_hash`, `expires_at` phiên của B
- Các bước:
  1. A làm như P0-AUT-050 bước 2, bấm "Chỉ đổi mật khẩu" → request có `"signOutOtherDevices":false`, 204; toast "Đã đổi mật khẩu." [evidence]
  2. DB: phiên của B còn nguyên `token_hash`, `expires_at`; phiên cũ của A được thay bằng phiên mới (tổng vẫn 2)
  3. B tải lại → vẫn trong app [evidence]
  4. `<log auth>` → `auth.password.changed` có `"signedOutOtherDevices":false`. Đặt lại mật khẩu

## P0-AUT-052 Hủy hộp thoại xác nhận không gửi gì
- Thiết kế: R-AUT-34; mục Màn hình Đổi mật khẩu
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`, ba ô đã nhập hợp lệ; ghi lại `password_hash`
- Các bước:
  1. Bấm "Đổi mật khẩu" → hộp thoại; nhấn Esc → hộp thoại đóng, ba ô giữ nguyên giá trị; tab Network không có request `change-password`
  2. Mở lại, bấm ra ngoài hộp thoại → như bước 1
  3. Mở lại, bấm "Hủy" → như bước 1 [evidence]
  4. `password_hash` không đổi

## P0-AUT-053 Đang gửi: khóa nút, không đóng được, bấm nhiều lần chỉ gửi một lần
- Thiết kế: mục Màn hình Đăng nhập (nút đang gửi), mục Màn hình Đổi mật khẩu (loading)
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: giả lập mạng chậm 3 giây; `<psql> "delete from user_sessions"`
- Các bước:
  1. Ở `/login`, nhập `mio` đúng, bấm "Đăng nhập" ba lần thật nhanh → nút đổi thành "Đang đăng nhập…" có vòng xoay, không bấm được [evidence]
  2. Chờ xong → vào `/`; tab Network chỉ có 1 request `POST /api/v1/sessions`; DB có đúng 1 phiên của `mio`
  3. Ở `/account/password` nhập form hợp lệ, mở hộp thoại, bấm "Đổi và đăng xuất thiết bị khác" → nút đó "Đang lưu…", "Chỉ đổi mật khẩu" và "Hủy" không bấm được [evidence]
  4. Trong lúc chờ: bấm lại nút, nhấn Esc, bấm ra ngoài → hộp thoại vẫn mở, không có request thứ hai
  5. Chờ xong → toast success; tab Network chỉ có 1 request `change-password`. Tắt giả lập, đặt lại mật khẩu

## P0-AUT-054 Màn hình Đổi mật khẩu, Không có quyền, Không tìm thấy khớp mockup
- Thiết kế: mục Màn hình Đổi mật khẩu, Không có quyền, Không tìm thấy trang; mockup `change-password/`, `forbidden/`, `not-found/`
- Khía cạnh: Hiển thị
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: người
- Tiền điều kiện: đã có ảnh evidence của P0-AUT-041, 050, 051, 052, 053, 055, 056, 058, 060, 061, 063, 072, 078
- Các bước:
  1. So ảnh với `docs/design/ui/change-password/screenshots/` cùng trạng thái → bố cục, chữ, lỗi dưới ô, banner ngay sau ô Nhập lại mật khẩu mới và trước nút "Đổi mật khẩu", toast ở góc dưới phải khớp [evidence]
  2. So P0-AUT-041 với `forbidden/screenshots/`, P0-AUT-078 với `not-found/screenshots/` → khớp

## P0-AUT-055 Bỏ trống cả ba ô đổi mật khẩu
- Thiết kế: R-AUT-19, R-AUT-21, R-AUT-22
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`
- Các bước:
  1. Bấm "Đổi mật khẩu" khi ba ô trống → "Nhập mật khẩu hiện tại", "Nhập mật khẩu mới", "Nhập lại mật khẩu mới" dưới từng ô; không mở hộp thoại; không có request [evidence]
  2. Ba ô đều có nút Hiện/Ẩn riêng: bấm "Hiện" ở ô Mật khẩu mới → chỉ ô đó hiện ký tự

## P0-AUT-056 Độ dài mật khẩu mới
- Thiết kế: R-AUT-21 (độ dài theo code point, sai kiểu)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`. Sau mỗi lần đổi thành công, lần sau dùng mật khẩu vừa đặt làm Mật khẩu hiện tại; ô Nhập lại luôn giống Mật khẩu mới
- Các bước:
  1. Mật khẩu mới `Abcd#12` (7 ký tự) → "Mật khẩu mới phải từ 8 đến 128 ký tự" dưới ô, không mở hộp thoại [evidence]
  2. `Abcd#123` (8) → mở hộp thoại; bấm "Chỉ đổi mật khẩu" → toast "Đã đổi mật khẩu."
  3. `x` × 128 → đổi thành công; `y` × 129 → lỗi như bước 1
  4. `😀` × 8 → đổi thành công; `😀` × 7 (14 đơn vị UTF-16) → lỗi như bước 1
  5. API: `newPassword` 7 ký tự, các trường khác hợp lệ → 400, `message` "Dữ liệu đổi mật khẩu không hợp lệ", `fields.newPassword` "Mật khẩu mới phải từ 8 đến 128 ký tự"
  6. API: `newPassword` là số `12345678`, rồi `null` → mỗi lần 400, `fields.newPassword` "Nhập mật khẩu mới"
  7. Đặt lại mật khẩu `mio`

## P0-AUT-057 Mật khẩu hiện tại quá dài hoặc trống
- Thiết kế: R-AUT-19
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`
- Các bước:
  1. Mật khẩu hiện tại `x` × 129, hai ô kia hợp lệ → "Mật khẩu tối đa 128 ký tự" dưới ô Mật khẩu hiện tại, không mở hộp thoại
  2. `x` × 128 → mở hộp thoại; gửi → "Mật khẩu hiện tại không đúng"
  3. API: `currentPassword` `""` → `fields.currentPassword` "Nhập mật khẩu hiện tại"; `currentPassword` là số `123` → cùng thông báo

## P0-AUT-058 Mật khẩu mới trùng tên đăng nhập
- Thiết kế: R-AUT-21
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `ngocanh.nail`, ở `/account/password`; Mật khẩu hiện tại `NgocAnh#2026`
- Các bước:
  1. Mật khẩu mới và Nhập lại `NgocAnh.Nail` → "Mật khẩu không được trùng tên đăng nhập" dưới ô Mật khẩu mới, không mở hộp thoại [evidence]
  2. `ngocanh.nail` → cùng lỗi
  3. `ngocanh.nail1` → không có lỗi, mở hộp thoại; bấm "Hủy"
  4. API: `newPassword` `NGOCANH.NAIL` → 400, `fields.newPassword` "Mật khẩu không được trùng tên đăng nhập"

## P0-AUT-059 Nhập lại mật khẩu mới trống hoặc không khớp
- Thiết kế: R-AUT-22
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`; Mật khẩu hiện tại đúng, Mật khẩu mới `MioMoi#2026x`
- Các bước:
  1. Nhập lại để trống → "Nhập lại mật khẩu mới", không mở hộp thoại
  2. Nhập lại `MioMoi#2026X` (khác một chữ hoa) → "Mật khẩu nhập lại không khớp" [evidence]
  3. Nhập lại `MioMoi#2026x ` (thừa khoảng trắng cuối) → "Mật khẩu nhập lại không khớp"

## P0-AUT-060 Mật khẩu hiện tại không đúng
- Thiết kế: R-AUT-20, R-AUT-30
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`; không có dòng `login_throttles`
- Các bước:
  1. Mật khẩu hiện tại `sai-mat-khau`, Mật khẩu mới và Nhập lại `MioMoi#2026x`, gửi qua hộp thoại → hộp thoại đóng; dưới ô Mật khẩu hiện tại "Mật khẩu hiện tại không đúng"; ba ô giữ dữ liệu [evidence]
  2. Response → 400, `{"code":"VALIDATION_ERROR","message":"Dữ liệu đổi mật khẩu không hợp lệ","fields":{"currentPassword":"Mật khẩu hiện tại không đúng"}}`
  3. DB: dòng `mio` trong `login_throttles` có `failed_count` 1; `password_hash` không đổi; tải lại trang → vẫn trong app
  4. `<log auth>` → `auth.password.change_failed` mức warn, `userId`, `"username":"mio"`, `"reason":"current_password_incorrect"`, `"failedCount":1` [evidence]

## P0-AUT-061 Mật khẩu mới giống mật khẩu hiện tại
- Thiết kế: R-AUT-21
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`; không có dòng `login_throttles`
- Các bước:
  1. Cả ba ô `MioQuanLy#2026` → web mở hộp thoại; gửi → hộp thoại đóng, dưới ô Mật khẩu mới "Mật khẩu mới phải khác mật khẩu hiện tại" [evidence]
  2. DB: không có dòng `mio` trong `login_throttles`; `password_hash` và phiên không đổi

## P0-AUT-062 Thứ tự kiểm tra khi đổi mật khẩu
- Thiết kế: R-AUT-21 (thứ tự), R-AUT-20
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: bảng quyết định
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`; không có dòng `login_throttles`; mọi bước gọi `POST <api>/users/me/change-password` với `<origin>`, cookie `mio.jar`
- Các bước:
  1. `currentPassword` sai, `newPassword` `abc`, thiếu `signOutOtherDevices` → 400 có `fields.newPassword` "Mật khẩu mới phải từ 8 đến 128 ký tự" và `fields.signOutOtherDevices` cùng lúc, không có `fields.currentPassword`; không có dòng `mio` trong `login_throttles` [evidence]
  2. `<psql> "insert into login_throttles (username, failed_count, window_started_at, locked_until) values ('mio', 0, now(), now() + interval '10 minutes')"`; gửi `newPassword` `abc` → 400 lỗi hình thức như bước 1 (kiểm hình thức trước khóa)
  3. Đang khóa, dữ liệu hợp lệ với `currentPassword` đúng → 429 `LOGIN_LOCKED` "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 10 phút.", `Retry-After` trong 590–600; `password_hash` không đổi [evidence]
  4. Xóa khóa; `currentPassword` sai và `newPassword` cũng là chuỗi sai đó → chỉ `fields.currentPassword` "Mật khẩu hiện tại không đúng" (chưa kiểm "khác mật khẩu hiện tại")

## P0-AUT-063 Khóa do nhập sai mật khẩu hiện tại
- Thiết kế: R-AUT-20, R-AUT-06, R-AUT-30
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context A đăng nhập `mio`, ở `/account/password`; context B chưa đăng nhập; không có dòng `login_throttles`
- Các bước:
  1. A gửi mật khẩu hiện tại sai 4 lần → mỗi lần "Mật khẩu hiện tại không đúng"
  2. Lần 5 → hộp thoại đóng; banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu"; ba ô giữ dữ liệu [evidence]
  3. A sửa Mật khẩu hiện tại thành đúng, gửi lại → vẫn banner khóa; `password_hash` không đổi
  4. B đăng nhập `mio` đúng mật khẩu → banner "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." trên màn Đăng nhập [evidence]
  5. A tải lại `/` → vẫn trong app
  6. `<log auth>` → 5 dòng `auth.password.change_failed` `"reason":"current_password_incorrect"`, `failedCount` 1 … 5 (dòng thứ 5 có `lockedUntil`); một dòng `auth.lock.started` `"source":"change_password"`; bước 3 có `auth.password.change_failed` `"reason":"locked"` kèm `lockedUntil` [evidence]
  7. Xóa bộ đếm; B đăng nhập sai 3 lần; A nhập sai mật khẩu hiện tại 2 lần → lần thứ 2 của A hiện banner khóa (dùng chung bộ đếm)

## P0-AUT-064 `signOutOtherDevices` thiếu hoặc sai kiểu
- Thiết kế: R-AUT-23
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập mio>`; thân cơ sở `{"currentPassword":"MioQuanLy#2026","newPassword":"MioMoi#2026x"}`
- Các bước:
  1. Gửi thân cơ sở (thiếu trường) → 400, `fields.signOutOtherDevices` "Chọn có đăng xuất các thiết bị khác hay không"; `password_hash` không đổi [evidence]
  2. `"signOutOtherDevices":"true"` (chuỗi), `1`, `null` → mỗi lần như bước 1
  3. `"signOutOtherDevices":true` → 204. Đặt lại mật khẩu

## P0-AUT-065 Đổi mật khẩu thành công xóa bộ đếm đăng nhập sai
- Thiết kế: R-AUT-23
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context A đăng nhập `mio`
- Các bước:
  1. Context B đăng nhập `mio` sai 3 lần → `failed_count` 3
  2. A đổi mật khẩu thành công → dòng `mio` không còn, hoặc `failed_count` 0
  3. B đăng nhập sai 4 lần → cả 4 lần 401, chưa khóa. Đặt lại mật khẩu

## P0-AUT-066 Hai thiết bị đổi mật khẩu cùng lúc
- Thiết kế: R-AUT-23 (xếp hàng bằng khóa dòng `users`), R-AUT-24
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; hai jar `a.jar`, `b.jar` cùng đăng nhập `mio`
- Các bước:
  1. Gửi song song: A với `newPassword` `MoiCuaA#2026`, B với `MoiCuaB#2026`, cả hai `currentPassword` `MioQuanLy#2026`, `signOutOtherDevices: true` → đúng một request 204; request kia 400 `fields.currentPassword` "Mật khẩu hiện tại không đúng" hoặc 401; không có 500 [evidence]
  2. Đăng nhập thử cả hai mật khẩu → chỉ mật khẩu của request 204 được 201
  3. `<psql> "select token_hash from user_sessions where user_id = <id mio>"` → mọi phiên còn lại là phiên mới do một request 204 tạo (so SHA-256 cookie trong response); không còn phiên cũ của A hay B
  4. Lặp bước 1–3 thêm 4 lần (đặt lại mật khẩu, xóa `login_throttles`, đăng nhập lại giữa các lần) → lần nào cũng thỏa
  5. Lặp bước 1–2 với `signOutOtherDevices: false` → vẫn đúng một request 204 và mật khẩu dùng được là của request đó

## P0-AUT-067 Hai tab cùng trình duyệt sau khi đổi mật khẩu
- Thiết kế: R-AUT-23 (thiết bị hiện tại nhận phiên mới)
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: một context đăng nhập `mio`, mở hai tab: tab 1 ở `/account/password`, tab 2 ở `/`
- Các bước:
  1. Tab 1 đổi mật khẩu bằng "Đổi và đăng xuất thiết bị khác" → thành công
  2. Tab 2 bấm "Đổi mật khẩu" trên thanh điều hướng rồi tải lại → vẫn trong app, không bị đẩy về `/login` (hai tab dùng chung cookie mới) [evidence]. Đặt lại mật khẩu

## P0-AUT-068 Lỗi hệ thống khi đăng nhập
- Thiết kế: mục Xử lý lỗi; R-SKL-16, R-SKL-30
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context mở `/login`
- Các bước:
  1. `docker compose stop postgres`
  2. Đăng nhập `mio` đúng → response 500 `INTERNAL_ERROR`; banner danger "Lỗi hệ thống, vui lòng thử lại sau"; ô Tên giữ `mio`, ô Mật khẩu bị xóa [evidence]
  3. `docker compose ps` → container api vẫn chạy; log api có dòng mức error, không chứa `MioQuanLy#2026`
  4. `docker compose start postgres`, chờ api `healthy`; đăng nhập lại → vào app

## P0-AUT-069 Mất kết nối khi đăng nhập
- Thiết kế: mục Xử lý lỗi; mục Màn hình Đăng nhập (vùng thông báo)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: context mở `/login`; `<psql> "delete from user_sessions"`
- Các bước:
  1. Nhập `mio` / mật khẩu đúng; `context.setOffline(true)`; bấm "Đăng nhập" → banner danger "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."; giữ cả hai ô [evidence]
  2. `context.setOffline(false)`, bấm lại → vào app; DB có đúng 1 phiên của `mio`
  3. Đăng xuất; `docker compose stop api`; đăng nhập → cùng banner như bước 1; `docker compose start api`

## P0-AUT-070 Trình duyệt chặn cookie
- Thiết kế: mục Xử lý lỗi (cookie bị tắt)
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: người
- Tiền điều kiện: Chrome thật; Cài đặt › Quyền riêng tư và bảo mật › Cài đặt trang web › Cookie: chặn cho `http://localhost:3000`
- Các bước:
  1. Mở `http://localhost:3000/login`, đăng nhập `mio` đúng → banner danger "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại."; vẫn ở `/login` [evidence]
  2. Bật lại cookie, đăng nhập → vào app

## P0-AUT-071 Mở app khi nạp phiên chậm, lỗi hoặc mất kết nối
- Thiết kế: mục Khung app (màn hình chờ, màn hình lỗi, nút "Thử lại")
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`
- Các bước:
  1. Bật giả lập mạng chậm, tải lại `/` → màn hình chờ: logo "Mio", vòng xoay, "Đang tải…", chưa có thanh điều hướng [evidence]; tắt giả lập
  2. `docker compose stop postgres`; tải lại `/` → màn hình lỗi "Lỗi hệ thống, vui lòng thử lại sau", nút "Thử lại"; không chuyển `/login` [evidence]
  3. `docker compose stop api` (trang vẫn mở); bấm "Thử lại" → thông báo đổi thành "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại." [evidence]
  4. `docker compose start postgres api`, chờ `healthy`; bấm "Thử lại" → màn hình chờ rồi Trang chính

## P0-AUT-072 Lỗi hệ thống và mất kết nối khi đổi mật khẩu
- Thiết kế: mục Màn hình Đổi mật khẩu (lỗi), mục Xử lý lỗi
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/account/password`, ba ô hợp lệ; ghi lại `password_hash`
- Các bước:
  1. `docker compose stop postgres`; gửi qua hộp thoại → hộp thoại đóng; banner danger "Lỗi hệ thống, vui lòng thử lại sau" ngay sau ô Nhập lại mật khẩu mới; giữ dữ liệu [evidence]
  2. `docker compose start postgres`, chờ `healthy`; `context.setOffline(true)`; gửi → banner "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."; giữ dữ liệu
  3. `context.setOffline(false)`; gửi lại → toast success; `password_hash` đổi đúng một lần. Đặt lại mật khẩu

## P0-AUT-073 Tài khoản bị xóa trong DB khi đang đăng nhập
- Thiết kế: mục Thay đổi DB (`user_sessions.user_id` on delete cascade), R-AUT-11
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: tạo `tam.thoi` (Thợ) bằng CLI; web đăng nhập `tam.thoi`
- Các bước:
  1. `<psql> "delete from users where username = 'tam.thoi'"` → `<psql> "select count(*) from user_sessions s left join users u on u.id = s.user_id where u.id is null"` → `0`
  2. Tải lại trang → `/login?next=%2F` kèm banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại"; `GET /api/v1/sessions/current` 401 [evidence]
  3. `<cli> list-users` → không còn `tam.thoi`

## P0-AUT-074 Vai trò và tên hiển thị đổi trong DB khi đang đăng nhập
- Thiết kế: mục Kiểm tra request (đọc `users` mỗi request), R-AUT-29
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`, ở `/`
- Các bước:
  1. `<psql> "update users set role = 'technician', display_name = 'Mio Thử' where username = 'mio'"`
  2. Tải lại → khối tài khoản "Mio Thử", badge "Thợ"; `GET /api/v1/sessions/current` trả `"role":"technician"` [evidence]
  3. Đặt lại `role = 'manager'`, `display_name = 'Huỳnh Mio'`; tải lại → "Huỳnh Mio", "Quản lý"

## P0-AUT-075 Chuỗi băm mật khẩu trong DB bị hỏng
- Thiết kế: mục Xử lý lỗi (chuỗi băm hỏng, R-SKL-16)
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: tạo `hong.hash` (Thợ) bằng CLI
- Các bước:
  1. `<psql> "update users set password_hash = 'khong-phai-phc' where username = 'hong.hash'"`
  2. Đăng nhập `hong.hash` với mật khẩu bất kỳ → 500 `INTERNAL_ERROR`, "Lỗi hệ thống, vui lòng thử lại sau", không có chi tiết lỗi trong thân; api vẫn chạy [evidence]
  3. `<psql> "select count(*) from login_throttles where username = 'hong.hash'"` → `0`; log api có dòng mức error kèm `userId`, không chứa `khong-phai-phc`; `<log auth>` không có `auth.login.failed` cho `hong.hash`
  4. Đăng nhập `mio` → bình thường
  5. `reset-password --username hong.hash` → đăng nhập bằng mật khẩu mới được

## P0-AUT-076 Tên hiển thị dài, có dấu và emoji trên thanh điều hướng
- Thiết kế: mục Khung app; component `app-nav` (tên hiển thị 1–50 ký tự, xuống dòng khi dài)
- Khía cạnh: Hiển thị
- Kỹ thuật: giá trị biên
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: tạo `ten.dai` (Thợ) với tên hiển thị đúng 50 ký tự gồm chữ có dấu và emoji (ghi chuỗi dùng vào `results.md`)
- Các bước:
  1. Đăng nhập `ten.dai` → khối tài khoản hiện đủ 50 ký tự, xuống dòng, không tràn khỏi thanh điều hướng, trang không cuộn ngang; badge "Thợ" không bị đè [evidence]
  2. `GET /api/v1/sessions/current` → `displayName` đúng chuỗi đã tạo

## P0-AUT-077 Băm lại mật khẩu khi tham số băm cũ
- Thiết kế: R-AUT-08; mục Tham số cài đặt (argon2id)
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: có tài khoản `mio`
- Các bước:
  1. `<psql> "select password_hash from users where username = 'mio'"` → bắt đầu bằng `$argon2id$v=19$m=19456,t=2,p=1$`
  2. Tạo chuỗi băm tham số cũ: `docker compose exec -T api node -e "require('@node-rs/argon2').hash('MioQuanLy#2026',{algorithm:2,memoryCost:4096,timeCost:1,parallelism:1}).then(console.log)"` → ghi vào `users.password_hash` của `mio`
  3. Đăng nhập `mio` / `MioQuanLy#2026` → 201; `password_hash` mới bắt đầu bằng `$argon2id$v=19$m=19456,t=2,p=1$` [evidence]
  4. Đăng nhập lại → 201; `password_hash` không đổi so với bước 3

## P0-AUT-078 Đường dẫn không tồn tại
- Thiết kế: mục Màn hình Không tìm thấy trang, R-AUT-28
- Khía cạnh: Hiển thị
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: web đăng nhập `mio`
- Các bước:
  1. Mở `/khong-co` → trong khung app tiêu đề "Không tìm thấy trang", nút "Về Trang chính"; không mục điều hướng nào được chọn [evidence]
  2. Bấm "Về Trang chính" → `/`
  3. Đăng xuất; mở `/khong-co` → `/login?next=%2Fkhong-co`; đăng nhập → màn hình như bước 1
  4. Đăng nhập `ngocanh.nail` ở context khác, mở `/khong-co` → cùng màn hình

## P0-AUT-079 Log các sự kiện đăng nhập, đăng xuất, đổi mật khẩu, CLI
- Thiết kế: R-AUT-30
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không có dòng `login_throttles`
- Các bước:
  1. `<đăng nhập mio>` thêm `-H 'User-Agent: <x × 300>'` → `<log auth>` có dòng `auth.login.succeeded` mức info với `userId`, `"username":"mio"`, `time`, `requestId`, `ip`, `userAgent` dài đúng 200 ký tự [evidence]
  2. Đăng nhập `mio` sai 1 lần → `auth.login.failed` mức warn, `"userExists":true`, `"reason":"invalid_credentials"`, `"failedCount":1`
  3. `DELETE <api>/sessions/current` với `mio.jar` → `auth.logout` có `userId`
  4. Đổi mật khẩu qua API với `signOutOtherDevices: false` → `auth.password.changed` có `userId`, `"signedOutOtherDevices":false`
  5. `create-user` một tài khoản mới, `reset-password` tài khoản đó → output mỗi lệnh chỉ có câu cho người đọc ("Đã tạo tài khoản…", "Đã đặt lại mật khẩu…"), không có dòng JSON; `docker compose logs api` có `auth.cli.user_created` và `auth.cli.password_reset` kèm `username`, `time`, không có `requestId`, `ip` [evidence]
  6. Lọc bằng `docker compose logs api | grep '"event":"auth.'` → ra đủ các dòng của bước 1–5. Đặt lại mật khẩu `mio`

## P0-AUT-080 Log không chứa mật khẩu, token, chuỗi băm
- Thiết kế: R-AUT-30, R-SKL-17
- Khía cạnh: Phân quyền
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. Lần lượt: đăng nhập sai với mật khẩu `LoNgoaiLog#91`; `<đăng nhập mio>`; đổi mật khẩu với `newPassword` `LoNgoaiLog#92`; gửi `change-password` thân JSON hỏng `{"currentPassword":"LoNgoaiLog#93",`; `create-user` với mật khẩu `LoNgoaiLog#94` (ghi lại output lệnh)
  2. `docker compose logs api | grep -c -e 'LoNgoaiLog' -e 'MioQuanLy#2026'` → `0`; output lệnh CLI không chứa `LoNgoaiLog#94` [evidence]
  3. Tìm trong log token cookie (lấy từ `mio.jar`), `token_hash` của phiên, chuỗi `$argon2id$` → không có [evidence]
  4. Đặt lại mật khẩu `mio`

## P0-AUT-081 Tạo tài khoản Quản lý và Thợ bằng CLI
- Thiết kế: R-AUT-25, R-AUT-26 (`list-users`), R-AUT-27; mục Tham số cài đặt (argon2id)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: môi trường thử, bảng `users` trống (`<psql> "delete from users"`)
- Các bước:
  1. `<cli> list-users; echo $?` → "Chưa có tài khoản nào.", `0`
  2. `printf '%s\n' 'MioQuanLy#2026' | <cli> create-user --username mio --role manager --display-name "Huỳnh Mio"; echo $?` → output đúng một dòng "Đã tạo tài khoản mio (Quản lý)", `0` [evidence]
  3. `printf '%s\n' 'NgocAnh#2026' | <cli> create-user --username ngocanh.nail --role technician --display-name "Ngọc Anh"` → "Đã tạo tài khoản ngocanh.nail (Thợ)", mã 0
  4. `<psql> "select username, role, display_name, left(password_hash, 31) from users order by username"` → `mio | manager | Huỳnh Mio | $argon2id$v=19$m=19456,t=2,p=1$` và `ngocanh.nail | technician | Ngọc Anh | $argon2id$v=19$m=19456,t=2,p=1$` [evidence]
  5. Đăng nhập web bằng cả hai tài khoản → vào app đúng vai trò

## P0-AUT-082 Nhập mật khẩu CLI trên terminal
- Thiết kế: R-AUT-27; R-AUT-25, R-AUT-26 (kiểm tham số trước khi hỏi mật khẩu)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: người
- Tiền điều kiện: terminal thật trên máy local
- Các bước:
  1. `docker compose exec -it api node dist/cli.js create-user --username tty.test --role technician --display-name "Thử TTY"` → hỏi "Mật khẩu: "; gõ `TtyTest#2026` → không hiện ký tự nào (kể cả dấu `*`) [evidence]
  2. Hỏi "Nhập lại mật khẩu: ", gõ `TtyTest#2026` → "Đã tạo tài khoản tty.test (Thợ)", mã 0
  3. Lặp với `tty.test2`, lần nhập lại gõ `TtyTest#2027` → "Mật khẩu nhập lại không khớp", mã 1; `list-users` không có `tty.test2` [evidence]
  4. `docker compose exec -it api node dist/cli.js reset-password --username tty.test` → hỏi hai lần như bước 1–2, đặt lại thành công
  5. `docker compose exec -it api node dist/cli.js create-user --username tty.test3 --display-name "Thử TTY"` (thiếu `--role`) → in ngay "Thiếu --role", mã 1, không hỏi "Mật khẩu: "; lặp với `--username tty.test --role technician --display-name "Trùng"` → in ngay "Tên đăng nhập đã tồn tại: tty.test", không hỏi mật khẩu [evidence]
  6. `docker compose exec -it api node dist/cli.js reset-password --username khongco` → in ngay "Không tìm thấy tài khoản: khongco", không hỏi mật khẩu
  7. `history` của shell → không chứa mật khẩu đã gõ

## P0-AUT-083 Tên đăng nhập khi tạo bằng CLI
- Thiết kế: R-AUT-25, R-AUT-07
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: mọi lệnh dùng `printf '%s\n' 'TaoMoi#2026' | <cli> create-user --username <tên> --role technician --display-name "Thử"`
- Các bước:
  1. `ab` → "Tên đăng nhập phải dài 3–32 ký tự, chỉ gồm chữ thường không dấu, số, dấu chấm, gạch dưới, gạch ngang", mã 1 [evidence]
  2. `abc` → tạo được; `b` × 32 → tạo được; `c` × 33 → lỗi như bước 1
  3. `Mio.Test` → "Đã tạo tài khoản mio.test (Thợ)"; `"  pad.test  "` → "Đã tạo tài khoản pad.test (Thợ)"
  4. `thợ.nail`, `"mio nail"`, `mio@nail`, `mio+1` → mỗi lần lỗi như bước 1, không tạo
  5. `a_b-c.9` → tạo được
  6. `<psql> "select username from users order by username"` → có `a_b-c.9`, `abc`, `b…b` (32), `mio.test`, `pad.test`; không có tên nào ở bước 1, 4

## P0-AUT-084 Tên đăng nhập đã tồn tại
- Thiết kế: R-AUT-25
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: có `mio`; ghi lại `password_hash`, `display_name` của `mio`
- Các bước:
  1. `create-user --username mio --role technician --display-name "Trùng"` → "Tên đăng nhập đã tồn tại: mio", mã 1 [evidence]
  2. `--username MIO` → "Tên đăng nhập đã tồn tại: mio", mã 1
  3. `mio` giữ nguyên `password_hash`, `display_name`, `role`

## P0-AUT-085 Vai trò khi tạo bằng CLI
- Thiết kế: R-AUT-25
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. Bỏ `--role` → "Thiếu --role", mã 1
  2. `--role admin`, `--role ""` → "Vai trò phải là manager hoặc technician", mã 1
  3. Không tài khoản nào được tạo

## P0-AUT-086 Tên hiển thị khi tạo bằng CLI
- Thiết kế: R-AUT-25 (độ dài theo code point, bỏ khoảng trắng hai đầu)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: mỗi bước dùng một tên đăng nhập mới
- Các bước:
  1. Bỏ `--display-name` → "Thiếu --display-name", mã 1
  2. `--display-name "   "` → "Tên hiển thị phải từ 1 đến 50 ký tự", mã 1
  3. `"A"` → tạo được; `ệ` × 50 → tạo được; `ệ` × 51 → lỗi như bước 2 [evidence]
  4. `💅` × 50 → tạo được; `💅` × 51 → lỗi như bước 2
  5. `"  Ngọc Anh  "` → `display_name` lưu là `Ngọc Anh`

## P0-AUT-087 Mật khẩu khi tạo bằng CLI
- Thiết kế: R-AUT-25; quy tắc chung "mỗi trường một lỗi"
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: mỗi bước dùng một tên đăng nhập mới
- Các bước:
  1. Mật khẩu `Abcd#12` (7) → "Mật khẩu phải từ 8 đến 128 ký tự", mã 1 [evidence]
  2. `Abcd#123` (8) → tạo được; `x` × 128 → tạo được; `x` × 129 → lỗi như bước 1
  3. `--username pw.same.name` với mật khẩu `pw.same.name` → "Mật khẩu không được trùng tên đăng nhập", mã 1
  4. Đăng nhập web bằng tài khoản mật khẩu 128 ký tự ở bước 2 → vào app
  5. `--username pw.x` với mật khẩu `pw.x` (vừa ngắn vừa trùng tên) → chỉ một dòng "Mật khẩu phải từ 8 đến 128 ký tự" (mỗi trường một lỗi, độ dài xét trước), mã 1

## P0-AUT-088 CLI in mọi lỗi cùng lúc
- Thiết kế: R-AUT-25 ("in mọi lỗi, mỗi lỗi một dòng")
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không
- Các bước:
  1. `printf '%s\n' 'ngan' | <cli> create-user --username ab --role admin --display-name "   "` → 4 dòng: lỗi tên đăng nhập, vai trò, tên hiển thị, mật khẩu (nguyên văn như P0-AUT-083, 085, 086, 087); mã 1 [evidence]
  2. `printf '%s\n' 'HopLe#2026' | <cli> create-user` → 3 dòng "Thiếu --username", "Thiếu --role", "Thiếu --display-name"; mã 1

## P0-AUT-089 Mật khẩu qua stdin và tham số không hợp lệ
- Thiết kế: R-AUT-27
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: mỗi bước dùng một tên đăng nhập mới, `--role technician --display-name "Thử"`
- Các bước:
  1. `<cli> create-user … < /dev/null` (stdin rỗng) → "Thiếu mật khẩu", mã 1
  2. `printf 'Crlf#2026\r\n' | <cli> create-user …` → tạo được; đăng nhập với `Crlf#2026` → 201 [evidence]
  3. `printf 'Dong1#2026\nDong2#2026\n' | …` → tạo được; đăng nhập `Dong1#2026` → 201, `Dong2#2026` → 401
  4. `printf ' CachDau#2026 \n' | …` → tạo được; đăng nhập ` CachDau#2026 ` (có khoảng trắng hai đầu) → 201, `CachDau#2026` → 401
  5. `<cli> create-user --username p.arg --role technician --display-name "Thử" --password Abc#12345` → "Tham số không hợp lệ: --password", mã 1; không tạo `p.arg` [evidence]

## P0-AUT-090 Tạo cùng một tên đăng nhập đồng thời
- Thiết kế: R-AUT-25 (DB unique chặn cả khi tạo đồng thời)
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: không có `song.song`
- Các bước:
  1. Chạy song song hai lệnh `create-user --username song.song …` (hai tiến trình nền, `wait`) → một lệnh "Đã tạo tài khoản song.song (Thợ)" mã 0; lệnh kia "Tên đăng nhập đã tồn tại: song.song" mã 1, không phải lỗi hệ thống [evidence]
  2. `<psql> "select count(*) from users where username = 'song.song'"` → `1`
  3. Lặp bước 1–2 thêm 4 lần với tên khác → lần nào cũng thỏa

## P0-AUT-091 `reset-password` đặt lại mật khẩu, đăng xuất mọi thiết bị, gỡ khóa
- Thiết kế: R-AUT-26, R-AUT-31, R-AUT-30
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: context A ở `/`, context B ở `/account/password`, cả hai đăng nhập `ngocanh.nail`; context C chưa đăng nhập
- Các bước:
  1. C đăng nhập `ngocanh.nail` sai 5 lần → khóa
  2. `printf '%s\n' 'NgocAnhMoi#2026' | <cli> reset-password --username ngocanh.nail; echo $?` → "Đã đặt lại mật khẩu cho ngocanh.nail. Mọi phiên đăng nhập của tài khoản đã bị đăng xuất.", `0` [evidence]
  3. DB: không còn phiên của `ngocanh.nail`; dòng `ngocanh.nail` trong `login_throttles` không còn khóa (không còn dòng hoặc `locked_until` rỗng); `password_hash` đã đổi
  4. A tải lại → `/login?next=%2F` kèm banner "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại"; B gửi form đổi mật khẩu → `/login?next=%2Faccount%2Fpassword` kèm banner "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" [evidence]
  5. C đăng nhập ngay bằng `NgocAnhMoi#2026` → 201 (không còn bị khóa); bằng `NgocAnh#2026` → 401
  6. Log có `auth.cli.password_reset` với `"username":"ngocanh.nail"`. Đặt lại mật khẩu về `NgocAnh#2026`

## P0-AUT-092 `reset-password` báo lỗi
- Thiết kế: R-AUT-26, R-AUT-07
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<đăng nhập ngocanh>`; ghi lại `password_hash` của `ngocanh.nail`
- Các bước:
  1. `printf '%s\n' 'HopLe#2026' | <cli> reset-password` → "Thiếu --username", mã 1
  2. `… reset-password --username khongco` → "Không tìm thấy tài khoản: khongco", mã 1 [evidence]
  3. `printf '%s\n' 'ngan' | <cli> reset-password --username ngocanh.nail` → "Mật khẩu phải từ 8 đến 128 ký tự", mã 1; mật khẩu `ngocanh.nail` → "Mật khẩu không được trùng tên đăng nhập", mã 1
  4. Sau bước 3: `password_hash` không đổi; `curl -b ngocanh.jar <api>/sessions/current` → 200 (phiên không bị xóa)
  5. `printf '%s\n' 'NgocAnh#2026' | <cli> reset-password --username "  NGOCANH.NAIL "` → đặt lại cho `ngocanh.nail` (tên được chuẩn hóa), mã 0

## P0-AUT-093 `list-users` liệt kê tài khoản
- Thiết kế: R-AUT-26
- Khía cạnh: Hiển thị
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: bảng `users` chỉ có `mio`, `ngocanh.nail` và `abc` (Thợ, "Thử")
- Các bước:
  1. `<cli> list-users; echo $?` → đúng 3 dòng theo thứ tự "abc | Thợ | Thử", "mio | Quản lý | Huỳnh Mio", "ngocanh.nail | Thợ | Ngọc Anh"; mã `0`; không in chuỗi băm hay id [evidence]
  2. Trường hợp chưa có tài khoản: xem P0-AUT-081 bước 1

## P0-AUT-094 Quên mật khẩu Quản lý: tự đặt lại bằng CLI
- Thiết kế: R-AUT-33
- Khía cạnh: Phân quyền
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: chạy bằng `compose.yml` (không có `compose.dev.yml`); `<psql> "delete from user_sessions"` (không còn ai đăng nhập web)
- Các bước:
  1. `printf '%s\n' 'MioKhoiPhuc#2026' | <cli> reset-password --username mio` → thành công, không đòi mật khẩu cũ hay phiên web [evidence]
  2. Đăng nhập web `mio` / `MioKhoiPhuc#2026` → vào app, badge "Quản lý"
  3. `docker compose ps --format '{{.Name}} {{.Ports}}'` → chỉ api có `127.0.0.1:3000->3000/tcp`; không container nào mở cổng khác cho CLI [evidence]
  4. Đặt lại mật khẩu `mio`

## P0-AUT-095 Phần dùng chung của khung app vẫn đúng sau khi thêm auth
- Thiết kế: R-AUT-16, R-SKL-13, R-SKL-14, R-SKL-15, R-SKL-31; thiết kế `app-skeleton` mục `cli.ts`
- Khía cạnh: Regression
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống chạy như P0-SKL-001, có mã auth
- Các bước:
  1. `docker compose ps` → 4 dịch vụ `running (healthy)` (healthcheck gọi `/api/v1/health` không cookie)
  2. Chạy lại P0-SKL-016, P0-SKL-021, P0-SKL-023 → đều đạt (health, 404 và file tĩnh không cần đăng nhập) [evidence]
  3. `<cli> help` → danh sách có `create-user`, `reset-password`, `list-users`; `<cli> khong-co` → "Lệnh không tồn tại: khong-co. Chạy help để xem danh sách.", mã 1

## P0-AUT-096 Đăng nhập lại khi đang có phiên; route công khai không gia hạn
- Thiết kế: R-AUT-08 (thay phiên của cookie đang gửi), R-AUT-10 (route công khai không gia hạn)
- Khía cạnh: Phiên đăng nhập và cookie
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `<psql> "delete from user_sessions"`; `<đăng nhập mio>`; ghi lại `token_hash` của phiên (`<psql> "select token_hash from user_sessions where user_id = <id mio>"`)
- Các bước:
  1. `curl -s -i -b mio.jar -c mio.jar <origin> <json> -d '{"username":"mio","password":"MioQuanLy#2026"}' <api>/sessions` → 201, `Set-Cookie` token mới
  2. `<psql> "select token_hash from user_sessions where user_id = <id mio>"` → đúng 1 dòng, khác `token_hash` đã ghi (phiên cũ bị xóa) [evidence]
  3. Đăng nhập `ngocanh.nail` bằng `-b mio.jar -c mio.jar` (đổi tài khoản) → 201; `mio` không còn phiên nào, `ngocanh.nail` có 1 phiên
  4. `<đăng nhập mio>`; `<psql> "update user_sessions set updated_at = now() - interval '25 hours', expires_at = now() + interval '89 days' where user_id = <id mio>"`; `curl -s -i -b mio.jar <api>/health` → 200, không có `Set-Cookie`; `updated_at`, `expires_at` giữ nguyên giá trị vừa đặt [evidence]
  5. `curl -s -i -b mio.jar <api>/sessions/current` → 200 kèm `Set-Cookie` (route có `@Roles` thì gia hạn, như P0-AUT-027)

## Lịch sử thay đổi

- 2026-10-31: tạo mới (`/test-case-design auth`)
- 2026-10-31: `/design-review auth`: theo RV-01 … RV-16 sửa P0-AUT-001, 007, 020, 023, 034, 036, 038, 044, 045, 056, 063, 066, 075, 079, 081, 082, 087; đổi câu banner thành "Phiên đăng nhập đã kết thúc…" ở mọi case; thêm P0-AUT-096; Ghi chú chạy bỏ mục chờ quyết định, thêm phần chỉ kiểm bằng test tự động
