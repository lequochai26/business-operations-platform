# Test case – Khung ứng dụng (`app-skeleton`, `SKL`)

- Thiết kế: `docs/phases/phase-0/design/app-skeleton.md`
- Mockup: không có
- Cập nhật: 2026-10-31

## Khía cạnh không áp dụng

- 5. Phân quyền: khung chưa có vai trò và đăng nhập (thuộc `auth`). Chỉ kiểm quyền truy cập mức hệ thống: `/health` công khai, cổng chỉ mở trên `127.0.0.1`, container không chạy bằng root (xếp vào khía cạnh 3 và 11).
- 6. Phiên đăng nhập và cookie: khung không có phiên web app (thuộc `auth`) và không mở phiên Facebook (thuộc `fb-account-session`).
- 9. Phía Facebook và Messenger: khung không gọi Facebook, Gemini hay Messenger (thiết kế mục Tích hợp bên ngoài).

## Ghi chú chạy

- Mọi lệnh chạy từ gốc repo, Docker Desktop đang chạy, `.env` tạo từ `.env.example`. `<image api>`, `<image browser-worker>` là image do `pnpm docker:build` tạo.
- Khóa Redis của BullMQ dùng tiền tố mặc định `bull` (ví dụ `bull:fb-browser:meta`); implement đặt tiền tố khác thì thay tương ứng.
- Case cần tính năng sau (ghi trong Tiền điều kiện; chạy `/manual-test-run` khi chưa có tính năng đó thì case là `bị chặn`, chạy lại sau):
  - cần `crawl-settings` (khóa `crawl-schedule` và endpoint `/api/v1/settings/crawl-schedule`) và `auth` (phiên Quản lý): P0-SKL-045 … P0-SKL-055, P0-SKL-065, P0-SKL-068. Tên trường, giới hạn và thông báo của khóa lấy theo thiết kế `crawl-settings`; ví dụ dưới đây dùng `maxScrolls` (1–20) như R-SKL-12.
  - cần `group-crawl-job` (job thật trên `fb-browser`): P0-SKL-056 … P0-SKL-064, P0-SKL-069.
- Phần "hàng đợi `render` không dùng profile Facebook" của R-SKL-05 kiểm chứng trong test case của tính năng render ở giai đoạn 4.
- Phần chỉ kiểm được bằng test tự động (không tạo được bằng thao tác bên ngoài code); `/implementation-plan` phải có test tương ứng:
  - R-SKL-07: mọi Worker đặt `maxStalledCount: 0` (hành vi kiểm ở P0-SKL-060, P0-SKL-061);
  - R-SKL-10: khóa không có trong `SETTINGS` lúc chạy → 500 `INTERNAL_ERROR`;
  - R-SKL-28, R-SKL-29: processor ném lỗi vẫn gửi kết quả `UnexpectedError`; stalled giả (kết quả thật tới sau `WorkerCrashedError`) → kết quả thật thắng, mỗi tín hiệu ghi nhận một lần;
  - R-SKL-17: từng đường dẫn trong danh sách che.
- Khóa nhịp sống theo container: `mio:heartbeat:browser-worker:<hostname>`, hostname lấy bằng `docker compose exec browser-worker hostname`; các bước dưới viết tắt là `<khóa nhịp sống>`.

## P0-SKL-001 Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose
- Thiết kế: R-SKL-03, R-SKL-13, R-SKL-14; mục Trạng thái và thuật toán › Khởi động
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `MIO_DATA_DIR` trỏ tới thư mục trống; chưa có volume DB (`docker compose down -v` trên môi trường thử, không có dữ liệu cần giữ)
- Các bước:
  1. `pnpm docker:build` → build xong, không lỗi
  2. `docker compose up -d`, chờ tối đa 2 phút, `docker compose ps` → 4 dịch vụ `postgres`, `redis`, `api`, `browser-worker` đều `running (healthy)` [evidence]
  3. `docker inspect -f '{{.Name}} {{.State.StartedAt}}'` cho 4 container → `api` khởi động sau khi `postgres`, `redis` healthy; `browser-worker` khởi động sau khi `api` healthy [evidence]
  4. `docker inspect -f '{{.HostConfig.RestartPolicy.Name}}'` cho 4 container → đều `unless-stopped`
  5. `curl -s http://127.0.0.1:3000/api/v1/health` → 200, thân `{"status":"ok","checks":{"database":"up","redis":"up"}}` [evidence]
  6. Mở `http://127.0.0.1:3000/` bằng Playwright → trang hiển thị "Tiệm Nhà Mio" [evidence]

## P0-SKL-002 api thiếu một biến môi trường bắt buộc
- Thiết kế: R-SKL-01
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã build `<image api>`
- Các bước:
  1. `docker run --rm -e DATABASE_URL=postgres://mio:x@postgres:5432/mio -e DATA_DIR=/data -e PUBLIC_URL=http://localhost:3000 <image api>` (bỏ `REDIS_URL`) → tiến trình dừng ngay, `echo $?` → `1` [evidence]
  2. Đọc log → một dòng JSON mức error có thông báo "Thiếu biến môi trường: REDIS_URL"; không có dòng log mở cổng 3000 [evidence]

## P0-SKL-003 api thiếu cả bốn biến môi trường
- Thiết kế: R-SKL-01
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã build `<image api>`
- Các bước:
  1. `docker run --rm <image api>` (không truyền biến nào) → thoát mã 1
  2. Đọc log → đúng một dòng thông báo liệt kê cả bốn biến: "Thiếu biến môi trường: DATABASE_URL, REDIS_URL, DATA_DIR, PUBLIC_URL" (thứ tự có thể khác, nhưng đủ 4 tên trong một dòng) [evidence]

## P0-SKL-004 Biến bắt buộc thiếu hoặc rỗng trong `.env` và trong container
- Thiết kế: R-SKL-01; bảng biến Compose (cú pháp `${TÊN:?…}`)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001; sao lưu `.env`; ghi lại `StartedAt` của 4 container
- Các bước:
  1. Xóa dòng `MIO_PUBLIC_URL` trong `.env`, `docker compose up -d; echo $?` → lệnh dừng ngay, in "Thiếu MIO_PUBLIC_URL trong .env", mã khác `0` [evidence]
  2. `StartedAt` của 4 container → không đổi (không container nào bị tạo lại hay khởi động lại)
  3. Đặt `MIO_PUBLIC_URL=` (rỗng) → cùng kết quả như bước 1–2
  4. Lặp lại bước 1 với `POSTGRES_PASSWORD`, `MIO_DATA_DIR` → thông báo đúng tên biến tương ứng
  5. Trả lại `.env`. `docker run --rm` `<image api>` với đủ biến nhưng `-e PUBLIC_URL=` → thoát mã 1, log "Thiếu biến môi trường: PUBLIC_URL" [evidence]
  6. Lặp lại bước 5 với `-e "PUBLIC_URL=   "` (chỉ khoảng trắng) → cùng thông báo, thoát mã 1

