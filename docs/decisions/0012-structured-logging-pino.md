# 0012 – Log JSON bằng pino (nestjs-pino)

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: phase-0 app-skeleton (R-SKL-17); mọi app NestJS (`@mio/api`, `@mio/browser-worker`); docs/project/04-technical.md mục 7

## Bối cảnh

- App chạy liên tục trong Docker, cần đọc log để điều tra lỗi quét, tự dừng, đo tài nguyên.
- Log không được chứa khóa bí mật, cookie, mật khẩu hay dữ liệu cá nhân (nội dung bài, tin nhắn khách).
- Máy đích (Oracle A1) ít tài nguyên, log nên nhẹ.

## Các phương án

### A. nestjs-pino (pino), log JSON một dòng ra stdout
- Ưu: nhanh, nhẹ; có `redact` theo đường dẫn khóa để che bí mật; tự gắn `requestId`; JSON dễ lọc bằng `jq` hoặc đưa vào công cụ log sau này.
- Nhược: thêm hai thư viện; log thô khó đọc bằng mắt khi dev (dùng `pino-pretty` lúc dev).

### B. `ConsoleLogger` có sẵn của NestJS (chế độ `json`)
- Ưu: không thêm thư viện.
- Nhược: không có che khóa bí mật sẵn, phải tự viết; không tự gắn ngữ cảnh request; chậm hơn pino.

### C. winston (nest-winston)
- Ưu: nhiều transport, phổ biến.
- Nhược: nặng hơn pino; che bí mật phải tự viết format.

## Quyết định

Chọn A vì có sẵn che khóa bí mật và ngữ cảnh request, nhẹ cho máy ARM.

## Hệ quả

- Được: một định dạng log cho cả api và browser-worker; che bí mật ở một chỗ; `requestId`/`jobId` để lần theo một lượt xử lý.
- Mất / rủi ro: thêm phụ thuộc `nestjs-pino`, `pino-http` (và `pino-pretty` ở dev); danh sách khóa cần che phải được bổ sung khi có loại bí mật mới.
