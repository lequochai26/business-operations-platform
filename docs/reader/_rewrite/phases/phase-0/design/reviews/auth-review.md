<!-- src-section: 0b0fa0b228 e1a96deca2d0 -->
# Review thiết kế – Đăng nhập và phân quyền (`auth`)

**Tóm tắt.** Bản review này soát thiết kế chi tiết, mockup, test case, traceability và tài liệu API, DB của tính năng đăng nhập và phân quyền. Review tìm ra 16 điểm (2 chặn, 9 nên sửa, 5 gợi ý), và tất cả đều đã được sửa.

- Ngày: 2026-10-31
- Đối tượng:
  - thiết kế chi tiết;
  - mockup (`login/`, `app-shell/`, `change-password/`, `forbidden/`, `not-found/`);
  - test case, traceability;
  - `api/sessions.md`, `api/users.md`, `db-schema.md`.
- Tổng: 16 điểm (2 chặn, 9 nên sửa, 5 gợi ý)

<!-- src-section: 548465f277 285ea9a8da37 -->
### RV-01 R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7

- Mức độ: chặn
- Vị trí: design/auth.md R-AUT-06, mục Trạng thái › Bộ đếm đăng nhập sai, mục Đăng nhập (`AuthService.login`); test P0-AUT-023, Ghi chú chạy

**Tóm tắt.** Câu hỏi 7 đã được chốt, nhưng quy tắc giới hạn đăng nhập sai và thuật toán bộ đếm vẫn giữ như cũ. Implement theo văn bản hiện tại thì P0-AUT-023 không đạt.

**Vấn đề**
- Bước đọc khóa chạy ngoài transaction và chạy trước bước kiểm mật khẩu.
- Bước ghi lần sai không kiểm xem tài khoản có đang bị khóa không. Vì vậy, khi đang khóa, lần sai vẫn được đếm. Tới lần thứ 5, khóa bị kéo dài.
- Một request đúng mật khẩu đã qua bước đọc khóa trước khi khóa được ghi vẫn đăng nhập được sau khi khóa đã ghi.
- Chưa có thuật toán đổi mật khẩu, dù R-AUT-20 dùng chung bộ đếm.

**Đề xuất**
- Bước ghi lần sai:
  - chạy trong transaction, khóa dòng rồi mới đọc;
  - nếu đang bị khóa thì trả về khóa và không thay đổi gì;
  - các trường hợp còn lại xử lý như bước 2–5 hiện tại.
- Nhánh đúng mật khẩu (đăng nhập, đổi mật khẩu):
  - chạy trong transaction, khóa dòng và kiểm lại khóa;
  - đang bị khóa thì trả 429, không tạo phiên, không đổi mật khẩu;
  - không bị khóa thì đặt lại bộ đếm;
  - mọi request bị chặn ở bước này đều được ghi log thất bại với lý do bị khóa.
- Ghi rõ: request đã qua bước kiểm mật khẩu mà gặp khóa lúc ghi luôn nhận 429. Nhờ vậy, kẻ dò không biết kết quả của các lần đoán vượt quá 5.
- Mục Trạng thái thêm chuyển không hợp lệ "bị khóa → bị khóa (kéo dài)". Mục này cũng thêm thuật toán đổi mật khẩu.
- P0-AUT-023 bước 2 đổi "tối đa 4 × 401" thành "đúng 4 × 401, 6 × 429".
- Bỏ dòng câu hỏi 7 khỏi Ghi chú chạy.

**Kết quả.** Đã sửa (R-AUT-06; `LoginThrottleService`; mục Trạng thái: bộ đếm, đăng nhập, thêm đổi mật khẩu; P0-AUT-023; Ghi chú chạy: test tự động).

**Chi tiết kỹ thuật**
- Bước đọc khóa: `getLock`. Bước kiểm mật khẩu: `verify`. Bước ghi lần sai: `recordFailure`. Đặt lại bộ đếm: `reset`.
- Điều kiện đang khóa: `locked_until > bây giờ`.
- Khóa dòng trong transaction: `SELECT … FOR UPDATE`.
- Thuật toán đổi mật khẩu cần thêm: `changePassword`, tức `AuthService.changePassword`.
- Log khi bị chặn: `auth.login.failed` / `auth.password.change_failed` với `reason: locked`.