## P0-SKL-005 REDIS_URL sai định dạng
- Thiết kế: R-SKL-02
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã build `<image api>`, `<image browser-worker>`
- Các bước:
  1. Chạy `<image api>` với đủ biến, `REDIS_URL=http://redis:6379` → thoát mã 1, log "Biến môi trường không hợp lệ: REDIS_URL (phải là URL redis://)" [evidence]
  2. Lặp lại với `REDIS_URL=redis` (không phải URL) → cùng thông báo, thoát mã 1
  3. Lặp lại bước 1 với `<image browser-worker>` → cùng thông báo, thoát mã 1 [evidence]
  4. Tìm `http://redis:6379` trong toàn bộ log của các lần chạy → không có (giá trị biến không bị in)

## P0-SKL-006 DATABASE_URL: phân vùng hợp lệ / không hợp lệ và không lộ mật khẩu
- Thiết kế: R-SKL-02, R-SKL-17
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. Chạy api với `DATABASE_URL=postgresql://mio:<mật khẩu đúng>@postgres:5432/mio` (tiền tố `postgresql://`), nối vào mạng Compose → khởi động bình thường, `/api/v1/health` của container này trả 200
  2. Chạy api với `DATABASE_URL=mysql://mio:Secret123@postgres:5432/mio` → thoát mã 1, log "Biến môi trường không hợp lệ: DATABASE_URL (phải là URL postgres:// hoặc postgresql://)" [evidence]
  3. Chạy api với `DATABASE_URL=abc` → cùng thông báo, thoát mã 1
  4. Tìm `Secret123` trong log của bước 2 → không có [evidence]

## P0-SKL-007 PUBLIC_URL: phân vùng hợp lệ / không hợp lệ
- Thiết kế: R-SKL-02
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương, giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `PUBLIC_URL=https://mio.example.com` → api khởi động bình thường
  2. `PUBLIC_URL=http://localhost:3000/` (có `/` cuối) → thoát mã 1, "Biến môi trường không hợp lệ: PUBLIC_URL (phải là URL http:// hoặc https://, không có / cuối)" [evidence]
  3. `PUBLIC_URL=localhost:3000` (thiếu scheme) → cùng thông báo, thoát mã 1
  4. `PUBLIC_URL=ftp://localhost` → cùng thông báo, thoát mã 1

## P0-SKL-008 DATA_DIR, BROWSER_PROFILE_DIR là đường dẫn tương đối
- Thiết kế: R-SKL-02
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã build `<image api>`, `<image browser-worker>`
- Các bước:
  1. Chạy api với `DATA_DIR=data` → thoát mã 1, "Biến môi trường không hợp lệ: DATA_DIR (phải là đường dẫn tuyệt đối)" [evidence]
  2. Lặp lại với browser-worker → cùng thông báo, thoát mã 1
  3. Chạy browser-worker với `DATA_DIR=/data`, `BROWSER_PROFILE_DIR=browser-profile` → thoát mã 1, "Biến môi trường không hợp lệ: BROWSER_PROFILE_DIR (phải là đường dẫn tuyệt đối)"

## P0-SKL-009 browser-worker chỉ cần REDIS_URL, DATA_DIR, BROWSER_PROFILE_DIR
- Thiết kế: R-SKL-01, R-SKL-04
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: `redis` đang chạy
- Các bước:
  1. Chạy `<image browser-worker>` trong mạng Compose với `--hostname skl-009`, chỉ có `REDIS_URL`, `DATA_DIR`, `BROWSER_PROFILE_DIR` (không có `DATABASE_URL`, `PUBLIC_URL`) → chạy bình thường, sau 20 giây khóa `mio:heartbeat:browser-worker:skl-009` có giá trị mới [evidence]
  2. Chạy lại chỉ với `DATA_DIR` → thoát mã 1, "Thiếu biến môi trường: REDIS_URL, BROWSER_PROFILE_DIR" (thứ tự có thể khác; không đòi `DATABASE_URL`, `PUBLIC_URL`) [evidence]

## P0-SKL-010 Thư mục dữ liệu không ghi được
- Thiết kế: R-SKL-20
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã build hai image
- Các bước:
  1. Chạy api, gắn thư mục chỉ đọc `-v <thư mục tạm>:/data:ro`, `DATA_DIR=/data` → thoát mã 1, "Không ghi được vào thư mục dữ liệu: /data" [evidence]
  2. Lặp lại bước 1 với browser-worker → cùng thông báo, thoát mã 1
  3. Chạy api với `DATA_DIR=/khong-co-quyen/data` (thư mục cha không ghi được bằng user không root) → thoát mã 1, "Không ghi được vào thư mục dữ liệu: /khong-co-quyen/data"
  4. Chạy browser-worker với `-v <thư mục tạm>:/browser-profile:ro`, `BROWSER_PROFILE_DIR=/browser-profile` → thoát mã 1, "Không ghi được vào thư mục dữ liệu: /browser-profile" [evidence]

## P0-SKL-011 Thư mục con, profile trong named volume, cùng user không phải root
- Thiết kế: R-SKL-20; ADR 0013
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: `MIO_DATA_DIR` trỏ tới thư mục trống; hệ thống đang dừng; chưa có volume `mio-browser-profile` (`docker compose down -v` trên môi trường thử)
- Các bước:
  1. `docker compose up -d postgres redis api`, chờ api healthy, liệt kê `MIO_DATA_DIR` → có `images/`, `debug-dumps/` [evidence]
  2. `docker compose up -d browser-worker`, chờ healthy → `docker volume ls` có volume tên kết thúc bằng `mio-browser-profile`; `MIO_DATA_DIR` không có `browser-profile/` [evidence]
  3. `docker compose exec browser-worker stat -c '%a %u:%g' /browser-profile` → `700 1000:1000` [evidence]
  4. `id -u` và `id -g` trong api và trong browser-worker → cả hai container đều `1000` và `1000` [evidence]
  5. `docker compose exec browser-worker sh -c 'echo x > /data/debug-dumps/probe.txt'` → ghi được; `docker compose exec api cat /data/debug-dumps/probe.txt` → `x`; `docker compose exec api rm /data/debug-dumps/probe.txt` → xóa được, không lỗi quyền [evidence]

## P0-SKL-012 Khởi động lại không làm mất dữ liệu có sẵn trong DATA_DIR
- Thiết kế: R-SKL-20
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. Tạo file `images/probe.txt` nội dung `probe` trong `MIO_DATA_DIR`
  2. `docker compose restart api browser-worker`, chờ healthy → `images/probe.txt` còn, nội dung `probe`; `/browser-profile` vẫn quyền `700` [evidence]
  3. `docker compose exec browser-worker sh -c 'echo p > /browser-profile/probe.txt'`, `docker compose down` (không `-v`), `docker compose up -d` → `/browser-profile/probe.txt` còn (profile giữ qua lần tạo lại container); xóa file thử [evidence]

