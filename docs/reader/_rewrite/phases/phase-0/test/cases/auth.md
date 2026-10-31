<!-- src-section: 0b0fa0b228 1f6d1756fb54 -->
# Test case – Đăng nhập và phân quyền (`auth`, `AUT`)

**Tóm tắt.** Tài liệu này gồm các manual test case cho tính năng đăng nhập và phân quyền.

- Thiết kế: `docs/phases/phase-0/design/auth.md`
- Mockup: `docs/design/ui/login/`, `docs/design/ui/app-shell/`, `docs/design/ui/change-password/`, `docs/design/ui/forbidden/`, `docs/design/ui/not-found/`
- Cập nhật: 2026-10-31

<!-- src-section: bee2e72c3a 9fde7fa046ba -->
## Khía cạnh không áp dụng

**Tóm tắt.** Hai khía cạnh test không áp dụng cho tính năng này. Tính năng cũng không thuộc lằn ranh đỏ nào.

- Khía cạnh 9. Phía Facebook và Messenger:
  - Đăng nhập không dùng dịch vụ ngoài (thiết kế mục Tích hợp bên ngoài).
  - Ghép nối Messenger của thợ thuộc giai đoạn sau.
- Khía cạnh 1. Hiển thị, phần giao diện điện thoại và ngày giờ:
  - Giai đoạn 0 chỉ mở qua `127.0.0.1` trên máy tính và chưa thiết kế bố cục điện thoại (thiết kế mục Màn hình).
  - Tính năng không hiển thị ngày giờ nào.
- Lằn ranh đỏ: không lằn ranh nào thuộc tính năng này.
  - Tính năng không nói với khách, không comment, không đụng lịch hay tài khoản Facebook.
  - Các case cốt lõi về bảo mật (khóa đăng nhập, phiên, CSRF, không lộ mật khẩu) vẫn gắn `Regression: có`.

<!-- src-section: 8ba43f44af e41ef8551d03 -->
## Ghi chú chạy

**Tóm tắt.** Phần này nêu môi trường chạy, dữ liệu mẫu, cách giả lập thời gian và mạng, các case phụ thuộc tính năng khác, và các phần chỉ kiểm được bằng test tự động.

**Môi trường**
- Hệ thống chạy như P0-SKL-001 bằng `compose.yml`. File `.env` có `MIO_PUBLIC_URL=http://localhost:3000`.
- Web mở bằng Playwright (Chromium) tại `http://localhost:3000`, khung 1440×900.
- "Context A/B/C" là các browser context riêng. Mỗi context tương ứng với một thiết bị.
- Lệnh CLI nhận mật khẩu qua stdin.

**Dữ liệu mẫu**

Nếu chưa có thì tạo như P0-AUT-081.
- `mio`: Quản lý, tên hiển thị "Huỳnh Mio", mật khẩu `MioQuanLy#2026`.
- `ngocanh.nail`: Thợ, tên hiển thị "Ngọc Anh", mật khẩu `NgocAnh#2026`.
- Case nào làm đổi mật khẩu của tài khoản mẫu thì cuối case đặt lại bằng `printf '%s\n' '<mật khẩu mẫu>' | <cli> reset-password --username <tên>`.

**Trước mỗi case**
- Chạy `<psql> "delete from login_throttles"`, trừ khi tiền điều kiện ghi khác.

**Giả lập thời gian và mạng**
- Thời gian trôi qua được giả lập bằng cách sửa cột thời gian qua SQL theo `now()` của PostgreSQL.
- Các container dùng chung đồng hồ máy local nên chỉ chênh vài giây. Khoảng sai số ghi trong từng bước.
- Mạng chậm được giả lập bằng Chrome DevTools Protocol qua Playwright, độ trễ 3000 ms. Cách này tương đương chỉnh Network throttling trong DevTools. Lệnh CDP dùng là `Network.emulateNetworkConditions`.
- Mất mạng được giả lập bằng `context.setOffline(true)`.

**Case cần tính năng sau**

Khi chạy `/manual-test-run` mà tính năng cần thiết chưa có thì case là `bị chặn` và được chạy lại sau.
- P0-AUT-041, P0-AUT-043 cần trang `/settings` (thêm bởi `group-settings`) và `/system-log` (thêm bởi `emergency-stop`).
- P0-AUT-042, P0-AUT-044 cần ít nhất một endpoint chỉ Quản lý có nút thao tác trên web (`group-settings` hoặc `crawl-settings`).
- Trước khi có các tính năng đó, Quản lý cũng chỉ thấy mục "Trang chính". Thiết kế mục Khung app quy định mỗi tính năng tự thêm mục của mình.

**Banner hết phiên**
- Banner "Phiên đăng nhập đã kết thúc…" dựa vào cờ `mio.hadSession` trong `localStorage` (R-AUT-31).
- Context đã từng vào app thì có cờ. Context mới hoặc vừa bấm "Đăng xuất" thì không có cờ.

**Phần chỉ kiểm được bằng test tự động**

Các phần sau không tạo được bằng thao tác bên ngoài code. `/implementation-plan` phải có test tương ứng.
- R-AUT-14: route thiếu `@Public()` / `@Roles(...)` làm api thoát mã 1 và ghi log "Route chưa khai báo quyền: <METHOD> <path>". Manual chỉ kiểm hệ quả ở P0-AUT-040.
- R-AUT-24: test cả hai nhánh thứ tự, tức phiên bị xóa trước và sau bước kiểm phiên. Manual chỉ kiểm bất biến ở P0-AUT-066.
- R-AUT-06: transaction khóa dòng của `recordFailure`, `confirmSuccess`. Request đúng mật khẩu đã qua `getLock` mà gặp khóa lúc `confirmSuccess` thì nhận 429 và không có phiên nào được tạo. Manual kiểm hệ quả ở P0-AUT-023.
- R-AUT-23, R-AUT-26: đổi mật khẩu và `reset-password` khóa dòng `users`. Lần đổi thứ hai chạy sau và kiểm mật khẩu hiện tại trên chuỗi băm mới. Manual kiểm hệ quả ở P0-AUT-066.
- R-AUT-30: CLI không mở được `/proc/1/fd/1` thì ghi log ra stderr.
- R-AUT-05: tên không tồn tại vẫn gọi `verify` trên chuỗi băm giả. Manual chỉ đo thời gian ở P0-AUT-013.
- R-AUT-30: danh sách `redact` ở độ sâu 1 đến 3.

<!-- src-section: 4744441925 c9c5eb8e4766 -->
## P0-AUT-001 Quản lý đăng nhập từ trang cần đăng nhập

**Kiểm tra điều gì.** Quản lý mở một trang cần đăng nhập, được đưa sang trang Đăng nhập, đăng nhập rồi vào app. Phiên mới có hạn 90 ngày và còn giữ khi tải lại trang.

**Thông tin**
- Thiết kế: R-AUT-08, R-AUT-09, R-AUT-28; mục Khung app.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Có tài khoản `mio`.
- Chạy `<psql> "delete from user_sessions"`.
- Dùng context mới, không có cookie.

**Các bước**
1. Mở `http://localhost:3000/`.
   - Mong đợi: Màn hình chờ hiện ra, rồi trang chuyển sang `/login?next=%2F` với form Đăng nhập trống.
   - 📷 Chụp evidence.
2. Nhập `mio` / `MioQuanLy#2026`, bấm "Đăng nhập".
   - Mong đợi: `POST /api/v1/sessions` trả 201 với thân `{"user":{"id":"<uuid>","username":"mio","displayName":"Huỳnh Mio","role":"manager"}}`. Trang chuyển sang `/` với tiêu đề "Hôm nay", mục "Trang chính" đang được chọn.
   - 📷 Chụp evidence.
3. Xem khối tài khoản ở cuối thanh điều hướng.
   - Mong đợi: Khối hiện "Huỳnh Mio", badge "Quản lý", "Đổi mật khẩu" và "Đăng xuất".
   - 📷 Chụp evidence.
4. Chạy `<psql> "select expires_at - now() as con_lai from user_sessions where user_id = <id mio>"`.
   - Mong đợi: Có đúng 1 dòng. Giá trị `con_lai` khoảng 90 ngày, sai số 1 phút.
   - 📷 Chụp evidence.
5. Tải lại trang.
   - Mong đợi: Trang vẫn ở `/`, không quay về `/login`.
6. Chạy `localStorage.getItem('mio.hadSession')` trong trang.
   - Mong đợi: Kết quả khác `null` (R-AUT-31).

<!-- src-section: a9d6758e6e 2d7ca294ec77 -->
## P0-AUT-002 Thợ đăng nhập, thanh điều hướng chỉ có mục của Thợ

**Kiểm tra điều gì.** Thợ đăng nhập xong chỉ thấy mục điều hướng dành cho Thợ. Khối tài khoản hiện đúng tên và vai trò.

**Thông tin**
- Thiết kế: R-AUT-08, R-AUT-29; mục Khung app.
- Khía cạnh: Phân quyền. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Có tài khoản `ngocanh.nail`.
- Dùng context mới.

**Các bước**
1. Mở `/login`, đăng nhập `ngocanh.nail` / `NgocAnh#2026`.
   - Mong đợi: Trang chuyển sang `/` với tiêu đề "Hôm nay".
2. Xem thanh điều hướng.
   - Mong đợi: Chỉ có "Trang chính". Không có "Cài đặt", "Nhật ký hệ thống" và không có đường kẻ nhóm Quản lý.
   - 📷 Chụp evidence.
3. Xem khối tài khoản.
   - Mong đợi: Khối hiện "Ngọc Anh", badge "Thợ", "Đổi mật khẩu" và "Đăng xuất".
   - 📷 Chụp evidence.

<!-- src-section: bb844d5e79 e37c2d3f1c81 -->
## P0-AUT-003 Màn hình Đăng nhập và khung app khớp mockup

**Kiểm tra điều gì.** Người kiểm so ảnh chụp thật với ảnh mockup để xác nhận màn hình Đăng nhập và khung app hiển thị đúng thiết kế.

**Thông tin**
- Thiết kế: mục Màn hình Đăng nhập, Khung app; mockup `login/`, `app-shell/`.
- Khía cạnh: Hiển thị. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: người.

**Chuẩn bị**
- Đã có ảnh evidence của P0-AUT-001, 002, 005, 007, 008, 012, 014, 028, 030, 034, 047, 053, 068, 069, 071.

**Các bước**
1. Đặt từng ảnh evidence cạnh ảnh mockup cùng trạng thái trong `docs/design/ui/login/screenshots/`.
   - Mong đợi: Bố cục, màu, chữ và nút khớp mockup. Banner nằm ngay sau ô Mật khẩu, trước nút "Đăng nhập". Chữ tiếng Việt có dấu hiển thị đủ, không vỡ font.
   - 📷 Chụp evidence.
2. So ảnh Trang chính của Quản lý, của Thợ, màn hình chờ và màn hình lỗi nạp phiên với `docs/design/ui/app-shell/screenshots/`.
   - Mong đợi: Các ảnh khớp mockup. Badge vai trò dễ đọc trên nền thanh điều hướng.
   - 📷 Chụp evidence.

<!-- src-section: bcd7e9f29c 62f26fe4296d -->
## P0-AUT-004 Thuộc tính ô nhập và nút Hiện/Ẩn trên màn Đăng nhập

**Kiểm tra điều gì.** Các ô nhập trên màn Đăng nhập có đúng thuộc tính HTML. Nút Hiện/Ẩn chỉ đổi cách hiển thị mật khẩu và không gửi form.

**Thông tin**
- Thiết kế: mục Màn hình Đăng nhập; component `password-field`.
- Khía cạnh: Hiển thị. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Đọc DOM của form.
   - Mong đợi: Ô Tên đăng nhập có `autocomplete="username"`, `autocapitalize="none"`. Ô Mật khẩu có `type="password"`, `autocomplete="current-password"`. Không ô nào có `maxlength`.
2. Gõ `abc 123` vào ô Mật khẩu, bấm "Hiện". Sau đó bấm "Ẩn".
   - Mong đợi: Sau khi bấm "Hiện", ô hiện `abc 123` và nút đổi thành "Ẩn" (`aria-label` "Ẩn mật khẩu"). Sau khi bấm "Ẩn", ô ẩn lại và giá trị không đổi.
   - 📷 Chụp evidence.
3. Dùng phím Tab đi tới nút Hiện/Ẩn, nhấn Enter rồi nhấn Space.
   - Mong đợi: Mỗi lần nhấn chỉ đổi trạng thái hiện/ẩn. Tab Network không có request `POST /api/v1/sessions`.
4. Đặt con trỏ trong ô Mật khẩu, nhấn Enter.
   - Mong đợi: Form được gửi, tab Network có một request `POST /api/v1/sessions`.

<!-- src-section: 4567ce5a66 3ffafbb8142d -->
## P0-AUT-005 Bỏ trống cả hai ô khi đăng nhập

**Kiểm tra điều gì.** Bấm "Đăng nhập" khi ô còn trống thì web báo lỗi dưới từng ô và không gọi API.

**Thông tin**
- Thiết kế: R-AUT-01, R-AUT-03.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Để trống hai ô, bấm "Đăng nhập".
   - Mong đợi: Dưới ô Tên đăng nhập hiện "Nhập tên đăng nhập". Dưới ô Mật khẩu hiện "Nhập mật khẩu". Không có banner. Không có request `POST /api/v1/sessions`.
   - 📷 Chụp evidence.
2. Nhập `mio` vào ô Tên đăng nhập, bấm lại.
   - Mong đợi: Chỉ còn lỗi "Nhập mật khẩu".

<!-- src-section: f7bf69ea22 203143262f1b -->
## P0-AUT-006 Ô chỉ có khoảng trắng

**Kiểm tra điều gì.** Tên đăng nhập chỉ có khoảng trắng bị coi là trống. Mật khẩu chỉ có khoảng trắng vẫn được gửi đi và tính là một lần sai.

**Thông tin**
- Thiết kế: R-AUT-01, R-AUT-03, R-AUT-07.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Nhập tên đăng nhập gồm 3 khoảng trắng, mật khẩu `x`, bấm "Đăng nhập".
   - Mong đợi: Dưới ô hiện "Nhập tên đăng nhập". Web không gửi API.
2. Nhập tên `mio`, mật khẩu gồm 3 khoảng trắng, bấm "Đăng nhập".
   - Mong đợi: Không có lỗi theo trường. API trả 401 và hiện banner danger "Tên đăng nhập hoặc mật khẩu không đúng".
   - 📷 Chụp evidence.
3. Chạy `<psql> "select failed_count from login_throttles where username = 'mio'"`.
   - Mong đợi: Kết quả là `1`.

<!-- src-section: b3d161bde4 e6b8b954b4f3 -->
## P0-AUT-007 Tên đăng nhập 32 và 33 ký tự

**Kiểm tra điều gì.** Tên đăng nhập dài tối đa 32 ký tự. Độ dài tính theo code point và đo sau khi chuẩn hóa.

**Thông tin**
- Thiết kế: R-AUT-02, R-AUT-07 (độ dài theo code point, đo sau khi chuẩn hóa).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.
- Mật khẩu nhập `x`.

**Các bước**
1. Nhập tên gồm 32 ký tự `a`, gửi form.
   - Mong đợi: Không có lỗi theo trường. Banner hiện "Tên đăng nhập hoặc mật khẩu không đúng".
2. Nhập tên gồm 33 ký tự `a`, gửi form.
   - Mong đợi: Dưới ô hiện "Tên đăng nhập tối đa 32 ký tự". Web không gửi API.
   - 📷 Chụp evidence.
3. Nhập tên gồm 2 khoảng trắng, 32 ký tự `a`, rồi 2 khoảng trắng.
   - Mong đợi: Kết quả như bước 1, vì độ dài tính sau khi bỏ khoảng trắng hai đầu.
4. Nhập tên gồm 32 ký tự `ệ` (chữ dựng sẵn), rồi tên gồm 32 ký tự `😀`. Sau đó nhập 33 ký tự `ệ` và 33 ký tự `😀`.
   - Mong đợi: Hai tên 32 ký tự cho kết quả như bước 1. Hai tên 33 ký tự cho kết quả như bước 2.
5. Gọi API: `curl -s <origin> <json> -d '{"username":"<a × 33>","password":"x"}' <api>/sessions`.
   - Mong đợi: API trả 400 với thân `{"code":"VALIDATION_ERROR","message":"Dữ liệu đăng nhập không hợp lệ","fields":{"username":"Tên đăng nhập tối đa 32 ký tự"}}`.
   - 📷 Chụp evidence.
6. Thử tên gồm 32 ký tự `İ` trên web và qua API. Đây là chữ I hoa có chấm, U+0130; khi đổi sang chữ thường, mỗi ký tự thành 2 code point. Sau đó thử tên gồm 16 ký tự `İ`.
   - Mong đợi: Với 32 ký tự, web báo "Tên đăng nhập tối đa 32 ký tự" và API trả 400 `VALIDATION_ERROR`, không có 500. Với 16 ký tự, API trả 401 bình thường.
   - 📷 Chụp evidence.

<!-- src-section: 1ba04e2d11 bf45db955434 -->
## P0-AUT-008 Mật khẩu đăng nhập 128 và 129 ký tự

**Kiểm tra điều gì.** Mật khẩu đăng nhập dài tối đa 128 ký tự, tính theo code point. Lỗi 400 do quá dài không bị đếm vào giới hạn đăng nhập sai (R-AUT-06).

**Thông tin**
- Thiết kế: R-AUT-04 (độ dài theo code point; lỗi 400 không đếm vào R-AUT-06).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.
- Tên nhập `mio`.

**Các bước**
1. Nhập mật khẩu gồm 128 ký tự `x`, gửi form.
   - Mong đợi: Không có lỗi theo trường. API trả 401, banner hiện "Tên đăng nhập hoặc mật khẩu không đúng".
2. Nhập mật khẩu gồm 129 ký tự `x`, gửi form.
   - Mong đợi: Dưới ô hiện "Mật khẩu tối đa 128 ký tự". Web không gửi API.
   - 📷 Chụp evidence.
