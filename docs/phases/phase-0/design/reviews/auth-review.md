# Review thiết kế – Đăng nhập và phân quyền (`auth`)

- Ngày: 2026-10-31
- Đối tượng: thiết kế chi tiết, mockup (`login/`, `app-shell/`, `change-password/`, `forbidden/`, `not-found/`), test case, traceability, `api/sessions.md`, `api/users.md`, `db-schema.md`
- Tổng: 16 điểm (2 chặn, 9 nên sửa, 5 gợi ý)

### RV-01 R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7
- Mức độ: chặn
- Vị trí: design/auth.md R-AUT-06, mục Trạng thái › Bộ đếm đăng nhập sai, mục Đăng nhập (`AuthService.login`); test P0-AUT-023, Ghi chú chạy
- Vấn đề: câu hỏi 7 đã chốt nhưng quy tắc vẫn như cũ:
  - `getLock` chạy ngoài transaction, trước `verify`; `recordFailure` không kiểm `locked_until > bây giờ` nên khi đang khóa vẫn đếm, tới lần thứ 5 thì kéo dài khóa;
  - request đúng mật khẩu đã qua `getLock` trước khi khóa vẫn đăng nhập được sau khi khóa đã ghi;
  - chưa có thuật toán `changePassword`, dù R-AUT-20 dùng chung bộ đếm.
  Implement theo văn bản hiện tại thì P0-AUT-023 không đạt.
- Đề xuất:
  - `recordFailure`: trong transaction có `SELECT … FOR UPDATE`, đọc dòng; `locked_until > bây giờ` → trả khóa, không đổi gì; còn lại như bước 2–5 hiện tại;
  - nhánh đúng mật khẩu (đăng nhập, đổi mật khẩu): trong transaction khóa dòng, kiểm lại khóa; đang khóa → 429, không tạo phiên, không đổi mật khẩu; không khóa → `reset`. Mọi request bị chặn ở bước này ghi `auth.login.failed` / `auth.password.change_failed` với `reason: locked`;
  - ghi rõ: request đã qua `verify` mà gặp khóa lúc ghi luôn nhận 429, nên kẻ dò không biết kết quả của các lần đoán vượt quá 5;
  - mục Trạng thái: thêm chuyển không hợp lệ "bị khóa → bị khóa (kéo dài)"; thêm thuật toán `AuthService.changePassword`;
  - P0-AUT-023 bước 2 đổi "tối đa 4 × 401" thành "đúng 4 × 401, 6 × 429"; bỏ dòng câu hỏi 7 khỏi Ghi chú chạy.
- Kết quả: đã sửa (R-AUT-06; `LoginThrottleService`; mục Trạng thái: bộ đếm, đăng nhập, thêm đổi mật khẩu; P0-AUT-023; Ghi chú chạy: test tự động)

### RV-02 R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câu hỏi mở 8)
- Mức độ: chặn
- Vị trí: design/auth.md R-AUT-28, R-AUT-31, mục `apps/web`; test P0-AUT-028, 029, 034, 037, 073, 091; traceability dòng R-AUT-31
- Vấn đề: câu hỏi 8 chốt "phiên không còn dùng được thì có banner, chưa từng đăng nhập thì không", nhưng chưa có cơ chế:
  - cookie là `HttpOnly`, web không đọc được; `Set-Cookie` xóa cookie cũng không đọc được từ `fetch`;
  - phiên hết hạn tự nhiên sau 90 ngày: trình duyệt tự bỏ cookie theo `Max-Age`, request tới api không mang cookie, nên api không phân biệt được với "chưa từng đăng nhập". Thêm mã lỗi riêng ở api không giải quyết được trường hợp chính này;
  - chưa nói banner được truyền thế nào; nếu để trong `history.state` thì tải lại `/login` vẫn còn banner, trái P0-AUT-029 bước 5.