## P0-SKL-013 Migration lần đầu, lần sau và cấu trúc bảng `app_settings`
- Thiết kế: R-SKL-03; `docs/design/db-schema.md` mục `app_settings`
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-001 (volume DB mới)
- Các bước:
  1. `docker compose up -d`, `docker compose logs api` → log chạy migration nằm trước log mở cổng 3000 [evidence]
  2. `docker compose exec postgres psql -U mio -d mio -c '\d app_settings'` → cột `id uuid`, `key text`, `value jsonb`, `created_at timestamptz`, `updated_at timestamptz`, đều not null; mặc định `gen_random_uuid()`, `now()`; index unique `app_settings_key_key`; check kebab-case trên `key` [evidence]
  3. `insert into app_settings (key, value) values ('Crawl_Schedule', '{}')` → lỗi vi phạm check constraint
  4. Chèn `('probe-key', '{}')` hai lần → lần hai lỗi vi phạm unique `app_settings_key_key`; xóa dòng `probe-key`
  5. Đếm bản ghi bảng migration của Drizzle, `docker compose restart api`, đếm lại → không đổi, api healthy, log không có lỗi migration

## P0-SKL-014 Migration lỗi thì api không mở cổng
- Thiết kế: R-SKL-03
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: volume DB mới (`docker compose down -v` trên môi trường thử)
- Các bước:
  1. `docker compose up -d postgres redis`, rồi `psql -c 'create table app_settings (x int)'` (bảng trùng tên, sai cấu trúc)
  2. `docker compose up -d api` → log api mức error nêu migration lỗi, thoát mã 1, Compose khởi động lại liên tục [evidence]
  3. `curl -s -m 5 http://127.0.0.1:3000/api/v1/health` → không kết nối được (không có HTTP trả về) [evidence]
  4. `docker compose ps browser-worker` → chưa khởi động (chờ api healthy)
  5. `psql -c 'drop table app_settings'` → ở lần khởi động lại kế tiếp, migration chạy xong, api healthy, `/api/v1/health` trả 200

## P0-SKL-015 browser-worker không kết nối PostgreSQL, không mở cổng, không gọi API
- Thiết kế: R-SKL-04
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `docker compose exec browser-worker sh -c 'env | grep -c DATABASE_URL'` → `0`
  2. `psql -c "select client_addr from pg_stat_activity where datname = 'mio'"` → chỉ có IP của container api (đối chiếu `docker inspect`), không có IP của browser-worker [evidence]
  3. `docker compose exec browser-worker cat /proc/net/tcp /proc/net/tcp6` → không có dòng nào trạng thái `0A` (không lắng nghe cổng nào) [evidence]
  4. Đọc log api 2 phút → không có request nào từ IP của browser-worker
  5. `docker compose stop postgres`, chờ 30 giây → browser-worker vẫn healthy, khóa nhịp sống vẫn cập nhật; `docker compose start postgres`

## P0-SKL-016 Health trả ok, không cần đăng nhập, không lộ thông tin
- Thiết kế: R-SKL-13
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: bảng quyết định (DB up, Redis up)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `curl -i http://127.0.0.1:3000/api/v1/health` (không cookie, không header xác thực) → 200, `Content-Type: application/json`, thân đúng `{"status":"ok","checks":{"database":"up","redis":"up"}}` [evidence]
  2. Kiểm tra thân → chỉ có khóa `status`, `checks`; không có phiên bản, đường dẫn, tên máy

## P0-SKL-017 Health khi PostgreSQL dừng rồi chạy lại
- Thiết kế: R-SKL-13; mục Xử lý lỗi (tự kết nối lại)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB down, Redis up)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001; ghi lại `RestartCount` của api
- Các bước:
  1. `docker compose stop postgres`, gọi health → 503, thân đúng `{"status":"error","checks":{"database":"down","redis":"up"}}`, không có thông báo lỗi chi tiết [evidence]
  2. Kiểm tra api → tiến trình vẫn chạy, `RestartCount` không đổi
  3. `docker compose start postgres`, gọi health mỗi 5 giây → trong 60 giây trả 200 `status: ok`; `RestartCount` của api không đổi [evidence]

## P0-SKL-018 Health khi Redis dừng rồi chạy lại
- Thiết kế: R-SKL-13, R-SKL-18; mục Xử lý lỗi (tự kết nối lại)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB up, Redis down)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-017
- Các bước:
  1. `docker compose stop redis`, gọi health → 503, thân `{"status":"error","checks":{"database":"up","redis":"down"}}` [evidence]
  2. `docker compose start redis` → trong 60 giây health trả 200; `RestartCount` của api không đổi
  3. Đọc `<khóa nhịp sống>` hai lần cách 20 giây → giá trị thay đổi (worker đã tự kết nối lại) [evidence]

## P0-SKL-019 Health khi cả PostgreSQL và Redis dừng
- Thiết kế: R-SKL-13
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB down, Redis down)
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-017
- Các bước:
  1. `docker compose stop postgres redis`, gọi health → 503, thân `{"status":"error","checks":{"database":"down","redis":"down"}}` [evidence]
  2. `docker compose start postgres redis` → trong 60 giây health trả 200

## P0-SKL-020 Health khi DB hoặc Redis treo (không trả lời)
- Thiết kế: R-SKL-13 (kiểm song song); mục Tham số (chờ 2 giây)
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `docker compose pause postgres`, `curl -s -w '%{http_code} %{time_total}' http://127.0.0.1:3000/api/v1/health` → 503, `database: down`, thời gian trả về từ 2 đến 3 giây (không treo) [evidence]
  2. `docker compose unpause postgres` → health trả 200
  3. Lặp lại bước 1–2 với `redis` → 503 `redis: down` trong 2–3 giây, sau khi unpause trả 200 [evidence]
  4. `docker compose pause postgres redis`, gọi health có đo thời gian → 503, cả `database` và `redis` là `down`, thời gian trả về từ 2 đến 3 giây (hai kiểm tra chạy song song, không phải 4 giây) [evidence]; `docker compose unpause postgres redis`

## P0-SKL-021 Đường dẫn API không tồn tại trả 404 đúng định dạng
- Thiết kế: R-SKL-15, R-SKL-14
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `curl -i http://127.0.0.1:3000/api/v1/khong-co` → 404, `Content-Type: application/json`, thân đúng `{"code":"NOT_FOUND","message":"Không tìm thấy địa chỉ yêu cầu"}` (không có `fields`, `statusCode`, `error`, stack) [evidence]
  2. `curl -i -X POST http://127.0.0.1:3000/api/v1/health` → 404, thân như bước 1
  3. `curl -i http://127.0.0.1:3000/api/khong-co` và `http://127.0.0.1:3000/api/v1/` → 404 JSON như bước 1, không trả `index.html`

## P0-SKL-022 Trang web giữ chỗ hiển thị đúng
- Thiết kế: R-SKL-14; mục `apps/web`
- Khía cạnh: Hiển thị
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. Playwright mở `http://127.0.0.1:3000/` khung 1440×900 → chữ "Tiệm Nhà Mio" hiển thị đủ dấu, không có lỗi trong console [evidence]
  2. Kiểm tra mạng → file CSS chứa token trả 200; `getComputedStyle(document.documentElement).getPropertyValue('--color-brand-primary')` → `#8FA284`
  3. Lặp lại bước 1 với khung 390×844 → không cuộn ngang, chữ không bị cắt [evidence]