3. Nhập mật khẩu gồm 128 ký tự `😀` (256 đơn vị UTF-16), rồi 129 ký tự `😀`.
   - Mong đợi: 128 ký tự cho kết quả như bước 1. 129 ký tự cho kết quả như bước 2.
4. Gọi API với mật khẩu gồm 129 ký tự `x`.
   - Mong đợi: API trả 400 `VALIDATION_ERROR`, `fields.password` là "Mật khẩu tối đa 128 ký tự".
5. Chạy `<psql> "select failed_count from login_throttles where username = 'mio'"`.
   - Mong đợi: Kết quả là `2`. Chỉ hai lần 401 được đếm.

<!-- src-section: 2d15ab27af b5445b2dc707 -->
## P0-AUT-009 Tên đăng nhập được chuẩn hóa, mật khẩu giữ nguyên

**Kiểm tra điều gì.** Tên đăng nhập được bỏ khoảng trắng hai đầu và không phân biệt hoa thường. Mật khẩu thì so khớp nguyên văn, kể cả hoa thường và khoảng trắng.

**Thông tin**
- Thiết kế: R-AUT-07.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Đăng nhập với tên `  MIO  `, mật khẩu `MioQuanLy#2026`.
   - Mong đợi: API trả 201. Trang vào `/` với "Huỳnh Mio".
   - 📷 Chụp evidence.
2. Đăng xuất. Đăng nhập với tên `Mio`, mật khẩu `miOQuanLy#2026` (khác hoa thường).
   - Mong đợi: API trả 401, banner hiện "Tên đăng nhập hoặc mật khẩu không đúng".
3. Đăng nhập với tên `mio`, mật khẩu `MioQuanLy#2026 ` (thêm khoảng trắng cuối). Sau đó thử mật khẩu ` MioQuanLy#2026` (thêm khoảng trắng đầu).
   - Mong đợi: Cả hai lần đều trả 401.
4. Chạy `<psql> "select username, failed_count from login_throttles"`.
   - Mong đợi: Có đúng một dòng `mio | 3`.

<!-- src-section: e55deb0183 4419374a8160 -->
## P0-AUT-010 API đăng nhập: thiếu trường, sai kiểu

**Kiểm tra điều gì.** API đăng nhập trả lỗi 400 theo từng trường khi thiếu trường hoặc sai kiểu. Các lỗi này không được đếm là lần đăng nhập sai.

**Thông tin**
- Thiết kế: R-AUT-01 … R-AUT-04 (phần API).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Gọi `curl -s <origin> <json> -d '{}' <api>/sessions`.
   - Mong đợi: API trả 400 với thân `{"code":"VALIDATION_ERROR","message":"Dữ liệu đăng nhập không hợp lệ","fields":{"username":"Nhập tên đăng nhập","password":"Nhập mật khẩu"}}`.
   - 📷 Chụp evidence.
2. Gửi thân `{"username":123,"password":true}`.
   - Mong đợi: Kết quả như bước 1.
3. Gửi thân `{"username":null,"password":"x"}`.
   - Mong đợi: `fields` chỉ có `username` với "Nhập tên đăng nhập".
4. Gửi thân `{"username":"mio","password":""}`.
   - Mong đợi: `fields` chỉ có `password` với "Nhập mật khẩu".
5. Chạy `<psql> "select count(*) from login_throttles"`.
   - Mong đợi: Kết quả là `0`.

<!-- src-section: e7e7ac50e7 b53246a8c091 -->
## P0-AUT-011 Thân request đăng nhập không phải JSON hoặc quá lớn

**Kiểm tra điều gì.** API đăng nhập từ chối thân request không phải JSON hoặc quá lớn. Các request này không được đếm là lần đăng nhập sai.

**Thông tin**
- Thiết kế: R-SKL-15 (qua `POST /api/v1/sessions`, `docs/design/api/sessions.md`).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: đoán lỗi.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Gọi `curl -s <origin> <json> -d 'username=mio' <api>/sessions`.
   - Mong đợi: API trả 400 `INVALID_JSON` với "Dữ liệu gửi lên không đúng định dạng JSON".
2. Gửi thân JSON 1,1 MB, trong đó `password` dài 1.100.000 ký tự.
   - Mong đợi: API trả 413 `PAYLOAD_TOO_LARGE` với "Dữ liệu gửi lên quá lớn".
3. Chạy `<psql> "select count(*) from login_throttles"`.
   - Mong đợi: Kết quả là `0`.

<!-- src-section: 2f40739972 5c87aa62406b -->
## P0-AUT-012 Sai mật khẩu và tên không tồn tại trả giống hệt nhau

**Kiểm tra điều gì.** Sai mật khẩu và tên đăng nhập không tồn tại cho cùng một phản hồi, trên web lẫn qua API. Nhờ vậy người ngoài không biết được tên nào có thật.

**Thông tin**
- Thiết kế: R-AUT-05; mục Màn hình Đăng nhập (vùng thông báo).
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Nhập `mio` / `sai-mat-khau`, bấm "Hiện" ở ô Mật khẩu, rồi bấm "Đăng nhập".
   - Mong đợi: Banner danger "Tên đăng nhập hoặc mật khẩu không đúng" hiện ngay sau ô Mật khẩu, trước nút "Đăng nhập". Ô Tên giữ `mio`. Ô Mật khẩu trống và về trạng thái ẩn (nút "Hiện").
   - 📷 Chụp evidence.
2. Nhập lại mật khẩu sai, gửi lần nữa.
   - Mong đợi: Form vẫn chỉ có một banner.
3. Nhập `khongco` / `sai-mat-khau`, gửi form.
   - Mong đợi: Banner y hệt bước 1.
4. Gọi `curl -s -i` cho hai trường hợp trên.
   - Mong đợi: Cả hai trả 401 với thân giống hệt `{"code":"INVALID_CREDENTIALS","message":"Tên đăng nhập hoặc mật khẩu không đúng"}`. Không có `Set-Cookie`.
   - 📷 Chụp evidence.

<!-- src-section: 1dc9902115 68529971f993 -->
## P0-AUT-013 Thời gian phản hồi tên không tồn tại và sai mật khẩu tương đương

**Kiểm tra điều gì.** Thời gian phản hồi khi tên không tồn tại và khi sai mật khẩu gần như nhau. Nhờ vậy không đoán được tên nào có thật qua thời gian chờ.

**Thông tin**
- Thiết kế: R-AUT-05.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Lặp 10 vòng. Mỗi vòng chạy `<psql> "delete from login_throttles"`, rồi gửi `mio` / `sai-mat-khau` và `khongco` / `sai-mat-khau` bằng `curl -s -o /dev/null -w '%{http_code} %{time_total}\n'`.
   - Mong đợi: Cả 20 kết quả đều là `401`.
2. Tính trung vị thời gian của nhóm `mio` và nhóm `khongco`.
   - Mong đợi: Hai trung vị chênh nhau không quá 20%.
   - 📷 Chụp evidence.

<!-- src-section: ca96763667 1f5943d3ab05 -->
## P0-AUT-014 Lần sai thứ 5 khóa tên đăng nhập 15 phút

**Kiểm tra điều gì.** Lần đăng nhập sai thứ 5 khóa tên đăng nhập 15 phút. Trong lúc khóa, nhập đúng mật khẩu cũng không vào được.

**Thông tin**
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: giá trị biên.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập, mở `/login`.

**Các bước**
1. Đăng nhập `mio` sai 4 lần. Sau đó chạy `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"`.
   - Mong đợi: Mỗi lần sai hiện banner "Tên đăng nhập hoặc mật khẩu không đúng". Câu SQL trả `4` và cột khóa rỗng.
2. Đăng nhập sai lần thứ 5.
   - Mong đợi: Banner danger hiện "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút.". Response là 429 `LOGIN_LOCKED` với header `Retry-After: 900`.
   - 📷 Chụp evidence.
3. Chạy lại câu SQL ở bước 1.
   - Mong đợi: `failed_count` là 0. `locked_until` khoảng 15 phút sau thời điểm hiện tại, sai số 1 phút.
   - 📷 Chụp evidence.
4. Nhập mật khẩu đúng `MioQuanLy#2026`.
   - Mong đợi: Vẫn nhận 429 với cùng câu "Thử lại sau 15 phút.". Trang ở lại `/login`. Response không có `Set-Cookie`.
   - 📷 Chụp evidence.

<!-- src-section: f588134a15 7c4b6c11aacf -->
## P0-AUT-015 Đang khóa: không đếm thêm, không kéo dài khóa

**Kiểm tra điều gì.** Khi tên đăng nhập đang bị khóa, các lần sai tiếp theo không được đếm thêm và không kéo dài thời gian khóa. Mỗi lần vẫn được ghi log.

**Thông tin**
- Thiết kế: R-AUT-06, R-AUT-30.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- `mio` vừa bị khóa như P0-AUT-014.
- Ghi lại giá trị `locked_until`.

**Các bước**
1. Gửi thêm 3 lần sai qua API.
   - Mong đợi: Cả 3 lần đều trả 429 `LOGIN_LOCKED`. `Retry-After` không tăng giữa các lần.
2. Chạy `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"`.
   - Mong đợi: `failed_count` là 0. `locked_until` bằng đúng giá trị đã ghi lại.
3. Chạy `<log auth>`.
   - Mong đợi: Mỗi lần gửi ở bước 1 có đúng một dòng `auth.login.failed` mức warn, `"reason":"locked"`, có `lockedUntil`, không có `failedCount`. Không có thêm dòng `auth.lock.started`.
   - 📷 Chụp evidence.

<!-- src-section: d66eacf909 38573d2c46cf -->
## P0-AUT-016 Số phút còn lại làm tròn lên, tối thiểu 1

**Kiểm tra điều gì.** Thông báo khóa hiện số phút còn lại được làm tròn lên và không bao giờ nhỏ hơn 1. Header `Retry-After` không bao giờ bằng 0.

**Thông tin**
- Thiết kế: R-AUT-06.
- Khía cạnh: Thời gian. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- `mio` đang bị khóa như P0-AUT-014.
- Context mở `/login`.

**Các bước**
1. Chạy `<psql> "update login_throttles set locked_until = now() + interval '150 seconds' where username = 'mio'"`, rồi gửi ngay một lần đăng nhập trên web.
   - Mong đợi: Banner hiện "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 3 phút.". `Retry-After` nằm trong khoảng 140–150.
   - 📷 Chụp evidence.
2. Đặt `locked_until = now() + interval '30 seconds'`, gửi ngay.
   - Mong đợi: Thông báo là "Thử lại sau 1 phút.". `Retry-After` nằm trong khoảng 20–30.
3. Đặt `locked_until = now() + interval '3 seconds'`, gửi ngay qua API.
   - Mong đợi: Thông báo là "Thử lại sau 1 phút.". `Retry-After` nằm trong khoảng 1–3, không bao giờ là 0.

<!-- src-section: 7a99a207fc 1b680f1c727d -->
## P0-AUT-017 Hết khóa: đăng nhập lại được, bộ đếm bắt đầu từ 0

**Kiểm tra điều gì.** Khi hết thời gian khóa, người dùng đăng nhập lại được. Bộ đếm lần sai bắt đầu lại từ 0.

**Thông tin**
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai.
- Khía cạnh: Thời gian. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- `mio` đang bị khóa như P0-AUT-014.

**Các bước**
1. Chạy `<psql> "update login_throttles set locked_until = now() - interval '1 second' where username = 'mio'"`, rồi đăng nhập đúng.
   - Mong đợi: API trả 201, người dùng vào app.
   - 📷 Chụp evidence.
2. Chạy `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"`.
   - Mong đợi: Không còn dòng nào, hoặc dòng có `0` và cột khóa rỗng.
3. Khóa lại bằng 5 lần sai, đặt `locked_until = now() - interval '1 second'`, rồi gửi 1 lần sai.
   - Mong đợi: API trả 401, không phải 429.
4. Chạy lại câu SQL ở bước 2.
   - Mong đợi: `failed_count` là 1, `locked_until` rỗng, `window_started_at` gần bằng thời điểm hiện tại.
   - 📷 Chụp evidence.

<!-- src-section: 5ffdc891b2 f2acaeba74cd -->
## P0-AUT-018 Cửa sổ đếm 15 phút

**Kiểm tra điều gì.** Các lần sai chỉ được cộng dồn trong cửa sổ 15 phút. Lần sai đến sau khi cửa sổ đã hết thì bắt đầu cửa sổ mới.

**Thông tin**
- Thiết kế: R-AUT-06; mục Trạng thái › Bộ đếm đăng nhập sai (bước 2).
- Khía cạnh: Thời gian. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Đăng nhập sai 4 lần với `mio`. Chạy `<psql> "update login_throttles set window_started_at = now() - interval '15 minutes 5 seconds' where username = 'mio'"`. Gửi lần sai thứ 5.
   - Mong đợi: API trả 401, tài khoản không bị khóa. `failed_count` là 1, `window_started_at` gần bằng thời điểm hiện tại.
   - 📷 Chụp evidence.
2. Xóa bộ đếm. Đăng nhập sai 4 lần. Đặt `window_started_at = now() - interval '14 minutes 50 seconds'`. Gửi ngay lần sai thứ 5.
   - Mong đợi: API trả 429, tài khoản bị khóa 15 phút.
   - 📷 Chụp evidence.

<!-- src-section: 0ff6f9bd79 ac22dcec2953 -->
## P0-AUT-019 Đăng nhập đúng xóa bộ đếm

**Kiểm tra điều gì.** Một lần đăng nhập đúng xóa bộ đếm lần sai. Sau đó phải sai đủ 5 lần mới bị khóa.

**Thông tin**
- Thiết kế: R-AUT-06.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Đăng nhập sai 4 lần với `mio`.
   - Mong đợi: `failed_count` là 4.
2. Đăng nhập đúng.
   - Mong đợi: API trả 201. Dòng `mio` không còn, hoặc `failed_count` là 0.
3. Đăng nhập sai thêm 4 lần, rồi sai lần thứ 5.
   - Mong đợi: Cả 4 lần đầu trả 401. Lần thứ 5 trả 429.

<!-- src-section: 198a4cd976 ce4b90941489 -->
## P0-AUT-020 Giới hạn áp cả tên đăng nhập không tồn tại

**Kiểm tra điều gì.** Tên đăng nhập không tồn tại cũng bị đếm và bị khóa giống tài khoản thật. Log ghi đủ các lần sai và lần bắt đầu khóa.

**Thông tin**
- Thiết kế: R-AUT-06, R-AUT-05, R-AUT-30.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không có tài khoản `khongco`.

**Các bước**
1. Đăng nhập `khongco` sai 5 lần trên web.
   - Mong đợi: 4 lần đầu hiện banner "Tên đăng nhập hoặc mật khẩu không đúng". Lần 5 hiện banner "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút.", giống tài khoản thật.
   - 📷 Chụp evidence.
2. Chạy `<psql> "select locked_until - now() from login_throttles where username = 'khongco'"`.
   - Mong đợi: Kết quả khoảng 15 phút.
3. Chạy `<log auth>`.
   - Mong đợi: Có 5 dòng `auth.login.failed` với `"username":"khongco"`, `"userExists":false`, `"reason":"invalid_credentials"`.
   - Mong đợi: 4 dòng đầu có `failedCount` từ 1 tới 4. Dòng thứ 5 có `failedCount` 5 và `lockedUntil`.
   - Mong đợi: Có một dòng `auth.lock.started` với `"source":"login"`, `"userExists":false`, cùng `requestId` với dòng `failed` thứ 5.
   - 📷 Chụp evidence.

<!-- src-section: ff4108baff a8f429cbb342 -->
## P0-AUT-021 Khóa đăng nhập không ảnh hưởng phiên đang có

**Kiểm tra điều gì.** Khi tên đăng nhập bị khóa, thiết bị đang đăng nhập sẵn vẫn dùng app bình thường.

**Thông tin**
- Thiết kế: R-AUT-06 (phiên đang có không bị ảnh hưởng).
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context A đã đăng nhập `mio` trên web.

**Các bước**
1. Ở context B, đăng nhập `mio` sai 5 lần.
   - Mong đợi: Tên đăng nhập bị khóa.
2. Ở context A, tải lại `/`.
   - Mong đợi: Context A vẫn ở trong app. `GET /api/v1/sessions/current` trả 200.
   - 📷 Chụp evidence.

<!-- src-section: 99dff929e0 4fb6abcc73ac -->
## P0-AUT-022 Bộ đếm tính theo tên đã chuẩn hóa

**Kiểm tra điều gì.** Các cách viết khác nhau của cùng một tên đăng nhập dùng chung một bộ đếm lần sai.

**Thông tin**
- Thiết kế: R-AUT-06, R-AUT-07.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Gửi đăng nhập sai lần lượt với `mio`, `MIO`, ` Mio`, `mIo `, `MiO`.
   - Mong đợi: 4 lần đầu trả 401. Lần 5 trả 429.
   - 📷 Chụp evidence.
2. Chạy `<psql> "select username from login_throttles"`.
   - Mong đợi: Có đúng một dòng `mio`.

<!-- src-section: c4d0d9075b 8002f6482ee1 -->
## P0-AUT-023 Nhiều lần đăng nhập sai gửi đồng thời

**Kiểm tra điều gì.** Khi nhiều request sai mật khẩu đến cùng lúc, hệ thống vẫn đếm đúng và khóa đúng một lần. Request đến trong lúc khóa không được đếm và không kéo dài khóa.

**Thông tin**
- Thiết kế: R-AUT-06 (đồng thời: kiểm lại khóa trong transaction, không đếm khi đang khóa, không kéo dài khóa).
- Khía cạnh: Thao tác đồng thời. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Gửi song song 10 request `mio` / `sai-mat-khau` bằng `seq 10 | xargs -P 10 -I{} curl -s -o /dev/null -w '%{http_code}\n' …`.
   - Mong đợi: Mỗi request trả 401 hoặc 429. Không có 500.