- Đề xuất (chỉ đổi web, không đổi API):
  - web giữ cờ `mio.hadSession` trong `localStorage`: đặt khi `GET /api/v1/sessions/current` trả 200; xóa khi bấm "Đăng xuất" (trước khi gọi API) và khi đã dùng cờ để hiện banner; đọc và ghi trong try/catch, lỗi thì coi như không có cờ;
  - mở app nhận 401: có cờ → xóa cờ, chuyển `/login?next=…` kèm banner "Phiên đăng nhập…"; không có cờ → chuyển, không banner;
  - đang dùng (đã có người dùng trong `auth-provider`) nhận 401 → luôn có banner, như R-AUT-31 hiện tại;
  - banner info của R-AUT-31, R-AUT-32 giữ trong bộ nhớ của `auth-provider`, không đưa vào URL hay `history.state`; tải lại `/login` thì mất banner;
  - sửa dòng R-AUT-31 trong traceability, bỏ dòng câu hỏi 8 khỏi Ghi chú chạy của test case.
- Kết quả: đã sửa (R-AUT-31, R-AUT-32, `auth-provider`, màn Đăng nhập; P0-AUT-001, 034; traceability R-AUT-31; Ghi chú chạy). Người dùng chấp nhận: trình duyệt chặn lưu dữ liệu thì không có banner

### RV-03 Câu hỏi mở 9 chưa đưa vào mục Xử lý lỗi
- Mức độ: nên sửa
- Vị trí: design/auth.md mục Xử lý lỗi; test P0-AUT-075
- Vấn đề: đã chốt "`password_hash` không phải chuỗi PHC → 500" nhưng mục Xử lý lỗi không có dòng này; chưa nói có đếm vào R-AUT-06 hay ghi log `auth.login.failed` không.
- Đề xuất: thêm vào mục Xử lý lỗi: `verify` ném lỗi vì chuỗi băm hỏng → 500 `INTERNAL_ERROR` (R-SKL-16), log mức error có `userId` (không có chuỗi băm), không đếm vào R-AUT-06, không ghi `auth.login.failed`; áp dụng cả đăng nhập và đổi mật khẩu.
- Kết quả: đã sửa (mục Xử lý lỗi; P0-AUT-075 bước 3)

### RV-04 Hai lần đổi mật khẩu đồng thời có thể mất cập nhật
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-23, R-AUT-24; test P0-AUT-066
- Vấn đề: chưa quy định transaction cho đổi mật khẩu. A và B cùng đọc chuỗi băm cũ, cùng `verify` đúng, lần lượt ghi: cả hai nhận 204 và toast "Đã đổi mật khẩu", nhưng chỉ mật khẩu của người ghi sau dùng được. Với `signOutOtherDevices: false` thì A tin mật khẩu là của mình mà không phải. `reset-password` chạy cùng lúc cũng bị như vậy.
- Đề xuất:
  - R-AUT-23: đổi mật khẩu chạy trong một transaction, khóa dòng `users` (`SELECT … FOR UPDATE`), `verify` mật khẩu hiện tại trên chuỗi băm đọc sau khi khóa; ghi chuỗi băm, phiên, bộ đếm trong cùng transaction. `reset-password` cũng khóa dòng `users`;
  - P0-AUT-066 bước 1: "đúng một request 204; request còn lại 400 'Mật khẩu hiện tại không đúng' hoặc 401".
- Kết quả: đã sửa (R-AUT-23, R-AUT-26, `UsersRepository.lockById`/`lockByUsername`, thuật toán đổi mật khẩu; P0-AUT-066; Ghi chú chạy: test tự động)

### RV-05 `failedCount` của lần sai làm khóa chưa rõ
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-30; test P0-AUT-020 bước 3, P0-AUT-063 bước 6
- Vấn đề: `failedCount` là "số lần sai trong cửa sổ sau lần này", nhưng lần thứ 5 đặt `failed_count = 0` trong DB, nên dòng log có thể là 5 hoặc 0. Test chỉ kiểm 4 dòng đầu.
- Đề xuất: R-AUT-30 ghi "lần sai làm khóa: `failedCount` 5 và có `lockedUntil`"; P0-AUT-020 bước 3 thêm "dòng thứ 5 có `failedCount` 5, `lockedUntil`".
- Kết quả: đã sửa (R-AUT-30; P0-AUT-020 bước 3, P0-AUT-023 bước 3, P0-AUT-063 bước 6)