## P0-SKL-023 Định tuyến SPA và file tĩnh
- Thiết kế: R-SKL-14
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `curl -i http://127.0.0.1:3000/settings/groups` → 200, thân giống hệt `GET /` (`index.html`) [evidence]
  2. Lấy một file JS thật trong `apps/web/dist/assets/`, gọi `/assets/<file>` → 200, `Content-Type` là JavaScript, nội dung trùng file
  3. `curl -i http://127.0.0.1:3000/khong-co.png` → 200, `index.html`
  4. `curl -i http://127.0.0.1:3000/apifoo` → 200, `index.html` (không bắt đầu bằng `/api/`)

## P0-SKL-024 Vite dev proxy chuyển `/api` sang api
- Thiết kế: mục `apps/web` (Dev)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: api đang chạy ở `localhost:3000`
- Các bước:
  1. `pnpm --filter @mio/web dev` → Vite chạy, in cổng dev
  2. `curl http://localhost:<cổng dev>/api/v1/health` → 200, thân giống gọi thẳng api [evidence]

## P0-SKL-025 Log là JSON một dòng, đủ trường bắt buộc
- Thiết kế: R-SKL-17
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy; đã gọi vài request (health, 404)
- Các bước:
  1. `docker compose logs --no-log-prefix api browser-worker` → mọi dòng parse được bằng `json.loads`, mỗi lỗi nằm gọn trong một dòng [evidence]
  2. Mỗi dòng có `time`, `level`, `app`, `msg`; `app` là `api` hoặc `browser-worker` đúng container
  3. Dòng log của request `GET /api/v1/khong-co` có `requestId` [evidence]

## P0-SKL-026 Log che khóa nhạy cảm và không ghi giá trị biến môi trường
- Thiết kế: R-SKL-17, R-SKL-02
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy
- Các bước:
  1. `curl -H 'Authorization: Bearer tok-ABC123' -H 'Cookie: sid=COOKIE-XYZ789' http://127.0.0.1:3000/api/v1/khong-co`
  2. Tìm `tok-ABC123`, `COOKIE-XYZ789` trong log api → không có; nếu log có header `authorization`, `cookie` thì giá trị là `[REDACTED]` [evidence]
  3. Tìm giá trị `POSTGRES_PASSWORD` (trong `.env`) và chuỗi `DATABASE_URL` đầy đủ trong log của mọi container → không có [evidence]

## P0-SKL-027 Giới hạn kích thước log Docker
- Thiết kế: R-SKL-26
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy
- Các bước:
  1. `docker inspect -f '{{json .HostConfig.LogConfig}}'` cho 4 container → đều `{"Type":"json-file","Config":{"max-file":"5","max-size":"10m"}}` [evidence]

## P0-SKL-028 Chỉ cổng api được mở, và chỉ trên 127.0.0.1
- Thiết kế: R-SKL-19
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống chạy chỉ bằng `compose.yml`
- Các bước:
  1. `docker compose ps --format '{{.Service}} {{.Ports}}'` → chỉ `api` có `127.0.0.1:3000->3000/tcp`; `postgres`, `redis`, `browser-worker` không publish cổng [evidence]
  2. `curl -m 5 http://<IP LAN của máy>:3000/api/v1/health` → không kết nối được; `curl http://127.0.0.1:3000/api/v1/health` → 200 [evidence]
  3. `Test-NetConnection 127.0.0.1 -Port 5432` và `-Port 6379` → không kết nối được

## P0-SKL-029 compose.dev.yml mở PostgreSQL và Redis chỉ trên 127.0.0.1
- Thiết kế: R-SKL-19
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang dừng
- Các bước:
  1. `docker compose -f compose.yml -f compose.dev.yml up -d`, `docker compose ps` → `postgres` `127.0.0.1:5432->5432`, `redis` `127.0.0.1:6379->6379` [evidence]
  2. Từ máy host `psql -h 127.0.0.1 -U mio -d mio -c 'select 1'` → `1`; `redis-cli -h 127.0.0.1 ping` → `PONG`
  3. Kết nối tới `<IP LAN của máy>:5432` và `:6379` → không kết nối được

## P0-SKL-030 Container và phiên PostgreSQL dùng múi giờ UTC
- Thiết kế: R-SKL-23
- Khía cạnh: Thời gian
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy; máy host đặt múi giờ UTC+7
- Các bước:
  1. `docker compose exec api node -e "console.log(Intl.DateTimeFormat().resolvedOptions().timeZone, new Date().getTimezoneOffset())"` → `UTC 0`; lặp lại với browser-worker → `UTC 0` [evidence]
  2. `psql -c 'show timezone'` → `UTC`
  3. `redis-cli GET <khóa nhịp sống>` → chuỗi ISO kết thúc bằng `Z`, lệch giờ UTC thực tế không quá 15 giây

## P0-SKL-031 Lint chặn `Date.now()` và `new Date()` không tham số
- Thiết kế: R-SKL-23
- Khía cạnh: Thời gian
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: nhánh sạch, `pnpm lint` đang đạt
- Các bước:
  1. Tạo tạm `apps/api/src/core/lint-probe.ts` gồm `Date.now()`, `new Date()`, `new Date('2026-10-29')`
  2. `pnpm lint` → đúng 2 lỗi `no-restricted-syntax` ở dòng `Date.now()` và `new Date()`; dòng `new Date('2026-10-29')` không lỗi [evidence]
  3. Xóa file tạm, `pnpm lint` → không lỗi, không warning (`system-clock.ts` được miễn)

## P0-SKL-032 browser-worker ghi nhịp sống đều đặn
- Thiết kế: R-SKL-18
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `redis-cli --scan --pattern 'mio:heartbeat:browser-worker:*'` → đúng một khóa, là `<khóa nhịp sống>` của container đang chạy [evidence]
  2. `redis-cli TTL <khóa nhịp sống>` mỗi 5 giây trong 1 phút → luôn trong khoảng 45–60 [evidence]
  3. `redis-cli GET <khóa nhịp sống>` mỗi 5 giây trong 1 phút → giá trị đổi khoảng mỗi 15 giây, là thời điểm ISO
  4. `docker inspect -f '{{.State.Health.Status}}' <container browser-worker>` → `healthy`

## P0-SKL-033 Khóa nhịp sống hết hạn khi worker dừng; healthcheck chỉ đọc khóa của chính container
- Thiết kế: R-SKL-18, R-SKL-31
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. Khi worker đang chạy: `docker compose exec browser-worker node <đường dẫn healthcheck đã build>; echo $?` → `0`
  2. Vẫn khi worker đang chạy: `docker compose run --rm --no-deps --entrypoint node browser-worker <đường dẫn healthcheck>; echo $?` (container mới, không chạy worker, hostname khác) → `1` dù khóa của worker đang chạy vẫn còn [evidence]
  3. `docker compose stop browser-worker`, ghi thời điểm; `redis-cli EXISTS <khóa nhịp sống>` mỗi 5 giây → về `0` trong vòng 60 giây sau thời điểm dừng [evidence]
  4. `docker compose start browser-worker` → khóa (cùng hostname) xuất hiện lại, container `healthy`