2. Đếm các mã trả về.
   - Mong đợi: Có đúng 4 mã 401 và 6 mã 429. Lần sai được tính tối đa 5. Lần thứ 5 làm khóa, 5 request còn lại gặp khóa.
   - 📷 Chụp evidence.
3. Chạy `<log auth>`.
   - Mong đợi: Có đúng một dòng `auth.lock.started` cho `mio`. Có 10 dòng `auth.login.failed`, gồm 5 dòng `invalid_credentials` (`failedCount` từ 1 tới 5) và 5 dòng `locked`.
   - 📷 Chụp evidence.
4. Chạy `<psql> "select failed_count, locked_until from login_throttles where username = 'mio'"` và ghi lại kết quả.
   - Mong đợi: `failed_count` là 0. `locked_until` khoảng 15 phút sau thời điểm hiện tại.
5. Gửi song song thêm 5 request, trong đó có 1 request đúng mật khẩu.
   - Mong đợi: Tất cả trả 429. `locked_until` bằng giá trị đã ghi lại.

<!-- src-section: 005c5c4305 0db2ec8c8a2a -->
## P0-AUT-024 Cookie phiên đúng thuộc tính, token chỉ lưu dạng băm

**Kiểm tra điều gì.** Cookie phiên có đủ thuộc tính bảo mật. Token chỉ được lưu trong DB dưới dạng băm, và JavaScript trong trang không đọc được cookie.

**Thông tin**
- Thiết kế: R-AUT-09.
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- `PUBLIC_URL` là `http://localhost:3000`.

**Các bước**
1. Chạy `<đăng nhập mio>`.
   - Mong đợi: API trả 201. `Set-Cookie: mio_session=<token>` có `HttpOnly`, `SameSite=Lax`, `Path=/`, `Max-Age` trong khoảng 7775990–7776000. Không có `Secure`.
   - 📷 Chụp evidence.
2. Xem giá trị `<token>`.
   - Mong đợi: Token dài 43 ký tự, chỉ gồm `A–Z`, `a–z`, `0–9`, `-`, `_`.
3. Chạy `printf '%s' '<token>' | sha256sum`. So với `token_hash` của phiên mới nhất, lấy bằng `<psql> "select token_hash from user_sessions order by created_at desc limit 1"`.
   - Mong đợi: Hai giá trị bằng nhau.
   - 📷 Chụp evidence.
4. Chạy `docker compose exec -T postgres pg_dump -U mio mio | grep -c '<token>'`.
   - Mong đợi: Kết quả là `0`.
5. Đăng nhập trên web, chạy `document.cookie` trong trang.
   - Mong đợi: Kết quả không chứa `mio_session`.

<!-- src-section: e4fdce1729 5e58bd596b0b -->
## P0-AUT-025 Cookie có `Secure` khi `PUBLIC_URL` là https

**Kiểm tra điều gì.** Khi app chạy với địa chỉ https, cookie phiên và cookie xóa phiên đều có thuộc tính `Secure`. Khi quay lại http thì không còn `Secure`.

**Thông tin**
- Thiết kế: R-AUT-09.
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Sao lưu `.env`.

**Các bước**
1. Đặt `MIO_PUBLIC_URL=https://localhost:3000`, chạy `docker compose up -d api` và chờ `healthy`.
   - Mong đợi: Service api khởi động lại và healthy.
2. Gọi `curl -s -i <json> -H 'Origin: https://localhost:3000' -d '{"username":"mio","password":"MioQuanLy#2026"}' <api>/sessions`.
   - Mong đợi: API trả 201, `Set-Cookie` có `Secure`.
   - 📷 Chụp evidence.
3. Gọi `DELETE <api>/sessions/current` với cookie vừa nhận, cùng `Origin`.
   - Mong đợi: API trả 204. `Set-Cookie` xóa cookie cũng có `Secure`.
4. Trả lại `.env`, chạy `docker compose up -d api`, rồi chạy `<đăng nhập mio>`.
   - Mong đợi: `Set-Cookie` không có `Secure`.

<!-- src-section: 61ac7d7b8e 1068d9bb152c -->
## P0-AUT-026 Một tài khoản đăng nhập trên nhiều thiết bị

**Kiểm tra điều gì.** Một tài khoản có thể đăng nhập trên nhiều thiết bị cùng lúc. Đăng xuất ở một thiết bị không ảnh hưởng thiết bị khác.

**Thông tin**
- Thiết kế: R-AUT-09, R-AUT-12.
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.

**Các bước**
1. Ở context A và B, cùng đăng nhập `mio` trên web. Sau đó chạy `<psql> "select count(*) from user_sessions where user_id = <id mio>"`.
   - Mong đợi: Kết quả là `2`.
2. Ở context A, bấm "Đăng xuất". Đếm lại số phiên, rồi tải lại context B.
   - Mong đợi: Số phiên còn `1`. Context B vẫn ở trong app.
   - 📷 Chụp evidence.

<!-- src-section: 1dcd0078cf 8ac3d41f79c2 -->
## P0-AUT-027 Gia hạn phiên trượt sau 24 giờ

**Kiểm tra điều gì.** Phiên chỉ được gia hạn khi lần gia hạn trước đã cách hơn 24 giờ. Khi gia hạn, phiên có lại hạn 90 ngày và cookie được gửi lại.

**Thông tin**
- Thiết kế: R-AUT-10.
- Khía cạnh: Thời gian. Kỹ thuật: giá trị biên.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.
- Chạy `<đăng nhập mio>`.

**Các bước**
1. Chạy `<psql> "update user_sessions set updated_at = now() - interval '23 hours 59 minutes', expires_at = now() + interval '89 days'"`. Sau đó gọi `curl -s -i -b mio.jar <api>/sessions/current`.
   - Mong đợi: API trả 200, không có `Set-Cookie`. `expires_at`, `updated_at` giữ nguyên giá trị vừa đặt.
   - 📷 Chụp evidence.
2. Đặt `updated_at = now() - interval '24 hours 1 minute'`, `expires_at = now() + interval '89 days'`, rồi gọi lại.
   - Mong đợi: API trả 200 kèm `Set-Cookie` cùng token, `Max-Age` trong khoảng 7775990–7776000. `expires_at` khoảng 90 ngày sau thời điểm hiện tại. `updated_at` gần bằng thời điểm hiện tại.
   - 📷 Chụp evidence.
3. Gọi lại ngay.
   - Mong đợi: API trả 200, không có `Set-Cookie`.

<!-- src-section: d1822d6a99 64150d424bee -->
## P0-AUT-028 Phiên hết hạn

**Kiểm tra điều gì.** Phiên hết hạn thì người dùng bị đưa về trang Đăng nhập kèm thông báo. Phiên bị xóa khỏi DB và cookie bị xóa.

**Thông tin**
- Thiết kế: R-AUT-11, R-AUT-28; mục Trạng thái › Phiên.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: giá trị biên.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.
- Web đăng nhập `mio`, đang ở `/`.

**Các bước**
1. Chạy `<psql> "update user_sessions set expires_at = now() - interval '1 second' where user_id = <id mio>"`.
   - Mong đợi: Phiên của `mio` đã quá hạn.
2. Tải lại trang.
   - Mong đợi: Trang chuyển sang `/login?next=%2F` với banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" (câu hỏi mở 8).
   - 📷 Chụp evidence.
3. Xem response của `GET /api/v1/sessions/current`.
   - Mong đợi: API trả 401 với `{"code":"UNAUTHENTICATED","message":"Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn"}` và `Set-Cookie: mio_session=; Max-Age=0`.
   - 📷 Chụp evidence.
4. Chạy `<psql> "select count(*) from user_sessions where user_id = <id mio>"`.
   - Mong đợi: Kết quả là `0`.
5. Chạy `<đăng nhập mio>`, đặt `expires_at = now() + interval '5 seconds'`, gọi ngay `curl -b mio.jar <api>/sessions/current`. Chờ 6 giây rồi gọi lại.
   - Mong đợi: Lần gọi đầu trả 200. Lần gọi sau 6 giây trả 401.

<!-- src-section: 3fb9d0a6ea fce32edb9320 -->
## P0-AUT-029 Không có cookie hoặc cookie bị sửa

**Kiểm tra điều gì.** Request không có cookie hoặc có cookie sai đều bị từ chối. Cookie sai bị xóa. Trên web, người dùng được đưa về trang Đăng nhập.

**Thông tin**
- Thiết kế: R-AUT-11.
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.

**Các bước**
1. Gọi `curl -s -i <api>/sessions/current` không kèm cookie.
   - Mong đợi: API trả 401 `UNAUTHENTICATED`, không có `Set-Cookie`.
2. Gọi lại với `-H 'Cookie: mio_session=abc'`.
   - Mong đợi: API trả 401. `Set-Cookie` xóa cookie (`Max-Age=0`).
   - 📷 Chụp evidence.
3. Đổi ký tự cuối của token hợp lệ trong `mio.jar`, gọi lại.
   - Mong đợi: Kết quả như bước 2.
4. Trên web đang đăng nhập, sửa giá trị cookie `mio_session` trong context, rồi tải lại.
   - Mong đợi: Trang chuyển sang `/login?next=%2F` kèm banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". Cookie `mio_session` không còn trong context.
   - 📷 Chụp evidence.
5. Tải lại `/login?next=%2F` lần nữa. Lúc này không còn cookie.
   - Mong đợi: Không còn banner.

<!-- src-section: 2efffaf53c 673207e279cf -->
## P0-AUT-030 Mất cookie giữa chừng khi đang đổi mật khẩu

**Kiểm tra điều gì.** Nếu cookie mất trong lúc đang đổi mật khẩu, thao tác đổi bị từ chối và mật khẩu giữ nguyên. Người dùng được đưa về trang Đăng nhập rồi quay lại đúng trang Đổi mật khẩu.

**Thông tin**
- Thiết kế: R-AUT-31, R-AUT-28.
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, mở `/account/password`.
- Ghi lại `password_hash` của `mio`.

**Các bước**
1. Nhập Mật khẩu hiện tại `MioQuanLy#2026`. Nhập Mật khẩu mới và Nhập lại là `MioMoi#2026x`.
   - Mong đợi: Form không báo lỗi.
2. Xóa cookie của context bằng `context.clearCookies()`.
   - Mong đợi: Context không còn cookie.
3. Bấm "Đổi mật khẩu", trong hộp thoại bấm "Đổi và đăng xuất thiết bị khác".
   - Mong đợi: API trả 401. Trang chuyển sang `/login?next=%2Faccount%2Fpassword` với banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại".
   - 📷 Chụp evidence.
4. Kiểm `password_hash` của `mio`, rồi đăng nhập bằng `MioQuanLy#2026`.
   - Mong đợi: `password_hash` không đổi. Sau khi đăng nhập, trang vào `/account/password` với form trống.

<!-- src-section: b604caa4eb cc0a6e8e1ccc -->
## P0-AUT-031 Dùng lại cookie cũ sau khi đăng xuất

**Kiểm tra điều gì.** Sau khi đăng xuất, cookie cũ không dùng lại được, kể cả để đổi mật khẩu.

**Thông tin**
- Thiết kế: R-AUT-12; mục Trạng thái › Phiên (chuyển không hợp lệ).
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.
- Sao chép `mio.jar` thành `old.jar`.

**Các bước**
1. Gọi `curl -s -i -X DELETE -b mio.jar <origin> <api>/sessions/current`.
   - Mong đợi: API trả 204.
2. Gọi `curl -s -i -b old.jar <api>/sessions/current`.
   - Mong đợi: API trả 401 `UNAUTHENTICATED`. `Set-Cookie` xóa cookie.
   - 📷 Chụp evidence.
3. Gọi `curl -s -i -b old.jar <origin> <json> -d '{"currentPassword":"MioQuanLy#2026","newPassword":"MioMoi#2026x","signOutOtherDevices":true}' <api>/users/me/change-password`.
   - Mong đợi: API trả 401. Mật khẩu không đổi.

<!-- src-section: f9f9624e1d 4263265652f6 -->
## P0-AUT-032 Đăng nhập thành công dọn phiên hết hạn

**Kiểm tra điều gì.** Mỗi lần đăng nhập thành công dọn mọi phiên hết hạn của mọi tài khoản. Đăng nhập sai thì không dọn.

**Thông tin**
- Thiết kế: R-AUT-13.
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- `mio` và `ngocanh.nail` đều có một phiên còn hạn: chạy `<đăng nhập mio>` và `<đăng nhập ngocanh>`.

**Các bước**
1. Chạy `<psql> "insert into user_sessions (user_id, token_hash, expires_at) select id, md5(random()::text), now() - interval '1 day' from users"`.
   - Mong đợi: Mỗi tài khoản có thêm một phiên hết hạn.
2. Đăng nhập sai `ngocanh.nail` 1 lần. Sau đó chạy `<psql> "select count(*) from user_sessions where expires_at <= now()"`.
   - Mong đợi: Kết quả vẫn lớn hơn hoặc bằng 2, vì đăng nhập sai không dọn phiên.
3. Đăng nhập đúng `ngocanh.nail`, rồi đếm lại phiên hết hạn.
   - Mong đợi: Kết quả là `0`, kể cả phiên của `mio`. Hai phiên còn hạn ban đầu vẫn còn.
   - 📷 Chụp evidence.

<!-- src-section: feb02b614f 1efe678be035 -->
## P0-AUT-033 Dọn bộ đếm đăng nhập sai đã cũ

**Kiểm tra điều gì.** Hệ thống dọn các dòng bộ đếm đăng nhập sai đã cũ hơn 24 giờ và không còn khóa. Dòng còn mới hoặc đang khóa được giữ lại.

**Thông tin**
- Thiết kế: R-AUT-13.
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Chèn bốn dòng vào `login_throttles`, với `window_started_at` = `updated_at`:
   - `a1`: `failed_count` 2, `updated_at` cách đây 25 giờ.
   - `a2`: `failed_count` 2, `updated_at` cách đây 23 giờ.
   - `a3`: `failed_count` 0, `locked_until` sau thời điểm hiện tại 5 phút, `updated_at` cách đây 25 giờ.
   - `a4`: `failed_count` 0, `locked_until` đã qua 1 giờ, `updated_at` cách đây 25 giờ.
2. Gửi đăng nhập sai cho `khac`.
   - Mong đợi: API trả 401.
3. Chạy `<psql> "select username from login_throttles order by username"`.
   - Mong đợi: Còn `a2`, `a3`, `khac`. Không còn `a1`, `a4`.
   - 📷 Chụp evidence.

<!-- src-section: 062acc2dff 9b45daee067c -->
## P0-AUT-034 Đăng xuất từ thanh điều hướng

**Kiểm tra điều gì.** Bấm "Đăng xuất" xóa phiên, xóa cookie và đưa người dùng về trang Đăng nhập. Bấm Back sau đó không xem lại được nội dung app.

**Thông tin**
- Thiết kế: R-AUT-32, R-AUT-12, R-AUT-30.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.
- Web đăng nhập `mio`, ở `/`.

**Các bước**
1. Bấm "Đăng xuất".
   - Mong đợi: `DELETE /api/v1/sessions/current` trả 204. Trang chuyển sang `/login` với banner info "Bạn đã đăng xuất".
   - 📷 Chụp evidence.
2. Chạy `<psql> "select count(*) from user_sessions where user_id = <id mio>"`. Xem cookie của context và chạy `localStorage.getItem('mio.hadSession')`.
   - Mong đợi: Kết quả SQL là `0`. Context không còn cookie `mio_session`. Lệnh `localStorage` trả `null`.
3. Bấm Back.
   - Mong đợi: Nội dung app không hiện ra. Trang chuyển sang `/login?next=%2F` với form trống. Không có banner "Phiên đăng nhập đã kết thúc…", vì cookie đã bị xóa khi đăng xuất.
   - 📷 Chụp evidence.
4. Chạy `<log auth>`.
   - Mong đợi: Có dòng `auth.logout` với `userId` của `mio`.

<!-- src-section: a9a08f1450 79b53bc7c588 -->
## P0-AUT-035 Đăng xuất qua API là idempotent

**Kiểm tra điều gì.** Gọi đăng xuất qua API luôn trả 204 và xóa cookie, dù không có cookie, phiên đã hết hạn hay gọi nhiều lần.

**Thông tin**
- Thiết kế: R-AUT-12, R-AUT-18.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Gọi `curl -s -i -X DELETE <origin> <api>/sessions/current` không kèm cookie.
   - Mong đợi: API trả 204 với `Set-Cookie: mio_session=; Max-Age=0`.
2. Chạy `<đăng nhập mio>`, đặt `expires_at = now() - interval '1 second'`, rồi gọi DELETE với `mio.jar`.
   - Mong đợi: API trả 204 và xóa cookie. Phiên không còn trong DB.
3. Chạy `<đăng nhập mio>`, rồi gọi DELETE hai lần với cùng `mio.jar` (không ghi lại jar).
   - Mong đợi: Cả hai lần đều trả 204.
4. Xem header của mọi response ở bước 1–3.
   - Mong đợi: Response nào cũng có `Cache-Control: no-store`.

<!-- src-section: 0969892a1c 0b0768baf4cf -->
## P0-AUT-036 Đăng xuất khi máy chủ lỗi hoặc mất kết nối

**Kiểm tra điều gì.** Khi máy chủ lỗi hoặc mất kết nối, bấm "Đăng xuất" vẫn đưa người dùng về trang Đăng nhập. Trang không báo đã đăng xuất và không hiện màn hình lỗi.