<!-- src-section: 49b8d93df9 5dd8ac69f480 -->
### RV-02 R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câu hỏi mở 8)

- Mức độ: chặn
- Vị trí: design/auth.md R-AUT-28, R-AUT-31, mục `apps/web`; test P0-AUT-028, 029, 034, 037, 073, 091; traceability dòng R-AUT-31

**Tóm tắt.** Câu hỏi 8 đã chốt khi nào hiện banner báo phiên đã mất, nhưng thiết kế chưa có cơ chế để web biết điều đó. Đề xuất web tự giữ một cờ trong trình duyệt, không cần đổi API.

**Vấn đề**
- Câu hỏi 8 đã chốt "phiên không còn dùng được thì có banner, chưa từng đăng nhập thì không". Nhưng thiết kế chưa có cơ chế để làm việc này.
- Cookie phiên chỉ server đọc được, web không đọc được. Header xóa cookie cũng không đọc được từ phía web.
- Phiên hết hạn tự nhiên sau 90 ngày thì trình duyệt tự bỏ cookie. Request tới api không còn mang cookie, nên api không phân biệt được với trường hợp "chưa từng đăng nhập". Thêm mã lỗi riêng ở api không giải quyết được trường hợp chính này.
- Thiết kế chưa nói banner được truyền thế nào. Nếu banner được lưu trong trạng thái lịch sử của trình duyệt, tải lại trang đăng nhập vẫn còn banner. Điều này trái P0-AUT-029 bước 5.

**Đề xuất.** Chỉ đổi web, không đổi API:
- Web giữ một cờ "đã từng có phiên" trong bộ nhớ trình duyệt:
  - đặt cờ khi API lấy phiên hiện tại trả 200;
  - xóa cờ khi bấm "Đăng xuất" (trước khi gọi API), và khi đã dùng cờ để hiện banner;
  - đọc và ghi cờ trong try/catch; lỗi thì coi như không có cờ.
- Mở app mà nhận 401:
  - có cờ thì xóa cờ, chuyển tới trang đăng nhập kèm banner "Phiên đăng nhập…";
  - không có cờ thì chuyển tới trang đăng nhập, không có banner.
- Đang dùng app (đã có người dùng trong bộ quản lý phiên) mà nhận 401 thì luôn có banner, như R-AUT-31 hiện tại.
- Banner info của R-AUT-31 và R-AUT-32 được giữ trong bộ nhớ của bộ quản lý phiên. Banner không đưa vào URL hay trạng thái lịch sử. Tải lại trang đăng nhập thì banner mất.
- Sửa dòng R-AUT-31 trong traceability. Bỏ dòng câu hỏi 8 khỏi Ghi chú chạy của test case.

**Kết quả.** Đã sửa (R-AUT-31, R-AUT-32, `auth-provider`, màn Đăng nhập; P0-AUT-001, 034; traceability R-AUT-31; Ghi chú chạy). Người dùng chấp nhận: nếu trình duyệt chặn lưu dữ liệu thì không có banner.

**Chi tiết kỹ thuật**
- Cookie phiên: `HttpOnly`. Header xóa cookie: `Set-Cookie`, không đọc được từ `fetch`.
- Trình duyệt bỏ cookie theo `Max-Age`.
- Trạng thái lịch sử: `history.state`. Trang đăng nhập: `/login`.
- Cờ: `mio.hadSession` trong `localStorage`.
- API lấy phiên hiện tại: `GET /api/v1/sessions/current`.
- Chuyển trang khi có cờ: `/login?next=…`.
- Bộ quản lý phiên phía web: `auth-provider`.

<!-- src-section: c007295390 ea442d2828d7 -->
### RV-03 Câu hỏi mở 9 chưa đưa vào mục Xử lý lỗi

- Mức độ: nên sửa
- Vị trí: design/auth.md mục Xử lý lỗi; test P0-AUT-075