### RV-06 Thứ tự kiểm tra chưa tính bước đọc thân request
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-15, `OriginCheckMiddleware`; test P0-AUT-045
- Vấn đề: R-AUT-15 ghi thứ tự R-AUT-17 → R-AUT-11 → R-AUT-15 → kiểm dữ liệu. Trong NestJS, body parser (sinh `INVALID_JSON`, `PAYLOAD_TOO_LARGE`) chạy trước middleware đăng ký qua module và trước guard. Nếu không nói gì, request `Origin` lạ kèm JSON hỏng nhận 400 thay vì 403, trái thứ tự đã ghi.
- Đề xuất: R-AUT-15 ghi đủ thứ tự: R-AUT-17 → đọc thân (`INVALID_JSON`, `PAYLOAD_TOO_LARGE`) → R-AUT-11 → R-AUT-15 → kiểm dữ liệu; kiểm `Origin` đăng ký bằng `app.use` trước body parser. P0-AUT-045 thêm bước: `Origin` lạ + JSON hỏng → 403 `INVALID_ORIGIN`; `Origin` đúng, không cookie, JSON hỏng → 400 `INVALID_JSON`.
- Kết quả: đã sửa (R-AUT-15, `OriginCheckMiddleware`; P0-AUT-045 bước 6, 7)

### RV-07 Đổi mật khẩu: trường sai kiểu chưa có quy tắc
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-19, R-AUT-21; test P0-AUT-057 bước 3, P0-AUT-056
- Vấn đề: câu "Trường không phải chuỗi hoặc thiếu → cùng thông báo như trống" chỉ có ở phần đăng nhập. P0-AUT-057 lại mong `currentPassword: 123` → "Nhập mật khẩu hiện tại", tức test đặt ra hành vi mà thiết kế chưa ghi. `newPassword` sai kiểu chưa có case (checklist test: mọi trường có case sai kiểu).
- Đề xuất: R-AUT-21 thêm dòng chung cho R-AUT-19, R-AUT-21: `currentPassword`, `newPassword` không phải chuỗi hoặc thiếu → cùng thông báo như trống. P0-AUT-056 bước 5 thêm `newPassword` là số `12345678` → "Nhập mật khẩu mới".
- Kết quả: đã sửa (R-AUT-21; P0-AUT-056 bước 6)

### RV-08 Tên đăng nhập dài hơn 32 ký tự sau khi đổi chữ thường làm lỗi 500
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-02, R-AUT-07; `db-schema.md` `login_throttles.username` (check 1–32); test P0-AUT-007
- Vấn đề: R-AUT-02 đo độ dài sau khi bỏ khoảng trắng, trước khi đổi chữ thường. Một số ký tự dài ra khi đổi chữ thường, ví dụ `'İ'.toLowerCase()` = `i` + dấu chấm kết hợp (2 code point). Nhập `İ` × 32 qua được R-AUT-02, tên đã chuẩn hóa dài 64, ghi `login_throttles` vi phạm check → 500.
- Đề xuất: R-AUT-02 đo độ dài trên tên đã chuẩn hóa (`normalizeUsername`, cả web lẫn API). P0-AUT-007 thêm bước: `İ` × 32 → 400 "Tên đăng nhập tối đa 32 ký tự", không có 500.
- Kết quả: đã sửa (R-AUT-02; `api/sessions.md`, `openapi.yaml` bỏ `maxLength` của `username`; P0-AUT-007 bước 6)

### RV-09 Log của lệnh CLI không nằm trong `docker compose logs api`
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-30 (`auth.cli.*`, cách lọc log); test P0-AUT-079 bước 5–6, P0-AUT-080 bước 2, P0-AUT-081, P0-AUT-093
- Vấn đề: `docker compose exec api node dist/cli.js …` là tiến trình riêng; stdout của nó ra terminal của người chạy, không vào log của container. Vì vậy:
  - `docker compose logs api | grep '"event":"auth.'` không thấy `auth.cli.*` (P0-AUT-079 bước 6 không đạt);
  - dòng log JSON in lẫn với thông báo cho người ("Đã tạo tài khoản…"), `list-users` không còn "đúng 3 dòng" nếu có log;
  - sự kiện CLI không có `requestId`, `ip` như R-AUT-30 đòi "mọi sự kiện".