**Thông tin**
- Thiết kế: R-AUT-32.
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/`.

**Các bước**
1. Chạy `docker compose stop postgres`, rồi bấm "Đăng xuất".
   - Mong đợi: DELETE trả 500. Trang vẫn chuyển sang `/login` và form Đăng nhập hiện ra. Không có banner "Bạn đã đăng xuất" và không có màn hình lỗi.
   - 📷 Chụp evidence.
2. Chạy `docker compose start postgres`, chờ api `healthy`, rồi mở `/`.
   - Mong đợi: Người dùng vào lại app. Phiên và cookie vẫn còn; thiết kế chấp nhận điều này.
3. Chạy `docker compose stop api`, bấm "Đăng xuất". Sau đó chạy `docker compose start api`.
   - Mong đợi: Trang vẫn chuyển sang `/login`. Không có banner "Bạn đã đăng xuất".

<!-- src-section: d1b0047072 354a230af014 -->
## P0-AUT-037 Chưa đăng nhập mở đường dẫn bên trong rồi quay lại đúng trang

**Kiểm tra điều gì.** Người chưa đăng nhập mở một đường dẫn bên trong app thì được đưa sang trang Đăng nhập. Sau khi đăng nhập, người dùng quay lại đúng đường dẫn đó, kể cả tham số.

**Thông tin**
- Thiết kế: R-AUT-28.
- Khía cạnh: Phân quyền. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập.

**Các bước**
1. Mở `/account/password?tu=link`.
   - Mong đợi: Trang chuyển sang `/login?next=%2Faccount%2Fpassword%3Ftu%3Dlink`. Không có banner, vì context chưa từng đăng nhập và không có cookie.
   - 📷 Chụp evidence.
2. Đăng nhập `mio`.
   - Mong đợi: Trang chuyển sang `/account/password?tu=link`, hiện trang Đổi mật khẩu.
   - 📷 Chụp evidence.

<!-- src-section: c898014295 148d05c20c25 -->
## P0-AUT-038 Tham số `next` không an toàn bị bỏ qua

**Kiểm tra điều gì.** Tham số `next` trỏ ra ngoài app hoặc không hợp lệ bị bỏ qua. Khi đó người dùng được đưa về `/` thay vì bị dẫn sang trang khác.

**Thông tin**
- Thiết kế: R-AUT-28.
- Khía cạnh: Phân quyền. Kỹ thuật: bảng quyết định.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context chưa đăng nhập.
- Giữa các bước bấm "Đăng xuất".

**Các bước**
1. Mở `/login?next=%2F%2Fevil.example` (tức `//evil.example`), đăng nhập `mio`.
   - Mong đợi: Trang chuyển sang `http://localhost:3000/`, không rời khỏi app.
   - 📷 Chụp evidence.
2. Thử `next=%2F%5Cevil.example` (tức `/\evil.example`).
   - Mong đợi: Trang chuyển sang `/`.
   - 📷 Chụp evidence.
3. Thử `next=https%3A%2F%2Fevil.example`.
   - Mong đợi: Trang chuyển sang `/`.
4. Thử `next=evil`, giá trị không bắt đầu bằng `/`.
   - Mong đợi: Trang chuyển sang `/`.
5. Thử `next=%2Flogin`.
   - Mong đợi: Trang chuyển sang `/`.
6. Thử `next=%2Fkhong-co`.
   - Mong đợi: Trang chuyển sang `/khong-co` và hiện màn hình Không tìm thấy trang. Đường dẫn này hợp lệ dù không có trang.
7. Đăng nhập không kèm `next`.
   - Mong đợi: Trang chuyển sang `/`.
8. Thử `next=%2F%09%2Fevil.example` (dấu `/`, ký tự tab, rồi `/evil.example`) và `next=%2F%0A%2Fevil.example` (có ký tự xuống dòng).
   - Mong đợi: Cả hai chuyển sang `/`, không rời app.
   - 📷 Chụp evidence.

<!-- src-section: 207a10d44c 1c5992b726ea -->
## P0-AUT-039 Đã đăng nhập mà mở trang Đăng nhập

**Kiểm tra điều gì.** Người đã đăng nhập mở trang Đăng nhập thì được chuyển về `/` và không thấy form.

**Thông tin**
- Thiết kế: R-AUT-28.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`.

**Các bước**
1. Gõ `/login` vào thanh địa chỉ.
   - Mong đợi: Trang chuyển sang `/`, không hiện form Đăng nhập.
2. Gõ `/login?next=%2Faccount%2Fpassword`.
   - Mong đợi: Trang chuyển sang `/`.
3. Từ `/`, bấm Back để về mục lịch sử `/login`.
   - Mong đợi: Trang lại chuyển sang `/`.

<!-- src-section: 99613b67f1 bf1073c00ca0 -->
## P0-AUT-040 Quyền của route API khi chưa đăng nhập

**Kiểm tra điều gì.** Mọi operation API đều đòi đăng nhập, trừ ba route công khai. Địa chỉ API không tồn tại trả 404, và file tĩnh của web không cần cookie.

**Thông tin**
- Thiết kế: R-AUT-14, R-AUT-16, R-SKL-14.
- Khía cạnh: Phân quyền. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không có cookie.

**Các bước**
1. Gọi mọi operation trong `docs/design/api/openapi.yaml` không kèm cookie, có `<origin>`, kèm thân hợp lệ nếu cần.
   - Mong đợi: Mọi operation trả 401 `UNAUTHENTICATED`, trừ ba route công khai:
     `GET /api/v1/health` trả 200, `POST /api/v1/sessions` trả 201 với `mio`, `DELETE /api/v1/sessions/current` trả 204.
   - 📷 Chụp evidence.
2. Gọi `GET <api>/khong-co` và `POST <api>/khong-co`.
   - Mong đợi: Cả hai trả 404 `NOT_FOUND` với "Không tìm thấy địa chỉ yêu cầu", không phải 401.
3. Gọi `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/` và một file trong `/assets/`.
   - Mong đợi: Cả hai trả `200`, không cần cookie.

<!-- src-section: cf52952c75 36c52a52d43b -->
## P0-AUT-041 Thợ mở thẳng trang chỉ dành cho Quản lý

**Kiểm tra điều gì.** Thợ gõ thẳng địa chỉ trang chỉ dành cho Quản lý thì thấy màn hình Không có quyền ngay trong khung app.

**Thông tin**
- Thiết kế: R-AUT-29; mục Màn hình Không có quyền.
- Khía cạnh: Phân quyền. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Đã có `group-settings` (`/settings`) và `emergency-stop` (`/system-log`).
- Web đăng nhập `ngocanh.nail`.

**Các bước**
1. Gõ `/settings` vào thanh địa chỉ.
   - Mong đợi: Trong khung app hiện tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý." và nút "Về Trang chính". Địa chỉ vẫn là `/settings`. Không mục điều hướng nào được chọn.
   - 📷 Chụp evidence.
2. Gõ `/system-log`, rồi gõ một trang con của Cài đặt (ví dụ `/settings/groups`).
   - Mong đợi: Kết quả như bước 1.
3. Bấm "Về Trang chính".
   - Mong đợi: Trang chuyển sang `/`.

<!-- src-section: 35f70b9a73 bcedfdaf671a -->
## P0-AUT-042 Thợ gọi thẳng API chỉ dành cho Quản lý

**Kiểm tra điều gì.** Thợ gọi thẳng API chỉ dành cho Quản lý thì nhận 403 và dữ liệu không đổi. Vai trò được kiểm trước dữ liệu gửi lên.

**Thông tin**
- Thiết kế: R-AUT-15, R-AUT-16.
- Khía cạnh: Phân quyền. Kỹ thuật: bảng quyết định.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Có ít nhất một endpoint chỉ Quản lý, của `group-settings` hoặc `crawl-settings`, ví dụ `GET`/`PUT /api/v1/settings/<khóa>`.
- Chạy `<đăng nhập ngocanh>` và `<đăng nhập mio>`.

**Các bước**
1. Thợ gọi `GET` endpoint đó.
   - Mong đợi: API trả 403 với `{"code":"FORBIDDEN","message":"Bạn không có quyền thực hiện thao tác này"}`.
   - 📷 Chụp evidence.
2. Thợ gọi `PUT`/`POST` có `<origin>` với thân sai quy tắc.
   - Mong đợi: API trả 403 `FORBIDDEN`, không phải 400, vì vai trò được kiểm trước dữ liệu.
3. Thợ gọi `PUT`/`POST` với thân hợp lệ.
   - Mong đợi: API trả 403. Dữ liệu trong DB không đổi.
   - 📷 Chụp evidence.
4. Quản lý gọi như bước 1.
   - Mong đợi: API trả 200.

<!-- src-section: 517a23ddaf d3a54f7695ce -->
## P0-AUT-043 Thanh điều hướng của Quản lý đủ mục

**Kiểm tra điều gì.** Thanh điều hướng của Quản lý có đủ các mục dành cho Quản lý. Thợ thì chỉ thấy "Trang chính".

**Thông tin**
- Thiết kế: R-AUT-29; mục Khung app.
- Khía cạnh: Hiển thị. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Như P0-AUT-041.
- Web đăng nhập `mio`.

**Các bước**
1. Xem thanh điều hướng.
   - Mong đợi: Thanh có "Trang chính", đường kẻ, "Cài đặt", "Nhật ký hệ thống", rồi tới khối tài khoản.
   - 📷 Chụp evidence.
2. Bấm "Cài đặt".
   - Mong đợi: Trang chuyển sang `/settings`. Mục "Cài đặt" đang được chọn (`aria-current="page"`).
3. Đăng nhập `ngocanh.nail` ở context khác.
   - Mong đợi: Thanh điều hướng chỉ có "Trang chính".

<!-- src-section: ba5361499a 29a9121f25ce -->
## P0-AUT-044 API trả 403 khi đang thao tác

**Kiểm tra điều gì.** Khi vai trò bị đổi trong lúc đang dùng app, thao tác tiếp theo nhận 403. Web báo lỗi đúng vị trí, rồi cập nhật giao diện theo vai trò mới mà không cần tải lại.

**Thông tin**
- Thiết kế: R-AUT-29; `ui-style.md` mục "Vị trí thông báo".
- Khía cạnh: Phân quyền. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Như P0-AUT-042.
- Web đăng nhập `mio`, mở một màn hình Cài đặt có form và nút lưu.

**Các bước**
1. Chạy `<psql> "update users set role = 'technician' where username = 'mio'"`. Không tải lại trang.
   - Mong đợi: Vai trò của `mio` trong DB đổi thành Thợ.
2. Sửa một trường, bấm nút lưu.
   - Mong đợi: API trả 403. Banner danger "Bạn không có quyền thực hiện thao tác này" hiện ở vùng thông báo ngay trên hàng nút của form, không phải toast. Dữ liệu trên form giữ nguyên.
   - 📷 Chụp evidence.
3. Xem trang ngay sau đó, không tải lại.
   - Mong đợi: Thanh điều hướng chỉ còn "Trang chính". Khối tài khoản có badge "Thợ". Vùng nội dung chuyển sang màn hình Không có quyền, đường dẫn giữ nguyên.
   - 📷 Chụp evidence.
4. Nếu đã có thao tác chỉ dành cho Quản lý mà không có form (nút trong danh sách, công tắc): làm lại bước 1, bấm thao tác đó, rồi bấm "Đóng" trên toast. Nếu chưa có thao tác như vậy thì ghi `không áp dụng` cho bước này.
   - Mong đợi: Toast danger cùng câu hiện ở góc dưới phải, không tự ẩn và có nút "Đóng". Bấm "Đóng" thì toast biến mất.
5. Đặt lại `role = 'manager'`.
   - Mong đợi: `mio` trở lại vai trò Quản lý.

<!-- src-section: 34ba900de8 92bc99834bc3 -->
## P0-AUT-045 Thứ tự kiểm tra: Origin, rồi phiên, rồi dữ liệu

**Kiểm tra điều gì.** Request ghi được kiểm theo thứ tự: Origin trước, rồi phiên, rồi dữ liệu. Riêng việc đọc thân JSON xảy ra sau khi kiểm Origin và trước khi kiểm phiên.

**Thông tin**
- Thiết kế: R-AUT-15 (thứ tự kiểm tra), R-AUT-17, R-AUT-11, R-SKL-15.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: bảng quyết định.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.
- Mọi bước đều gọi `POST <api>/users/me/change-password` với thân `{}`, trừ khi bước ghi khác.

**Các bước**
1. Gửi với `Origin: http://evil.example`, không cookie.
   - Mong đợi: API trả 403 `INVALID_ORIGIN`.
   - 📷 Chụp evidence.
2. Gửi với `<origin>`, không cookie.
   - Mong đợi: API trả 401 `UNAUTHENTICATED`.
3. Gửi với `<origin>`, cookie `mio.jar`.
   - Mong đợi: API trả 400 `VALIDATION_ERROR` với "Dữ liệu đổi mật khẩu không hợp lệ". Trường `fields` là `{"currentPassword":"Nhập mật khẩu hiện tại","newPassword":"Nhập mật khẩu mới","signOutOtherDevices":"Chọn có đăng xuất các thiết bị khác hay không"}`.
   - 📷 Chụp evidence.
4. Gửi không có header `Origin`, cookie `mio.jar`.
   - Mong đợi: Kết quả như bước 3.
5. Thứ tự giữa kiểm vai trò và kiểm dữ liệu được kiểm ở P0-AUT-042 bước 2.
   - Mong đợi: Xem P0-AUT-042.
6. Gửi với `Origin: http://evil.example`, không cookie, thân là JSON hỏng `{"currentPassword":`.
   - Mong đợi: API trả 403 `INVALID_ORIGIN`, vì Origin được kiểm trước khi đọc thân.
   - 📷 Chụp evidence.
7. Gửi với `<origin>`, không cookie, thân là JSON hỏng.
   - Mong đợi: API trả 400 `INVALID_JSON`, vì thân được đọc trước khi kiểm phiên.

<!-- src-section: acd3d95c09 3ea9727bf6e2 -->
## P0-AUT-046 Chống CSRF: so origin của request ghi

**Kiểm tra điều gì.** Request ghi có `Origin` khác địa chỉ của app bị từ chối, để chống CSRF. Request GET không bị kiểm. Request bị chặn không được đếm là lần đăng nhập sai.

**Thông tin**
- Thiết kế: R-AUT-17.
- Khía cạnh: Phân quyền. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.
- Bước 1–3 gọi `POST <api>/sessions` với thân đăng nhập đúng của `mio`.

**Các bước**
1. Gửi với `Origin: http://evil.example`.
   - Mong đợi: API trả 403 với `{"code":"INVALID_ORIGIN","message":"Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000"}`. Không có `Set-Cookie` và không có phiên nào được tạo.
   - 📷 Chụp evidence.
2. Gửi lần lượt với `Origin: http://localhost:3001` (khác cổng), `https://localhost:3000` (khác scheme), `http://127.0.0.1:3000` (khác host).
   - Mong đợi: Cả ba đều trả 403 `INVALID_ORIGIN`.
3. Gửi với `Origin: http://localhost:3000`. Sau đó gửi không có header `Origin`.
   - Mong đợi: Cả hai trả 201.
4. Gọi `DELETE <api>/sessions/current` với cookie hợp lệ và `Origin: http://evil.example`.
   - Mong đợi: API trả 403. Phiên vẫn còn trong DB.
5. Gọi `GET <api>/sessions/current` với cookie hợp lệ và `Origin: http://evil.example`.
   - Mong đợi: API trả 200, vì GET không bị kiểm.
6. Chạy `<psql> "select count(*) from login_throttles"`.
   - Mong đợi: Kết quả là `0`. Request bị chặn ở bước 1–2 không được đếm.

<!-- src-section: 15663273b2 22f393437121 -->
## P0-AUT-047 Mở app bằng địa chỉ khác `PUBLIC_URL`

**Kiểm tra điều gì.** Mở app bằng địa chỉ khác `PUBLIC_URL` thì không đăng nhập được. Web báo người dùng mở lại bằng đúng địa chỉ.

**Thông tin**
- Thiết kế: R-AUT-17; mục Màn hình Đăng nhập (vùng thông báo).
- Khía cạnh: Phân quyền. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- `PUBLIC_URL` là `http://localhost:3000`.

**Các bước**
1. Mở `http://127.0.0.1:3000/login`, đăng nhập `mio` đúng mật khẩu.
   - Mong đợi: Banner danger hiện "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000". Ô Tên giữ `mio`, ô Mật khẩu bị xóa.
   - 📷 Chụp evidence.
2. Chạy `<psql> "select count(*) from user_sessions where created_at > now() - interval '1 minute'"`.
   - Mong đợi: Kết quả là `0`.

<!-- src-section: 0e5f326f2b 43fd5833886c -->
## P0-AUT-048 Đăng nhập qua Vite dev server

**Kiểm tra điều gì.** Khi chạy web bằng Vite dev server, đăng nhập và đăng xuất vẫn hoạt động. Lý do là Vite proxy đặt lại `Origin`.

**Thông tin**
- Thiết kế: mục `apps/web` (Dev: Vite proxy đặt lại `Origin`), R-AUT-17, R-AUT-32.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: tình huống thực tế.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- api chạy ở cổng 3000.
- Chạy `pnpm --filter @mio/web dev`. Cổng do Vite in ra, mặc định là 5173.

**Các bước**
1. Mở `http://localhost:5173/login`, đăng nhập `mio`.
   - Mong đợi: Người dùng vào `/`. Không có banner `INVALID_ORIGIN`.
   - 📷 Chụp evidence.
2. Bấm "Đăng xuất".
   - Mong đợi: Trang chuyển sang `/login` với banner "Bạn đã đăng xuất".

<!-- src-section: 2e4ddeec46 1fdbbab83087 -->
## P0-AUT-049 Header bảo mật và chặn nhúng khung

**Kiểm tra điều gì.** Mọi response đều có các header bảo mật. Response liên quan đến phiên và mật khẩu không được cache. Trang không nhúng được vào iframe của trang khác.

**Thông tin**
- Thiết kế: R-AUT-18.
- Khía cạnh: Phân quyền. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.

**Các bước**
1. Gọi `curl -s -D -` tới `/`, `/assets/<một file>`, `<api>/health`, `<api>/khong-co`, và `POST <api>/sessions` với mật khẩu sai.
   - Mong đợi: Response nào cũng có `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`.
   - 📷 Chụp evidence.
2. Xem header của các response sau: `POST <api>/sessions` (201, 400, 401, 429), `GET`/`DELETE <api>/sessions/current` (200, 401, 204), `POST <api>/users/me/change-password` (204, 400).
   - Mong đợi: Tất cả đều có `Cache-Control: no-store`.