**Tóm tắt.** Quyết định cho trường hợp chuỗi băm mật khẩu bị hỏng đã được chốt nhưng chưa có trong mục Xử lý lỗi. Đề xuất ghi rõ cách xử lý.

**Vấn đề**
- Đã chốt "`password_hash` không phải chuỗi PHC → 500", nhưng mục Xử lý lỗi chưa có dòng này.
- Thiết kế chưa nói lỗi này có được đếm vào R-AUT-06 hay ghi log `auth.login.failed` không.

**Đề xuất.** Thêm vào mục Xử lý lỗi:
- Khi bước kiểm mật khẩu ném lỗi vì chuỗi băm hỏng, API trả 500 (R-SKL-16).
- Ghi log mức error có mã người dùng. Log không chứa chuỗi băm.
- Không đếm vào R-AUT-06 và không ghi `auth.login.failed`.
- Áp dụng cho cả đăng nhập và đổi mật khẩu.

**Kết quả.** Đã sửa (mục Xử lý lỗi; P0-AUT-075 bước 3).

**Chi tiết kỹ thuật**
- Bước kiểm mật khẩu: `verify`.
- Mã lỗi: 500 `INTERNAL_ERROR`.
- Trường mã người dùng trong log: `userId`.

<!-- src-section: a6d1239d02 8b86bbe0dcea -->
### RV-04 Hai lần đổi mật khẩu đồng thời có thể mất cập nhật

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-23, R-AUT-24; test P0-AUT-066

**Tóm tắt.** Hai request đổi mật khẩu chạy cùng lúc có thể cùng báo thành công, nhưng chỉ một mật khẩu thật sự được lưu. Đề xuất chạy đổi mật khẩu trong transaction có khóa dòng.

**Vấn đề**
- Thiết kế chưa quy định transaction cho việc đổi mật khẩu.
- Hai request A và B cùng đọc chuỗi băm cũ, cùng kiểm mật khẩu đúng, rồi lần lượt ghi.
- Cả hai nhận 204 và toast "Đã đổi mật khẩu". Nhưng chỉ mật khẩu của request ghi sau là dùng được.
- Nếu không chọn đăng xuất thiết bị khác, A tin mật khẩu mới là của mình, nhưng thực tế không phải.
- Lệnh đặt lại mật khẩu chạy cùng lúc cũng bị như vậy.

**Đề xuất**
- R-AUT-23:
  - đổi mật khẩu chạy trong một transaction và khóa dòng người dùng;
  - mật khẩu hiện tại được kiểm trên chuỗi băm đọc sau khi đã khóa;
  - chuỗi băm, phiên và bộ đếm được ghi trong cùng transaction đó.
- Lệnh đặt lại mật khẩu cũng khóa dòng người dùng.
- P0-AUT-066 bước 1 đổi kết quả mong đợi thành "đúng một request 204; request còn lại 400 'Mật khẩu hiện tại không đúng' hoặc 401".

**Kết quả.** Đã sửa (R-AUT-23, R-AUT-26, `UsersRepository.lockById`/`lockByUsername`, thuật toán đổi mật khẩu; P0-AUT-066; Ghi chú chạy: test tự động).

**Chi tiết kỹ thuật**
- Bước kiểm mật khẩu: `verify`.
- Tùy chọn không đăng xuất thiết bị khác: `signOutOtherDevices: false`.
- Lệnh đặt lại mật khẩu: `reset-password`.
- Khóa dòng bảng `users`: `SELECT … FOR UPDATE`.

<!-- src-section: c02158d7d3 1b2f6b81ec4b -->
### RV-05 `failedCount` của lần sai làm khóa chưa rõ

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-30; test P0-AUT-020 bước 3, P0-AUT-063 bước 6

**Tóm tắt.** Số lần sai ghi trong log ở lần sai làm khóa tài khoản có thể là 5 hoặc 0. Đề xuất chốt giá trị là 5.

**Vấn đề**
- Trường số lần sai trong log được định nghĩa là "số lần sai trong cửa sổ sau lần này".
- Nhưng ở lần sai thứ 5, DB đặt bộ đếm về 0. Vì vậy dòng log có thể ghi 5 hoặc 0.
- Test chỉ kiểm 4 dòng đầu.

