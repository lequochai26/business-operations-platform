<!-- src-section: 0b0fa0b228 9d402496485d -->
# 0012 – Log JSON bằng pino (nestjs-pino)

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton (R-SKL-17);
  - mọi app NestJS (`@mio/api`, `@mio/browser-worker`);
  - docs/project/04-technical.md mục 7.

**Tóm tắt.** Mọi app NestJS ghi log dạng JSON một dòng ra stdout bằng nestjs-pino. Lý do là thư viện này có sẵn cơ chế che khoá bí mật, tự gắn ngữ cảnh request và nhẹ cho máy ARM.

<!-- src-section: 0bc81167ac 754274332ec3 -->
## Bối cảnh

- App chạy liên tục trong Docker. Cần đọc log để điều tra lỗi quét, việc tự dừng và đo tài nguyên.
- Log không được chứa khoá bí mật, cookie, mật khẩu hay dữ liệu cá nhân như nội dung bài và tin nhắn của khách.
- Máy đích (Oracle A1) ít tài nguyên, nên log cần nhẹ.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 723a648454 4567230bd42d -->
### A. nestjs-pino (pino), log JSON một dòng ra stdout

**Ưu**

- Nhanh và nhẹ.
- Có `redact` để che bí mật theo đường dẫn khoá.
- Tự gắn `requestId`.
- Log JSON dễ lọc bằng `jq` hoặc đưa vào công cụ log sau này.

**Nhược**

- Thêm hai thư viện.
- Log thô khó đọc bằng mắt khi dev. Lúc dev dùng `pino-pretty` để đọc dễ hơn.

<!-- src-section: 36da071471 2cee0e6b6fdd -->
### B. `ConsoleLogger` có sẵn của NestJS (chế độ `json`)

**Ưu**

- Không thêm thư viện.

**Nhược**

- Không có sẵn cơ chế che khoá bí mật, phải tự viết.
- Không tự gắn ngữ cảnh request.
- Chậm hơn pino.

<!-- src-section: 1fea0098e9 115bd7b3d4eb -->
### C. winston (nest-winston)

**Ưu**

- Nhiều transport, phổ biến.

**Nhược**

- Nặng hơn pino.
- Muốn che bí mật thì phải tự viết format.

<!-- src-section: 254160d409 eedc3784a1d8 -->
## Quyết định

Chọn phương án A.

**Vì sao.** nestjs-pino có sẵn cơ chế che khoá bí mật và ngữ cảnh request. Thư viện này cũng nhẹ, hợp với máy ARM.

<!-- src-section: 58c5fdb1ed 163235f974dd -->
## Hệ quả

**Được**

- Cả api và browser-worker dùng chung một định dạng log.
- Việc che bí mật nằm ở một chỗ.
- Có `requestId` và `jobId` để lần theo một lượt xử lý.

**Mất và rủi ro**

- Thêm phụ thuộc `nestjs-pino`, `pino-http`, và `pino-pretty` ở môi trường dev.
- Danh sách khoá cần che phải được bổ sung mỗi khi có loại bí mật mới.