3. Dùng Playwright mở một file HTML cục bộ chứa `<iframe src="http://localhost:3000/login">`.
   - Mong đợi: Khung không hiển thị trang Đăng nhập. Console báo bị chặn do `X-Frame-Options`.
   - 📷 Chụp evidence.

<!-- src-section: 1a8b1cd461 e67cf2b4ca1f -->
## P0-AUT-050 Đổi mật khẩu và đăng xuất các thiết bị khác

**Kiểm tra điều gì.** Người dùng đổi mật khẩu và chọn đăng xuất các thiết bị khác. Thiết bị hiện tại nhận phiên mới và ở lại app. Mọi phiên khác bị xóa, và mật khẩu cũ không dùng được nữa.

**Thông tin**
- Thiết kế: R-AUT-23, R-AUT-34, R-AUT-31, R-AUT-30; mục Màn hình Đổi mật khẩu.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.
- Context A và B đăng nhập `mio`. B đang ở `/account/password`.
- Ghi lại `password_hash` và cookie của A.

**Các bước**
1. Ở A, bấm "Đổi mật khẩu" trong khối tài khoản.
   - Mong đợi: Trang chuyển sang `/account/password`, mục "Đổi mật khẩu" đang được chọn. Ba ô trống. Dưới ô Mật khẩu mới có gợi ý "Ít nhất 8 ký tự".
   - 📷 Chụp evidence.
2. Nhập `MioQuanLy#2026`, `MioMoi#2026x`, `MioMoi#2026x`, rồi bấm "Đổi mật khẩu".
   - Mong đợi: Hộp thoại hiện ra với tiêu đề "Đổi mật khẩu" và nội dung "Bạn có muốn đăng xuất khỏi các thiết bị khác đang đăng nhập tài khoản này không? Nên chọn đăng xuất nếu bạn nghi có người khác biết mật khẩu cũ.".
   - Mong đợi: Hộp thoại có ba nút "Đổi và đăng xuất thiết bị khác", "Chỉ đổi mật khẩu", "Hủy". Nút đầu đang được focus.
   - 📷 Chụp evidence.
3. Bấm "Đổi và đăng xuất thiết bị khác".
   - Mong đợi: Request có `"signOutOtherDevices":true`. Response trả 204 kèm `Set-Cookie` mới. Hộp thoại đóng, ba ô trống, trang giữ nguyên. Toast success hiện "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất.".
   - 📷 Chụp evidence.
4. Kiểm DB, rồi dùng cookie cũ của A gọi `GET <api>/sessions/current`.
   - Mong đợi: `password_hash` khác giá trị cũ. `user_sessions` của `mio` còn đúng 1 dòng, `token_hash` bằng SHA-256 của cookie mới của A. Lệnh gọi bằng cookie cũ trả 401.
   - 📷 Chụp evidence.
5. Tải lại A.
   - Mong đợi: A vẫn ở trong app.
6. Ở B, nhập form hợp lệ và gửi qua hộp thoại.
   - Mong đợi: API trả 401. Trang chuyển sang `/login?next=%2Faccount%2Fpassword` với banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại".
   - 📷 Chụp evidence.
7. Đăng nhập `mio` bằng `MioQuanLy#2026`, rồi bằng `MioMoi#2026x`.
   - Mong đợi: Mật khẩu cũ trả 401. Mật khẩu mới trả 201.
8. Chạy `<log auth>`.
   - Mong đợi: Có dòng `auth.password.changed` với `userId` và `"signedOutOtherDevices":true`.
9. Đặt lại mật khẩu `mio` về `MioQuanLy#2026`.
   - Mong đợi: Đăng nhập lại được bằng mật khẩu mẫu.

<!-- src-section: fc92be0736 05a7392b7408 -->
## P0-AUT-051 Chỉ đổi mật khẩu, giữ phiên thiết bị khác

**Kiểm tra điều gì.** Người dùng chọn "Chỉ đổi mật khẩu" thì phiên của thiết bị khác được giữ nguyên. Thiết bị hiện tại vẫn nhận phiên mới.

**Thông tin**
- Thiết kế: R-AUT-23, R-AUT-34.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Như P0-AUT-050.
- Ghi lại `token_hash`, `expires_at` của phiên B.

**Các bước**
1. Ở A, làm như P0-AUT-050 bước 2, rồi bấm "Chỉ đổi mật khẩu".
   - Mong đợi: Request có `"signOutOtherDevices":false` và trả 204. Toast hiện "Đã đổi mật khẩu.".
   - 📷 Chụp evidence.
2. Kiểm DB.
   - Mong đợi: Phiên của B còn nguyên `token_hash`, `expires_at`. Phiên cũ của A được thay bằng phiên mới, tổng vẫn là 2.
3. Tải lại B.
   - Mong đợi: B vẫn ở trong app.
   - 📷 Chụp evidence.
4. Chạy `<log auth>`. Sau đó đặt lại mật khẩu.
   - Mong đợi: Có dòng `auth.password.changed` với `"signedOutOtherDevices":false`.

<!-- src-section: 98ce1df89f 37e43e9bb6b1 -->
## P0-AUT-052 Hủy hộp thoại xác nhận không gửi gì

**Kiểm tra điều gì.** Đóng hộp thoại xác nhận bằng mọi cách đều không gửi request và giữ nguyên dữ liệu trên form.

**Thông tin**
- Thiết kế: R-AUT-34; mục Màn hình Đổi mật khẩu.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`, ba ô đã nhập hợp lệ.
- Ghi lại `password_hash`.

**Các bước**
1. Bấm "Đổi mật khẩu" để mở hộp thoại, rồi nhấn Esc.
   - Mong đợi: Hộp thoại đóng. Ba ô giữ nguyên giá trị. Tab Network không có request `change-password`.
2. Mở lại hộp thoại, bấm ra ngoài hộp thoại.
   - Mong đợi: Kết quả như bước 1.
3. Mở lại hộp thoại, bấm "Hủy".
   - Mong đợi: Kết quả như bước 1.
   - 📷 Chụp evidence.
4. Kiểm `password_hash`.
   - Mong đợi: `password_hash` không đổi.

<!-- src-section: c88a69a3d5 c976a8965cbd -->
## P0-AUT-053 Đang gửi: khóa nút, không đóng được, bấm nhiều lần chỉ gửi một lần

**Kiểm tra điều gì.** Trong lúc đang gửi, nút bị khóa và hộp thoại không đóng được. Bấm nhiều lần chỉ tạo một request.

**Thông tin**
- Thiết kế: mục Màn hình Đăng nhập (nút đang gửi), mục Màn hình Đổi mật khẩu (loading).
- Khía cạnh: Thao tác đồng thời. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Giả lập mạng chậm 3 giây.
- Chạy `<psql> "delete from user_sessions"`.

**Các bước**
1. Ở `/login`, nhập `mio` với mật khẩu đúng, bấm "Đăng nhập" ba lần thật nhanh.
   - Mong đợi: Nút đổi thành "Đang đăng nhập…" có vòng xoay và không bấm được.
   - 📷 Chụp evidence.
2. Chờ request xong.
   - Mong đợi: Người dùng vào `/`. Tab Network chỉ có 1 request `POST /api/v1/sessions`. DB có đúng 1 phiên của `mio`.
3. Ở `/account/password`, nhập form hợp lệ, mở hộp thoại, bấm "Đổi và đăng xuất thiết bị khác".
   - Mong đợi: Nút đó đổi thành "Đang lưu…". Nút "Chỉ đổi mật khẩu" và "Hủy" không bấm được.
   - 📷 Chụp evidence.
4. Trong lúc chờ, bấm lại nút, nhấn Esc và bấm ra ngoài.
   - Mong đợi: Hộp thoại vẫn mở. Không có request thứ hai.
5. Chờ request xong. Sau đó tắt giả lập và đặt lại mật khẩu.
   - Mong đợi: Toast success hiện ra. Tab Network chỉ có 1 request `change-password`.

<!-- src-section: e3bf592b0d 58d4d6550b25 -->
## P0-AUT-054 Màn hình Đổi mật khẩu, Không có quyền, Không tìm thấy khớp mockup

**Kiểm tra điều gì.** Người kiểm so ảnh chụp thật với mockup của các màn hình Đổi mật khẩu, Không có quyền và Không tìm thấy trang.

**Thông tin**
- Thiết kế: mục Màn hình Đổi mật khẩu, Không có quyền, Không tìm thấy trang; mockup `change-password/`, `forbidden/`, `not-found/`.
- Khía cạnh: Hiển thị. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: người.

**Chuẩn bị**
- Đã có ảnh evidence của P0-AUT-041, 050, 051, 052, 053, 055, 056, 058, 060, 061, 063, 072, 078.

**Các bước**
1. So ảnh với `docs/design/ui/change-password/screenshots/` cùng trạng thái.
   - Mong đợi: Bố cục, chữ và lỗi dưới ô khớp mockup. Banner nằm ngay sau ô Nhập lại mật khẩu mới và trước nút "Đổi mật khẩu". Toast ở góc dưới phải.
   - 📷 Chụp evidence.
2. So ảnh P0-AUT-041 với `forbidden/screenshots/`, ảnh P0-AUT-078 với `not-found/screenshots/`.
   - Mong đợi: Các ảnh khớp mockup.

<!-- src-section: 1a31fc55ad 832543bf724f -->
## P0-AUT-055 Bỏ trống cả ba ô đổi mật khẩu

**Kiểm tra điều gì.** Bấm "Đổi mật khẩu" khi ba ô còn trống thì web báo lỗi dưới từng ô, không mở hộp thoại và không gửi request. Mỗi ô có nút Hiện/Ẩn riêng.

**Thông tin**
- Thiết kế: R-AUT-19, R-AUT-21, R-AUT-22.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.

**Các bước**
1. Để trống ba ô, bấm "Đổi mật khẩu".
   - Mong đợi: Dưới từng ô lần lượt hiện "Nhập mật khẩu hiện tại", "Nhập mật khẩu mới", "Nhập lại mật khẩu mới". Hộp thoại không mở. Không có request.
   - 📷 Chụp evidence.
2. Bấm "Hiện" ở ô Mật khẩu mới.
   - Mong đợi: Ba ô đều có nút Hiện/Ẩn riêng. Chỉ ô Mật khẩu mới hiện ký tự.

<!-- src-section: fa21bae8f5 3fc63cc1a6b2 -->
## P0-AUT-056 Độ dài mật khẩu mới

**Kiểm tra điều gì.** Mật khẩu mới dài từ 8 đến 128 ký tự, tính theo code point. API cũng từ chối mật khẩu mới sai kiểu.

**Thông tin**
- Thiết kế: R-AUT-21 (độ dài theo code point, sai kiểu).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.
- Sau mỗi lần đổi thành công, lần sau dùng mật khẩu vừa đặt làm Mật khẩu hiện tại.
- Ô Nhập lại luôn giống Mật khẩu mới.

**Các bước**
1. Nhập Mật khẩu mới `Abcd#12` (7 ký tự), gửi form.
   - Mong đợi: Dưới ô hiện "Mật khẩu mới phải từ 8 đến 128 ký tự". Hộp thoại không mở.
   - 📷 Chụp evidence.
2. Nhập `Abcd#123` (8 ký tự), gửi form, rồi bấm "Chỉ đổi mật khẩu".
   - Mong đợi: Hộp thoại mở. Sau khi bấm, toast hiện "Đã đổi mật khẩu.".
3. Nhập mật khẩu gồm 128 ký tự `x`, rồi mật khẩu gồm 129 ký tự `y`.
   - Mong đợi: 128 ký tự đổi thành công. 129 ký tự báo lỗi như bước 1.
4. Nhập mật khẩu gồm 8 ký tự `😀`, rồi 7 ký tự `😀` (14 đơn vị UTF-16).
   - Mong đợi: 8 ký tự đổi thành công. 7 ký tự báo lỗi như bước 1.
5. Gọi API với `newPassword` dài 7 ký tự, các trường khác hợp lệ.
   - Mong đợi: API trả 400, `message` là "Dữ liệu đổi mật khẩu không hợp lệ", `fields.newPassword` là "Mật khẩu mới phải từ 8 đến 128 ký tự".
6. Gọi API với `newPassword` là số `12345678`, rồi là `null`.
   - Mong đợi: Mỗi lần trả 400, `fields.newPassword` là "Nhập mật khẩu mới".
7. Đặt lại mật khẩu `mio`.
   - Mong đợi: Đăng nhập lại được bằng mật khẩu mẫu.

<!-- src-section: 4bcc309261 dd44585421bd -->
## P0-AUT-057 Mật khẩu hiện tại quá dài hoặc trống

**Kiểm tra điều gì.** Mật khẩu hiện tại dài tối đa 128 ký tự và không được trống hay sai kiểu.

**Thông tin**
- Thiết kế: R-AUT-19.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.

**Các bước**
1. Nhập Mật khẩu hiện tại gồm 129 ký tự `x`, hai ô kia hợp lệ, gửi form.
   - Mong đợi: Dưới ô Mật khẩu hiện tại hiện "Mật khẩu tối đa 128 ký tự". Hộp thoại không mở.
2. Nhập Mật khẩu hiện tại gồm 128 ký tự `x`, gửi form và xác nhận trong hộp thoại.
   - Mong đợi: Hộp thoại mở. Sau khi gửi, web báo "Mật khẩu hiện tại không đúng".
3. Gọi API với `currentPassword` là `""`, rồi là số `123`.
   - Mong đợi: Cả hai lần `fields.currentPassword` đều là "Nhập mật khẩu hiện tại".

<!-- src-section: aa76d5cf26 e65fceba57b5 -->
## P0-AUT-058 Mật khẩu mới trùng tên đăng nhập

**Kiểm tra điều gì.** Mật khẩu mới không được trùng tên đăng nhập, không phân biệt hoa thường.

**Thông tin**
- Thiết kế: R-AUT-21.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `ngocanh.nail`, ở `/account/password`.
- Mật khẩu hiện tại là `NgocAnh#2026`.

**Các bước**
1. Nhập Mật khẩu mới và Nhập lại là `NgocAnh.Nail`, gửi form.
   - Mong đợi: Dưới ô Mật khẩu mới hiện "Mật khẩu không được trùng tên đăng nhập". Hộp thoại không mở.
   - 📷 Chụp evidence.
2. Thử `ngocanh.nail`.
   - Mong đợi: Cùng lỗi như bước 1.
3. Thử `ngocanh.nail1`, rồi bấm "Hủy" trong hộp thoại.
   - Mong đợi: Không có lỗi, hộp thoại mở.
4. Gọi API với `newPassword` là `NGOCANH.NAIL`.
   - Mong đợi: API trả 400, `fields.newPassword` là "Mật khẩu không được trùng tên đăng nhập".

<!-- src-section: 394203fdc8 ac9f93961d22 -->
## P0-AUT-059 Nhập lại mật khẩu mới trống hoặc không khớp

**Kiểm tra điều gì.** Ô Nhập lại mật khẩu mới phải có giá trị và khớp nguyên văn với Mật khẩu mới.

**Thông tin**
- Thiết kế: R-AUT-22.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.
- Mật khẩu hiện tại đúng, Mật khẩu mới là `MioMoi#2026x`.

**Các bước**
1. Để trống ô Nhập lại, gửi form.
   - Mong đợi: Web báo "Nhập lại mật khẩu mới". Hộp thoại không mở.
2. Nhập lại `MioMoi#2026X` (khác một chữ hoa), gửi form.
   - Mong đợi: Web báo "Mật khẩu nhập lại không khớp".
   - 📷 Chụp evidence.
3. Nhập lại `MioMoi#2026x ` (thừa khoảng trắng cuối), gửi form.
   - Mong đợi: Web báo "Mật khẩu nhập lại không khớp".

<!-- src-section: 233bc2026f ae74651b65a0 -->
## P0-AUT-060 Mật khẩu hiện tại không đúng

**Kiểm tra điều gì.** Nhập sai mật khẩu hiện tại thì web báo lỗi dưới ô và giữ dữ liệu. Lần sai được đếm vào bộ đếm đăng nhập sai và ghi log.

**Thông tin**
- Thiết kế: R-AUT-20, R-AUT-30.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.
- Không có dòng `login_throttles`.

**Các bước**
1. Nhập Mật khẩu hiện tại `sai-mat-khau`, Mật khẩu mới và Nhập lại là `MioMoi#2026x`, gửi qua hộp thoại.
   - Mong đợi: Hộp thoại đóng. Dưới ô Mật khẩu hiện tại hiện "Mật khẩu hiện tại không đúng". Ba ô giữ dữ liệu.
   - 📷 Chụp evidence.
2. Xem response.
   - Mong đợi: API trả 400 với `{"code":"VALIDATION_ERROR","message":"Dữ liệu đổi mật khẩu không hợp lệ","fields":{"currentPassword":"Mật khẩu hiện tại không đúng"}}`.
3. Kiểm DB, rồi tải lại trang.
   - Mong đợi: Dòng `mio` trong `login_throttles` có `failed_count` là 1. `password_hash` không đổi. Sau khi tải lại, người dùng vẫn ở trong app.
4. Chạy `<log auth>`.
   - Mong đợi: Có dòng `auth.password.change_failed` mức warn với `userId`, `"username":"mio"`, `"reason":"current_password_incorrect"`, `"failedCount":1`.
   - 📷 Chụp evidence.

<!-- src-section: e6c8415dbd 5d404394602e -->
## P0-AUT-061 Mật khẩu mới giống mật khẩu hiện tại

**Kiểm tra điều gì.** Mật khẩu mới phải khác mật khẩu hiện tại. Lỗi này không được đếm là lần nhập sai và không làm đổi phiên.

**Thông tin**
- Thiết kế: R-AUT-21.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`.
- Không có dòng `login_throttles`.

**Các bước**
1. Nhập cả ba ô là `MioQuanLy#2026`, gửi form và xác nhận trong hộp thoại.
   - Mong đợi: Web mở hộp thoại. Sau khi gửi, hộp thoại đóng và dưới ô Mật khẩu mới hiện "Mật khẩu mới phải khác mật khẩu hiện tại".
   - 📷 Chụp evidence.