**Đề xuất**
- R-AUT-30 ghi "lần sai làm khóa: `failedCount` 5 và có `lockedUntil`".
- P0-AUT-020 bước 3 thêm kết quả mong đợi "dòng thứ 5 có `failedCount` 5, `lockedUntil`".

**Kết quả.** Đã sửa (R-AUT-30; P0-AUT-020 bước 3, P0-AUT-023 bước 3, P0-AUT-063 bước 6).

**Chi tiết kỹ thuật**
- Trường số lần sai trong log: `failedCount`. Trường thời điểm hết khóa: `lockedUntil`.
- DB đặt `failed_count = 0` ở lần sai thứ 5.

<!-- src-section: 808024fba1 3c265de897e1 -->
### RV-06 Thứ tự kiểm tra chưa tính bước đọc thân request

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-15, `OriginCheckMiddleware`; test P0-AUT-045

**Tóm tắt.** Thứ tự kiểm tra request trong thiết kế bỏ sót bước đọc thân request. Vì vậy, request có nguồn gốc lạ kèm JSON hỏng sẽ nhận 400 thay vì 403.

**Vấn đề**
- R-AUT-15 ghi thứ tự kiểm tra: R-AUT-17, rồi R-AUT-11, rồi R-AUT-15, rồi kiểm dữ liệu.
- Trong NestJS, bước đọc thân request chạy trước middleware đăng ký qua module và trước guard. Bước này sinh lỗi JSON sai cú pháp và lỗi thân quá lớn.
- Nếu thiết kế không nói gì, request có nguồn gốc lạ kèm JSON hỏng nhận 400 thay vì 403. Kết quả này trái thứ tự đã ghi.

**Đề xuất**
- R-AUT-15 ghi đủ thứ tự:
  - R-AUT-17;
  - đọc thân request (lỗi JSON sai cú pháp, lỗi thân quá lớn);
  - R-AUT-11;
  - R-AUT-15;
  - kiểm dữ liệu.
- Bước kiểm nguồn gốc request được đăng ký ở cấp app, trước bước đọc thân request.
- P0-AUT-045 thêm bước:
  - nguồn gốc lạ và JSON hỏng thì nhận 403;
  - nguồn gốc đúng, không có cookie, JSON hỏng thì nhận 400.

**Kết quả.** Đã sửa (R-AUT-15, `OriginCheckMiddleware`; P0-AUT-045 bước 6, 7).

**Chi tiết kỹ thuật**
- Lỗi của bước đọc thân: `INVALID_JSON`, `PAYLOAD_TOO_LARGE`.
- Header nguồn gốc: `Origin`.
- Đăng ký trước body parser: `app.use`.
- Lỗi nguồn gốc lạ: 403 `INVALID_ORIGIN`. Lỗi JSON hỏng: 400 `INVALID_JSON`.

<!-- src-section: a02048905c 7a7e6955b394 -->
### RV-07 Đổi mật khẩu: trường sai kiểu chưa có quy tắc

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-19, R-AUT-21; test P0-AUT-057 bước 3, P0-AUT-056

**Tóm tắt.** Form đổi mật khẩu chưa có quy tắc cho trường sai kiểu, nhưng test case đã giả định một hành vi. Đề xuất thêm quy tắc chung và bổ sung case còn thiếu.

**Vấn đề**
- Câu "Trường không phải chuỗi hoặc thiếu → cùng thông báo như trống" chỉ có ở phần đăng nhập.
- P0-AUT-057 lại mong khi mật khẩu hiện tại là số thì hiện "Nhập mật khẩu hiện tại". Tức là test đặt ra một hành vi mà thiết kế chưa ghi.
- Trường mật khẩu mới sai kiểu chưa có case. Checklist test yêu cầu mọi trường đều có case sai kiểu.

**Đề xuất**
- R-AUT-21 thêm một dòng chung cho R-AUT-19 và R-AUT-21: mật khẩu hiện tại hoặc mật khẩu mới không phải chuỗi, hoặc bị thiếu, thì hiện cùng thông báo như khi để trống.
- P0-AUT-056 bước 5 thêm trường hợp mật khẩu mới là số `12345678`. Kết quả mong đợi là "Nhập mật khẩu mới".