- Đề xuất:
  - CLI in thông báo cho người ra stdout; log JSON ghi vào `/proc/1/fd/1` (stdout của tiến trình chính, cùng uid 1000, Node là PID 1 theo R-SKL-22) để `docker compose logs api` thấy. Mở không được thì ghi ra stderr. Cần kiểm chứng khi implement;
  - phương án khác: chấp nhận log CLI chỉ ra stderr của lệnh, R-AUT-30 ghi rõ `docker compose logs` chỉ có sự kiện HTTP;
  - R-AUT-30: sự kiện CLI có `event`, `time`, `username`, không có `requestId`, `ip`;
  - P0-AUT-079 bước 5–6, P0-AUT-080 bước 2 sửa theo phương án được chọn.
- Kết quả: đã sửa theo phương án A (R-AUT-30; P0-AUT-079 bước 5–6, P0-AUT-081 bước 2; Ghi chú chạy: phương án dự phòng stderr kiểm bằng test tự động)

### RV-10 Đăng xuất lỗi: chưa rõ có hiện "Bạn đã đăng xuất" không
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-32; test P0-AUT-036 bước 1
- Vấn đề: R-AUT-32 nói đăng xuất lỗi vẫn chuyển `/login`, không nói banner. Hiện "Bạn đã đăng xuất" khi phiên và cookie còn là báo sai: người dùng tưởng đã thoát, người sau mở app vào thẳng được.
- Đề xuất: R-AUT-32 ghi: chỉ hiện banner "Bạn đã đăng xuất" khi API trả 204; lỗi mạng hoặc 500 thì chuyển `/login` không có banner. P0-AUT-036 bước 1, 3 thêm "không có banner 'Bạn đã đăng xuất'". (Phương án khác: ở lại trang, toast danger, cho bấm lại; đổi quyết định đã ghi nên không đề xuất mặc định.)
- Kết quả: đã sửa (R-AUT-32; `login/notes.md`; P0-AUT-036 bước 1, 3)

### RV-11 403 khi gửi form hiện bằng toast, trái quy ước vị trí thông báo
- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-29; test P0-AUT-044; `docs/design/ui/app-shell/notes.md` (`forbidden.html`)
- Vấn đề: R-AUT-29 luôn hiện toast danger khi API trả 403. Theo `ui-style.md` mục "Vị trí thông báo" (ADR 0016), lỗi khi gửi form hiện ở vùng thông báo ngay trên hàng nút gửi; toast chỉ dùng cho thao tác không có form. P0-AUT-044 bấm nút lưu trên màn Cài đặt (là form) nhưng mong toast. Ngoài ra vai trò vừa bị đổi mà thanh điều hướng vẫn giữ mục cũ.
- Đề xuất: R-AUT-29: 403 `FORBIDDEN` → gửi form: banner danger ở vùng thông báo của form; thao tác không có form: toast danger; cả hai gọi `refresh()` của `auth-provider` để thanh điều hướng và màn Không có quyền theo vai trò mới. P0-AUT-044 bước 2 đổi thành banner trên form, thêm bước "thanh điều hướng còn 'Trang chính', trang hiện màn Không có quyền". `app-shell/notes.md` ghi `forbidden.html` là trường hợp không có form.
- Kết quả: đã sửa (R-AUT-29, `api-client.ts`; `app-shell/notes.md`; P0-AUT-044)