2. Kiểm DB.
   - Mong đợi: Không có dòng `mio` trong `login_throttles`. `password_hash` và phiên không đổi.

<!-- src-section: fcf8213f27 5357da4fd375 -->
## P0-AUT-062 Thứ tự kiểm tra khi đổi mật khẩu

**Kiểm tra điều gì.** Khi đổi mật khẩu, hệ thống kiểm hình thức dữ liệu trước, rồi tới khóa, rồi tới mật khẩu hiện tại. Quy tắc "khác mật khẩu hiện tại" chỉ được kiểm sau khi mật khẩu hiện tại đúng.

**Thông tin**
- Thiết kế: R-AUT-21 (thứ tự), R-AUT-20.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: bảng quyết định.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.
- Không có dòng `login_throttles`.
- Mọi bước gọi `POST <api>/users/me/change-password` với `<origin>`, cookie `mio.jar`.

**Các bước**
1. Gửi `currentPassword` sai, `newPassword` là `abc`, thiếu `signOutOtherDevices`.
   - Mong đợi: API trả 400 có cùng lúc `fields.newPassword` "Mật khẩu mới phải từ 8 đến 128 ký tự" và `fields.signOutOtherDevices`. Không có `fields.currentPassword`. Không có dòng `mio` trong `login_throttles`.
   - 📷 Chụp evidence.
2. Chạy `<psql> "insert into login_throttles (username, failed_count, window_started_at, locked_until) values ('mio', 0, now(), now() + interval '10 minutes')"`. Gửi `newPassword` là `abc`.
   - Mong đợi: API trả 400 với lỗi hình thức như bước 1, vì hình thức được kiểm trước khóa.
3. Trong lúc đang khóa, gửi dữ liệu hợp lệ với `currentPassword` đúng.
   - Mong đợi: API trả 429 `LOGIN_LOCKED` với "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 10 phút.". `Retry-After` nằm trong khoảng 590–600. `password_hash` không đổi.
   - 📷 Chụp evidence.
4. Xóa khóa. Gửi `currentPassword` sai và `newPassword` cũng là chính chuỗi sai đó.
   - Mong đợi: Chỉ có `fields.currentPassword` "Mật khẩu hiện tại không đúng". Quy tắc "khác mật khẩu hiện tại" chưa được kiểm.

<!-- src-section: 4ca2a5ab65 d6de170f0669 -->
## P0-AUT-063 Khóa do nhập sai mật khẩu hiện tại

**Kiểm tra điều gì.** Nhập sai mật khẩu hiện tại 5 lần thì tên đăng nhập bị khóa, giống đăng nhập sai. Màn Đổi mật khẩu và màn Đăng nhập dùng chung một bộ đếm.

**Thông tin**
- Thiết kế: R-AUT-20, R-AUT-06, R-AUT-30.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context A đăng nhập `mio`, ở `/account/password`.
- Context B chưa đăng nhập.
- Không có dòng `login_throttles`.

**Các bước**
1. Ở A, gửi mật khẩu hiện tại sai 4 lần.
   - Mong đợi: Mỗi lần web báo "Mật khẩu hiện tại không đúng".
2. Gửi sai lần 5.
   - Mong đợi: Hộp thoại đóng. Banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." hiện ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu". Ba ô giữ dữ liệu.
   - 📷 Chụp evidence.
3. Ở A, sửa Mật khẩu hiện tại thành đúng rồi gửi lại.
   - Mong đợi: Banner khóa vẫn hiện. `password_hash` không đổi.
4. Ở B, đăng nhập `mio` đúng mật khẩu.
   - Mong đợi: Màn Đăng nhập hiện banner "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút.".
   - 📷 Chụp evidence.
5. Ở A, tải lại `/`.
   - Mong đợi: A vẫn ở trong app.
6. Chạy `<log auth>`.
   - Mong đợi: Có 5 dòng `auth.password.change_failed` với `"reason":"current_password_incorrect"`, `failedCount` từ 1 tới 5; dòng thứ 5 có `lockedUntil`.
   - Mong đợi: Có một dòng `auth.lock.started` với `"source":"change_password"`. Lần gửi ở bước 3 có dòng `auth.password.change_failed` với `"reason":"locked"` kèm `lockedUntil`.
   - 📷 Chụp evidence.
7. Xóa bộ đếm. Ở B, đăng nhập sai 3 lần. Ở A, nhập sai mật khẩu hiện tại 2 lần.
   - Mong đợi: Lần thứ 2 của A hiện banner khóa, vì hai màn dùng chung bộ đếm.

<!-- src-section: 7cff55d818 4487eb0dcd80 -->
## P0-AUT-064 `signOutOtherDevices` thiếu hoặc sai kiểu

**Kiểm tra điều gì.** API đổi mật khẩu bắt buộc có trường `signOutOtherDevices` kiểu boolean.

**Thông tin**
- Thiết kế: R-AUT-23.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập mio>`.
- Thân cơ sở là `{"currentPassword":"MioQuanLy#2026","newPassword":"MioMoi#2026x"}`.

**Các bước**
1. Gửi thân cơ sở, tức thiếu trường.
   - Mong đợi: API trả 400, `fields.signOutOtherDevices` là "Chọn có đăng xuất các thiết bị khác hay không". `password_hash` không đổi.
   - 📷 Chụp evidence.
2. Gửi lần lượt `"signOutOtherDevices":"true"` (chuỗi), `1`, `null`.
   - Mong đợi: Mỗi lần cho kết quả như bước 1.
3. Gửi `"signOutOtherDevices":true`. Sau đó đặt lại mật khẩu.
   - Mong đợi: API trả 204.

<!-- src-section: 005e587e4f 877794848c14 -->
## P0-AUT-065 Đổi mật khẩu thành công xóa bộ đếm đăng nhập sai

**Kiểm tra điều gì.** Đổi mật khẩu thành công xóa bộ đếm đăng nhập sai của tài khoản.

**Thông tin**
- Thiết kế: R-AUT-23.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context A đăng nhập `mio`.

**Các bước**
1. Ở context B, đăng nhập `mio` sai 3 lần.
   - Mong đợi: `failed_count` là 3.
2. Ở A, đổi mật khẩu thành công.
   - Mong đợi: Dòng `mio` không còn, hoặc `failed_count` là 0.
3. Ở B, đăng nhập sai 4 lần. Sau đó đặt lại mật khẩu.
   - Mong đợi: Cả 4 lần đều trả 401, tài khoản chưa bị khóa.

<!-- src-section: cce1c177a5 851f29609199 -->
## P0-AUT-066 Hai thiết bị đổi mật khẩu cùng lúc

**Kiểm tra điều gì.** Khi hai thiết bị đổi mật khẩu cùng lúc, chỉ một request thành công. Mật khẩu dùng được và các phiên còn lại đều thuộc về request thành công đó.

**Thông tin**
- Thiết kế: R-AUT-23 (xếp hàng bằng khóa dòng `users`), R-AUT-24.
- Khía cạnh: Thao tác đồng thời. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`.
- Hai jar `a.jar`, `b.jar` cùng đăng nhập `mio`.

**Các bước**
1. Gửi song song hai request: A với `newPassword` là `MoiCuaA#2026`, B với `MoiCuaB#2026`. Cả hai có `currentPassword` là `MioQuanLy#2026` và `signOutOtherDevices: true`.
   - Mong đợi: Đúng một request trả 204. Request kia trả 400 với `fields.currentPassword` "Mật khẩu hiện tại không đúng", hoặc trả 401. Không có 500.
   - 📷 Chụp evidence.
2. Đăng nhập thử bằng cả hai mật khẩu.
   - Mong đợi: Chỉ mật khẩu của request 204 đăng nhập được với mã 201.
3. Chạy `<psql> "select token_hash from user_sessions where user_id = <id mio>"`. So với SHA-256 của cookie trong response.
   - Mong đợi: Mọi phiên còn lại là phiên mới do request 204 tạo. Không còn phiên cũ của A hay B.
4. Lặp bước 1–3 thêm 4 lần. Giữa các lần, đặt lại mật khẩu, xóa `login_throttles` và đăng nhập lại.
   - Mong đợi: Lần nào cũng thỏa các mong đợi trên.
5. Lặp bước 1–2 với `signOutOtherDevices: false`.
   - Mong đợi: Vẫn chỉ đúng một request trả 204. Mật khẩu dùng được là của request đó.

<!-- src-section: f1f7765005 2a306777683f -->
## P0-AUT-067 Hai tab cùng trình duyệt sau khi đổi mật khẩu

**Kiểm tra điều gì.** Sau khi một tab đổi mật khẩu và đăng xuất thiết bị khác, tab còn lại trong cùng trình duyệt vẫn dùng được app. Hai tab dùng chung cookie mới.

**Thông tin**
- Thiết kế: R-AUT-23 (thiết bị hiện tại nhận phiên mới).
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Một context đăng nhập `mio`, mở hai tab: tab 1 ở `/account/password`, tab 2 ở `/`.

**Các bước**
1. Ở tab 1, đổi mật khẩu bằng "Đổi và đăng xuất thiết bị khác".
   - Mong đợi: Đổi mật khẩu thành công.
2. Ở tab 2, bấm "Đổi mật khẩu" trên thanh điều hướng rồi tải lại. Sau đó đặt lại mật khẩu.
   - Mong đợi: Tab 2 vẫn ở trong app, không bị đẩy về `/login`, vì hai tab dùng chung cookie mới.
   - 📷 Chụp evidence.

<!-- src-section: 2afa90860f 1fc498f32f54 -->
## P0-AUT-068 Lỗi hệ thống khi đăng nhập

**Kiểm tra điều gì.** Khi DB không hoạt động, đăng nhập báo lỗi hệ thống mà không làm sập api và không ghi mật khẩu vào log. Khi DB chạy lại, đăng nhập bình thường.

**Thông tin**
- Thiết kế: mục Xử lý lỗi; R-SKL-16, R-SKL-30.
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context mở `/login`.

**Các bước**
1. Chạy `docker compose stop postgres`.
   - Mong đợi: Container postgres dừng.
2. Đăng nhập `mio` đúng mật khẩu.
   - Mong đợi: Response là 500 `INTERNAL_ERROR`. Banner danger hiện "Lỗi hệ thống, vui lòng thử lại sau". Ô Tên giữ `mio`, ô Mật khẩu bị xóa.
   - 📷 Chụp evidence.
3. Chạy `docker compose ps` và xem log api.
   - Mong đợi: Container api vẫn chạy. Log api có dòng mức error, không chứa `MioQuanLy#2026`.
4. Chạy `docker compose start postgres`, chờ api `healthy`, rồi đăng nhập lại.
   - Mong đợi: Người dùng vào app.

<!-- src-section: 35a0b486f0 fd6b87059edf -->
## P0-AUT-069 Mất kết nối khi đăng nhập

**Kiểm tra điều gì.** Khi mất mạng hoặc api không chạy, đăng nhập báo không kết nối được và giữ dữ liệu đã nhập. Khi có mạng lại, đăng nhập bình thường.

**Thông tin**
- Thiết kế: mục Xử lý lỗi; mục Màn hình Đăng nhập (vùng thông báo).
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Context mở `/login`.
- Chạy `<psql> "delete from user_sessions"`.

**Các bước**
1. Nhập `mio` với mật khẩu đúng. Chạy `context.setOffline(true)`, rồi bấm "Đăng nhập".
   - Mong đợi: Banner danger hiện "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.". Cả hai ô giữ dữ liệu.
   - 📷 Chụp evidence.
2. Chạy `context.setOffline(false)`, bấm lại.
   - Mong đợi: Người dùng vào app. DB có đúng 1 phiên của `mio`.
3. Đăng xuất. Chạy `docker compose stop api`, rồi đăng nhập. Sau đó chạy `docker compose start api`.
   - Mong đợi: Banner giống bước 1.

<!-- src-section: 0fbf6db294 f45e8f3876fe -->
## P0-AUT-070 Trình duyệt chặn cookie

**Kiểm tra điều gì.** Khi trình duyệt chặn cookie, web báo người dùng bật cookie thay vì đăng nhập thất bại không lý do.

**Thông tin**
- Thiết kế: mục Xử lý lỗi (cookie bị tắt).
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: người.

**Chuẩn bị**
- Dùng Chrome thật.
- Vào Cài đặt › Quyền riêng tư và bảo mật › Cài đặt trang web › Cookie, chặn cookie cho `http://localhost:3000`.

**Các bước**
1. Mở `http://localhost:3000/login`, đăng nhập `mio` đúng mật khẩu.
   - Mong đợi: Banner danger hiện "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại.". Trang vẫn ở `/login`.
   - 📷 Chụp evidence.
2. Bật lại cookie, đăng nhập.
   - Mong đợi: Người dùng vào app.

<!-- src-section: 3e63a22de3 51d197f3ab95 -->
## P0-AUT-071 Mở app khi nạp phiên chậm, lỗi hoặc mất kết nối

**Kiểm tra điều gì.** Khi mở app, web hiện màn hình chờ trong lúc nạp phiên. Nếu nạp phiên lỗi hoặc mất kết nối, web hiện màn hình lỗi có nút "Thử lại" thay vì đẩy về trang Đăng nhập.

**Thông tin**
- Thiết kế: mục Khung app (màn hình chờ, màn hình lỗi, nút "Thử lại").
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`.

**Các bước**
1. Bật giả lập mạng chậm, tải lại `/`. Sau đó tắt giả lập.
   - Mong đợi: Màn hình chờ hiện logo "Mio", vòng xoay và "Đang tải…". Chưa có thanh điều hướng.
   - 📷 Chụp evidence.
2. Chạy `docker compose stop postgres`, tải lại `/`.
   - Mong đợi: Màn hình lỗi hiện "Lỗi hệ thống, vui lòng thử lại sau" với nút "Thử lại". Trang không chuyển sang `/login`.
   - 📷 Chụp evidence.
3. Chạy `docker compose stop api`, trang vẫn mở. Bấm "Thử lại".
   - Mong đợi: Thông báo đổi thành "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.".
   - 📷 Chụp evidence.
4. Chạy `docker compose start postgres api`, chờ `healthy`, rồi bấm "Thử lại".
   - Mong đợi: Màn hình chờ hiện ra, rồi tới Trang chính.

<!-- src-section: 6b3f4a50d6 cd1200e8e5e5 -->
## P0-AUT-072 Lỗi hệ thống và mất kết nối khi đổi mật khẩu

**Kiểm tra điều gì.** Khi đổi mật khẩu gặp lỗi hệ thống hoặc mất kết nối, web báo lỗi đúng vị trí và giữ dữ liệu. Khi gửi lại thành công, mật khẩu chỉ đổi một lần.

**Thông tin**
- Thiết kế: mục Màn hình Đổi mật khẩu (lỗi), mục Xử lý lỗi.
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/account/password`, ba ô hợp lệ.
- Ghi lại `password_hash`.

**Các bước**
1. Chạy `docker compose stop postgres`, gửi form qua hộp thoại.
   - Mong đợi: Hộp thoại đóng. Banner danger "Lỗi hệ thống, vui lòng thử lại sau" hiện ngay sau ô Nhập lại mật khẩu mới. Dữ liệu được giữ.
   - 📷 Chụp evidence.
2. Chạy `docker compose start postgres`, chờ `healthy`. Chạy `context.setOffline(true)`, rồi gửi.
   - Mong đợi: Banner hiện "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.". Dữ liệu được giữ.
3. Chạy `context.setOffline(false)`, gửi lại. Sau đó đặt lại mật khẩu.
   - Mong đợi: Toast success hiện ra. `password_hash` đổi đúng một lần.

<!-- src-section: 13e0a9ef36 06547c4a4491 -->
## P0-AUT-073 Tài khoản bị xóa trong DB khi đang đăng nhập

**Kiểm tra điều gì.** Khi tài khoản bị xóa trong DB, mọi phiên của tài khoản đó bị xóa theo. Thiết bị đang dùng bị đưa về trang Đăng nhập.

**Thông tin**
- Thiết kế: mục Thay đổi DB (`user_sessions.user_id` on delete cascade), R-AUT-11.
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Tạo `tam.thoi` (Thợ) bằng CLI.
- Web đăng nhập `tam.thoi`.

**Các bước**
1. Chạy `<psql> "delete from users where username = 'tam.thoi'"`. Sau đó chạy `<psql> "select count(*) from user_sessions s left join users u on u.id = s.user_id where u.id is null"`.
   - Mong đợi: Câu đếm trả `0`.
2. Tải lại trang.
   - Mong đợi: Trang chuyển sang `/login?next=%2F` kèm banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại". `GET /api/v1/sessions/current` trả 401.
   - 📷 Chụp evidence.
3. Chạy `<cli> list-users`.
   - Mong đợi: Danh sách không còn `tam.thoi`.

<!-- src-section: d63fc2d8c3 91916bb205d1 -->
## P0-AUT-074 Vai trò và tên hiển thị đổi trong DB khi đang đăng nhập

**Kiểm tra điều gì.** Vai trò và tên hiển thị được đọc lại từ DB ở mỗi request. Khi chúng đổi trong DB, web hiện giá trị mới sau khi tải lại.