**Kết quả.** Đã sửa (R-AUT-21; P0-AUT-056 bước 6).

**Chi tiết kỹ thuật**
- Giá trị thử trong P0-AUT-057: `currentPassword: 123`.
- Tên trường: `currentPassword`, `newPassword`.

<!-- src-section: 5fc14e1926 140a9cc9acb6 -->
### RV-08 Tên đăng nhập dài hơn 32 ký tự sau khi đổi chữ thường làm lỗi 500

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-02, R-AUT-07; `db-schema.md` `login_throttles.username` (check 1–32); test P0-AUT-007

**Tóm tắt.** Độ dài tên đăng nhập đang được đo trước khi đổi sang chữ thường. Một số ký tự dài ra khi đổi chữ thường, nên tên đã chuẩn hóa có thể vượt giới hạn của DB và gây lỗi 500.

**Vấn đề**
- R-AUT-02 đo độ dài sau khi bỏ khoảng trắng, nhưng trước khi đổi chữ thường.
- Một số ký tự dài ra khi đổi chữ thường. Ví dụ: chữ `İ` khi đổi chữ thường thành `i` cộng một dấu chấm kết hợp (2 code point).
- Nhập 32 ký tự `İ` thì qua được R-AUT-02. Nhưng tên đã chuẩn hóa dài 64 ký tự.
- Khi ghi vào bảng giới hạn đăng nhập, giá trị này vi phạm ràng buộc độ dài, nên API trả 500.

**Đề xuất**
- R-AUT-02 đo độ dài trên tên đã chuẩn hóa, ở cả web lẫn API.
- P0-AUT-007 thêm bước: nhập 32 ký tự `İ` thì nhận 400 "Tên đăng nhập tối đa 32 ký tự", không có 500.

**Kết quả.** Đã sửa (R-AUT-02; `api/sessions.md`, `openapi.yaml` bỏ `maxLength` của `username`; P0-AUT-007 bước 6).

**Chi tiết kỹ thuật**
- Ví dụ: `'İ'.toLowerCase()` cho ra `i` + dấu chấm kết hợp.
- Giá trị thử: `İ` × 32.
- Bảng giới hạn đăng nhập: `login_throttles`.
- Hàm chuẩn hóa: `normalizeUsername`.

<!-- src-section: 50f58f0b24 71ac854a0435 -->
### RV-09 Log của lệnh CLI không nằm trong `docker compose logs api`

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-30 (`auth.cli.*`, cách lọc log); test P0-AUT-079 bước 5–6, P0-AUT-080 bước 2, P0-AUT-081, P0-AUT-093

**Tóm tắt.** Lệnh CLI chạy thành một tiến trình riêng, nên log của nó không vào log của container api. Đề xuất ghi log CLI vào stdout của tiến trình chính.

**Vấn đề**
- Lệnh CLI chạy trong container là một tiến trình riêng. Stdout của nó ra terminal của người chạy, không vào log của container.
- Hệ quả:
  - lọc log của container không thấy sự kiện CLI, nên P0-AUT-079 bước 6 không đạt;
  - dòng log JSON in lẫn với thông báo cho người dùng ("Đã tạo tài khoản…"); lệnh liệt kê tài khoản không còn ra "đúng 3 dòng" nếu có log;
  - sự kiện CLI không có mã request và địa chỉ IP, trong khi R-AUT-30 đòi "mọi sự kiện" phải có.

**Đề xuất**
- Phương án A:
  - CLI in thông báo cho người dùng ra stdout;
  - log JSON được ghi vào stdout của tiến trình chính, để lệnh xem log của container thấy được. Điều này làm được vì cùng uid 1000 và Node là PID 1 theo R-SKL-22;
  - nếu không mở được thì ghi ra stderr;
  - cách này cần kiểm chứng khi implement.
