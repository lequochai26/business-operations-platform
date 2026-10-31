> Bản đọc sinh từ docs/decisions/0012-structured-logging-pino.md (phiên bản f37b503, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0012 – Log JSON bằng pino (nestjs-pino)

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton ([R-SKL-17](../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*);
  - mọi app NestJS (`@mio/api`, `@mio/browser-worker`);
  - docs/project/04-technical.md mục 7.

**Tóm tắt.** Mọi app NestJS ghi log dạng JSON một dòng ra stdout bằng nestjs-pino. Lý do là thư viện này có sẵn cơ chế che khoá bí mật, tự gắn ngữ cảnh request và nhẹ cho máy ARM.

<a id="s-0bc81167ac"></a>

## Bối cảnh

- App chạy liên tục trong Docker. Cần đọc log để điều tra lỗi quét, việc tự dừng và đo tài nguyên.
- Log không được chứa khoá bí mật, cookie, mật khẩu hay dữ liệu cá nhân như nội dung bài và tin nhắn của khách.
- Máy đích (Oracle A1) ít tài nguyên, nên log cần nhẹ.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-723a648454"></a>

### A. nestjs-pino (pino), log JSON một dòng ra stdout

**Ưu**

- Nhanh và nhẹ.
- Có `redact` để che bí mật theo đường dẫn khoá.
- Tự gắn `requestId`.
- Log JSON dễ lọc bằng `jq` hoặc đưa vào công cụ log sau này.

**Nhược**

- Thêm hai thư viện.
- Log thô khó đọc bằng mắt khi dev. Lúc dev dùng `pino-pretty` để đọc dễ hơn.

<a id="s-36da071471"></a>

### B. `ConsoleLogger` có sẵn của NestJS (chế độ `json`)

**Ưu**

- Không thêm thư viện.

**Nhược**

- Không có sẵn cơ chế che khoá bí mật, phải tự viết.
- Không tự gắn ngữ cảnh request.
- Chậm hơn pino.

<a id="s-1fea0098e9"></a>

### C. winston (nest-winston)

**Ưu**

- Nhiều transport, phổ biến.

**Nhược**

- Nặng hơn pino.
- Muốn che bí mật thì phải tự viết format.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A.

**Vì sao.** nestjs-pino có sẵn cơ chế che khoá bí mật và ngữ cảnh request. Thư viện này cũng nhẹ, hợp với máy ARM.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Cả api và browser-worker dùng chung một định dạng log.
- Việc che bí mật nằm ở một chỗ.
- Có `requestId` và `jobId` để lần theo một lượt xử lý.

**Mất và rủi ro**

- Thêm phụ thuộc `nestjs-pino`, `pino-http`, và `pino-pretty` ở môi trường dev.
- Danh sách khoá cần che phải được bổ sung mỗi khi có loại bí mật mới.