## P0-SKL-034 Dừng bình thường khi không có job
- Thiết kế: R-SKL-22; mục Tham số (thời gian ân hạn)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy, không có job
- Các bước:
  1. `docker compose config` → `stop_grace_period` của api là 30s, browser-worker là 2m
  2. `docker compose exec api sh -c "tr '\0' ' ' < /proc/1/cmdline"`, lặp lại với browser-worker → bắt đầu bằng `node` (Node là PID 1, không qua `pnpm` hay `sh`) [evidence]
  3. `docker compose stop api browser-worker` → mỗi container dừng trong vài giây (không chờ hết ân hạn)
  4. `docker inspect -f '{{.State.ExitCode}}'` cho hai container → `0`; log cuối không có lỗi [evidence]

## P0-SKL-035 Lệnh CLI: help và lệnh không tồn tại
- Thiết kế: mục `apps/api` › `cli.ts`
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy (api đang giữ cổng 3000)
- Các bước:
  1. `docker compose exec api node dist/cli.js help; echo $?` → in danh sách lệnh có `help`, mã `0`, không lỗi `EADDRINUSE` (CLI không mở HTTP) [evidence]
  2. `docker compose exec api node dist/cli.js khong-co; echo $?` → "Lệnh không tồn tại: khong-co. Chạy help để xem danh sách.", mã `1` [evidence]

## P0-SKL-036 Redis bật AOF, noeviction, giữ dữ liệu khi bị dừng cứng
- Thiết kế: R-SKL-27
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy
- Các bước:
  1. `redis-cli CONFIG GET appendonly` → `yes`; `CONFIG GET maxmemory-policy` → `noeviction` [evidence]
  2. `redis-cli SET mio:test:aof 1`, chờ 2 giây, `docker kill <container redis>` (dừng cứng, không lưu khi tắt), `docker compose up -d redis` → `GET mio:test:aof` trả `1` [evidence]
  3. `docker compose down` (không `-v`), `docker compose up -d` → `GET mio:test:aof` vẫn `1`; xóa khóa thử

## P0-SKL-037 Hàng đợi đăng ký đúng tên, global concurrency 1
- Thiết kế: R-SKL-05, R-SKL-06
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `redis-cli HGET bull:fb-browser:meta concurrency` → `1` [evidence]
  2. `redis-cli --scan --pattern 'bull:fb-inbox:*'` và `--pattern 'bull:render:*'` → không có khóa nào (giai đoạn 0 chưa đăng ký)
  3. `git grep -nE "'(fb-browser|fb-inbox|render|fb-browser-results|fb-inbox-results|ai-text|ai-image|messenger|page-publish)'" -- apps packages ':!apps/*/test'` → chỉ xuất hiện trong file khai báo `QUEUE_NAMES` của `@mio/shared` [evidence]