- Phương án khác: chấp nhận log CLI chỉ ra stderr của lệnh. R-AUT-30 ghi rõ log của container chỉ có sự kiện HTTP.
- R-AUT-30: sự kiện CLI có tên sự kiện, thời điểm và tên đăng nhập, không có mã request và địa chỉ IP.
- P0-AUT-079 bước 5–6 và P0-AUT-080 bước 2 sửa theo phương án được chọn.

**Kết quả.** Đã sửa theo phương án A (R-AUT-30; P0-AUT-079 bước 5–6, P0-AUT-081 bước 2; Ghi chú chạy: phương án dự phòng stderr kiểm bằng test tự động).

**Chi tiết kỹ thuật**
- Lệnh CLI: `docker compose exec api node dist/cli.js …`.
- Lệnh lọc log: `docker compose logs api | grep '"event":"auth.'`; không thấy `auth.cli.*`.
- Lệnh liệt kê tài khoản: `list-users`.
- Đường ghi log JSON: `/proc/1/fd/1`.
- Lệnh xem log: `docker compose logs api`; phương án khác ghi rõ `docker compose logs` chỉ có sự kiện HTTP.
- Trường của sự kiện CLI: `event`, `time`, `username`; không có `requestId`, `ip`.

<!-- src-section: 0d67ff357a 0bf8592e8cca -->
### RV-10 Đăng xuất lỗi: chưa rõ có hiện "Bạn đã đăng xuất" không

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-32; test P0-AUT-036 bước 1

**Tóm tắt.** Khi đăng xuất bị lỗi, thiết kế chưa nói có hiện banner báo đã đăng xuất không. Đề xuất chỉ hiện banner khi đăng xuất thật sự thành công.

**Vấn đề**
- R-AUT-32 nói đăng xuất lỗi thì vẫn chuyển tới trang đăng nhập, nhưng không nói về banner.
- Hiện "Bạn đã đăng xuất" khi phiên và cookie vẫn còn là báo sai. Người dùng tưởng đã thoát, và người sau mở app sẽ vào thẳng được.

**Đề xuất**
- R-AUT-32 ghi: chỉ hiện banner "Bạn đã đăng xuất" khi API trả 204.
- Lỗi mạng hoặc lỗi 500 thì chuyển tới trang đăng nhập, không có banner.
- P0-AUT-036 bước 1, 3 thêm kết quả mong đợi "không có banner 'Bạn đã đăng xuất'".
- Phương án khác: ở lại trang, hiện toast danger và cho bấm lại. Phương án này đổi quyết định đã ghi, nên không được đề xuất làm mặc định.

**Kết quả.** Đã sửa (R-AUT-32; `login/notes.md`; P0-AUT-036 bước 1, 3).

**Chi tiết kỹ thuật**
- Trang đăng nhập: `/login`.

<!-- src-section: 5c756ce928 48fd870f1d8a -->
### RV-11 403 khi gửi form hiện bằng toast, trái quy ước vị trí thông báo

- Mức độ: nên sửa
- Vị trí: design/auth.md R-AUT-29; test P0-AUT-044; `docs/design/ui/app-shell/notes.md` (`forbidden.html`)

**Tóm tắt.** Lỗi 403 luôn hiện bằng toast, kể cả khi người dùng gửi form. Điều này trái quy ước vị trí thông báo. Thanh điều hướng cũng chưa cập nhật khi vai trò bị đổi.

**Vấn đề**
- R-AUT-29 luôn hiện toast danger khi API trả 403.
- Theo `ui-style.md` mục "Vị trí thông báo" (ADR 0016), lỗi khi gửi form phải hiện ở vùng thông báo ngay trên hàng nút gửi. Toast chỉ dùng cho thao tác không có form.
- P0-AUT-044 bấm nút lưu trên màn Cài đặt, vốn là một form, nhưng lại mong toast.
- Ngoài ra, khi vai trò vừa bị đổi, thanh điều hướng vẫn giữ các mục cũ.

**Đề xuất**
- R-AUT-29 xử lý lỗi 403 như sau:
  - khi gửi form: hiện banner danger ở vùng thông báo của form;
  - khi thao tác không có form: hiện toast danger;
  - cả hai trường hợp đều tải lại thông tin phiên, để thanh điều hướng và màn Không có quyền theo vai trò mới.