**Thông tin**
- Thiết kế: mục Kiểm tra request (đọc `users` mỗi request), R-AUT-29.
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`, ở `/`.

**Các bước**
1. Chạy `<psql> "update users set role = 'technician', display_name = 'Mio Thử' where username = 'mio'"`.
   - Mong đợi: Vai trò và tên hiển thị của `mio` trong DB đã đổi.
2. Tải lại trang.
   - Mong đợi: Khối tài khoản hiện "Mio Thử" với badge "Thợ". `GET /api/v1/sessions/current` trả `"role":"technician"`.
   - 📷 Chụp evidence.
3. Đặt lại `role = 'manager'`, `display_name = 'Huỳnh Mio'`, rồi tải lại.
   - Mong đợi: Khối tài khoản hiện "Huỳnh Mio" và "Quản lý".

<!-- src-section: 49b2222098 2df4b34fe3d4 -->
## P0-AUT-075 Chuỗi băm mật khẩu trong DB bị hỏng

**Kiểm tra điều gì.** Khi chuỗi băm mật khẩu trong DB bị hỏng, đăng nhập trả lỗi hệ thống mà không lộ chi tiết. Lần thử không bị đếm là lần sai, và các tài khoản khác không bị ảnh hưởng.

**Thông tin**
- Thiết kế: mục Xử lý lỗi (chuỗi băm hỏng, R-SKL-16).
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: đoán lỗi.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Tạo `hong.hash` (Thợ) bằng CLI.

**Các bước**
1. Chạy `<psql> "update users set password_hash = 'khong-phai-phc' where username = 'hong.hash'"`.
   - Mong đợi: Chuỗi băm của `hong.hash` bị thay bằng giá trị hỏng.
2. Đăng nhập `hong.hash` với mật khẩu bất kỳ.
   - Mong đợi: API trả 500 `INTERNAL_ERROR` với "Lỗi hệ thống, vui lòng thử lại sau". Thân response không có chi tiết lỗi. api vẫn chạy.
   - 📷 Chụp evidence.
3. Chạy `<psql> "select count(*) from login_throttles where username = 'hong.hash'"`. Xem log api và chạy `<log auth>`.
   - Mong đợi: Câu SQL trả `0`. Log api có dòng mức error kèm `userId`, không chứa `khong-phai-phc`. `<log auth>` không có `auth.login.failed` cho `hong.hash`.
4. Đăng nhập `mio`.
   - Mong đợi: Đăng nhập bình thường.
5. Chạy `reset-password --username hong.hash`, rồi đăng nhập bằng mật khẩu mới.
   - Mong đợi: Đăng nhập được.

<!-- src-section: ad219f6ac4 bff966ff41e4 -->
## P0-AUT-076 Tên hiển thị dài, có dấu và emoji trên thanh điều hướng

**Kiểm tra điều gì.** Tên hiển thị dài tối đa, có dấu và emoji vẫn hiện đủ trên thanh điều hướng, xuống dòng và không làm vỡ bố cục.

**Thông tin**
- Thiết kế: mục Khung app; component `app-nav` (tên hiển thị 1–50 ký tự, xuống dòng khi dài).
- Khía cạnh: Hiển thị. Kỹ thuật: giá trị biên.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Tạo `ten.dai` (Thợ) với tên hiển thị đúng 50 ký tự gồm chữ có dấu và emoji.
- Ghi chuỗi đã dùng vào `results.md`.

**Các bước**
1. Đăng nhập `ten.dai`.
   - Mong đợi: Khối tài khoản hiện đủ 50 ký tự và xuống dòng. Tên không tràn khỏi thanh điều hướng. Trang không cuộn ngang. Badge "Thợ" không bị đè.
   - 📷 Chụp evidence.
2. Gọi `GET /api/v1/sessions/current`.
   - Mong đợi: `displayName` đúng chuỗi đã tạo.

<!-- src-section: 2c56869111 942765e8833e -->
## P0-AUT-077 Băm lại mật khẩu khi tham số băm cũ

**Kiểm tra điều gì.** Khi chuỗi băm trong DB dùng tham số cũ, lần đăng nhập đúng tiếp theo băm lại mật khẩu bằng tham số hiện tại. Chuỗi băm đã đúng tham số thì không đổi.

**Thông tin**
- Thiết kế: R-AUT-08; mục Tham số cài đặt (argon2id).
- Khía cạnh: Dữ liệu bất thường trong DB. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Có tài khoản `mio`.

**Các bước**
1. Chạy `<psql> "select password_hash from users where username = 'mio'"`.
   - Mong đợi: Chuỗi băm bắt đầu bằng `$argon2id$v=19$m=19456,t=2,p=1$`.
2. Tạo chuỗi băm với tham số cũ bằng `docker compose exec -T api node -e "require('@node-rs/argon2').hash('MioQuanLy#2026',{algorithm:2,memoryCost:4096,timeCost:1,parallelism:1}).then(console.log)"`. Ghi kết quả vào `users.password_hash` của `mio`.
   - Mong đợi: `mio` có chuỗi băm tham số cũ.
3. Đăng nhập `mio` / `MioQuanLy#2026`.
   - Mong đợi: API trả 201. `password_hash` mới bắt đầu bằng `$argon2id$v=19$m=19456,t=2,p=1$`.
   - 📷 Chụp evidence.
4. Đăng nhập lại.
   - Mong đợi: API trả 201. `password_hash` không đổi so với bước 3.

<!-- src-section: 3b420388fd 837a1109f42a -->
## P0-AUT-078 Đường dẫn không tồn tại

**Kiểm tra điều gì.** Đường dẫn không tồn tại hiện màn hình Không tìm thấy trang trong khung app, cho cả Quản lý lẫn Thợ. Người chưa đăng nhập phải đăng nhập trước.

**Thông tin**
- Thiết kế: mục Màn hình Không tìm thấy trang, R-AUT-28.
- Khía cạnh: Hiển thị. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Web đăng nhập `mio`.

**Các bước**
1. Mở `/khong-co`.
   - Mong đợi: Trong khung app hiện tiêu đề "Không tìm thấy trang" và nút "Về Trang chính". Không mục điều hướng nào được chọn.
   - 📷 Chụp evidence.
2. Bấm "Về Trang chính".
   - Mong đợi: Trang chuyển sang `/`.
3. Đăng xuất. Mở `/khong-co`, rồi đăng nhập.
   - Mong đợi: Trang chuyển sang `/login?next=%2Fkhong-co`. Sau khi đăng nhập, màn hình giống bước 1.
4. Đăng nhập `ngocanh.nail` ở context khác, mở `/khong-co`.
   - Mong đợi: Màn hình giống bước 1.

<!-- src-section: fd7e2e85bd e60b5281e2b0 -->
## P0-AUT-079 Log các sự kiện đăng nhập, đăng xuất, đổi mật khẩu, CLI

**Kiểm tra điều gì.** Mỗi sự kiện đăng nhập, đăng xuất, đổi mật khẩu và lệnh CLI đều có dòng log riêng với đủ trường. Output của CLI chỉ có câu cho người đọc.

**Thông tin**
- Thiết kế: R-AUT-30.
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không có dòng `login_throttles`.

**Các bước**
1. Chạy `<đăng nhập mio>` thêm `-H 'User-Agent: <x × 300>'`, rồi chạy `<log auth>`.
   - Mong đợi: Có dòng `auth.login.succeeded` mức info với `userId`, `"username":"mio"`, `time`, `requestId`, `ip`, và `userAgent` dài đúng 200 ký tự.
   - 📷 Chụp evidence.
2. Đăng nhập `mio` sai 1 lần.
   - Mong đợi: Có dòng `auth.login.failed` mức warn với `"userExists":true`, `"reason":"invalid_credentials"`, `"failedCount":1`.
3. Gọi `DELETE <api>/sessions/current` với `mio.jar`.
   - Mong đợi: Có dòng `auth.logout` với `userId`.
4. Đổi mật khẩu qua API với `signOutOtherDevices: false`.
   - Mong đợi: Có dòng `auth.password.changed` với `userId` và `"signedOutOtherDevices":false`.
5. Chạy `create-user` cho một tài khoản mới, rồi `reset-password` cho tài khoản đó.
   - Mong đợi: Output mỗi lệnh chỉ có câu cho người đọc ("Đã tạo tài khoản…", "Đã đặt lại mật khẩu…"), không có dòng JSON.
   - Mong đợi: `docker compose logs api` có `auth.cli.user_created` và `auth.cli.password_reset` kèm `username`, `time`, không có `requestId`, `ip`.
   - 📷 Chụp evidence.
6. Lọc bằng `docker compose logs api | grep '"event":"auth.'`. Sau đó đặt lại mật khẩu `mio`.
   - Mong đợi: Lệnh lọc ra đủ các dòng của bước 1–5.

<!-- src-section: 06bc6c5498 bef459aa8f09 -->
## P0-AUT-080 Log không chứa mật khẩu, token, chuỗi băm

**Kiểm tra điều gì.** Log và output CLI không chứa mật khẩu, token cookie hay chuỗi băm, kể cả khi request lỗi.

**Thông tin**
- Thiết kế: R-AUT-30, R-SKL-17.
- Khía cạnh: Phân quyền. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Làm lần lượt các thao tác sau:
   - Đăng nhập sai với mật khẩu `LoNgoaiLog#91`.
   - Chạy `<đăng nhập mio>`.
   - Đổi mật khẩu với `newPassword` là `LoNgoaiLog#92`.
   - Gửi `change-password` với thân JSON hỏng `{"currentPassword":"LoNgoaiLog#93",`.
   - Chạy `create-user` với mật khẩu `LoNgoaiLog#94` và ghi lại output lệnh.
2. Chạy `docker compose logs api | grep -c -e 'LoNgoaiLog' -e 'MioQuanLy#2026'`.
   - Mong đợi: Kết quả là `0`. Output lệnh CLI không chứa `LoNgoaiLog#94`.
   - 📷 Chụp evidence.
3. Tìm trong log token cookie (lấy từ `mio.jar`), `token_hash` của phiên và chuỗi `$argon2id$`.
   - Mong đợi: Không tìm thấy giá trị nào.
   - 📷 Chụp evidence.
4. Đặt lại mật khẩu `mio`.
   - Mong đợi: Đăng nhập lại được bằng mật khẩu mẫu.

<!-- src-section: 97ac09d5a4 4a19a96f8bde -->
## P0-AUT-081 Tạo tài khoản Quản lý và Thợ bằng CLI

**Kiểm tra điều gì.** Lệnh CLI tạo được tài khoản Quản lý và Thợ. Mật khẩu được băm bằng argon2id với đúng tham số, và hai tài khoản đăng nhập web được.

**Thông tin**
- Thiết kế: R-AUT-25, R-AUT-26 (`list-users`), R-AUT-27; mục Tham số cài đặt (argon2id).
- Khía cạnh: Logic nghiệp vụ. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Dùng môi trường thử, bảng `users` trống: chạy `<psql> "delete from users"`.

**Các bước**
1. Chạy `<cli> list-users; echo $?`.
   - Mong đợi: Output là "Chưa có tài khoản nào." và mã `0`.
2. Chạy `printf '%s\n' 'MioQuanLy#2026' | <cli> create-user --username mio --role manager --display-name "Huỳnh Mio"; echo $?`.
   - Mong đợi: Output có đúng một dòng "Đã tạo tài khoản mio (Quản lý)" và mã `0`.
   - 📷 Chụp evidence.
3. Chạy `printf '%s\n' 'NgocAnh#2026' | <cli> create-user --username ngocanh.nail --role technician --display-name "Ngọc Anh"`.
   - Mong đợi: Output là "Đã tạo tài khoản ngocanh.nail (Thợ)", mã 0.
4. Chạy `<psql> "select username, role, display_name, left(password_hash, 31) from users order by username"`.
   - Mong đợi: Có hai dòng `mio | manager | Huỳnh Mio | $argon2id$v=19$m=19456,t=2,p=1$` và `ngocanh.nail | technician | Ngọc Anh | $argon2id$v=19$m=19456,t=2,p=1$`.
   - 📷 Chụp evidence.
5. Đăng nhập web bằng cả hai tài khoản.
   - Mong đợi: Cả hai vào app với đúng vai trò.

<!-- src-section: 5e5de2c8f9 b2859605e427 -->
## P0-AUT-082 Nhập mật khẩu CLI trên terminal

**Kiểm tra điều gì.** Trên terminal thật, CLI hỏi mật khẩu hai lần mà không hiện ký tự gõ vào. CLI kiểm tham số trước khi hỏi mật khẩu, và mật khẩu không lọt vào lịch sử shell.

**Thông tin**
- Thiết kế: R-AUT-27; R-AUT-25, R-AUT-26 (kiểm tham số trước khi hỏi mật khẩu).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: người.

**Chuẩn bị**
- Terminal thật trên máy local.

**Các bước**
1. Chạy `docker compose exec -it api node dist/cli.js create-user --username tty.test --role technician --display-name "Thử TTY"`. Khi được hỏi, gõ `TtyTest#2026`.
   - Mong đợi: CLI hỏi "Mật khẩu: ". Khi gõ, không ký tự nào hiện ra, kể cả dấu `*`.
   - 📷 Chụp evidence.
2. Khi được hỏi lần hai, gõ `TtyTest#2026`.
   - Mong đợi: CLI hỏi "Nhập lại mật khẩu: ", rồi in "Đã tạo tài khoản tty.test (Thợ)", mã 0.
3. Lặp với `tty.test2`, lần nhập lại gõ `TtyTest#2027`. Sau đó chạy `list-users`.
   - Mong đợi: CLI in "Mật khẩu nhập lại không khớp", mã 1. `list-users` không có `tty.test2`.
   - 📷 Chụp evidence.
4. Chạy `docker compose exec -it api node dist/cli.js reset-password --username tty.test`.
   - Mong đợi: CLI hỏi mật khẩu hai lần như bước 1–2 và đặt lại thành công.
5. Chạy `docker compose exec -it api node dist/cli.js create-user --username tty.test3 --display-name "Thử TTY"` (thiếu `--role`). Sau đó lặp với `--username tty.test --role technician --display-name "Trùng"`.
   - Mong đợi: Lệnh thiếu `--role` in ngay "Thiếu --role", mã 1, không hỏi "Mật khẩu: ".
   - Mong đợi: Lệnh trùng tên in ngay "Tên đăng nhập đã tồn tại: tty.test", không hỏi mật khẩu.
   - 📷 Chụp evidence.
6. Chạy `docker compose exec -it api node dist/cli.js reset-password --username khongco`.
   - Mong đợi: CLI in ngay "Không tìm thấy tài khoản: khongco", không hỏi mật khẩu.
7. Xem `history` của shell.
   - Mong đợi: Lịch sử không chứa mật khẩu đã gõ.

<!-- src-section: d544b520b8 8bf1fcec7e26 -->
## P0-AUT-083 Tên đăng nhập khi tạo bằng CLI

**Kiểm tra điều gì.** Tên đăng nhập tạo bằng CLI phải đúng độ dài và bộ ký tự cho phép. Tên được chuẩn hóa về chữ thường và bỏ khoảng trắng hai đầu trước khi lưu.

**Thông tin**
- Thiết kế: R-AUT-25, R-AUT-07.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Mọi lệnh dùng `printf '%s\n' 'TaoMoi#2026' | <cli> create-user --username <tên> --role technician --display-name "Thử"`.

**Các bước**
1. Thử tên `ab`.
   - Mong đợi: CLI in "Tên đăng nhập phải dài 3–32 ký tự, chỉ gồm chữ thường không dấu, số, dấu chấm, gạch dưới, gạch ngang", mã 1.
   - 📷 Chụp evidence.
2. Thử `abc`, rồi tên gồm 32 ký tự `b`, rồi tên gồm 33 ký tự `c`.
   - Mong đợi: `abc` và tên 32 ký tự tạo được. Tên 33 ký tự báo lỗi như bước 1.
3. Thử `Mio.Test`, rồi `"  pad.test  "`.
   - Mong đợi: Lần đầu in "Đã tạo tài khoản mio.test (Thợ)". Lần sau in "Đã tạo tài khoản pad.test (Thợ)".
4. Thử lần lượt `thợ.nail`, `"mio nail"`, `mio@nail`, `mio+1`.
   - Mong đợi: Mỗi lần báo lỗi như bước 1 và không tạo tài khoản.
5. Thử `a_b-c.9`.
   - Mong đợi: Tạo được.
6. Chạy `<psql> "select username from users order by username"`.
   - Mong đợi: Có `a_b-c.9`, `abc`, `b…b` (32), `mio.test`, `pad.test`. Không có tên nào ở bước 1, 4.

<!-- src-section: a8fd6d734c bf7144a2d2ec -->
## P0-AUT-084 Tên đăng nhập đã tồn tại

**Kiểm tra điều gì.** CLI không tạo tài khoản trùng tên đăng nhập, kể cả khi khác hoa thường. Tài khoản đang có giữ nguyên.

**Thông tin**
- Thiết kế: R-AUT-25.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Có `mio`.
- Ghi lại `password_hash`, `display_name` của `mio`.

**Các bước**
1. Chạy `create-user --username mio --role technician --display-name "Trùng"`.
   - Mong đợi: CLI in "Tên đăng nhập đã tồn tại: mio", mã 1.
   - 📷 Chụp evidence.
2. Chạy lại với `--username MIO`.
   - Mong đợi: CLI in "Tên đăng nhập đã tồn tại: mio", mã 1.
3. Kiểm tài khoản `mio`.
   - Mong đợi: `mio` giữ nguyên `password_hash`, `display_name`, `role`.

<!-- src-section: e962481f8e ee048cb827bc -->
## P0-AUT-085 Vai trò khi tạo bằng CLI

**Kiểm tra điều gì.** CLI bắt buộc có vai trò và chỉ nhận manager hoặc technician.

**Thông tin**
- Thiết kế: R-AUT-25.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Chạy `create-user` bỏ `--role`.
   - Mong đợi: CLI in "Thiếu --role", mã 1.
2. Chạy với `--role admin`, rồi `--role ""`.
   - Mong đợi: CLI in "Vai trò phải là manager hoặc technician", mã 1.
3. Kiểm danh sách tài khoản.
   - Mong đợi: Không tài khoản nào được tạo.

<!-- src-section: 213e668290 a8b6bbcc241c -->
## P0-AUT-086 Tên hiển thị khi tạo bằng CLI

**Kiểm tra điều gì.** Tên hiển thị dài từ 1 đến 50 ký tự, tính theo code point sau khi bỏ khoảng trắng hai đầu.

**Thông tin**
- Thiết kế: R-AUT-25 (độ dài theo code point, bỏ khoảng trắng hai đầu).
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Mỗi bước dùng một tên đăng nhập mới.

**Các bước**
1. Chạy `create-user` bỏ `--display-name`.
   - Mong đợi: CLI in "Thiếu --display-name", mã 1.