## P0-SKL-038 Build image đa kiến trúc và chạy được trên arm64
- Thiết kế: R-SKL-21; mục Build đa kiến trúc; ADR 0014
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: Docker Desktop có buildx và QEMU
- Các bước:
  1. `pnpm docker:build:multiarch` → target `api`, `browser-worker` build xong cho `linux/amd64` và `linux/arm64` [evidence]
  2. Build image arm64 của từng target vào Docker local, `docker run --rm --platform linux/arm64 <image> node --version` → api `v26.x.x`; browser-worker đúng phiên bản Node của image Playwright ghi trong `plan.md` [evidence]
  3. Dòng `FROM` trong `apps/*/Dockerfile` chỉ dùng `node:26-bookworm-slim`, `mcr.microsoft.com/playwright:v1.63.0-noble` (hoặc bản vá cùng dòng ghi trong `plan.md`); `docker buildx imagetools inspect` từng base image → có `linux/amd64` và `linux/arm64`
  4. Tìm trong `compose.yml`, `apps/*/Dockerfile`, `docker-bake.hcl`: đường dẫn ổ đĩa của máy (`D:\`, `C:\`, `/home/…`), IP cố định, `platform:` cứng → không có

## P0-SKL-039 Chuyển máy chỉ bằng biến môi trường và volume
- Thiết kế: R-SKL-20, R-SKL-21; ADR 0009, ADR 0013
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang dừng; `git status` sạch
- Các bước:
  1. Đổi `.env`: `MIO_DATA_DIR` sang thư mục trống khác, `MIO_PUBLIC_URL=http://127.0.0.1:3000`
  2. `docker compose up -d` → 4 dịch vụ healthy; thư mục mới có `images/`, `debug-dumps/`; volume `mio-browser-profile` không đổi (phiên Facebook giữ nguyên) [evidence]
  3. `git status` → không có file code, Dockerfile, `compose.yml` nào bị sửa; trả lại `.env`

## P0-SKL-040 Đo RAM/CPU: ghi CSV theo chu kỳ
- Thiết kế: R-SKL-24; mục Đo RAM/CPU từng container
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy (4 container); thêm một container ngoài project: `docker run -d --name skl-probe redis:8-alpine`
- Các bước:
  1. `py tools/ops/container_stats.py record --interval 10 --out .local/metrics/skl-040.csv`, chạy khoảng 65 giây rồi Ctrl+C → thoát gọn, không in traceback
  2. Mở CSV → dòng đầu đúng `time,container,cpu_percent,mem_bytes,mem_limit_bytes`; mỗi chu kỳ một dòng cho mỗi container của app (khoảng 6–7 chu kỳ × 4 container, chu kỳ đầu lấy ngay khi bắt đầu); không có dòng nào của `skl-probe` hay container khác; dòng cuối đầy đủ [evidence]
  3. Cột `time` là ISO UTC; `cpu_percent`, `mem_bytes`, `mem_limit_bytes` là số; `mem_bytes` ≤ `mem_limit_bytes`; tên container có tiền tố project (ví dụ `mio-api-1`)
  4. `docker rm -f skl-probe`

## P0-SKL-041 Đo RAM/CPU: ghi nối tiếp và tổng hợp
- Thiết kế: R-SKL-24
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã có file của P0-SKL-040
- Các bước:
  1. Chạy `record` thêm khoảng 30 giây vào cùng file → số dòng tăng, dòng tiêu đề chỉ có một lần, dòng cũ giữ nguyên
  2. `py tools/ops/container_stats.py summary .local/metrics/skl-040.csv` → mỗi container một dòng: số mẫu, CPU trung bình, CPU lớn nhất, RAM trung bình, RAM lớn nhất (MiB) [evidence]
  3. Tự tính lại từ CSV bằng Python → khớp với bảng tổng hợp (sai số làm tròn ≤ 0,1)

## P0-SKL-042 Đo RAM/CPU khi Docker không chạy
- Thiết kế: R-SKL-24
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: tắt Docker Desktop; có file CSV của P0-SKL-041
- Các bước:
  1. `py tools/ops/container_stats.py record --out .local/metrics/skl-040.csv; echo $?` → "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại.", mã `1` [evidence]
  2. File CSV không đổi (cùng số dòng, cùng thời điểm sửa)

## P0-SKL-043 `pnpm test:int` khi Docker không chạy thì fail, không skip
- Thiết kế: R-SKL-25
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: tắt Docker Desktop
- Các bước:
  1. `pnpm test:int; echo $?` → in "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại.", mã khác `0` [evidence]
  2. Kết quả không có dòng báo test passed hay skipped
  3. `pnpm test` → vẫn chạy và đạt (unit + contract không cần Docker)

## P0-SKL-044 Testcontainers dùng cùng image với compose.yml
- Thiết kế: R-SKL-25; mục Tham số (phiên bản hạ tầng)
- Khía cạnh: Regression
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: Docker Desktop đang chạy
- Các bước:
  1. `docker compose config --images` → ghi lại image `postgres`, `redis`
  2. Chạy `pnpm test:int`, trong lúc chạy `docker ps --format '{{.Image}}'` → container của Testcontainers dùng đúng hai image ở bước 1 [evidence]
  3. `git grep -n "postgres:18\|redis:8"` trong code và cấu hình (bỏ `docs/`) → mỗi tag chỉ khai báo ở một chỗ

## P0-SKL-045 Khóa cài đặt chưa có bản ghi trả giá trị mặc định
- Thiết kế: R-SKL-09
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `crawl-settings`, `auth`; phiên Quản lý; `delete from app_settings where key = 'crawl-schedule'`
- Các bước:
  1. `GET /api/v1/settings/crawl-schedule` → 200, thân bằng giá trị mặc định khai báo trong `SETTINGS` [evidence]
  2. `select count(*) from app_settings where key = 'crawl-schedule'` → `0` (đọc không ghi vào DB) [evidence]

## P0-SKL-046 Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục
- Thiết kế: R-SKL-11; `db-schema.md` Quy ước chung (`CLOCK`)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: chuyển trạng thái (chưa có bản ghi → có bản ghi → cập nhật)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-045
- Các bước:
  1. `PUT /api/v1/settings/crawl-schedule` với giá trị hợp lệ A (`maxScrolls: 10`) → 200, thân bằng A; DB có 1 dòng, `value` = A, `created_at` bằng đúng `updated_at`, gần giờ hiện tại [evidence]
  2. `PUT` giá trị hợp lệ B (`maxScrolls: 12`, các trường khác cũng đổi) → 200; DB vẫn 1 dòng, `value` = B toàn bộ (không còn trường nào của A), `updated_at` mới hơn bước 1, `created_at` không đổi [evidence]

## P0-SKL-047 Sửa cài đặt trong DB có hiệu lực ngay, không cần khởi động lại
- Thiết kế: R-SKL-08
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2
- Các bước:
  1. `update app_settings set value = jsonb_set(value, '{maxScrolls}', '15') where key = 'crawl-schedule'`
  2. `GET /api/v1/settings/crawl-schedule` ngay sau đó → `maxScrolls: 15`; `RestartCount` và `StartedAt` của api không đổi [evidence]

## P0-SKL-048 Ghi cài đặt sai schema thì báo lỗi theo trường, không ghi DB
- Thiết kế: R-SKL-11
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2; ghi lại `value`, `updated_at` hiện tại
- Các bước:
  1. `PUT` với `maxScrolls: 21` → 400, thân `{"code":"VALIDATION_ERROR","message":"Dữ liệu cài đặt không hợp lệ","fields":{"maxScrolls":"<thông báo của schema>"}}` [evidence]
  2. `PUT` với `maxScrolls: "abc"` → 400 `VALIDATION_ERROR`, `fields.maxScrolls` có thông báo
  3. `PUT` thân `{}` → 400, `fields` liệt kê mọi trường bắt buộc
  4. `PUT` thân `[]` (không phải object) → 400 `VALIDATION_ERROR`, `fields` có khóa `_root`
  5. DB → `value`, `updated_at` giống hệt trước bước 1 [evidence]

## P0-SKL-049 Khóa cài đặt không tồn tại
- Thiết kế: R-SKL-10, R-SKL-15
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-045
- Các bước:
  1. `PUT /api/v1/settings/khong-co` với thân bất kỳ → 404, thân đúng `{"code":"NOT_FOUND","message":"Không tìm thấy địa chỉ yêu cầu"}` (khóa lạ không có route); `GET` cùng địa chỉ → như trên [evidence]
  2. `select count(*) from app_settings where key = 'khong-co'` → `0`

## P0-SKL-050 Giá trị đang lưu sai một trường thì báo 409, không dùng mặc định
- Thiết kế: R-SKL-12
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2
- Các bước:
  1. `update app_settings set value = jsonb_set(value, '{maxScrolls}', '25') where key = 'crawl-schedule'`
  2. `GET /api/v1/settings/crawl-schedule` → 409, thân `{"code":"INVALID_STORED_SETTING","message":"Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)","fields":{"maxScrolls":"phải từ 1 đến 20"}}`; không trả giá trị mặc định [evidence]
  3. Log api → một dòng mức error có thông báo trên, `key: "crawl-schedule"`, danh sách `[{ path: "maxScrolls", reason: "phải từ 1 đến 20", storedValue: 25 }]` [evidence]
  4. `PUT` một giá trị không hợp lệ khác (`maxScrolls: 21`) → 400 `VALIDATION_ERROR`, DB vẫn lưu `25`

## P0-SKL-051 Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài
- Thiết kế: R-SKL-12
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2; schema `crawl-schedule` có `goldenHours` là mảng ít nhất 2 phần tử
- Các bước:
  1. Bằng SQL: đặt `maxScrolls = 25`, xóa một trường bắt buộc `<A>`, đặt `goldenHours[1].end` là chuỗi 99 ký tự (chuỗi JSON kèm ngoặc kép dài 101 ký tự)
  2. `GET` → 409; `message` liệt kê đủ 3 trường, ngăn bằng "; ": `maxScrolls: … (đang lưu: 25)`, `<A>: … (đang lưu: không có)`, `goldenHours[1].end: … (đang lưu: <100 ký tự đầu của chuỗi JSON, bắt đầu bằng ngoặc kép>…)`; `fields` có đủ 3 khóa [evidence]
  3. Đổi `goldenHours[1].end` thành chuỗi 98 ký tự (chuỗi JSON đúng 100 ký tự, vẫn sai định dạng) → phần "đang lưu" in đủ chuỗi JSON, có ngoặc kép hai đầu, không có "…" [evidence]

## P0-SKL-052 Ghi giá trị hợp lệ sau lỗi 409 thì hết lỗi
- Thiết kế: R-SKL-12
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái (lưu hỏng → lưu hợp lệ)
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: sau P0-SKL-050 (DB đang lưu `maxScrolls: 25`)
- Các bước:
  1. `PUT` giá trị hợp lệ (`maxScrolls: 10`) → 200 [evidence]
  2. `GET` → 200, `maxScrolls: 10`; DB `value` đúng giá trị mới

## P0-SKL-053 Hai lần ghi cài đặt cùng lúc
- Thiết kế: R-SKL-11; mục Đọc / ghi cài đặt (ghi sau thắng)
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046
- Các bước:
  1. Gửi song song hai `PUT` (giá trị A `maxScrolls: 5` và B `maxScrolls: 7`, khác nhau ở mọi trường) → cả hai 200, không có 500
  2. DB → đúng 1 dòng `crawl-schedule`; `value` bằng trọn A hoặc trọn B, không trộn trường của hai bên [evidence]
  3. `GET` → bằng giá trị trong DB

## P0-SKL-054 Lỗi không lường trước trả 500 không lộ chi tiết
- Thiết kế: R-SKL-16
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-045
- Các bước:
  1. `alter table app_settings rename to app_settings_bak`
  2. `GET /api/v1/settings/crawl-schedule` → 500, thân đúng `{"code":"INTERNAL_ERROR","message":"Lỗi hệ thống, vui lòng thử lại sau"}`; không có stack, tên bảng, câu SQL [evidence]
  3. Log api → dòng mức error có `requestId` và lỗi gốc đầy đủ (quan hệ `app_settings` không tồn tại) [evidence]
  4. `alter table app_settings_bak rename to app_settings` → `GET` trả 200

## P0-SKL-055 DB có dòng khóa cài đặt lạ
- Thiết kế: R-SKL-08, R-SKL-09
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-045
- Các bước:
  1. `insert into app_settings (key, value) values ('old-key', '{"a":1}')`
  2. `GET /api/v1/settings/crawl-schedule` → 200 bình thường [evidence]
  3. `docker compose restart api` → api healthy, log không có lỗi; xóa dòng `old-key`

## P0-SKL-056 Kết quả job trình duyệt đi qua hàng đợi kết quả
- Thiết kế: R-SKL-28; mục Job và hàng đợi (chiều dữ liệu)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; có ít nhất một job quét chạy xong thành công, biết `<id>` job gốc
- Các bước:
  1. `redis-cli HGETALL bull:fb-browser-results:<id>-result` → job tồn tại; `data` có `sourceJobId = <id>`, `sourceJobName` đúng tên job, `outcome: "ok"`, có `data`, không có `error` [evidence]
  2. DB của tính năng → kết quả quét được ghi đúng một lần cho `<id>`

## P0-SKL-057 Tùy chọn job mặc định
- Thiết kế: R-SKL-07
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-056
- Các bước:
  1. `redis-cli HGET bull:fb-browser:<id> opts` → thể hiện `attempts` 1, `removeOnComplete` `{count: 1000}`, `removeOnFail` `{count: 5000}` (trừ khi `group-crawl-job` khai báo khác trong thiết kế) [evidence]
  2. Lặp lại với job `bull:fb-browser-results:<id>-result` → cùng giá trị

## P0-SKL-058 Hai tiến trình browser-worker vẫn chỉ chạy một job fb-browser cùng lúc
- Thiết kế: R-SKL-05
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; ít nhất 3 job quét đang chờ trong `fb-browser`
- Các bước:
  1. `docker compose up -d --scale browser-worker=2` → 2 container browser-worker healthy
  2. Đọc `redis-cli LLEN bull:fb-browser:active` mỗi giây cho tới khi hết job → không lần nào lớn hơn `1` [evidence]
  3. Log hai worker → các khoảng (bắt đầu, kết thúc) của các job không chồng nhau; cả hai worker đều có thể nhận job [evidence]
  4. `docker compose up -d --scale browser-worker=1`

## P0-SKL-059 Dừng browser-worker khi đang có job thì chờ job xong
- Thiết kế: R-SKL-22
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; một job quét đang chạy (ngắn hơn 120 giây), còn ít nhất một job chờ
- Các bước:
  1. `docker compose stop browser-worker` khi job đang chạy → container chưa dừng ngay, chờ job xong [evidence]
  2. Job đang chạy chuyển `completed`, có job kết quả `<id>-result`; job đang chờ vẫn ở `wait`, không được bắt đầu [evidence]
  3. `ExitCode` của container → `0`

## P0-SKL-060 Quá thời gian ân hạn: job dở dang thất bại, không chạy lại
- Thiết kế: R-SKL-22, R-SKL-29, R-SKL-07
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; một job quét đang chạy và còn hơn 5 giây mới xong; biết `<id>`
- Các bước:
  1. `docker compose stop -t 5 browser-worker` → container bị dừng cứng sau 5 giây (`ExitCode` 137)
  2. `docker compose start browser-worker`, chờ tối đa 2 phút → job `<id>` ở trạng thái `failed` (`ZSCORE bull:fb-browser:failed <id>` có giá trị); log worker không có lần bắt đầu thứ hai cho `<id>` [evidence]
  3. DB của tính năng → lượt quét của `<id>` ghi thất bại với loại lỗi `WorkerCrashedError` (bảng, cột theo thiết kế `group-crawl-job`); chỉ một bản ghi [evidence]

## P0-SKL-061 Một worker chết giữa job, worker còn lại không chạy lại job đó
- Thiết kế: R-SKL-29, R-SKL-07
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; `--scale browser-worker=2`; một job quét đang chạy trên worker 1, biết `<id>`
- Các bước:
  1. `docker kill <container worker 1>` khi job đang chạy
  2. Chờ tối đa 2 phút → job `<id>` chuyển `failed`; log worker 2 không có lần bắt đầu `<id>` [evidence]
  3. DB của tính năng → lượt quét `<id>` thất bại với `WorkerCrashedError`, đúng một bản ghi; job chờ khác vẫn được worker 2 xử lý bình thường [evidence]

## P0-SKL-062 Job kết quả sai cấu trúc
- Thiết kế: R-SKL-28
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; script ngoài app (Node + `bullmq`) thêm được job vào `fb-browser-results`
- Các bước:
  1. Thêm job `jobId = probe-1-result`, data `{ "sourceJobId": "probe-1", "sourceJobName": "<tên job quét>" }` (thiếu `outcome`) → job chuyển `failed`, `failedReason` nêu lỗi cấu trúc [evidence]
  2. Log api → dòng mức error có `sourceJobId: "probe-1"` [evidence]
  3. Thêm job `probe-2-result` với `outcome: "failed"` nhưng không có `error` → cũng `failed`, log có `probe-2`
  4. DB của tính năng → không có bản ghi nào cho `probe-1`, `probe-2`; api vẫn healthy

## P0-SKL-063 Job đọc cài đặt hỏng thì thất bại với đúng thông báo
- Thiết kế: R-SKL-12
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `crawl-settings`, `group-crawl-job`; DB lưu `crawl-schedule` với `maxScrolls: 25`
- Các bước:
  1. Chờ (hoặc kích hoạt) lượt quét kế tiếp → job thất bại, lý do đúng "Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)" [evidence]
  2. Kiểm tra → app không quét bằng giá trị mặc định (không có job `fb-browser` nào được thêm với `maxScrolls` mặc định)
  3. `PUT` giá trị hợp lệ → lượt quét kế tiếp chạy bình thường

## P0-SKL-064 api dừng khi worker đang trả kết quả: kết quả không mất, xử lý một lần
- Thiết kế: R-SKL-28; mục Job và hàng đợi (kết quả nằm trong Redis)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; một job quét đang chạy, biết `<id>`
- Các bước:
  1. `docker compose stop api` khi job đang chạy → worker vẫn chạy, job xong, `bull:fb-browser-results:<id>-result` ở `wait` [evidence]
  2. `docker compose start api` → trong 1 phút job kết quả chuyển `completed`
  3. DB của tính năng → kết quả `<id>` ghi đúng một lần [evidence]

## P0-SKL-065 Thân request sai JSON hoặc quá lớn
- Thiết kế: R-SKL-15
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên, đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2; ghi lại `value`, `updated_at` của `crawl-schedule`
- Các bước:
  1. `PUT /api/v1/settings/crawl-schedule`, `Content-Type: application/json`, thân `{"maxScrolls":` (cắt dở) → 400, thân đúng `{"code":"INVALID_JSON","message":"Dữ liệu gửi lên không đúng định dạng JSON"}`, không có stack [evidence]
  2. `PUT` thân dài 1 048 577 byte (JSON hợp lệ, thêm trường lạ chứa chuỗi dài) → 413, thân đúng `{"code":"PAYLOAD_TOO_LARGE","message":"Dữ liệu gửi lên quá lớn"}` [evidence]
  3. DB → `value`, `updated_at` giống hệt trước bước 1
  4. `PUT` thân hợp lệ theo schema, thêm trường lạ để dài đúng 1 048 576 byte → không bị 413, trả 200 (trường lạ bị bỏ, R-SKL-11)

## P0-SKL-066 Hai browser-worker: worker treo không bị worker kia che
- Thiết kế: R-SKL-18
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `docker compose up -d --scale browser-worker=2`, chờ healthy → `redis-cli --scan --pattern 'mio:heartbeat:browser-worker:*'` có đúng 2 khóa, mỗi khóa ứng với hostname một container [evidence]
  2. `docker pause <container worker 1>` (giả lập treo), ghi thời điểm → trong vòng 60 giây khóa của worker 1 hết hạn; khóa của worker 2 vẫn cập nhật mỗi 15 giây [evidence]
  3. `docker unpause <container worker 1>` → khóa của worker 1 xuất hiện lại, cả hai `healthy`
  4. `docker compose up -d --scale browser-worker=1`

## P0-SKL-067 Đo RAM/CPU: tham số `--interval`, `--out` và file tổng hợp không tồn tại
- Thiết kế: R-SKL-24; mục Đo RAM/CPU từng container
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy; chưa có `.local/metrics/skl-067.csv`
- Các bước:
  1. `py tools/ops/container_stats.py record --interval 4 --out .local/metrics/skl-067.csv; echo $?` → "--interval phải là số nguyên từ 5 đến 3600", mã `2`, không tạo file [evidence]
  2. Lặp lại với `--interval 3601`, `--interval abc`, `--interval 7.5` → cùng thông báo, mã `2`
  3. `record --interval 5 --out .local/metrics/skl-067.csv`, khoảng 12 giây sau bấm Ctrl+C → có 3 chu kỳ dữ liệu (giây 0, 5, 10), thoát mã `0`
  4. `record --interval 3600 --out .local/metrics/skl-067b.csv`, khoảng 5 giây sau bấm Ctrl+C → có 1 chu kỳ dữ liệu, thoát mã `0`
  5. `record` không có `--interval`, `--out`; sau khi có chu kỳ đầu thì bấm Ctrl+C → tạo `.local/metrics/<YYYY-MM-DD-HHmm>.csv`, tên theo giờ Việt Nam lúc bắt đầu [evidence]
  6. `py tools/ops/container_stats.py summary .local/metrics/khong-co.csv; echo $?` → "Không tìm thấy file: .local/metrics/khong-co.csv", mã `1`

## P0-SKL-068 Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc
- Thiết kế: R-SKL-11
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: như P0-SKL-046 sau bước 2
- Các bước:
  1. `PUT` giá trị hợp lệ kèm trường lạ `"foo": 1` → 200, thân trả về không có `foo`; DB `value` không có `foo` [evidence]
  2. `update app_settings set value = value || '{"bar": 2}' where key = 'crawl-schedule'`
  3. `GET /api/v1/settings/crawl-schedule` → 200 (không phải 409), thân không có `bar` [evidence]

## P0-SKL-069 Worker chết khi api đang tắt: job vẫn được ghi thất bại sau khi api chạy lại
- Thiết kế: R-SKL-29
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đã có `group-crawl-job`; một job quét đang chạy, biết `<id>`
- Các bước:
  1. `docker compose stop api`, rồi `docker kill <container browser-worker>` khi job vẫn đang chạy
  2. `docker start <container browser-worker>` (api vẫn tắt), chờ tối đa 2 phút → job `<id>` ở `failed`, không có lần bắt đầu thứ hai [evidence]
  3. `docker compose start api`, chờ healthy thêm 1 phút → DB của tính năng có lượt quét `<id>` thất bại với `WorkerCrashedError`, đúng một bản ghi [evidence]
  4. `docker compose restart api`, chờ thêm 6 phút (qua ít nhất một lần đối soát định kỳ) → vẫn đúng một bản ghi cho `<id>` [evidence]

## P0-SKL-070 Khởi động khi PostgreSQL hoặc Redis chưa sẵn sàng
- Thiết kế: R-SKL-30
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001; ghi lại `RestartCount` của api, browser-worker
- Các bước:
  1. `docker compose stop postgres`, `docker restart <container api>` → log api có các lần thử kết nối; khoảng 30 giây sau khi khởi động có dòng mức error "Không kết nối được PostgreSQL", tiến trình thoát mã 1, `RestartCount` tăng [evidence]
  2. `docker compose start postgres` → ở lần khởi động lại kế tiếp api healthy, `/api/v1/health` trả 200
  3. Lặp lại bước 1–2 với `redis` → "Không kết nối được Redis" [evidence]
  4. `docker compose stop redis`, `docker restart <container browser-worker>` → khoảng 30 giây sau "Không kết nối được Redis", thoát mã 1; `docker compose start redis` → worker healthy

## P0-SKL-071 Cấu hình healthcheck; container unhealthy không bị khởi động lại
- Thiết kế: R-SKL-31; mục Tham số (healthcheck Compose)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001; ghi lại `RestartCount` của api
- Các bước:
  1. `docker inspect -f '{{json .Config.Healthcheck}}'` cho 4 container → lệnh: postgres `pg_isready -U mio -d mio`, redis `redis-cli ping`, api và browser-worker `node dist/healthcheck.js`; `Interval` 10s, `Timeout` 5s, `Retries` 3; `StartPeriod` 60s cho api, 30s cho dịch vụ khác [evidence]
  2. `docker compose stop postgres`, chờ 40 giây → api `unhealthy`, tiến trình api vẫn chạy, `RestartCount` không đổi [evidence]
  3. `docker compose start postgres` → api trở lại `healthy`

## P0-SKL-072 File tĩnh không lộ file ngoài `apps/web/dist`
- Thiết kế: R-SKL-14
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: hệ thống đang chạy như P0-SKL-001
- Các bước:
  1. `curl -i --path-as-is http://127.0.0.1:3000/../package.json` → 200 trả `index.html` hoặc 404; không trả nội dung `package.json` [evidence]
  2. Lặp lại với `/%2e%2e/package.json`, `/assets/..%2f..%2fpackage.json`, `/..%5c..%5cpackage.json` → như bước 1 [evidence]
  3. Lặp lại với `/../../../../etc/passwd` (`--path-as-is`) → không trả nội dung `/etc/passwd`