- P0-AUT-044 bước 2 đổi thành banner trên form. Thêm bước "thanh điều hướng còn 'Trang chính', trang hiện màn Không có quyền".
- `app-shell/notes.md` ghi rõ `forbidden.html` là trường hợp không có form.

**Kết quả.** Đã sửa (R-AUT-29, `api-client.ts`; `app-shell/notes.md`; P0-AUT-044).

**Chi tiết kỹ thuật**
- Mã lỗi: 403 `FORBIDDEN`.
- Tải lại thông tin phiên: `refresh()` của `auth-provider`.

<!-- src-section: 5becdb5c01 94f1c810991a -->
### RV-12 Câu "Phiên đăng nhập đã hết hạn" dùng cả khi phiên bị xóa

- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-31; mockup `login/session-expired.html`; test P0-AUT-028, 029, 030, 050, 073, 091

**Tóm tắt.** Banner báo phiên hết hạn đang được dùng chung cho cả những trường hợp phiên bị xóa. Đề xuất đổi sang một câu trung tính.

**Vấn đề**
- Banner này dùng chung cho nhiều trường hợp:
  - phiên hết hạn;
  - bị đăng xuất do đổi hoặc đặt lại mật khẩu;
  - tài khoản bị xóa;
  - cookie hỏng.
- Theo ADR 0016, câu dùng chung phải đúng nghĩa ở mọi chỗ nó hiện. Chữ "hết hạn" chưa đúng hẳn khi phiên bị đăng xuất từ thiết bị khác.

**Đề xuất**
- Đổi thành câu trung tính "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" ở thiết kế, mockup và test case.
- Giữ câu cũ cũng chấp nhận được.

**Kết quả.** Đã sửa (R-AUT-31, màn Đăng nhập; mockup `login/session-expired.html` và ảnh chụp, `login/notes.md`; mọi case có banner này).

<!-- src-section: c731f7368d 8e205ca6ad92 -->
### RV-13 Một trường có hai lỗi cùng lúc: chưa nói hiện lỗi nào

- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-21, R-AUT-25

**Tóm tắt.** Một trường có thể vi phạm hai quy tắc cùng lúc, nhưng thiết kế chưa nói hiện lỗi nào. Đề xuất mỗi trường chỉ hiện một lỗi theo thứ tự ưu tiên.

**Vấn đề**
- Khi tên đăng nhập dài 3–7 ký tự, mật khẩu mới trùng tên đăng nhập sẽ vi phạm cả hai quy tắc: "8 đến 128 ký tự" và "không trùng tên đăng nhập".
- Zod trả về cả hai lỗi.
- Web chỉ hiện một dòng dưới ô. Còn CLI "in mọi lỗi" nên có thể in hai dòng cho mật khẩu.

**Đề xuất**
- Ghi quy tắc "mỗi trường chỉ một lỗi, lấy theo thứ tự trống → độ dài → trùng tên đăng nhập".
- Quy tắc áp dụng cho web, API và CLI.

**Kết quả.** Đã sửa (quy tắc chung đầu mục Quy tắc; P0-AUT-087 bước 5; traceability).

**Chi tiết kỹ thuật**
- Danh sách lỗi theo trường trong API: `fields`.

<!-- src-section: a5227a25e1 0cc3b760d441 -->
### RV-14 Kiểm tra `next` chưa chặn ký tự điều khiển

- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-28; test P0-AUT-038

**Tóm tắt.** Tham số chuyển trang sau đăng nhập chưa chặn ký tự điều khiển. Kẻ xấu có thể lợi dụng để đưa người dùng ra khỏi app.

**Vấn đề**
- Trình duyệt bỏ ký tự tab và xuống dòng khi phân tích URL.
- Vì vậy, một đường dẫn có ký tự tab qua được điều kiện "không bắt đầu bằng `//`", nhưng sau khi phân tích lại thành đường dẫn tới trang ngoài.
- Nếu chuyển trang bằng cách gán địa chỉ trực tiếp, người dùng sẽ rời app.