2. Chạy với `--display-name "   "`.
   - Mong đợi: CLI in "Tên hiển thị phải từ 1 đến 50 ký tự", mã 1.
3. Thử `"A"`, rồi tên gồm 50 ký tự `ệ`, rồi 51 ký tự `ệ`.
   - Mong đợi: `"A"` và 50 ký tự tạo được. 51 ký tự báo lỗi như bước 2.
   - 📷 Chụp evidence.
4. Thử tên gồm 50 ký tự `💅`, rồi 51 ký tự `💅`.
   - Mong đợi: 50 ký tự tạo được. 51 ký tự báo lỗi như bước 2.
5. Thử `"  Ngọc Anh  "`.
   - Mong đợi: `display_name` được lưu là `Ngọc Anh`.

<!-- src-section: 30faa103b2 bf847b8256d4 -->
## P0-AUT-087 Mật khẩu khi tạo bằng CLI

**Kiểm tra điều gì.** Mật khẩu tạo bằng CLI dài từ 8 đến 128 ký tự và không được trùng tên đăng nhập. Mỗi trường chỉ báo một lỗi, và độ dài được xét trước.

**Thông tin**
- Thiết kế: R-AUT-25; quy tắc chung "mỗi trường một lỗi".
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: giá trị biên.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Mỗi bước dùng một tên đăng nhập mới.

**Các bước**
1. Dùng mật khẩu `Abcd#12` (7 ký tự).
   - Mong đợi: CLI in "Mật khẩu phải từ 8 đến 128 ký tự", mã 1.
   - 📷 Chụp evidence.
2. Dùng `Abcd#123` (8 ký tự), rồi mật khẩu gồm 128 ký tự `x`, rồi 129 ký tự `x`.
   - Mong đợi: 8 ký tự và 128 ký tự tạo được. 129 ký tự báo lỗi như bước 1.
3. Chạy với `--username pw.same.name` và mật khẩu `pw.same.name`.
   - Mong đợi: CLI in "Mật khẩu không được trùng tên đăng nhập", mã 1.
4. Đăng nhập web bằng tài khoản có mật khẩu 128 ký tự ở bước 2.
   - Mong đợi: Người dùng vào app.
5. Chạy với `--username pw.x` và mật khẩu `pw.x`, vừa ngắn vừa trùng tên.
   - Mong đợi: CLI chỉ in một dòng "Mật khẩu phải từ 8 đến 128 ký tự", mã 1. Mỗi trường chỉ có một lỗi và độ dài được xét trước.

<!-- src-section: 3b2dd3479d b719b0389585 -->
## P0-AUT-088 CLI in mọi lỗi cùng lúc

**Kiểm tra điều gì.** Khi có nhiều tham số sai, CLI in mọi lỗi cùng lúc, mỗi lỗi một dòng.

**Thông tin**
- Thiết kế: R-AUT-25 ("in mọi lỗi, mỗi lỗi một dòng").
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không cần chuẩn bị gì thêm.

**Các bước**
1. Chạy `printf '%s\n' 'ngan' | <cli> create-user --username ab --role admin --display-name "   "`.
   - Mong đợi: CLI in 4 dòng: lỗi tên đăng nhập, vai trò, tên hiển thị và mật khẩu, nguyên văn như P0-AUT-083, 085, 086, 087. Mã thoát là 1.
   - 📷 Chụp evidence.
2. Chạy `printf '%s\n' 'HopLe#2026' | <cli> create-user`.
   - Mong đợi: CLI in 3 dòng "Thiếu --username", "Thiếu --role", "Thiếu --display-name". Mã thoát là 1.

<!-- src-section: 8b1f9e805a e24f9b58dbd6 -->
## P0-AUT-089 Mật khẩu qua stdin và tham số không hợp lệ

**Kiểm tra điều gì.** CLI đọc mật khẩu từ dòng đầu của stdin và giữ nguyên khoảng trắng hai đầu. CLI không nhận mật khẩu qua tham số dòng lệnh.

**Thông tin**
- Thiết kế: R-AUT-27.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: đoán lỗi.
- Ưu tiên: cao. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Mỗi bước dùng một tên đăng nhập mới, kèm `--role technician --display-name "Thử"`.

**Các bước**
1. Chạy `<cli> create-user … < /dev/null` (stdin rỗng).
   - Mong đợi: CLI in "Thiếu mật khẩu", mã 1.
2. Chạy `printf 'Crlf#2026\r\n' | <cli> create-user …`, rồi đăng nhập với `Crlf#2026`.
   - Mong đợi: Tài khoản được tạo. Đăng nhập trả 201.
   - 📷 Chụp evidence.
3. Chạy `printf 'Dong1#2026\nDong2#2026\n' | …`, rồi đăng nhập với `Dong1#2026` và `Dong2#2026`.
   - Mong đợi: Tài khoản được tạo. `Dong1#2026` trả 201, `Dong2#2026` trả 401.
4. Chạy `printf ' CachDau#2026 \n' | …`, rồi đăng nhập với ` CachDau#2026 ` (có khoảng trắng hai đầu) và `CachDau#2026`.
   - Mong đợi: Tài khoản được tạo. Mật khẩu có khoảng trắng trả 201, mật khẩu không khoảng trắng trả 401.
5. Chạy `<cli> create-user --username p.arg --role technician --display-name "Thử" --password Abc#12345`.
   - Mong đợi: CLI in "Tham số không hợp lệ: --password", mã 1. Không tạo `p.arg`.
   - 📷 Chụp evidence.

<!-- src-section: 64194427c9 a97eabb72887 -->
## P0-AUT-090 Tạo cùng một tên đăng nhập đồng thời

**Kiểm tra điều gì.** Khi hai lệnh tạo cùng một tên đăng nhập chạy cùng lúc, chỉ một lệnh thành công. Lệnh còn lại báo trùng tên, không báo lỗi hệ thống.

**Thông tin**
- Thiết kế: R-AUT-25 (DB unique chặn cả khi tạo đồng thời).
- Khía cạnh: Thao tác đồng thời. Kỹ thuật: đoán lỗi.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Không có `song.song`.

**Các bước**
1. Chạy song song hai lệnh `create-user --username song.song …` dưới dạng hai tiến trình nền, rồi `wait`.
   - Mong đợi: Một lệnh in "Đã tạo tài khoản song.song (Thợ)", mã 0. Lệnh kia in "Tên đăng nhập đã tồn tại: song.song", mã 1, không phải lỗi hệ thống.
   - 📷 Chụp evidence.
2. Chạy `<psql> "select count(*) from users where username = 'song.song'"`.
   - Mong đợi: Kết quả là `1`.
3. Lặp bước 1–2 thêm 4 lần với tên khác.
   - Mong đợi: Lần nào cũng thỏa các mong đợi trên.

<!-- src-section: 02eff2a163 744b8464ff9b -->
## P0-AUT-091 `reset-password` đặt lại mật khẩu, đăng xuất mọi thiết bị, gỡ khóa

**Kiểm tra điều gì.** Lệnh `reset-password` đặt mật khẩu mới, xóa mọi phiên của tài khoản và gỡ khóa đăng nhập. Mật khẩu cũ không dùng được nữa.

**Thông tin**
- Thiết kế: R-AUT-26, R-AUT-31, R-AUT-30.
- Khía cạnh: Chuyển trạng thái. Kỹ thuật: chuyển trạng thái.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Context A ở `/` và context B ở `/account/password`, cả hai đăng nhập `ngocanh.nail`.
- Context C chưa đăng nhập.

**Các bước**
1. Ở C, đăng nhập `ngocanh.nail` sai 5 lần.
   - Mong đợi: Tài khoản bị khóa.
2. Chạy `printf '%s\n' 'NgocAnhMoi#2026' | <cli> reset-password --username ngocanh.nail; echo $?`.
   - Mong đợi: CLI in "Đã đặt lại mật khẩu cho ngocanh.nail. Mọi phiên đăng nhập của tài khoản đã bị đăng xuất." và mã `0`.
   - 📷 Chụp evidence.
3. Kiểm DB.
   - Mong đợi: Không còn phiên của `ngocanh.nail`. Dòng `ngocanh.nail` trong `login_throttles` không còn khóa, tức không còn dòng hoặc `locked_until` rỗng. `password_hash` đã đổi.
4. Tải lại A. Ở B, gửi form đổi mật khẩu.
   - Mong đợi: A chuyển sang `/login?next=%2F` kèm banner "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại".
   - Mong đợi: B chuyển sang `/login?next=%2Faccount%2Fpassword` kèm banner "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại".
   - 📷 Chụp evidence.
5. Ở C, đăng nhập ngay bằng `NgocAnhMoi#2026`, rồi bằng `NgocAnh#2026`.
   - Mong đợi: Mật khẩu mới trả 201, vì không còn bị khóa. Mật khẩu cũ trả 401.
6. Xem log. Sau đó đặt lại mật khẩu về `NgocAnh#2026`.
   - Mong đợi: Log có `auth.cli.password_reset` với `"username":"ngocanh.nail"`.

<!-- src-section: ad16d0a1f6 0510c13a43e6 -->
## P0-AUT-092 `reset-password` báo lỗi

**Kiểm tra điều gì.** Lệnh `reset-password` báo lỗi khi thiếu tham số, không tìm thấy tài khoản hoặc mật khẩu không hợp lệ. Khi lỗi, mật khẩu và phiên giữ nguyên. Tên đăng nhập được chuẩn hóa trước khi tìm.

**Thông tin**
- Thiết kế: R-AUT-26, R-AUT-07.
- Khía cạnh: Kiểm tra dữ liệu nhập. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<đăng nhập ngocanh>`.
- Ghi lại `password_hash` của `ngocanh.nail`.

**Các bước**
1. Chạy `printf '%s\n' 'HopLe#2026' | <cli> reset-password`.
   - Mong đợi: CLI in "Thiếu --username", mã 1.
2. Chạy `… reset-password --username khongco`.
   - Mong đợi: CLI in "Không tìm thấy tài khoản: khongco", mã 1.
   - 📷 Chụp evidence.
3. Chạy `printf '%s\n' 'ngan' | <cli> reset-password --username ngocanh.nail`. Sau đó thử với mật khẩu `ngocanh.nail`.
   - Mong đợi: Lần đầu in "Mật khẩu phải từ 8 đến 128 ký tự", mã 1. Lần sau in "Mật khẩu không được trùng tên đăng nhập", mã 1.
4. Sau bước 3, kiểm `password_hash` và gọi `curl -b ngocanh.jar <api>/sessions/current`.
   - Mong đợi: `password_hash` không đổi. Lệnh gọi trả 200, tức phiên không bị xóa.
5. Chạy `printf '%s\n' 'NgocAnh#2026' | <cli> reset-password --username "  NGOCANH.NAIL "`.
   - Mong đợi: Mật khẩu được đặt lại cho `ngocanh.nail` vì tên được chuẩn hóa. Mã 0.

<!-- src-section: 4c83069527 63d8351f6ba0 -->
## P0-AUT-093 `list-users` liệt kê tài khoản

**Kiểm tra điều gì.** Lệnh `list-users` liệt kê tài khoản theo thứ tự tên, với vai trò và tên hiển thị. Lệnh không in chuỗi băm hay id.

**Thông tin**
- Thiết kế: R-AUT-26.
- Khía cạnh: Hiển thị. Kỹ thuật: phân vùng tương đương.
- Ưu tiên: thấp. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Bảng `users` chỉ có `mio`, `ngocanh.nail` và `abc` (Thợ, "Thử").

**Các bước**
1. Chạy `<cli> list-users; echo $?`.
   - Mong đợi: Có đúng 3 dòng theo thứ tự "abc | Thợ | Thử", "mio | Quản lý | Huỳnh Mio", "ngocanh.nail | Thợ | Ngọc Anh". Mã là `0`. Không in chuỗi băm hay id.
   - 📷 Chụp evidence.
2. Trường hợp chưa có tài khoản nào được kiểm ở P0-AUT-081 bước 1.
   - Mong đợi: Xem P0-AUT-081.

<!-- src-section: 00d5e429f4 2e9a39f7cb03 -->
## P0-AUT-094 Quên mật khẩu Quản lý: tự đặt lại bằng CLI

**Kiểm tra điều gì.** Quản lý quên mật khẩu có thể tự đặt lại bằng CLI mà không cần mật khẩu cũ hay phiên web. CLI không mở thêm cổng mạng nào.

**Thông tin**
- Thiết kế: R-AUT-33.
- Khía cạnh: Phân quyền. Kỹ thuật: tình huống thực tế.
- Ưu tiên: trung bình. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy bằng `compose.yml`, không có `compose.dev.yml`.
- Chạy `<psql> "delete from user_sessions"`, để không còn ai đăng nhập web.

**Các bước**
1. Chạy `printf '%s\n' 'MioKhoiPhuc#2026' | <cli> reset-password --username mio`.
   - Mong đợi: Lệnh thành công, không đòi mật khẩu cũ hay phiên web.
   - 📷 Chụp evidence.
2. Đăng nhập web `mio` / `MioKhoiPhuc#2026`.
   - Mong đợi: Người dùng vào app với badge "Quản lý".
3. Chạy `docker compose ps --format '{{.Name}} {{.Ports}}'`.
   - Mong đợi: Chỉ api có `127.0.0.1:3000->3000/tcp`. Không container nào mở cổng khác cho CLI.
   - 📷 Chụp evidence.
4. Đặt lại mật khẩu `mio`.
   - Mong đợi: Đăng nhập lại được bằng mật khẩu mẫu.

<!-- src-section: a730316e25 27cd1330f6bc -->
## P0-AUT-095 Phần dùng chung của khung app vẫn đúng sau khi thêm auth

**Kiểm tra điều gì.** Sau khi thêm auth, các phần dùng chung của khung app vẫn hoạt động: healthcheck, trang 404, file tĩnh và CLI.

**Thông tin**
- Thiết kế: R-AUT-16, R-SKL-13, R-SKL-14, R-SKL-15, R-SKL-31; thiết kế `app-skeleton` mục `cli.ts`.
- Khía cạnh: Regression. Kỹ thuật: tình huống thực tế.
- Ưu tiên: cao. Regression: có. Người thực hiện: Claude.

**Chuẩn bị**
- Hệ thống chạy như P0-SKL-001, đã có mã auth.

**Các bước**
1. Chạy `docker compose ps`.
   - Mong đợi: Cả 4 dịch vụ đều `running (healthy)`. Healthcheck gọi `/api/v1/health` không kèm cookie.
2. Chạy lại P0-SKL-016, P0-SKL-021, P0-SKL-023.
   - Mong đợi: Cả ba đều đạt. Health, 404 và file tĩnh không cần đăng nhập.
   - 📷 Chụp evidence.
3. Chạy `<cli> help`, rồi `<cli> khong-co`.
   - Mong đợi: Danh sách lệnh có `create-user`, `reset-password`, `list-users`. Lệnh không tồn tại in "Lệnh không tồn tại: khong-co. Chạy help để xem danh sách.", mã 1.

<!-- src-section: d586840649 46fc829e04dd -->
## P0-AUT-096 Đăng nhập lại khi đang có phiên; route công khai không gia hạn

**Kiểm tra điều gì.** Đăng nhập lại khi đang có phiên thì phiên cũ của cookie đang gửi bị thay bằng phiên mới. Gọi route công khai không gia hạn phiên.

**Thông tin**
- Thiết kế: R-AUT-08 (thay phiên của cookie đang gửi), R-AUT-10 (route công khai không gia hạn).
- Khía cạnh: Phiên đăng nhập và cookie. Kỹ thuật: đoán lỗi.
- Ưu tiên: trung bình. Regression: không. Người thực hiện: Claude.

**Chuẩn bị**
- Chạy `<psql> "delete from user_sessions"`, rồi `<đăng nhập mio>`.
- Ghi lại `token_hash` của phiên bằng `<psql> "select token_hash from user_sessions where user_id = <id mio>"`.

**Các bước**
1. Gọi `curl -s -i -b mio.jar -c mio.jar <origin> <json> -d '{"username":"mio","password":"MioQuanLy#2026"}' <api>/sessions`.
   - Mong đợi: API trả 201, `Set-Cookie` có token mới.
2. Chạy `<psql> "select token_hash from user_sessions where user_id = <id mio>"`.
   - Mong đợi: Có đúng 1 dòng, khác `token_hash` đã ghi. Phiên cũ đã bị xóa.
   - 📷 Chụp evidence.
3. Đăng nhập `ngocanh.nail` bằng `-b mio.jar -c mio.jar`, tức đổi tài khoản.
   - Mong đợi: API trả 201. `mio` không còn phiên nào, `ngocanh.nail` có 1 phiên.
4. Chạy `<đăng nhập mio>`, rồi `<psql> "update user_sessions set updated_at = now() - interval '25 hours', expires_at = now() + interval '89 days' where user_id = <id mio>"`. Sau đó gọi `curl -s -i -b mio.jar <api>/health`.
   - Mong đợi: API trả 200, không có `Set-Cookie`. `updated_at`, `expires_at` giữ nguyên giá trị vừa đặt.
   - 📷 Chụp evidence.
5. Gọi `curl -s -i -b mio.jar <api>/sessions/current`.
   - Mong đợi: API trả 200 kèm `Set-Cookie`. Route có `@Roles` thì được gia hạn, như P0-AUT-027.

<!-- src-section: 80b54c0db6 703bcc10ad56 -->
## Lịch sử thay đổi

**Tóm tắt.** Tài liệu được tạo và review trong cùng ngày 2026-10-31.

- 2026-10-31: tạo mới (`/test-case-design auth`).
- 2026-10-31: chạy `/design-review auth`.
  - Theo RV-01 … RV-16, sửa P0-AUT-001, 007, 020, 023, 034, 036, 038, 044, 045, 056, 063, 066, 075, 079, 081, 082, 087.
  - Đổi câu banner thành "Phiên đăng nhập đã kết thúc…" ở mọi case.
  - Thêm P0-AUT-096.
  - Ghi chú chạy bỏ mục chờ quyết định và thêm phần chỉ kiểm bằng test tự động.
