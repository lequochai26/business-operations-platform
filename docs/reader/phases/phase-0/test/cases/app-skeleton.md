> Bản đọc sinh từ docs/phases/phase-0/test/cases/app-skeleton.md (phiên bản 8d10d04, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Test case – Khung ứng dụng (`app-skeleton`, `SKL`)

**Tóm tắt.** Tài liệu này gồm các manual test case của tính năng khung ứng dụng. Tính năng này không có mockup.

- Thiết kế: `docs/phases/phase-0/design/app-skeleton.md`
- Mockup: không có
- Cập nhật: 2026-10-31

<a id="s-bee2e72c3a"></a>

## Khía cạnh không áp dụng

**Tóm tắt.** Ba khía cạnh test 5, 6 và 9 không áp dụng cho khung ứng dụng.

- Khía cạnh 5, Phân quyền:
  - Khung chưa có vai trò và đăng nhập. Phần này thuộc tính năng `auth`.
  - Bộ test chỉ kiểm quyền truy cập ở mức hệ thống: `/health` công khai, cổng chỉ mở trên `127.0.0.1`, container không chạy bằng root. Các điểm này được xếp vào khía cạnh 3 và 11.
- Khía cạnh 6, Phiên đăng nhập và cookie:
  - Khung không có phiên của web app. Phần này thuộc `auth`.
  - Khung không mở phiên Facebook. Phần này thuộc `fb-account-session`.
- Khía cạnh 9, Phía Facebook và Messenger:
  - Khung không gọi Facebook, Gemini hay Messenger. Thiết kế nêu điều này ở mục Tích hợp bên ngoài.

<a id="s-8ba43f44af"></a>

## Ghi chú chạy

**Tóm tắt.** Mục này nêu điều kiện chung để chạy bộ test, các case phải chờ tính năng khác và các phần chỉ kiểm được bằng test tự động.

**Môi trường chạy**

- Mọi lệnh chạy từ gốc repo.
- Docker Desktop phải đang chạy.
- File `.env` được tạo từ `.env.example`.
- `<image api>` và `<image browser-worker>` là image do lệnh `pnpm docker:build` tạo ra.
- Khoá Redis của BullMQ dùng tiền tố mặc định `bull`, ví dụ `bull:fb-browser:meta`. Nếu implement đặt tiền tố khác thì thay tiền tố trong lệnh cho tương ứng.
- Mỗi container browser-worker có khoá nhịp sống riêng là `mio:heartbeat:browser-worker:<hostname>`. Lấy hostname bằng lệnh `docker compose exec browser-worker hostname`. Các bước bên dưới viết tắt khoá này là `<khóa nhịp sống>`.

**Case cần tính năng khác**

- Các case này ghi tính năng cần có trong phần Chuẩn bị. Nếu chạy `/manual-test-run` khi tính năng đó chưa có, case được ghi là `bị chặn` và sẽ chạy lại sau.
- Cần `crawl-settings` và `auth`: từ [P0-SKL-045](#s-7e75a05b62 "Khóa cài đặt chưa có bản ghi trả giá trị mặc định") *(Khóa cài đặt chưa có bản ghi trả giá trị mặc định)* đến [P0-SKL-055](#s-e0eb883363 "DB có dòng khóa cài đặt lạ") *(DB có dòng khóa cài đặt lạ)*, [P0-SKL-065](#s-352c976967 "Thân request sai JSON hoặc quá lớn") *(Thân request sai JSON hoặc quá lớn)*, [P0-SKL-068](#s-25d0a70d96 "Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc") *(Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc)*.
  - `crawl-settings` cung cấp khoá `crawl-schedule` và endpoint `/api/v1/settings/crawl-schedule`. `auth` cung cấp phiên Quản lý.
  - Tên trường, giới hạn và thông báo của khoá lấy theo thiết kế `crawl-settings`. Các ví dụ bên dưới dùng trường `maxScrolls` với giới hạn từ 1 đến 20, giống [R-SKL-12](../../design/app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*.
- Cần `group-crawl-job`, tức job thật trên hàng đợi `fb-browser`: từ [P0-SKL-056](#s-73919d3075 "Kết quả job trình duyệt đi qua hàng đợi kết quả") *(Kết quả job trình duyệt đi qua hàng đợi kết quả)* đến [P0-SKL-064](#s-49762e0a06 "api dừng khi worker đang trả kết quả: kết quả không mất, xử…") *(api dừng khi worker đang trả kết quả: kết quả không mất, xử…)*, [P0-SKL-069](#s-3c1666c6f9 "Worker chết khi api đang tắt: job vẫn được ghi thất bại sau…") *(Worker chết khi api đang tắt: job vẫn được ghi thất bại sau…)*.

**Phần kiểm ở nơi khác**

- Phần "hàng đợi `render` không dùng profile Facebook" của [R-SKL-05](../../design/app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)* được kiểm chứng trong test case của tính năng render ở giai đoạn 4.

**Phần chỉ kiểm được bằng test tự động**

Các phần sau không tạo được bằng thao tác bên ngoài code. Vì vậy `/implementation-plan` phải có test tự động tương ứng.

- [R-SKL-07](../../design/app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*: mọi Worker đặt `maxStalledCount: 0`. Hành vi của quy tắc này được kiểm ở [P0-SKL-060](#s-2c9a4efd46 "Quá thời gian ân hạn: job dở dang thất bại, không chạy lại") *(Quá thời gian ân hạn: job dở dang thất bại, không chạy lại)* và [P0-SKL-061](#s-43c4e46785 "Một worker chết giữa job, worker còn lại không chạy lại job…") *(Một worker chết giữa job, worker còn lại không chạy lại job…)*.
- [R-SKL-10](../../design/app-skeleton.md#s-0f1edd606c "get / set với khóa không có trong SETTINGS") *(get / set với khóa không có trong SETTINGS)*: khi chạy, nếu khoá không có trong `SETTINGS` thì API trả 500 `INTERNAL_ERROR`.
- [R-SKL-28](../../design/app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)* và [R-SKL-29](../../design/app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*:
  - Processor ném lỗi thì vẫn gửi kết quả `UnexpectedError`.
  - Với stalled giả, tức kết quả thật tới sau `WorkerCrashedError`, kết quả thật thắng. Mỗi tín hiệu chỉ được ghi nhận một lần.
- [R-SKL-17](../../design/app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*: kiểm từng đường dẫn trong danh sách che.

<a id="s-9d0cec4336"></a>

## P0-SKL-001 Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose

**Kiểm tra điều gì.** Lần khởi động đầu tiên bằng Docker Compose đưa cả 4 dịch vụ lên trạng thái healthy theo đúng thứ tự phụ thuộc. Health check và trang web phản hồi đúng.

- Thiết kế: [R-SKL-03](../../design/app-skeleton.md#s-0f1edd606c "chỉ api chạy migration") *(chỉ api chạy migration)*, [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*, [R-SKL-14](../../design/app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*; mục Trạng thái và thuật toán › Khởi động
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- `MIO_DATA_DIR` trỏ tới thư mục trống.
- Chưa có volume DB. Trên môi trường thử, chạy `docker compose down -v`; môi trường này không có dữ liệu cần giữ.

**Các bước**

1. Chạy `pnpm docker:build`.
   - Mong đợi: build xong, không có lỗi.
2. Chạy `docker compose up -d`. Chờ tối đa 2 phút, rồi chạy `docker compose ps`.
   - Mong đợi: cả 4 dịch vụ `postgres`, `redis`, `api`, `browser-worker` đều ở trạng thái `running (healthy)`.
   - 📷 Chụp evidence.
3. Chạy `docker inspect -f '{{.Name}} {{.State.StartedAt}}'` cho 4 container.
   - Mong đợi: `api` khởi động sau khi `postgres` và `redis` đã healthy. `browser-worker` khởi động sau khi `api` đã healthy.
   - 📷 Chụp evidence.
4. Chạy `docker inspect -f '{{.HostConfig.RestartPolicy.Name}}'` cho 4 container.
   - Mong đợi: cả 4 container đều là `unless-stopped`.
5. Chạy `curl -s http://127.0.0.1:3000/api/v1/health`.
   - Mong đợi: trả 200, thân là `{"status":"ok","checks":{"database":"up","redis":"up"}}`.
   - 📷 Chụp evidence.
6. Mở `http://127.0.0.1:3000/` bằng Playwright.
   - Mong đợi: trang hiển thị "Tiệm Nhà Mio".
   - 📷 Chụp evidence.

<a id="s-7590720fdf"></a>

## P0-SKL-002 api thiếu một biến môi trường bắt buộc

**Kiểm tra điều gì.** api dừng ngay khi thiếu một biến môi trường bắt buộc. Log nêu đúng tên biến bị thiếu.

- Thiết kế: [R-SKL-01](../../design/app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã build `<image api>`.

**Các bước**

1. Chạy api không có biến `REDIS_URL` bằng lệnh `docker run --rm -e DATABASE_URL=postgres://mio:x@postgres:5432/mio -e DATA_DIR=/data -e PUBLIC_URL=http://localhost:3000 <image api>`. Sau đó chạy `echo $?`.
   - Mong đợi: tiến trình dừng ngay. Lệnh `echo $?` in ra `1`.
   - 📷 Chụp evidence.
2. Đọc log.
   - Mong đợi: có một dòng JSON mức error với thông báo "Thiếu biến môi trường: REDIS_URL". Không có dòng log mở cổng 3000.
   - 📷 Chụp evidence.

<a id="s-74e6a0b8fd"></a>

## P0-SKL-003 api thiếu cả bốn biến môi trường

**Kiểm tra điều gì.** Khi thiếu cả bốn biến bắt buộc, api báo đủ 4 tên biến trong cùng một dòng log.

- Thiết kế: [R-SKL-01](../../design/app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã build `<image api>`.

**Các bước**

1. Chạy `docker run --rm <image api>`, không truyền biến nào.
   - Mong đợi: tiến trình thoát với mã 1.
2. Đọc log.
   - Mong đợi: có đúng một dòng thông báo liệt kê cả bốn biến: "Thiếu biến môi trường: DATABASE_URL, REDIS_URL, DATA_DIR, PUBLIC_URL". Thứ tự tên có thể khác, nhưng phải đủ 4 tên trong cùng một dòng.
   - 📷 Chụp evidence.

<a id="s-b90f0e9e0f"></a>

## P0-SKL-004 Biến bắt buộc thiếu hoặc rỗng trong `.env` và trong container

**Kiểm tra điều gì.** Biến bắt buộc bị thiếu hoặc rỗng bị chặn ở hai lớp. Lớp thứ nhất là Docker Compose khi đọc `.env`. Lớp thứ hai là tiến trình api trong container.

- Thiết kế: [R-SKL-01](../../design/app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*; bảng biến Compose (cú pháp `${TÊN:?…}`)
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.
- Sao lưu `.env`.
- Ghi lại `StartedAt` của 4 container.

**Các bước**

1. Xoá dòng `MIO_PUBLIC_URL` trong `.env`. Chạy `docker compose up -d; echo $?`.
   - Mong đợi: lệnh dừng ngay và in "Thiếu MIO_PUBLIC_URL trong .env". Mã thoát khác `0`.
   - 📷 Chụp evidence.
2. Xem `StartedAt` của 4 container.
   - Mong đợi: giá trị không đổi. Không container nào bị tạo lại hay khởi động lại.
3. Đặt `MIO_PUBLIC_URL=` (giá trị rỗng), rồi lặp lại bước 1 và bước 2.
   - Mong đợi: kết quả giống bước 1 và bước 2.
4. Lặp lại bước 1 với `POSTGRES_PASSWORD` và `MIO_DATA_DIR`.
   - Mong đợi: thông báo nêu đúng tên biến tương ứng.
5. Trả lại `.env`. Chạy `docker run --rm` `<image api>` với đủ biến nhưng đặt `-e PUBLIC_URL=`.
   - Mong đợi: thoát mã 1. Log có "Thiếu biến môi trường: PUBLIC_URL".
   - 📷 Chụp evidence.
6. Lặp lại bước 5 với `-e "PUBLIC_URL=   "`, tức giá trị chỉ có khoảng trắng.
   - Mong đợi: cùng thông báo, thoát mã 1.

<a id="s-3c12995de6"></a>

## P0-SKL-005 REDIS_URL sai định dạng

**Kiểm tra điều gì.** api và browser-worker từ chối `REDIS_URL` không phải URL `redis://`. Log không in giá trị của biến.

- Thiết kế: [R-SKL-02](../../design/app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã build `<image api>` và `<image browser-worker>`.

**Các bước**

1. Chạy `<image api>` với đủ biến, đặt `REDIS_URL=http://redis:6379`.
   - Mong đợi: thoát mã 1. Log có "Biến môi trường không hợp lệ: REDIS_URL (phải là URL redis://)".
   - 📷 Chụp evidence.
2. Lặp lại với `REDIS_URL=redis`, là giá trị không phải URL.
   - Mong đợi: cùng thông báo, thoát mã 1.
3. Lặp lại bước 1 với `<image browser-worker>`.
   - Mong đợi: cùng thông báo, thoát mã 1.
   - 📷 Chụp evidence.
4. Tìm chuỗi `http://redis:6379` trong toàn bộ log của các lần chạy.
   - Mong đợi: không tìm thấy. Giá trị của biến không bị in ra log.

<a id="s-6ba381391d"></a>

## P0-SKL-006 DATABASE_URL: phân vùng hợp lệ / không hợp lệ và không lộ mật khẩu

**Kiểm tra điều gì.** `DATABASE_URL` chỉ nhận URL bắt đầu bằng `postgres://` hoặc `postgresql://`. Khi báo lỗi, log không làm lộ mật khẩu trong URL.

- Thiết kế: [R-SKL-02](../../design/app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*, [R-SKL-17](../../design/app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy api với `DATABASE_URL=postgresql://mio:<mật khẩu đúng>@postgres:5432/mio`, tức dùng tiền tố `postgresql://`. Nối container vào mạng Compose.
   - Mong đợi: api khởi động bình thường. `/api/v1/health` của container này trả 200.
2. Chạy api với `DATABASE_URL=mysql://mio:Secret123@postgres:5432/mio`.
   - Mong đợi: thoát mã 1. Log có "Biến môi trường không hợp lệ: DATABASE_URL (phải là URL postgres:// hoặc postgresql://)".
   - 📷 Chụp evidence.
3. Chạy api với `DATABASE_URL=abc`.
   - Mong đợi: cùng thông báo, thoát mã 1.
4. Tìm `Secret123` trong log của bước 2.
   - Mong đợi: không tìm thấy.
   - 📷 Chụp evidence.

<a id="s-1ac18aa3a0"></a>

## P0-SKL-007 PUBLIC_URL: phân vùng hợp lệ / không hợp lệ

**Kiểm tra điều gì.** `PUBLIC_URL` phải là URL `http://` hoặc `https://` và không có dấu `/` ở cuối.

- Thiết kế: [R-SKL-02](../../design/app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương, giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy api với `PUBLIC_URL=https://mio.example.com`.
   - Mong đợi: api khởi động bình thường.
2. Chạy api với `PUBLIC_URL=http://localhost:3000/`, có `/` ở cuối.
   - Mong đợi: thoát mã 1 với thông báo "Biến môi trường không hợp lệ: PUBLIC_URL (phải là URL http:// hoặc https://, không có / cuối)".
   - 📷 Chụp evidence.
3. Chạy api với `PUBLIC_URL=localhost:3000`, thiếu scheme.
   - Mong đợi: cùng thông báo, thoát mã 1.
4. Chạy api với `PUBLIC_URL=ftp://localhost`.
   - Mong đợi: cùng thông báo, thoát mã 1.

<a id="s-1630bac11e"></a>

## P0-SKL-008 DATA_DIR, BROWSER_PROFILE_DIR là đường dẫn tương đối

**Kiểm tra điều gì.** `DATA_DIR` và `BROWSER_PROFILE_DIR` phải là đường dẫn tuyệt đối. Đường dẫn tương đối làm tiến trình dừng với thông báo rõ.

- Thiết kế: [R-SKL-02](../../design/app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã build `<image api>` và `<image browser-worker>`.

**Các bước**

1. Chạy api với `DATA_DIR=data`.
   - Mong đợi: thoát mã 1 với thông báo "Biến môi trường không hợp lệ: DATA_DIR (phải là đường dẫn tuyệt đối)".
   - 📷 Chụp evidence.
2. Lặp lại bước 1 với browser-worker.
   - Mong đợi: cùng thông báo, thoát mã 1.
3. Chạy browser-worker với `DATA_DIR=/data` và `BROWSER_PROFILE_DIR=browser-profile`.
   - Mong đợi: thoát mã 1 với thông báo "Biến môi trường không hợp lệ: BROWSER_PROFILE_DIR (phải là đường dẫn tuyệt đối)".

<a id="s-4737cb2269"></a>

## P0-SKL-009 browser-worker chỉ cần REDIS_URL, DATA_DIR, BROWSER_PROFILE_DIR

**Kiểm tra điều gì.** browser-worker chỉ đòi ba biến `REDIS_URL`, `DATA_DIR`, `BROWSER_PROFILE_DIR`. Worker không đòi `DATABASE_URL` hay `PUBLIC_URL`.

- Thiết kế: [R-SKL-01](../../design/app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*, [R-SKL-04](../../design/app-skeleton.md#s-0f1edd606c "browser-worker chỉ kết nối Redis") *(browser-worker chỉ kết nối Redis)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- `redis` đang chạy.

**Các bước**

1. Chạy `<image browser-worker>` trong mạng Compose với `--hostname skl-009`. Chỉ truyền `REDIS_URL`, `DATA_DIR`, `BROWSER_PROFILE_DIR`; không truyền `DATABASE_URL`, `PUBLIC_URL`.
   - Mong đợi: worker chạy bình thường. Sau 20 giây, khoá `mio:heartbeat:browser-worker:skl-009` có giá trị mới.
   - 📷 Chụp evidence.
2. Chạy lại, lần này chỉ truyền `DATA_DIR`.
   - Mong đợi: thoát mã 1 với thông báo "Thiếu biến môi trường: REDIS_URL, BROWSER_PROFILE_DIR". Thứ tự tên có thể khác. Thông báo không đòi `DATABASE_URL`, `PUBLIC_URL`.
   - 📷 Chụp evidence.

<a id="s-df4b3f6164"></a>

## P0-SKL-010 Thư mục dữ liệu không ghi được

**Kiểm tra điều gì.** api và browser-worker dừng với thông báo rõ khi không ghi được vào thư mục dữ liệu hoặc thư mục profile.

- Thiết kế: [R-SKL-20](../../design/app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã build hai image.

**Các bước**

1. Chạy api, gắn thư mục chỉ đọc bằng `-v <thư mục tạm>:/data:ro` và đặt `DATA_DIR=/data`.
   - Mong đợi: thoát mã 1 với thông báo "Không ghi được vào thư mục dữ liệu: /data".
   - 📷 Chụp evidence.
2. Lặp lại bước 1 với browser-worker.
   - Mong đợi: cùng thông báo, thoát mã 1.
3. Chạy api với `DATA_DIR=/khong-co-quyen/data`. Thư mục cha của đường dẫn này không ghi được bằng user không phải root.
   - Mong đợi: thoát mã 1 với thông báo "Không ghi được vào thư mục dữ liệu: /khong-co-quyen/data".
4. Chạy browser-worker với `-v <thư mục tạm>:/browser-profile:ro` và `BROWSER_PROFILE_DIR=/browser-profile`.
   - Mong đợi: thoát mã 1 với thông báo "Không ghi được vào thư mục dữ liệu: /browser-profile".
   - 📷 Chụp evidence.

<a id="s-e686545008"></a>

## P0-SKL-011 Thư mục con, profile trong named volume, cùng user không phải root

**Kiểm tra điều gì.** api tạo các thư mục con trong thư mục dữ liệu. Profile trình duyệt nằm trong named volume riêng, không nằm trong thư mục dữ liệu. Hai container chạy cùng một user không phải root nên dùng chung được thư mục dữ liệu.

- Thiết kế: [R-SKL-20](../../design/app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*; [ADR 0013](../../../../decisions/0013-browser-profile-named-volume.md "Profile trình duyệt nằm trong named volume riêng") *(Profile trình duyệt nằm trong named volume riêng)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- `MIO_DATA_DIR` trỏ tới thư mục trống.
- Hệ thống đang dừng.
- Chưa có volume `mio-browser-profile`. Trên môi trường thử, chạy `docker compose down -v`.

**Các bước**

1. Chạy `docker compose up -d postgres redis api` và chờ api healthy. Liệt kê nội dung `MIO_DATA_DIR`.
   - Mong đợi: có `images/` và `debug-dumps/`.
   - 📷 Chụp evidence.
2. Chạy `docker compose up -d browser-worker` và chờ healthy. Chạy `docker volume ls`.
   - Mong đợi: có volume tên kết thúc bằng `mio-browser-profile`. `MIO_DATA_DIR` không có `browser-profile/`.
   - 📷 Chụp evidence.
3. Chạy `docker compose exec browser-worker stat -c '%a %u:%g' /browser-profile`.
   - Mong đợi: kết quả là `700 1000:1000`.
   - 📷 Chụp evidence.
4. Chạy `id -u` và `id -g` trong api và trong browser-worker.
   - Mong đợi: cả hai container đều trả `1000` và `1000`.
   - 📷 Chụp evidence.
5. Chạy lần lượt ba lệnh `docker compose exec browser-worker sh -c 'echo x > /data/debug-dumps/probe.txt'`, `docker compose exec api cat /data/debug-dumps/probe.txt` và `docker compose exec api rm /data/debug-dumps/probe.txt`.
   - Mong đợi: lệnh thứ nhất ghi được file. Lệnh thứ hai in `x`. Lệnh thứ ba xoá được file, không có lỗi quyền.
   - 📷 Chụp evidence.

<a id="s-84afd4755e"></a>

## P0-SKL-012 Khởi động lại không làm mất dữ liệu có sẵn trong DATA_DIR

**Kiểm tra điều gì.** Khởi động lại container không làm mất file có sẵn trong thư mục dữ liệu. Profile trình duyệt vẫn còn sau khi container bị tạo lại.

- Thiết kế: [R-SKL-20](../../design/app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Trong `MIO_DATA_DIR`, tạo file `images/probe.txt` với nội dung `probe`.
2. Chạy `docker compose restart api browser-worker` và chờ healthy.
   - Mong đợi: `images/probe.txt` vẫn còn, nội dung là `probe`. `/browser-profile` vẫn có quyền `700`.
   - 📷 Chụp evidence.
3. Chạy `docker compose exec browser-worker sh -c 'echo p > /browser-profile/probe.txt'`. Sau đó chạy `docker compose down` (không có `-v`), rồi `docker compose up -d`.
   - Mong đợi: `/browser-profile/probe.txt` vẫn còn, tức profile được giữ qua lần tạo lại container.
   - 📷 Chụp evidence.
   - Dọn dẹp: xoá file thử.

<a id="s-f9d0d276db"></a>

## P0-SKL-013 Migration lần đầu, lần sau và cấu trúc bảng `app_settings`

**Kiểm tra điều gì.** Migration chạy trước khi api mở cổng. Bảng `app_settings` có đúng cột và ràng buộc. Lần khởi động sau không chạy lại migration.

- Thiết kế: [R-SKL-03](../../design/app-skeleton.md#s-0f1edd606c "chỉ api chạy migration") *(chỉ api chạy migration)*; `docs/design/db-schema.md` mục `app_settings`
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*, tức volume DB mới.

**Các bước**

1. Chạy `docker compose up -d`, rồi xem `docker compose logs api`.
   - Mong đợi: log chạy migration nằm trước log mở cổng 3000.
   - 📷 Chụp evidence.
2. Chạy `docker compose exec postgres psql -U mio -d mio -c '\d app_settings'`.
   - Mong đợi: bảng có các cột `id uuid`, `key text`, `value jsonb`, `created_at timestamptz`, `updated_at timestamptz`, tất cả đều not null. Giá trị mặc định là `gen_random_uuid()` và `now()`. Có index unique `app_settings_key_key`. Có check kebab-case trên cột `key`.
   - 📷 Chụp evidence.
3. Chạy `insert into app_settings (key, value) values ('Crawl_Schedule', '{}')`.
   - Mong đợi: lỗi vi phạm check constraint.
4. Chèn `('probe-key', '{}')` hai lần.
   - Mong đợi: lần thứ hai lỗi vi phạm unique `app_settings_key_key`.
   - Dọn dẹp: xoá dòng `probe-key`.
5. Đếm số bản ghi trong bảng migration của Drizzle. Chạy `docker compose restart api`, rồi đếm lại.
   - Mong đợi: số bản ghi không đổi. api healthy, log không có lỗi migration.

<a id="s-ffa4907d59"></a>

## P0-SKL-014 Migration lỗi thì api không mở cổng

**Kiểm tra điều gì.** Khi migration lỗi, api không mở cổng và browser-worker không khởi động. Sau khi gỡ nguyên nhân, api lên lại ở lần khởi động lại kế tiếp.

- Thiết kế: [R-SKL-03](../../design/app-skeleton.md#s-0f1edd606c "chỉ api chạy migration") *(chỉ api chạy migration)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Volume DB mới. Trên môi trường thử, chạy `docker compose down -v`.

**Các bước**

1. Chạy `docker compose up -d postgres redis`. Sau đó chạy `psql -c 'create table app_settings (x int)'` để tạo một bảng trùng tên nhưng sai cấu trúc.
2. Chạy `docker compose up -d api`.
   - Mong đợi: log api mức error nêu migration lỗi. Tiến trình thoát mã 1. Compose khởi động lại api liên tục.
   - 📷 Chụp evidence.
3. Chạy `curl -s -m 5 http://127.0.0.1:3000/api/v1/health`.
   - Mong đợi: không kết nối được, không có HTTP response nào trả về.
   - 📷 Chụp evidence.
4. Chạy `docker compose ps browser-worker`.
   - Mong đợi: browser-worker chưa khởi động vì đang chờ api healthy.
5. Chạy `psql -c 'drop table app_settings'`.
   - Mong đợi: ở lần khởi động lại kế tiếp, migration chạy xong. api healthy và `/api/v1/health` trả 200.

<a id="s-0878af620e"></a>

## P0-SKL-015 browser-worker không kết nối PostgreSQL, không mở cổng, không gọi API

**Kiểm tra điều gì.** browser-worker không kết nối PostgreSQL, không lắng nghe cổng nào và không gọi API. Worker vẫn sống khi PostgreSQL dừng.

- Thiết kế: [R-SKL-04](../../design/app-skeleton.md#s-0f1edd606c "browser-worker chỉ kết nối Redis") *(browser-worker chỉ kết nối Redis)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `docker compose exec browser-worker sh -c 'env | grep -c DATABASE_URL'`.
   - Mong đợi: kết quả là `0`.
2. Chạy `psql -c "select client_addr from pg_stat_activity where datname = 'mio'"`.
   - Mong đợi: chỉ có IP của container api, đối chiếu bằng `docker inspect`. Không có IP của browser-worker.
   - 📷 Chụp evidence.
3. Chạy `docker compose exec browser-worker cat /proc/net/tcp /proc/net/tcp6`.
   - Mong đợi: không có dòng nào ở trạng thái `0A`, tức worker không lắng nghe cổng nào.
   - 📷 Chụp evidence.
4. Đọc log api trong 2 phút.
   - Mong đợi: không có request nào đến từ IP của browser-worker.
5. Chạy `docker compose stop postgres` và chờ 30 giây.
   - Mong đợi: browser-worker vẫn healthy. Khoá nhịp sống vẫn được cập nhật.
   - Dọn dẹp: chạy `docker compose start postgres`.

<a id="s-b4c1c046ab"></a>

## P0-SKL-016 Health trả ok, không cần đăng nhập, không lộ thông tin

**Kiểm tra điều gì.** Endpoint health trả ok khi DB và Redis đều chạy. Gọi endpoint này không cần đăng nhập. Thân response không lộ thông tin hệ thống.

- Thiết kế: [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: bảng quyết định (DB up, Redis up)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `curl -i http://127.0.0.1:3000/api/v1/health`, không gửi cookie hay header xác thực.
   - Mong đợi: trả 200 với `Content-Type: application/json`. Thân đúng là `{"status":"ok","checks":{"database":"up","redis":"up"}}`.
   - 📷 Chụp evidence.
2. Kiểm tra thân response.
   - Mong đợi: chỉ có khoá `status` và `checks`. Không có phiên bản, đường dẫn hay tên máy.

<a id="s-8c19408dd1"></a>

## P0-SKL-017 Health khi PostgreSQL dừng rồi chạy lại

**Kiểm tra điều gì.** Khi PostgreSQL dừng, health trả 503 và api không bị khởi động lại. Khi PostgreSQL chạy lại, api tự kết nối lại.

- Thiết kế: [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*; mục Xử lý lỗi (tự kết nối lại)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB down, Redis up)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.
- Ghi lại `RestartCount` của api.

**Các bước**

1. Chạy `docker compose stop postgres`, rồi gọi health.
   - Mong đợi: trả 503, thân đúng là `{"status":"error","checks":{"database":"down","redis":"up"}}`. Không có thông báo lỗi chi tiết.
   - 📷 Chụp evidence.
2. Kiểm tra api.
   - Mong đợi: tiến trình vẫn chạy. `RestartCount` không đổi.
3. Chạy `docker compose start postgres`, rồi gọi health mỗi 5 giây.
   - Mong đợi: trong 60 giây, health trả 200 với `status: ok`. `RestartCount` của api không đổi.
   - 📷 Chụp evidence.

<a id="s-35e615609e"></a>

## P0-SKL-018 Health khi Redis dừng rồi chạy lại

**Kiểm tra điều gì.** Khi Redis dừng, health trả 503. Khi Redis chạy lại, api và browser-worker tự kết nối lại mà không bị khởi động lại.

- Thiết kế: [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*, [R-SKL-18](../../design/app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*; mục Xử lý lỗi (tự kết nối lại)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB up, Redis down)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-017](#s-8c19408dd1 "Health khi PostgreSQL dừng rồi chạy lại") *(Health khi PostgreSQL dừng rồi chạy lại)*.

**Các bước**

1. Chạy `docker compose stop redis`, rồi gọi health.
   - Mong đợi: trả 503, thân là `{"status":"error","checks":{"database":"up","redis":"down"}}`.
   - 📷 Chụp evidence.
2. Chạy `docker compose start redis`.
   - Mong đợi: trong 60 giây, health trả 200. `RestartCount` của api không đổi.
3. Đọc `<khóa nhịp sống>` hai lần, cách nhau 20 giây.
   - Mong đợi: giá trị thay đổi, tức worker đã tự kết nối lại.
   - 📷 Chụp evidence.

<a id="s-fff1836c2e"></a>

## P0-SKL-019 Health khi cả PostgreSQL và Redis dừng

**Kiểm tra điều gì.** Khi cả PostgreSQL và Redis dừng, health trả 503 và báo cả hai đều down. Khi hai dịch vụ chạy lại, health trở về bình thường.

- Thiết kế: [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: bảng quyết định (DB down, Redis down)
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-017](#s-8c19408dd1 "Health khi PostgreSQL dừng rồi chạy lại") *(Health khi PostgreSQL dừng rồi chạy lại)*.

**Các bước**

1. Chạy `docker compose stop postgres redis`, rồi gọi health.
   - Mong đợi: trả 503, thân là `{"status":"error","checks":{"database":"down","redis":"down"}}`.
   - 📷 Chụp evidence.
2. Chạy `docker compose start postgres redis`.
   - Mong đợi: trong 60 giây, health trả 200.

<a id="s-04badc4434"></a>

## P0-SKL-020 Health khi DB hoặc Redis treo (không trả lời)

**Kiểm tra điều gì.** Khi DB hoặc Redis treo, health không treo theo mà trả 503 sau thời gian chờ 2 giây. Hai kiểm tra chạy song song nên tổng thời gian không cộng dồn.

- Thiết kế: [R-SKL-13](../../design/app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)* (kiểm song song); mục Tham số (chờ 2 giây)
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `docker compose pause postgres`, rồi chạy `curl -s -w '%{http_code} %{time_total}' http://127.0.0.1:3000/api/v1/health`.
   - Mong đợi: trả 503 với `database: down`. Thời gian trả về từ 2 đến 3 giây, không bị treo.
   - 📷 Chụp evidence.
2. Chạy `docker compose unpause postgres`.
   - Mong đợi: health trả 200.
3. Lặp lại bước 1 và bước 2 với `redis`.
   - Mong đợi: health trả 503 với `redis: down` trong khoảng 2 đến 3 giây. Sau khi unpause, health trả 200.
   - 📷 Chụp evidence.
4. Chạy `docker compose pause postgres redis`, rồi gọi health có đo thời gian.
   - Mong đợi: trả 503, cả `database` và `redis` đều là `down`. Thời gian trả về từ 2 đến 3 giây, không phải 4 giây, vì hai kiểm tra chạy song song.
   - 📷 Chụp evidence.
   - Dọn dẹp: chạy `docker compose unpause postgres redis`.

<a id="s-c4ede932f8"></a>

## P0-SKL-021 Đường dẫn API không tồn tại trả 404 đúng định dạng

**Kiểm tra điều gì.** Mọi đường dẫn API không tồn tại đều trả 404 với thân JSON theo định dạng lỗi chung. API không trả `index.html` cho các đường dẫn này.

- Thiết kế: [R-SKL-15](../../design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*, [R-SKL-14](../../design/app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `curl -i http://127.0.0.1:3000/api/v1/khong-co`.
   - Mong đợi: trả 404 với `Content-Type: application/json`. Thân đúng là `{"code":"NOT_FOUND","message":"Không tìm thấy địa chỉ yêu cầu"}`. Không có `fields`, `statusCode`, `error` hay stack.
   - 📷 Chụp evidence.
2. Chạy `curl -i -X POST http://127.0.0.1:3000/api/v1/health`.
   - Mong đợi: trả 404, thân giống bước 1.
3. Chạy `curl -i http://127.0.0.1:3000/api/khong-co` và gọi `http://127.0.0.1:3000/api/v1/`.
   - Mong đợi: cả hai trả 404 với JSON giống bước 1. Không trả `index.html`.

<a id="s-42435624aa"></a>

## P0-SKL-022 Trang web giữ chỗ hiển thị đúng

**Kiểm tra điều gì.** Trang web giữ chỗ hiển thị đúng chữ và đúng token màu, trên cả màn hình rộng và màn hình điện thoại.

- Thiết kế: [R-SKL-14](../../design/app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*; mục `apps/web`
- Khía cạnh: Hiển thị
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Dùng Playwright mở `http://127.0.0.1:3000/` với khung 1440×900.
   - Mong đợi: chữ "Tiệm Nhà Mio" hiển thị đủ dấu. Console không có lỗi.
   - 📷 Chụp evidence.
2. Kiểm tra tab mạng. Chạy `getComputedStyle(document.documentElement).getPropertyValue('--color-brand-primary')`.
   - Mong đợi: file CSS chứa token trả 200. Lệnh trả về `#8FA284`.
3. Lặp lại bước 1 với khung 390×844.
   - Mong đợi: trang không có cuộn ngang, chữ không bị cắt.
   - 📷 Chụp evidence.

<a id="s-58386390dc"></a>

## P0-SKL-023 Định tuyến SPA và file tĩnh

**Kiểm tra điều gì.** Đường dẫn không thuộc `/api/` được trả `index.html` để SPA tự định tuyến. File tĩnh có thật được trả đúng nội dung.

- Thiết kế: [R-SKL-14](../../design/app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `curl -i http://127.0.0.1:3000/settings/groups`.
   - Mong đợi: trả 200, thân giống hệt `GET /`, tức `index.html`.
   - 📷 Chụp evidence.
2. Lấy một file JS thật trong `apps/web/dist/assets/` và gọi `/assets/<file>`.
   - Mong đợi: trả 200, `Content-Type` là JavaScript, nội dung trùng với file.
3. Chạy `curl -i http://127.0.0.1:3000/khong-co.png`.
   - Mong đợi: trả 200 với `index.html`.
4. Chạy `curl -i http://127.0.0.1:3000/apifoo`.
   - Mong đợi: trả 200 với `index.html`, vì đường dẫn không bắt đầu bằng `/api/`.

<a id="s-0885e58331"></a>

## P0-SKL-024 Vite dev proxy chuyển `/api` sang api

**Kiểm tra điều gì.** Khi chạy web ở chế độ dev, Vite chuyển các request tới `/api` sang api.

- Thiết kế: mục `apps/web` (Dev)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- api đang chạy ở `localhost:3000`.

**Các bước**

1. Chạy `pnpm --filter @mio/web dev`.
   - Mong đợi: Vite chạy và in ra cổng dev.
2. Chạy `curl http://localhost:<cổng dev>/api/v1/health`.
   - Mong đợi: trả 200, thân giống khi gọi thẳng api.
   - 📷 Chụp evidence.

<a id="s-ffebda647f"></a>

## P0-SKL-025 Log là JSON một dòng, đủ trường bắt buộc

**Kiểm tra điều gì.** Log của api và browser-worker là JSON, mỗi bản ghi nằm trên một dòng và có đủ trường bắt buộc.

- Thiết kế: [R-SKL-17](../../design/app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.
- Đã gọi vài request, ví dụ health và 404.

**Các bước**

1. Chạy `docker compose logs --no-log-prefix api browser-worker`.
   - Mong đợi: mọi dòng đều parse được bằng `json.loads`. Mỗi lỗi nằm gọn trong một dòng.
   - 📷 Chụp evidence.
2. Kiểm tra các trường của từng dòng.
   - Mong đợi: mỗi dòng có `time`, `level`, `app`, `msg`. `app` là `api` hoặc `browser-worker`, đúng với container ghi log.
3. Tìm dòng log của request `GET /api/v1/khong-co`.
   - Mong đợi: dòng này có `requestId`.
   - 📷 Chụp evidence.

<a id="s-f73adfb051"></a>

## P0-SKL-026 Log che khoá nhạy cảm và không ghi giá trị biến môi trường

**Kiểm tra điều gì.** Log che giá trị của header nhạy cảm. Log không ghi giá trị của biến môi trường bí mật.

- Thiết kế: [R-SKL-17](../../design/app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*, [R-SKL-02](../../design/app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.

**Các bước**

1. Gửi request có header xác thực và cookie bằng `curl -H 'Authorization: Bearer tok-ABC123' -H 'Cookie: sid=COOKIE-XYZ789' http://127.0.0.1:3000/api/v1/khong-co`.
2. Tìm `tok-ABC123` và `COOKIE-XYZ789` trong log api.
   - Mong đợi: không tìm thấy. Nếu log có header `authorization` hoặc `cookie` thì giá trị là `[REDACTED]`.
   - 📷 Chụp evidence.
3. Tìm giá trị `POSTGRES_PASSWORD` (lấy trong `.env`) và chuỗi `DATABASE_URL` đầy đủ trong log của mọi container.
   - Mong đợi: không tìm thấy.
   - 📷 Chụp evidence.

<a id="s-d92e492827"></a>

## P0-SKL-027 Giới hạn kích thước log Docker

**Kiểm tra điều gì.** Cả 4 container đều giới hạn kích thước log Docker.

- Thiết kế: [R-SKL-26](../../design/app-skeleton.md#s-0f1edd606c "Docker giới hạn log mỗi container") *(Docker giới hạn log mỗi container)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.

**Các bước**

1. Chạy `docker inspect -f '{{json .HostConfig.LogConfig}}'` cho 4 container.
   - Mong đợi: cả 4 container đều là `{"Type":"json-file","Config":{"max-file":"5","max-size":"10m"}}`.
   - 📷 Chụp evidence.

<a id="s-c018c91fcd"></a>

## P0-SKL-028 Chỉ cổng api được mở, và chỉ trên 127.0.0.1

**Kiểm tra điều gì.** Chỉ api mở cổng ra máy host, và chỉ trên `127.0.0.1`. PostgreSQL, Redis và browser-worker không mở cổng nào.

- Thiết kế: [R-SKL-19](../../design/app-skeleton.md#s-0f1edd606c "compose") *(compose)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống chạy chỉ bằng `compose.yml`.

**Các bước**

1. Chạy `docker compose ps --format '{{.Service}} {{.Ports}}'`.
   - Mong đợi: chỉ `api` có `127.0.0.1:3000->3000/tcp`. `postgres`, `redis`, `browser-worker` không publish cổng.
   - 📷 Chụp evidence.
2. Chạy `curl -m 5 http://<IP LAN của máy>:3000/api/v1/health`, rồi chạy `curl http://127.0.0.1:3000/api/v1/health`.
   - Mong đợi: lệnh thứ nhất không kết nối được. Lệnh thứ hai trả 200.
   - 📷 Chụp evidence.
3. Chạy `Test-NetConnection 127.0.0.1 -Port 5432` và `-Port 6379`.
   - Mong đợi: không kết nối được.

<a id="s-d10e4d3215"></a>

## P0-SKL-029 compose.dev.yml mở PostgreSQL và Redis chỉ trên 127.0.0.1

**Kiểm tra điều gì.** Khi dùng thêm `compose.dev.yml`, PostgreSQL và Redis được mở cho máy host nhưng chỉ trên `127.0.0.1`.

- Thiết kế: [R-SKL-19](../../design/app-skeleton.md#s-0f1edd606c "compose") *(compose)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang dừng.

**Các bước**

1. Chạy `docker compose -f compose.yml -f compose.dev.yml up -d`, rồi chạy `docker compose ps`.
   - Mong đợi: `postgres` ở `127.0.0.1:5432->5432`, `redis` ở `127.0.0.1:6379->6379`.
   - 📷 Chụp evidence.
2. Từ máy host, chạy `psql -h 127.0.0.1 -U mio -d mio -c 'select 1'` và `redis-cli -h 127.0.0.1 ping`.
   - Mong đợi: lệnh thứ nhất trả `1`. Lệnh thứ hai trả `PONG`.
3. Kết nối tới `<IP LAN của máy>:5432` và `:6379`.
   - Mong đợi: không kết nối được.

<a id="s-ee5b3d310f"></a>

## P0-SKL-030 Container và phiên PostgreSQL dùng múi giờ UTC

**Kiểm tra điều gì.** Các container và phiên PostgreSQL dùng múi giờ UTC, kể cả khi máy host đặt múi giờ khác.

- Thiết kế: [R-SKL-23](../../design/app-skeleton.md#s-0f1edd606c "container đặt TZ=UTC") *(container đặt TZ=UTC)*
- Khía cạnh: Thời gian
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.
- Máy host đặt múi giờ UTC+7.

**Các bước**

1. Chạy `docker compose exec api node -e "console.log(Intl.DateTimeFormat().resolvedOptions().timeZone, new Date().getTimezoneOffset())"`, rồi lặp lại với browser-worker.
   - Mong đợi: cả hai container đều in `UTC 0`.
   - 📷 Chụp evidence.
2. Chạy `psql -c 'show timezone'`.
   - Mong đợi: kết quả là `UTC`.
3. Chạy `redis-cli GET <khóa nhịp sống>`.
   - Mong đợi: giá trị là chuỗi ISO kết thúc bằng `Z`. Thời điểm này lệch giờ UTC thực tế không quá 15 giây.

<a id="s-2bdadce2bf"></a>

## P0-SKL-031 Lint chặn `Date.now()` và `new Date()` không tham số

**Kiểm tra điều gì.** Lint báo lỗi khi code lấy giờ hiện tại trực tiếp bằng `Date.now()` hoặc `new Date()` không tham số. Lời gọi có tham số như `new Date('2026-10-29')` vẫn được phép.

- Thiết kế: [R-SKL-23](../../design/app-skeleton.md#s-0f1edd606c "container đặt TZ=UTC") *(container đặt TZ=UTC)*
- Khía cạnh: Thời gian
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Nhánh sạch, `pnpm lint` đang đạt.

**Các bước**

1. Tạo file tạm `apps/api/src/core/lint-probe.ts` chứa `Date.now()`, `new Date()` và `new Date('2026-10-29')`.
2. Chạy `pnpm lint`.
   - Mong đợi: có đúng 2 lỗi `no-restricted-syntax`, ở dòng `Date.now()` và dòng `new Date()`. Dòng `new Date('2026-10-29')` không lỗi.
   - 📷 Chụp evidence.
3. Xoá file tạm, rồi chạy lại `pnpm lint`.
   - Mong đợi: không có lỗi, không có warning. File `system-clock.ts` được miễn.

<a id="s-53c1e1ab68"></a>

## P0-SKL-032 browser-worker ghi nhịp sống đều đặn

**Kiểm tra điều gì.** browser-worker ghi khoá nhịp sống vào Redis đều đặn, với thời hạn sống đúng.

- Thiết kế: [R-SKL-18](../../design/app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `redis-cli --scan --pattern 'mio:heartbeat:browser-worker:*'`.
   - Mong đợi: có đúng một khoá, là `<khóa nhịp sống>` của container đang chạy.
   - 📷 Chụp evidence.
2. Chạy `redis-cli TTL <khóa nhịp sống>` mỗi 5 giây trong 1 phút.
   - Mong đợi: giá trị luôn nằm trong khoảng từ 45 đến 60.
   - 📷 Chụp evidence.
3. Chạy `redis-cli GET <khóa nhịp sống>` mỗi 5 giây trong 1 phút.
   - Mong đợi: giá trị đổi khoảng mỗi 15 giây. Giá trị là một thời điểm dạng ISO.
4. Chạy `docker inspect -f '{{.State.Health.Status}}' <container browser-worker>`.
   - Mong đợi: kết quả là `healthy`.

<a id="s-843cfc11a7"></a>

## P0-SKL-033 Khoá nhịp sống hết hạn khi worker dừng; healthcheck chỉ đọc khoá của chính container

**Kiểm tra điều gì.** Healthcheck của browser-worker chỉ đọc khoá nhịp sống của chính container đó. Khi worker dừng, khoá tự hết hạn.

- Thiết kế: [R-SKL-18](../../design/app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*, [R-SKL-31](../../design/app-skeleton.md#s-0f1edd606c "healthcheck và khởi động lại trong Compose") *(healthcheck và khởi động lại trong Compose)*
- Khía cạnh: Thời gian
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Khi worker đang chạy, chạy `docker compose exec browser-worker node <đường dẫn healthcheck đã build>; echo $?`.
   - Mong đợi: kết quả là `0`.
2. Vẫn khi worker đang chạy, chạy `docker compose run --rm --no-deps --entrypoint node browser-worker <đường dẫn healthcheck>; echo $?`. Lệnh này tạo một container mới, không chạy worker và có hostname khác.
   - Mong đợi: kết quả là `1`, dù khoá của worker đang chạy vẫn còn.
   - 📷 Chụp evidence.
3. Chạy `docker compose stop browser-worker` và ghi lại thời điểm dừng. Chạy `redis-cli EXISTS <khóa nhịp sống>` mỗi 5 giây.
   - Mong đợi: kết quả về `0` trong vòng 60 giây sau thời điểm dừng.
   - 📷 Chụp evidence.
4. Chạy `docker compose start browser-worker`.
   - Mong đợi: khoá với cùng hostname xuất hiện lại. Container ở trạng thái `healthy`.

<a id="s-f8ea86b185"></a>

## P0-SKL-034 Dừng bình thường khi không có job

**Kiểm tra điều gì.** Khi không có job, api và browser-worker dừng nhanh và sạch. Node chạy trực tiếp với vai trò PID 1 trong container.

- Thiết kế: [R-SKL-22](../../design/app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*; mục Tham số (thời gian ân hạn)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy, không có job.

**Các bước**

1. Chạy `docker compose config`.
   - Mong đợi: `stop_grace_period` của api là 30s, của browser-worker là 2m.
2. Chạy `docker compose exec api sh -c "tr '\0' ' ' < /proc/1/cmdline"`, rồi lặp lại với browser-worker.
   - Mong đợi: kết quả bắt đầu bằng `node`. Node là PID 1, không chạy qua `pnpm` hay `sh`.
   - 📷 Chụp evidence.
3. Chạy `docker compose stop api browser-worker`.
   - Mong đợi: mỗi container dừng trong vài giây, không chờ hết thời gian ân hạn.
4. Chạy `docker inspect -f '{{.State.ExitCode}}'` cho hai container.
   - Mong đợi: kết quả là `0`. Phần log cuối không có lỗi.
   - 📷 Chụp evidence.

<a id="s-79129f312b"></a>

## P0-SKL-035 Lệnh CLI: help và lệnh không tồn tại

**Kiểm tra điều gì.** CLI của api có lệnh `help` và báo lỗi rõ khi gọi lệnh không tồn tại. CLI không mở cổng HTTP.

- Thiết kế: mục `apps/api` › `cli.ts`
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy, api đang giữ cổng 3000.

**Các bước**

1. Chạy `docker compose exec api node dist/cli.js help; echo $?`.
   - Mong đợi: in danh sách lệnh, trong đó có `help`. Mã thoát là `0`. Không có lỗi `EADDRINUSE`, vì CLI không mở HTTP.
   - 📷 Chụp evidence.
2. Chạy `docker compose exec api node dist/cli.js khong-co; echo $?`.
   - Mong đợi: in "Lệnh không tồn tại: khong-co. Chạy help để xem danh sách." Mã thoát là `1`.
   - 📷 Chụp evidence.

<a id="s-0fcb6f201f"></a>

## P0-SKL-036 Redis bật AOF, noeviction, giữ dữ liệu khi bị dừng cứng

**Kiểm tra điều gì.** Redis bật AOF và dùng chính sách `noeviction`. Dữ liệu trong Redis còn nguyên sau khi Redis bị dừng cứng hoặc container bị tạo lại.

- Thiết kế: [R-SKL-27](../../design/app-skeleton.md#s-0f1edd606c "Redis bật AOF và maxmemory-policy noeviction") *(Redis bật AOF và maxmemory-policy noeviction)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.

**Các bước**

1. Chạy `redis-cli CONFIG GET appendonly` và `CONFIG GET maxmemory-policy`.
   - Mong đợi: lần lượt là `yes` và `noeviction`.
   - 📷 Chụp evidence.
2. Chạy `redis-cli SET mio:test:aof 1` và chờ 2 giây. Dừng cứng Redis bằng `docker kill <container redis>`, tức Redis không được lưu khi tắt. Chạy `docker compose up -d redis`.
   - Mong đợi: `GET mio:test:aof` trả `1`.
   - 📷 Chụp evidence.
3. Chạy `docker compose down` (không có `-v`), rồi chạy `docker compose up -d`.
   - Mong đợi: `GET mio:test:aof` vẫn trả `1`.
   - Dọn dẹp: xoá khoá thử.

<a id="s-6dc6f07c19"></a>

## P0-SKL-037 Hàng đợi đăng ký đúng tên, global concurrency 1

**Kiểm tra điều gì.** Hàng đợi `fb-browser` được đăng ký với global concurrency 1. Giai đoạn 0 chưa đăng ký `fb-inbox` và `render`. Tên hàng đợi chỉ được khai báo ở một chỗ.

- Thiết kế: [R-SKL-05](../../design/app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)*, [R-SKL-06](../../design/app-skeleton.md#s-0f1edd606c "tên hàng đợi chỉ lấy từ QUEUE_NAMES") *(tên hàng đợi chỉ lấy từ QUEUE\_NAMES)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `redis-cli HGET bull:fb-browser:meta concurrency`.
   - Mong đợi: kết quả là `1`.
   - 📷 Chụp evidence.
2. Chạy `redis-cli --scan --pattern 'bull:fb-inbox:*'` và `--pattern 'bull:render:*'`.
   - Mong đợi: không có khoá nào, vì giai đoạn 0 chưa đăng ký hai hàng đợi này.
3. Chạy `git grep -nE "'(fb-browser|fb-inbox|render|fb-browser-results|fb-inbox-results|ai-text|ai-image|messenger|page-publish)'" -- apps packages ':!apps/*/test'`.
   - Mong đợi: tên hàng đợi chỉ xuất hiện trong file khai báo `QUEUE_NAMES` của `@mio/shared`.
   - 📷 Chụp evidence.

<a id="s-5676b654ee"></a>

## P0-SKL-038 Build image đa kiến trúc và chạy được trên arm64

**Kiểm tra điều gì.** Image build được cho cả `linux/amd64` và `linux/arm64`, và chạy được trên arm64. Cấu hình build không gắn cứng vào một máy cụ thể.

- Thiết kế: [R-SKL-21](../../design/app-skeleton.md#s-0f1edd606c "image api và browser-worker build được cho linux/amd64 và l…") *(image api và browser-worker build được cho linux/amd64 và l…)*; mục Build đa kiến trúc; [ADR 0014](../../../../decisions/0014-browser-worker-playwright-image.md "browser-worker dùng image Playwright chính thức kèm Node củ…") *(browser-worker dùng image Playwright chính thức kèm Node củ…)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Docker Desktop có buildx và QEMU.

**Các bước**

1. Chạy `pnpm docker:build:multiarch`.
   - Mong đợi: target `api` và `browser-worker` build xong cho `linux/amd64` và `linux/arm64`.
   - 📷 Chụp evidence.
2. Build image arm64 của từng target vào Docker local, rồi chạy `docker run --rm --platform linux/arm64 <image> node --version`.
   - Mong đợi: api in `v26.x.x`. browser-worker in đúng phiên bản Node của image Playwright ghi trong `plan.md`.
   - 📷 Chụp evidence.
3. Xem dòng `FROM` trong `apps/*/Dockerfile`. Chạy `docker buildx imagetools inspect` cho từng base image.
   - Mong đợi: dòng `FROM` chỉ dùng `node:26-bookworm-slim` và `mcr.microsoft.com/playwright:v1.63.0-noble`, hoặc bản vá cùng dòng ghi trong `plan.md`. Mỗi base image có cả `linux/amd64` và `linux/arm64`.
4. Tìm trong `compose.yml`, `apps/*/Dockerfile`, `docker-bake.hcl` các mục sau: đường dẫn ổ đĩa của máy (`D:\`, `C:\`, `/home/…`), IP cố định, `platform:` ghi cứng.
   - Mong đợi: không có mục nào.

<a id="s-908a22103a"></a>

## P0-SKL-039 Chuyển máy chỉ bằng biến môi trường và volume

**Kiểm tra điều gì.** Chuyển hệ thống sang máy khác chỉ cần đổi biến môi trường và volume. Không phải sửa code hay cấu hình.

- Thiết kế: [R-SKL-20](../../design/app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*, [R-SKL-21](../../design/app-skeleton.md#s-0f1edd606c "image api và browser-worker build được cho linux/amd64 và l…") *(image api và browser-worker build được cho linux/amd64 và l…)*; [ADR 0009](../../../../decisions/0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*, [ADR 0013](../../../../decisions/0013-browser-profile-named-volume.md "Profile trình duyệt nằm trong named volume riêng") *(Profile trình duyệt nằm trong named volume riêng)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang dừng.
- `git status` sạch.

**Các bước**

1. Sửa `.env`: đổi `MIO_DATA_DIR` sang một thư mục trống khác và đặt `MIO_PUBLIC_URL=http://127.0.0.1:3000`.
2. Chạy `docker compose up -d`.
   - Mong đợi: 4 dịch vụ healthy. Thư mục mới có `images/` và `debug-dumps/`. Volume `mio-browser-profile` không đổi, nên phiên Facebook được giữ nguyên.
   - 📷 Chụp evidence.
3. Chạy `git status`.
   - Mong đợi: không có file code, Dockerfile hay `compose.yml` nào bị sửa.
   - Dọn dẹp: trả lại `.env`.

<a id="s-3cac25e098"></a>

## P0-SKL-040 Đo RAM/CPU: ghi CSV theo chu kỳ

**Kiểm tra điều gì.** Script đo RAM/CPU ghi số liệu của các container trong app ra file CSV theo chu kỳ. Script bỏ qua container ngoài project.

- Thiết kế: [R-SKL-24](../../design/app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*; mục Đo RAM/CPU từng container
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy với 4 container.
- Chạy thêm một container ngoài project bằng `docker run -d --name skl-probe redis:8-alpine`.

**Các bước**

1. Chạy `py tools/ops/container_stats.py record --interval 10 --out .local/metrics/skl-040.csv`. Để chạy khoảng 65 giây rồi bấm Ctrl+C.
   - Mong đợi: script thoát gọn, không in traceback.
2. Mở file CSV.
   - Mong đợi: dòng đầu đúng là `time,container,cpu_percent,mem_bytes,mem_limit_bytes`. Mỗi chu kỳ có một dòng cho mỗi container của app, tổng cộng khoảng 6 đến 7 chu kỳ nhân 4 container. Chu kỳ đầu được lấy ngay khi bắt đầu. Không có dòng nào của `skl-probe` hay container khác. Dòng cuối đầy đủ.
   - 📷 Chụp evidence.
3. Kiểm tra dữ liệu từng cột.
   - Mong đợi: cột `time` là thời điểm ISO UTC. `cpu_percent`, `mem_bytes`, `mem_limit_bytes` là số. `mem_bytes` không lớn hơn `mem_limit_bytes`. Tên container có tiền tố project, ví dụ `mio-api-1`.
4. Dọn dẹp: chạy `docker rm -f skl-probe`.

<a id="s-2069f058f4"></a>

## P0-SKL-041 Đo RAM/CPU: ghi nối tiếp và tổng hợp

**Kiểm tra điều gì.** Script đo ghi nối tiếp vào file CSV có sẵn mà không làm hỏng dữ liệu cũ. Lệnh tổng hợp tính đúng số liệu của từng container.

- Thiết kế: [R-SKL-24](../../design/app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có file của [P0-SKL-040](#s-3cac25e098 "Đo RAM/CPU: ghi CSV theo chu kỳ") *(Đo RAM/CPU: ghi CSV theo chu kỳ)*.

**Các bước**

1. Chạy `record` thêm khoảng 30 giây vào cùng file.
   - Mong đợi: số dòng tăng. Dòng tiêu đề chỉ xuất hiện một lần. Các dòng cũ giữ nguyên.
2. Chạy `py tools/ops/container_stats.py summary .local/metrics/skl-040.csv`.
   - Mong đợi: mỗi container có một dòng gồm số mẫu, CPU trung bình, CPU lớn nhất, RAM trung bình, RAM lớn nhất (MiB).
   - 📷 Chụp evidence.
3. Tự tính lại từ CSV bằng Python.
   - Mong đợi: kết quả khớp với bảng tổng hợp, sai số làm tròn không quá 0,1.

<a id="s-86263041a9"></a>

## P0-SKL-042 Đo RAM/CPU khi Docker không chạy

**Kiểm tra điều gì.** Khi Docker không chạy, script đo báo lỗi rõ và không động vào file CSV có sẵn.

- Thiết kế: [R-SKL-24](../../design/app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Tắt Docker Desktop.
- Có file CSV của [P0-SKL-041](#s-2069f058f4 "Đo RAM/CPU: ghi nối tiếp và tổng hợp") *(Đo RAM/CPU: ghi nối tiếp và tổng hợp)*.

**Các bước**

1. Chạy `py tools/ops/container_stats.py record --out .local/metrics/skl-040.csv; echo $?`.
   - Mong đợi: in "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại." Mã thoát là `1`.
   - 📷 Chụp evidence.
2. Kiểm tra file CSV.
   - Mong đợi: file không đổi, cùng số dòng và cùng thời điểm sửa.

<a id="s-0b48d5de17"></a>

## P0-SKL-043 `pnpm test:int` khi Docker không chạy thì fail, không skip

**Kiểm tra điều gì.** Khi Docker không chạy, `pnpm test:int` fail với thông báo rõ thay vì skip test. `pnpm test` vẫn chạy được.

- Thiết kế: [R-SKL-25](../../design/app-skeleton.md#s-0f1edd606c "pnpm test") *(pnpm test)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Tắt Docker Desktop.

**Các bước**

1. Chạy `pnpm test:int; echo $?`.
   - Mong đợi: in "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại." Mã thoát khác `0`.
   - 📷 Chụp evidence.
2. Đọc kết quả.
   - Mong đợi: không có dòng nào báo test passed hay skipped.
3. Chạy `pnpm test`.
   - Mong đợi: lệnh vẫn chạy và đạt, vì unit test và contract test không cần Docker.

<a id="s-ce94844341"></a>

## P0-SKL-044 Testcontainers dùng cùng image với compose.yml

**Kiểm tra điều gì.** Testcontainers dùng đúng image PostgreSQL và Redis khai báo trong `compose.yml`. Mỗi tag image chỉ được khai báo ở một chỗ.

- Thiết kế: [R-SKL-25](../../design/app-skeleton.md#s-0f1edd606c "pnpm test") *(pnpm test)*; mục Tham số (phiên bản hạ tầng)
- Khía cạnh: Regression
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Docker Desktop đang chạy.

**Các bước**

1. Chạy `docker compose config --images` và ghi lại image của `postgres`, `redis`.
2. Chạy `pnpm test:int`. Trong lúc test chạy, chạy `docker ps --format '{{.Image}}'`.
   - Mong đợi: container của Testcontainers dùng đúng hai image ở bước 1.
   - 📷 Chụp evidence.
3. Chạy `git grep -n "postgres:18\|redis:8"` trong code và cấu hình, bỏ qua `docs/`.
   - Mong đợi: mỗi tag chỉ được khai báo ở một chỗ.

<a id="s-7e75a05b62"></a>

## P0-SKL-045 Khoá cài đặt chưa có bản ghi trả giá trị mặc định

**Kiểm tra điều gì.** Khi khoá cài đặt chưa có bản ghi trong DB, API trả giá trị mặc định. Việc đọc không ghi gì vào DB.

- Thiết kế: [R-SKL-09](../../design/app-skeleton.md#s-0f1edd606c "khóa chưa có bản ghi trong DB") *(khóa chưa có bản ghi trong DB)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: phân vùng tương đương
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `crawl-settings` và `auth`.
- Đang có phiên Quản lý.
- Chạy `delete from app_settings where key = 'crawl-schedule'`.

**Các bước**

1. Gọi `GET /api/v1/settings/crawl-schedule`.
   - Mong đợi: trả 200, thân bằng giá trị mặc định khai báo trong `SETTINGS`.
   - 📷 Chụp evidence.
2. Chạy `select count(*) from app_settings where key = 'crawl-schedule'`.
   - Mong đợi: kết quả là `0`, tức việc đọc không ghi vào DB.
   - 📷 Chụp evidence.

<a id="s-b548d2ba78"></a>

## P0-SKL-046 Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục

**Kiểm tra điều gì.** Lần ghi cài đặt hợp lệ đầu tiên tạo một bản ghi. Lần ghi sau thay toàn bộ giá trị cũ và cập nhật thời điểm sửa.

- Thiết kế: [R-SKL-11](../../design/app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*; `db-schema.md` Quy ước chung (`CLOCK`)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: chuyển trạng thái (chưa có bản ghi, có bản ghi, cập nhật)
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-045](#s-7e75a05b62 "Khóa cài đặt chưa có bản ghi trả giá trị mặc định") *(Khóa cài đặt chưa có bản ghi trả giá trị mặc định)*.

**Các bước**

1. Gọi `PUT /api/v1/settings/crawl-schedule` với giá trị hợp lệ A (`maxScrolls: 10`).
   - Mong đợi: trả 200, thân bằng A. DB có 1 dòng với `value` bằng A. `created_at` bằng đúng `updated_at` và gần giờ hiện tại.
   - 📷 Chụp evidence.
2. Gọi `PUT` với giá trị hợp lệ B (`maxScrolls: 12`, các trường khác cũng đổi).
   - Mong đợi: trả 200. DB vẫn có 1 dòng, `value` bằng toàn bộ B, không còn trường nào của A. `updated_at` mới hơn bước 1. `created_at` không đổi.
   - 📷 Chụp evidence.

<a id="s-a30d1e815a"></a>

## P0-SKL-047 Sửa cài đặt trong DB có hiệu lực ngay, không cần khởi động lại

**Kiểm tra điều gì.** Sửa cài đặt trực tiếp trong DB có hiệu lực ngay. Không cần khởi động lại api.

- Thiết kế: [R-SKL-08](../../design/app-skeleton.md#s-0f1edd606c "SettingsService") *(SettingsService)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.

**Các bước**

1. Chạy `update app_settings set value = jsonb_set(value, '{maxScrolls}', '15') where key = 'crawl-schedule'`.
2. Gọi `GET /api/v1/settings/crawl-schedule` ngay sau đó.
   - Mong đợi: kết quả có `maxScrolls: 15`. `RestartCount` và `StartedAt` của api không đổi.
   - 📷 Chụp evidence.

<a id="s-808ee36bcc"></a>

## P0-SKL-048 Ghi cài đặt sai schema thì báo lỗi theo trường, không ghi DB

**Kiểm tra điều gì.** Ghi cài đặt sai schema thì API trả 400 kèm lỗi theo từng trường. DB không bị thay đổi.

- Thiết kế: [R-SKL-11](../../design/app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.
- Ghi lại `value` và `updated_at` hiện tại.

**Các bước**

1. Gọi `PUT` với `maxScrolls: 21`.
   - Mong đợi: trả 400, thân là `{"code":"VALIDATION_ERROR","message":"Dữ liệu cài đặt không hợp lệ","fields":{"maxScrolls":"<thông báo của schema>"}}`.
   - 📷 Chụp evidence.
2. Gọi `PUT` với `maxScrolls: "abc"`.
   - Mong đợi: trả 400 `VALIDATION_ERROR`. `fields.maxScrolls` có thông báo.
3. Gọi `PUT` với thân `{}`.
   - Mong đợi: trả 400. `fields` liệt kê mọi trường bắt buộc.
4. Gọi `PUT` với thân `[]`, tức không phải object.
   - Mong đợi: trả 400 `VALIDATION_ERROR`. `fields` có khoá `_root`.
5. Kiểm tra DB.
   - Mong đợi: `value` và `updated_at` giống hệt trước bước 1.
   - 📷 Chụp evidence.

<a id="s-de70ed5af5"></a>

## P0-SKL-049 Khoá cài đặt không tồn tại

**Kiểm tra điều gì.** Gọi cài đặt với khoá không tồn tại trả 404 như mọi đường dẫn lạ. DB không có bản ghi nào được tạo.

- Thiết kế: [R-SKL-10](../../design/app-skeleton.md#s-0f1edd606c "get / set với khóa không có trong SETTINGS") *(get / set với khóa không có trong SETTINGS)*, [R-SKL-15](../../design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-045](#s-7e75a05b62 "Khóa cài đặt chưa có bản ghi trả giá trị mặc định") *(Khóa cài đặt chưa có bản ghi trả giá trị mặc định)*.

**Các bước**

1. Gọi `PUT /api/v1/settings/khong-co` với thân bất kỳ. Sau đó gọi `GET` cùng địa chỉ.
   - Mong đợi: cả hai trả 404, thân đúng là `{"code":"NOT_FOUND","message":"Không tìm thấy địa chỉ yêu cầu"}`. Khoá lạ không có route.
   - 📷 Chụp evidence.
2. Chạy `select count(*) from app_settings where key = 'khong-co'`.
   - Mong đợi: kết quả là `0`.

<a id="s-733c5fb69f"></a>

## P0-SKL-050 Giá trị đang lưu sai một trường thì báo 409, không dùng mặc định

**Kiểm tra điều gì.** Khi giá trị đang lưu sai một trường, API trả 409 nêu rõ trường sai. API không thay bằng giá trị mặc định. Lỗi được ghi vào log.

- Thiết kế: [R-SKL-12](../../design/app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.

**Các bước**

1. Chạy `update app_settings set value = jsonb_set(value, '{maxScrolls}', '25') where key = 'crawl-schedule'`.
2. Gọi `GET /api/v1/settings/crawl-schedule`.
   - Mong đợi: trả 409, thân là `{"code":"INVALID_STORED_SETTING","message":"Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)","fields":{"maxScrolls":"phải từ 1 đến 20"}}`. API không trả giá trị mặc định.
   - 📷 Chụp evidence.
3. Đọc log api.
   - Mong đợi: có một dòng mức error chứa thông báo trên, `key: "crawl-schedule"` và danh sách `[{ path: "maxScrolls", reason: "phải từ 1 đến 20", storedValue: 25 }]`.
   - 📷 Chụp evidence.
4. Gọi `PUT` với một giá trị không hợp lệ khác (`maxScrolls: 21`).
   - Mong đợi: trả 400 `VALIDATION_ERROR`. DB vẫn lưu `25`.

<a id="s-80c5c4bf4c"></a>

## P0-SKL-051 Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài

**Kiểm tra điều gì.** Khi giá trị đang lưu sai nhiều trường, thông báo 409 liệt kê đủ các trường sai. Giá trị đang lưu quá dài chỉ được in 100 ký tự đầu.

- Thiết kế: [R-SKL-12](../../design/app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.
- Schema `crawl-schedule` có `goldenHours` là mảng ít nhất 2 phần tử.

**Các bước**

1. Dùng SQL sửa giá trị đang lưu:
   - đặt `maxScrolls = 25`;
   - xoá một trường bắt buộc `<A>`;
   - đặt `goldenHours[1].end` là chuỗi 99 ký tự. Khi tính cả ngoặc kép, chuỗi JSON dài 101 ký tự.
2. Gọi `GET`.
   - Mong đợi: trả 409. `message` liệt kê đủ 3 trường, ngăn cách bằng "; ". Ba phần lần lượt là `maxScrolls: … (đang lưu: 25)`, `<A>: … (đang lưu: không có)` và `goldenHours[1].end: … (đang lưu: <100 ký tự đầu của chuỗi JSON, bắt đầu bằng ngoặc kép>…)`. `fields` có đủ 3 khoá.
   - 📷 Chụp evidence.
3. Đổi `goldenHours[1].end` thành chuỗi 98 ký tự. Khi đó chuỗi JSON dài đúng 100 ký tự và vẫn sai định dạng.
   - Mong đợi: phần "đang lưu" in đủ chuỗi JSON, có ngoặc kép ở hai đầu, không có "…".
   - 📷 Chụp evidence.

<a id="s-d85299aeac"></a>

## P0-SKL-052 Ghi giá trị hợp lệ sau lỗi 409 thì hết lỗi

**Kiểm tra điều gì.** Sau lỗi 409, ghi một giá trị hợp lệ thì lỗi hết. API đọc lại cài đặt bình thường.

- Thiết kế: [R-SKL-12](../../design/app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*
- Khía cạnh: Chuyển trạng thái
- Kỹ thuật: chuyển trạng thái (lưu hỏng sang lưu hợp lệ)
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã chạy xong [P0-SKL-050](#s-733c5fb69f "Giá trị đang lưu sai một trường thì báo 409, không dùng mặc…") *(Giá trị đang lưu sai một trường thì báo 409, không dùng mặc…)*, DB đang lưu `maxScrolls: 25`.

**Các bước**

1. Gọi `PUT` với giá trị hợp lệ (`maxScrolls: 10`).
   - Mong đợi: trả 200.
   - 📷 Chụp evidence.
2. Gọi `GET`.
   - Mong đợi: trả 200 với `maxScrolls: 10`. `value` trong DB đúng giá trị mới.

<a id="s-8e1b9b6483"></a>

## P0-SKL-053 Hai lần ghi cài đặt cùng lúc

**Kiểm tra điều gì.** Hai lần ghi cài đặt cùng lúc không gây lỗi và không trộn giá trị của hai bên. Lần ghi sau thắng.

- Thiết kế: [R-SKL-11](../../design/app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*; mục Đọc / ghi cài đặt (ghi sau thắng)
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)*.

**Các bước**

1. Gửi song song hai `PUT`: giá trị A (`maxScrolls: 5`) và giá trị B (`maxScrolls: 7`). A và B khác nhau ở mọi trường.
   - Mong đợi: cả hai trả 200, không có 500.
2. Kiểm tra DB.
   - Mong đợi: có đúng 1 dòng `crawl-schedule`. `value` bằng trọn A hoặc trọn B, không trộn trường của hai bên.
   - 📷 Chụp evidence.
3. Gọi `GET`.
   - Mong đợi: kết quả bằng giá trị trong DB.

<a id="s-3da8871ae5"></a>

## P0-SKL-054 Lỗi không lường trước trả 500 không lộ chi tiết

**Kiểm tra điều gì.** Lỗi không lường trước trả 500 với thông báo chung, không lộ chi tiết. Log vẫn ghi đủ lỗi gốc.

- Thiết kế: [R-SKL-16](../../design/app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-045](#s-7e75a05b62 "Khóa cài đặt chưa có bản ghi trả giá trị mặc định") *(Khóa cài đặt chưa có bản ghi trả giá trị mặc định)*.

**Các bước**

1. Chạy `alter table app_settings rename to app_settings_bak`.
2. Gọi `GET /api/v1/settings/crawl-schedule`.
   - Mong đợi: trả 500, thân đúng là `{"code":"INTERNAL_ERROR","message":"Lỗi hệ thống, vui lòng thử lại sau"}`. Không có stack, tên bảng hay câu SQL.
   - 📷 Chụp evidence.
3. Đọc log api.
   - Mong đợi: có dòng mức error với `requestId` và lỗi gốc đầy đủ, nêu quan hệ `app_settings` không tồn tại.
   - 📷 Chụp evidence.
4. Chạy `alter table app_settings_bak rename to app_settings`.
   - Mong đợi: `GET` trả 200.

<a id="s-e0eb883363"></a>

## P0-SKL-055 DB có dòng khoá cài đặt lạ

**Kiểm tra điều gì.** Dòng có khoá cài đặt lạ trong DB không làm hỏng việc đọc cài đặt hay việc khởi động api.

- Thiết kế: [R-SKL-08](../../design/app-skeleton.md#s-0f1edd606c "SettingsService") *(SettingsService)*, [R-SKL-09](../../design/app-skeleton.md#s-0f1edd606c "khóa chưa có bản ghi trong DB") *(khóa chưa có bản ghi trong DB)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: thấp
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-045](#s-7e75a05b62 "Khóa cài đặt chưa có bản ghi trả giá trị mặc định") *(Khóa cài đặt chưa có bản ghi trả giá trị mặc định)*.

**Các bước**

1. Chạy `insert into app_settings (key, value) values ('old-key', '{"a":1}')`.
2. Gọi `GET /api/v1/settings/crawl-schedule`.
   - Mong đợi: trả 200 bình thường.
   - 📷 Chụp evidence.
3. Chạy `docker compose restart api`.
   - Mong đợi: api healthy, log không có lỗi.
   - Dọn dẹp: xoá dòng `old-key`.

<a id="s-73919d3075"></a>

## P0-SKL-056 Kết quả job trình duyệt đi qua hàng đợi kết quả

**Kiểm tra điều gì.** Kết quả của job trình duyệt được gửi về qua hàng đợi kết quả. Kết quả được ghi vào DB đúng một lần.

- Thiết kế: [R-SKL-28](../../design/app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)*; mục Job và hàng đợi (chiều dữ liệu)
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Có ít nhất một job quét đã chạy xong thành công. Biết `<id>` của job gốc.

**Các bước**

1. Chạy `redis-cli HGETALL bull:fb-browser-results:<id>-result`.
   - Mong đợi: job tồn tại. `data` có `sourceJobId = <id>`, `sourceJobName` đúng tên job, `outcome: "ok"` và có `data`. Không có `error`.
   - 📷 Chụp evidence.
2. Kiểm tra DB của tính năng.
   - Mong đợi: kết quả quét được ghi đúng một lần cho `<id>`.

<a id="s-a8527a39a1"></a>

## P0-SKL-057 Tuỳ chọn job mặc định

**Kiểm tra điều gì.** Job dùng đúng tuỳ chọn mặc định về số lần thử và số job được giữ lại.

- Thiết kế: [R-SKL-07](../../design/app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*
- Khía cạnh: Logic nghiệp vụ
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-056](#s-73919d3075 "Kết quả job trình duyệt đi qua hàng đợi kết quả") *(Kết quả job trình duyệt đi qua hàng đợi kết quả)*.

**Các bước**

1. Chạy `redis-cli HGET bull:fb-browser:<id> opts`.
   - Mong đợi: `attempts` là 1, `removeOnComplete` là `{count: 1000}`, `removeOnFail` là `{count: 5000}`. Ngoại lệ là khi `group-crawl-job` khai báo khác trong thiết kế.
   - 📷 Chụp evidence.
2. Lặp lại với job `bull:fb-browser-results:<id>-result`.
   - Mong đợi: cùng giá trị.

<a id="s-d9052f5a3d"></a>

## P0-SKL-058 Hai tiến trình browser-worker vẫn chỉ chạy một job fb-browser cùng lúc

**Kiểm tra điều gì.** Khi chạy hai tiến trình browser-worker, hàng đợi `fb-browser` vẫn chỉ chạy một job tại một thời điểm.

- Thiết kế: [R-SKL-05](../../design/app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)*
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Có ít nhất 3 job quét đang chờ trong `fb-browser`.

**Các bước**

1. Chạy `docker compose up -d --scale browser-worker=2`.
   - Mong đợi: 2 container browser-worker healthy.
2. Đọc `redis-cli LLEN bull:fb-browser:active` mỗi giây cho tới khi hết job.
   - Mong đợi: không lần nào lớn hơn `1`.
   - 📷 Chụp evidence.
3. Đọc log của hai worker.
   - Mong đợi: khoảng thời gian (bắt đầu, kết thúc) của các job không chồng nhau. Cả hai worker đều có thể nhận job.
   - 📷 Chụp evidence.
4. Dọn dẹp: chạy `docker compose up -d --scale browser-worker=1`.

<a id="s-c894b22d36"></a>

## P0-SKL-059 Dừng browser-worker khi đang có job thì chờ job xong

**Kiểm tra điều gì.** Khi dừng browser-worker lúc đang có job, worker chờ job hiện tại chạy xong. Worker không nhận thêm job mới.

- Thiết kế: [R-SKL-22](../../design/app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Một job quét đang chạy và ngắn hơn 120 giây.
- Còn ít nhất một job đang chờ.

**Các bước**

1. Chạy `docker compose stop browser-worker` khi job đang chạy.
   - Mong đợi: container chưa dừng ngay mà chờ job xong.
   - 📷 Chụp evidence.
2. Kiểm tra trạng thái các job.
   - Mong đợi: job đang chạy chuyển sang `completed` và có job kết quả `<id>-result`. Job đang chờ vẫn ở `wait`, không được bắt đầu.
   - 📷 Chụp evidence.
3. Xem `ExitCode` của container.
   - Mong đợi: kết quả là `0`.

<a id="s-2c9a4efd46"></a>

## P0-SKL-060 Quá thời gian ân hạn: job dở dang thất bại, không chạy lại

**Kiểm tra điều gì.** Khi quá thời gian ân hạn, job dở dang bị ghi thất bại với `WorkerCrashedError`. Job đó không được chạy lại.

- Thiết kế: [R-SKL-22](../../design/app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*, [R-SKL-29](../../design/app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*, [R-SKL-07](../../design/app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Một job quét đang chạy và còn hơn 5 giây nữa mới xong. Biết `<id>` của job này.

**Các bước**

1. Chạy `docker compose stop -t 5 browser-worker`.
   - Mong đợi: container bị dừng cứng sau 5 giây, `ExitCode` là 137.
2. Chạy `docker compose start browser-worker` và chờ tối đa 2 phút.
   - Mong đợi: job `<id>` ở trạng thái `failed`, tức `ZSCORE bull:fb-browser:failed <id>` có giá trị. Log worker không có lần bắt đầu thứ hai cho `<id>`.
   - 📷 Chụp evidence.
3. Kiểm tra DB của tính năng.
   - Mong đợi: lượt quét của `<id>` được ghi thất bại với loại lỗi `WorkerCrashedError`. Bảng và cột theo thiết kế `group-crawl-job`. Chỉ có một bản ghi.
   - 📷 Chụp evidence.

<a id="s-43c4e46785"></a>

## P0-SKL-061 Một worker chết giữa job, worker còn lại không chạy lại job đó

**Kiểm tra điều gì.** Khi một worker chết giữa job, worker còn lại không chạy lại job đó. Job được ghi thất bại đúng một lần.

- Thiết kế: [R-SKL-29](../../design/app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*, [R-SKL-07](../../design/app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Hệ thống chạy với `--scale browser-worker=2`.
- Một job quét đang chạy trên worker 1. Biết `<id>` của job này.

**Các bước**

1. Chạy `docker kill <container worker 1>` khi job đang chạy.
2. Chờ tối đa 2 phút.
   - Mong đợi: job `<id>` chuyển sang `failed`. Log worker 2 không có lần bắt đầu `<id>`.
   - 📷 Chụp evidence.
3. Kiểm tra DB của tính năng.
   - Mong đợi: lượt quét `<id>` thất bại với `WorkerCrashedError`, đúng một bản ghi. Các job đang chờ khác vẫn được worker 2 xử lý bình thường.
   - 📷 Chụp evidence.

<a id="s-c907c0427c"></a>

## P0-SKL-062 Job kết quả sai cấu trúc

**Kiểm tra điều gì.** Job kết quả sai cấu trúc bị đánh dấu thất bại và được ghi log. Job này không tạo bản ghi nào trong DB và không làm api ngừng hoạt động.

- Thiết kế: [R-SKL-28](../../design/app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Có một script ngoài app (Node và `bullmq`) thêm được job vào `fb-browser-results`.

**Các bước**

1. Thêm job `jobId = probe-1-result` với data `{ "sourceJobId": "probe-1", "sourceJobName": "<tên job quét>" }`. Data này thiếu `outcome`.
   - Mong đợi: job chuyển sang `failed`. `failedReason` nêu lỗi cấu trúc.
   - 📷 Chụp evidence.
2. Đọc log api.
   - Mong đợi: có dòng mức error với `sourceJobId: "probe-1"`.
   - 📷 Chụp evidence.
3. Thêm job `probe-2-result` với `outcome: "failed"` nhưng không có `error`.
   - Mong đợi: job cũng chuyển sang `failed`. Log có `probe-2`.
4. Kiểm tra DB của tính năng.
   - Mong đợi: không có bản ghi nào cho `probe-1`, `probe-2`. api vẫn healthy.

<a id="s-185c6f05a5"></a>

## P0-SKL-063 Job đọc cài đặt hỏng thì thất bại với đúng thông báo

**Kiểm tra điều gì.** Job đọc phải cài đặt hỏng thì thất bại với đúng thông báo. App không quét bằng giá trị mặc định.

- Thiết kế: [R-SKL-12](../../design/app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `crawl-settings` và `group-crawl-job`.
- DB lưu `crawl-schedule` với `maxScrolls: 25`.

**Các bước**

1. Chờ hoặc kích hoạt lượt quét kế tiếp.
   - Mong đợi: job thất bại với lý do đúng là "Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)".
   - 📷 Chụp evidence.
2. Kiểm tra hàng đợi.
   - Mong đợi: app không quét bằng giá trị mặc định. Không có job `fb-browser` nào được thêm với `maxScrolls` mặc định.
3. Gọi `PUT` với giá trị hợp lệ.
   - Mong đợi: lượt quét kế tiếp chạy bình thường.

<a id="s-49762e0a06"></a>

## P0-SKL-064 api dừng khi worker đang trả kết quả: kết quả không mất, xử lý một lần

**Kiểm tra điều gì.** Nếu api dừng lúc worker đang trả kết quả, kết quả vẫn nằm trong Redis. Khi api chạy lại, kết quả được xử lý đúng một lần.

- Thiết kế: [R-SKL-28](../../design/app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)*; mục Job và hàng đợi (kết quả nằm trong Redis)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Một job quét đang chạy. Biết `<id>` của job này.

**Các bước**

1. Chạy `docker compose stop api` khi job đang chạy.
   - Mong đợi: worker vẫn chạy và job chạy xong. `bull:fb-browser-results:<id>-result` ở trạng thái `wait`.
   - 📷 Chụp evidence.
2. Chạy `docker compose start api`.
   - Mong đợi: trong 1 phút, job kết quả chuyển sang `completed`.
3. Kiểm tra DB của tính năng.
   - Mong đợi: kết quả `<id>` được ghi đúng một lần.
   - 📷 Chụp evidence.

<a id="s-352c976967"></a>

## P0-SKL-065 Thân request sai JSON hoặc quá lớn

**Kiểm tra điều gì.** Thân request không phải JSON hợp lệ thì API trả 400. Thân vượt giới hạn kích thước thì API trả 413. Cả hai trường hợp đều không ghi gì vào DB.

- Thiết kế: [R-SKL-15](../../design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên, đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.
- Ghi lại `value` và `updated_at` của `crawl-schedule`.

**Các bước**

1. Gọi `PUT /api/v1/settings/crawl-schedule` với `Content-Type: application/json` và thân `{"maxScrolls":` bị cắt dở.
   - Mong đợi: trả 400, thân đúng là `{"code":"INVALID_JSON","message":"Dữ liệu gửi lên không đúng định dạng JSON"}`. Không có stack.
   - 📷 Chụp evidence.
2. Gọi `PUT` với thân dài 1 048 577 byte. Thân là JSON hợp lệ, có thêm trường lạ chứa chuỗi dài.
   - Mong đợi: trả 413, thân đúng là `{"code":"PAYLOAD_TOO_LARGE","message":"Dữ liệu gửi lên quá lớn"}`.
   - 📷 Chụp evidence.
3. Kiểm tra DB.
   - Mong đợi: `value` và `updated_at` giống hệt trước bước 1.
4. Gọi `PUT` với thân hợp lệ theo schema, thêm trường lạ để thân dài đúng 1 048 576 byte.
   - Mong đợi: không bị 413 mà trả 200. Trường lạ bị bỏ theo [R-SKL-11](../../design/app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*.

<a id="s-81fdea9a0b"></a>

## P0-SKL-066 Hai browser-worker: worker treo không bị worker kia che

**Kiểm tra điều gì.** Khi chạy hai browser-worker, mỗi worker có khoá nhịp sống riêng. Worker bị treo không được khoá của worker kia che đi.

- Thiết kế: [R-SKL-18](../../design/app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*
- Khía cạnh: Thao tác đồng thời
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `docker compose up -d --scale browser-worker=2` và chờ healthy. Chạy `redis-cli --scan --pattern 'mio:heartbeat:browser-worker:*'`.
   - Mong đợi: có đúng 2 khoá, mỗi khoá ứng với hostname của một container.
   - 📷 Chụp evidence.
2. Chạy `docker pause <container worker 1>` để giả lập treo, rồi ghi lại thời điểm.
   - Mong đợi: trong vòng 60 giây, khoá của worker 1 hết hạn. Khoá của worker 2 vẫn được cập nhật mỗi 15 giây.
   - 📷 Chụp evidence.
3. Chạy `docker unpause <container worker 1>`.
   - Mong đợi: khoá của worker 1 xuất hiện lại. Cả hai container đều `healthy`.
4. Dọn dẹp: chạy `docker compose up -d --scale browser-worker=1`.

<a id="s-8ea6efe961"></a>

## P0-SKL-067 Đo RAM/CPU: tham số `--interval`, `--out` và file tổng hợp không tồn tại

**Kiểm tra điều gì.** Script đo chỉ nhận `--interval` là số nguyên từ 5 đến 3600. Khi không truyền `--out`, script tự đặt tên file theo giờ. Lệnh tổng hợp báo lỗi rõ khi file không tồn tại.

- Thiết kế: [R-SKL-24](../../design/app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*; mục Đo RAM/CPU từng container
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy.
- Chưa có `.local/metrics/skl-067.csv`.

**Các bước**

1. Chạy `py tools/ops/container_stats.py record --interval 4 --out .local/metrics/skl-067.csv; echo $?`.
   - Mong đợi: in "--interval phải là số nguyên từ 5 đến 3600". Mã thoát là `2`. Không có file nào được tạo.
   - 📷 Chụp evidence.
2. Lặp lại với `--interval 3601`, `--interval abc`, `--interval 7.5`.
   - Mong đợi: cùng thông báo, mã thoát `2`.
3. Chạy `record --interval 5 --out .local/metrics/skl-067.csv`. Khoảng 12 giây sau, bấm Ctrl+C.
   - Mong đợi: file có 3 chu kỳ dữ liệu, ở giây 0, 5 và 10. Mã thoát là `0`.
4. Chạy `record --interval 3600 --out .local/metrics/skl-067b.csv`. Khoảng 5 giây sau, bấm Ctrl+C.
   - Mong đợi: file có 1 chu kỳ dữ liệu. Mã thoát là `0`.
5. Chạy `record` không có `--interval` và `--out`. Sau khi có chu kỳ đầu, bấm Ctrl+C.
   - Mong đợi: script tạo file `.local/metrics/<YYYY-MM-DD-HHmm>.csv`, tên theo giờ Việt Nam lúc bắt đầu.
   - 📷 Chụp evidence.
6. Chạy `py tools/ops/container_stats.py summary .local/metrics/khong-co.csv; echo $?`.
   - Mong đợi: in "Không tìm thấy file: .local/metrics/khong-co.csv". Mã thoát là `1`.

<a id="s-25d0a70d96"></a>

## P0-SKL-068 Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc

**Kiểm tra điều gì.** Trường lạ trong cài đặt bị bỏ khi ghi qua API. Trường lạ có sẵn trong DB cũng bị bỏ khi đọc ra, không gây lỗi.

- Thiết kế: [R-SKL-11](../../design/app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*
- Khía cạnh: Dữ liệu bất thường trong DB
- Kỹ thuật: đoán lỗi
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Như [P0-SKL-046](#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)* sau bước 2.

**Các bước**

1. Gọi `PUT` với giá trị hợp lệ kèm trường lạ `"foo": 1`.
   - Mong đợi: trả 200. Thân trả về không có `foo`. `value` trong DB cũng không có `foo`.
   - 📷 Chụp evidence.
2. Chạy `update app_settings set value = value || '{"bar": 2}' where key = 'crawl-schedule'`.
3. Gọi `GET /api/v1/settings/crawl-schedule`.
   - Mong đợi: trả 200, không phải 409. Thân không có `bar`.
   - 📷 Chụp evidence.

<a id="s-3c1666c6f9"></a>

## P0-SKL-069 Worker chết khi api đang tắt: job vẫn được ghi thất bại sau khi api chạy lại

**Kiểm tra điều gì.** Nếu worker chết trong lúc api đang tắt, job vẫn được ghi thất bại sau khi api chạy lại. Các lần đối soát định kỳ sau đó không ghi trùng.

- Thiết kế: [R-SKL-29](../../design/app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Đã có `group-crawl-job`.
- Một job quét đang chạy. Biết `<id>` của job này.

**Các bước**

1. Chạy `docker compose stop api`. Khi job vẫn đang chạy, chạy `docker kill <container browser-worker>`.
2. Chạy `docker start <container browser-worker>` trong khi api vẫn tắt. Chờ tối đa 2 phút.
   - Mong đợi: job `<id>` ở trạng thái `failed`, không có lần bắt đầu thứ hai.
   - 📷 Chụp evidence.
3. Chạy `docker compose start api`. Chờ api healthy, rồi chờ thêm 1 phút.
   - Mong đợi: DB của tính năng có lượt quét `<id>` thất bại với `WorkerCrashedError`, đúng một bản ghi.
   - 📷 Chụp evidence.
4. Chạy `docker compose restart api`. Chờ thêm 6 phút để qua ít nhất một lần đối soát định kỳ.
   - Mong đợi: vẫn chỉ có đúng một bản ghi cho `<id>`.
   - 📷 Chụp evidence.

<a id="s-9153860e30"></a>

## P0-SKL-070 Khởi động khi PostgreSQL hoặc Redis chưa sẵn sàng

**Kiểm tra điều gì.** Khi PostgreSQL hoặc Redis chưa sẵn sàng lúc khởi động, tiến trình thử kết nối trong khoảng 30 giây rồi thoát với thông báo rõ. Khi dịch vụ đã sẵn sàng, tiến trình lên lại bình thường.

- Thiết kế: [R-SKL-30](../../design/app-skeleton.md#s-0f1edd606c "kết nối PostgreSQL và Redis") *(kết nối PostgreSQL và Redis)*
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.
- Ghi lại `RestartCount` của api và browser-worker.

**Các bước**

1. Chạy `docker compose stop postgres`, rồi chạy `docker restart <container api>`.
   - Mong đợi: log api có các lần thử kết nối. Khoảng 30 giây sau khi khởi động, log có dòng mức error "Không kết nối được PostgreSQL". Tiến trình thoát mã 1 và `RestartCount` tăng.
   - 📷 Chụp evidence.
2. Chạy `docker compose start postgres`.
   - Mong đợi: ở lần khởi động lại kế tiếp, api healthy và `/api/v1/health` trả 200.
3. Lặp lại bước 1 và bước 2 với `redis`.
   - Mong đợi: thông báo là "Không kết nối được Redis".
   - 📷 Chụp evidence.
4. Chạy `docker compose stop redis`, rồi chạy `docker restart <container browser-worker>`.
   - Mong đợi: khoảng 30 giây sau, log có "Không kết nối được Redis" và tiến trình thoát mã 1.
   - Tiếp theo, chạy `docker compose start redis`.
   - Mong đợi: worker healthy.

<a id="s-63f466f034"></a>

## P0-SKL-071 Cấu hình healthcheck; container unhealthy không bị khởi động lại

**Kiểm tra điều gì.** Healthcheck của 4 container được cấu hình đúng lệnh và tham số. Container ở trạng thái unhealthy không bị khởi động lại.

- Thiết kế: [R-SKL-31](../../design/app-skeleton.md#s-0f1edd606c "healthcheck và khởi động lại trong Compose") *(healthcheck và khởi động lại trong Compose)*; mục Tham số (healthcheck Compose)
- Khía cạnh: Lỗi mạng và lỗi hệ thống bên ngoài
- Kỹ thuật: tình huống thực tế
- Ưu tiên: trung bình
- Regression: không
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.
- Ghi lại `RestartCount` của api.

**Các bước**

1. Chạy `docker inspect -f '{{json .Config.Healthcheck}}'` cho 4 container.
   - Mong đợi: lệnh healthcheck của postgres là `pg_isready -U mio -d mio`, của redis là `redis-cli ping`, của api và browser-worker là `node dist/healthcheck.js`. `Interval` là 10s, `Timeout` là 5s, `Retries` là 3. `StartPeriod` là 60s cho api và 30s cho các dịch vụ khác.
   - 📷 Chụp evidence.
2. Chạy `docker compose stop postgres` và chờ 40 giây.
   - Mong đợi: api ở trạng thái `unhealthy`. Tiến trình api vẫn chạy, `RestartCount` không đổi.
   - 📷 Chụp evidence.
3. Chạy `docker compose start postgres`.
   - Mong đợi: api trở lại `healthy`.

<a id="s-2de6c30b01"></a>

## P0-SKL-072 File tĩnh không lộ file ngoài `apps/web/dist`

**Kiểm tra điều gì.** Phần phục vụ file tĩnh không trả nội dung file nằm ngoài `apps/web/dist`, kể cả khi đường dẫn có `..` hoặc dạng mã hoá của nó.

- Thiết kế: [R-SKL-14](../../design/app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude

**Chuẩn bị**

- Hệ thống đang chạy như [P0-SKL-001](#s-9d0cec4336 "Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose") *(Khởi động toàn bộ hệ thống lần đầu bằng Docker Compose)*.

**Các bước**

1. Chạy `curl -i --path-as-is http://127.0.0.1:3000/../package.json`.
   - Mong đợi: trả 200 với `index.html`, hoặc trả 404. Không trả nội dung `package.json`.
   - 📷 Chụp evidence.
2. Lặp lại với `/%2e%2e/package.json`, `/assets/..%2f..%2fpackage.json`, `/..%5c..%5cpackage.json`.
   - Mong đợi: kết quả giống bước 1.
   - 📷 Chụp evidence.
3. Lặp lại với `/../../../../etc/passwd`, dùng `--path-as-is`.
   - Mong đợi: không trả nội dung `/etc/passwd`.