**Đề xuất**
- R-AUT-28 thêm quy tắc: tham số chuyển trang chứa ký tự điều khiển hoặc khoảng trắng thì chuyển về trang gốc.
- Chuyển trang bằng router của app, không gán địa chỉ trực tiếp.
- P0-AUT-038 thêm một bước thử với giá trị chứa ký tự tab. Kết quả mong đợi là về trang gốc.

**Kết quả.** Đã sửa (R-AUT-28; P0-AUT-038 bước 8).

**Chi tiết kỹ thuật**
- Tham số chuyển trang: `next`.
- Đường dẫn có tab: `/<tab>/evil.example`, sau khi phân tích thành `//evil.example`.
- Cách chuyển trang gây rời app: `location.href`.
- Trang gốc: `/`.
- Giá trị thử: `next=%2F%09%2Fevil.example`.

<!-- src-section: 0d0fe48bc0 ad88f32464aa -->
### RV-15 Phiên khi gọi route công khai lúc đang có cookie

- Mức độ: gợi ý
- Vị trí: design/auth.md mục Kiểm tra request bước 1, R-AUT-08, R-AUT-10

**Tóm tắt.** Thiết kế chưa nói rõ route công khai xử lý phiên đang có thế nào. Đăng nhập lại khi đang có phiên sẽ để lại phiên cũ, và đăng xuất có thể gửi hai lệnh đặt cookie.

**Vấn đề**
- Gọi API đăng nhập khi đang có phiên hợp lệ sẽ tạo phiên mới. Ví dụ: đăng nhập ở hai tab, hoặc đổi tài khoản qua API. Phiên cũ nằm lại tới 90 ngày.
- Route công khai "vẫn đọc phiên", nhưng thiết kế chưa nói có gia hạn phiên không.
- API đăng xuất gia hạn rồi xóa phiên sẽ gửi hai lệnh đặt cookie cho cùng một cookie.

**Đề xuất**
- Route công khai đọc phiên nhưng không gia hạn. R-AUT-10 chỉ áp dụng cho route có yêu cầu vai trò.
- Đăng nhập thành công mà request mang cookie của một phiên còn hiệu lực thì xóa phiên đó.

**Kết quả.** Đã sửa (R-AUT-08, R-AUT-10, mục Kiểm tra request bước 1, thuật toán đăng nhập; `api/sessions.md`, `openapi.yaml`; thêm P0-AUT-096).

**Chi tiết kỹ thuật**
- API đăng nhập: `POST /api/v1/sessions` (viết gọn `POST /sessions`).
- API đăng xuất: `DELETE /sessions/current`.
- Header đặt cookie: `Set-Cookie`.
- Route công khai: `@Public()`. Route có yêu cầu vai trò: `@Roles`.

<!-- src-section: 957cb7b3be b33d142e53ae -->
### RV-16 CLI: thứ tự hỏi mật khẩu và kiểm tham số

- Mức độ: gợi ý
- Vị trí: design/auth.md R-AUT-25, R-AUT-27; test P0-AUT-088

**Tóm tắt.** CLI đang hỏi mật khẩu trước khi kiểm tham số, nên người dùng phải gõ mật khẩu rồi mới biết tham số sai. Đề xuất kiểm tham số trước.

**Vấn đề**
- P0-AUT-088 cho thấy mật khẩu được đọc cả khi tham số sai, nhưng R-AUT-25 không ghi điều này.
- Trên terminal, người dùng gõ mật khẩu hai lần rồi mới biết thiếu tham số vai trò hoặc tên đã tồn tại.

**Đề xuất.** R-AUT-25 ghi thứ tự:
- Kiểm tham số và kiểm trùng tên trước.
- Có lỗi thì in hết lỗi, thoát mã 1, và không hỏi mật khẩu khi đầu vào là terminal.
- Khi đầu vào không phải terminal thì vẫn đọc và kiểm mật khẩu cùng lúc, để giữ đúng P0-AUT-088.

**Kết quả.** Đã sửa (R-AUT-25, R-AUT-26; P0-AUT-082 bước 5, 6).

**Chi tiết kỹ thuật**
- Tham số vai trò: `--role`.