### RV-12 Câu "Phiên đăng nhập đã hết hạn" dùng cả khi phiên bị xóa
- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-31; mockup `login/session-expired.html`; test P0-AUT-028, 029, 030, 050, 073, 091
- Vấn đề: banner dùng chung cho hết hạn, bị đăng xuất do đổi hoặc đặt lại mật khẩu, tài khoản bị xóa, cookie hỏng. Theo ADR 0016, câu dùng chung phải đúng nghĩa ở mọi chỗ; "hết hạn" chưa đúng hẳn khi phiên bị đăng xuất từ thiết bị khác.
- Đề xuất: đổi thành câu trung tính "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" ở thiết kế, mockup, test case. Giữ câu cũ cũng chấp nhận được.
- Kết quả: đã sửa (R-AUT-31, màn Đăng nhập; mockup `login/session-expired.html` và ảnh chụp, `login/notes.md`; mọi case có banner này)

### RV-13 Một trường có hai lỗi cùng lúc: chưa nói hiện lỗi nào
- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-21, R-AUT-25
- Vấn đề: tên đăng nhập 3–7 ký tự thì mật khẩu mới trùng tên vi phạm cả "8 đến 128 ký tự" lẫn "không trùng tên đăng nhập". Zod trả cả hai lỗi; web chỉ hiện một dòng dưới ô, CLI "in mọi lỗi" có thể in hai dòng cho mật khẩu.
- Đề xuất: ghi "mỗi trường chỉ một lỗi, lấy theo thứ tự trống → độ dài → trùng tên đăng nhập" cho web, API (`fields`) và CLI.
- Kết quả: đã sửa (quy tắc chung đầu mục Quy tắc; P0-AUT-087 bước 5; traceability)

### RV-14 Kiểm tra `next` chưa chặn ký tự điều khiển
- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-28; test P0-AUT-038
- Vấn đề: trình duyệt bỏ tab và xuống dòng khi phân tích URL, nên `/<tab>/evil.example` qua được điều kiện "không bắt đầu bằng `//`" nhưng thành `//evil.example`. Chuyển trang bằng `location.href` thì rời app.
- Đề xuất: R-AUT-28 thêm: `next` chứa ký tự điều khiển hoặc khoảng trắng → `/`; chuyển bằng router của app, không dùng `location.href`. P0-AUT-038 thêm bước `next=%2F%09%2Fevil.example` → `/`.
- Kết quả: đã sửa (R-AUT-28; P0-AUT-038 bước 8)

### RV-15 Phiên khi gọi route công khai lúc đang có cookie
- Mức độ: gợi ý
- Vị trí: design/auth.md mục Kiểm tra request bước 1, R-AUT-08, R-AUT-10
- Vấn đề:
  - `POST /api/v1/sessions` khi đang có phiên hợp lệ (đăng nhập ở hai tab, đổi tài khoản qua API) tạo phiên mới, phiên cũ nằm lại tới 90 ngày;
  - route công khai "vẫn đọc phiên" nhưng chưa nói có gia hạn không; `DELETE /sessions/current` gia hạn rồi xóa sẽ gửi hai `Set-Cookie` cho cùng cookie.
- Đề xuất: route `@Public()` đọc phiên nhưng không gia hạn (R-AUT-10 chỉ áp cho route có `@Roles`); `POST /sessions` thành công mà request mang cookie của phiên còn hiệu lực thì xóa phiên đó.
- Kết quả: đã sửa (R-AUT-08, R-AUT-10, mục Kiểm tra request bước 1, thuật toán đăng nhập; `api/sessions.md`, `openapi.yaml`; thêm P0-AUT-096)

### RV-16 CLI: thứ tự hỏi mật khẩu và kiểm tham số
- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-25, R-AUT-27; test P0-AUT-088
- Vấn đề: P0-AUT-088 cho thấy mật khẩu được đọc cả khi tham số sai, nhưng R-AUT-25 không ghi. Trên terminal, người dùng gõ mật khẩu hai lần rồi mới biết thiếu `--role` hoặc tên đã tồn tại.
- Đề xuất: R-AUT-25 ghi thứ tự: kiểm tham số và trùng tên trước; có lỗi thì in hết, thoát mã 1, không hỏi mật khẩu khi stdin là terminal; stdin không phải terminal thì vẫn đọc và kiểm mật khẩu cùng lúc (giữ P0-AUT-088).
- Kết quả: đã sửa (R-AUT-25, R-AUT-26; P0-AUT-082 bước 5, 6)
