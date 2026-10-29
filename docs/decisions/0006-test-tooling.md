# 0006 – Công cụ test tự động: vitest, fast-check, Testcontainers; thiếu fixture thì fail

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Test tự động; docs/process/2026-10-29-dev-process-skills-design.md mục 9; skill tdd

## Bối cảnh

Spec mục 9 yêu cầu: đồng hồ truyền vào, property-based test, integration test với Postgres và Redis thật trong Docker, contract test, không skip ngầm. POC dùng vitest; `story-parser.real.test.ts` bị skip khi thiếu fixture mà vẫn báo pass.

## Các phương án

### DB thật cho integration test

#### A. Testcontainers
- Ưu: test tự bật container sạch, chạy migration thật mỗi lần, không cần bước chuẩn bị.
- Nhược: khởi động chậm hơn vài giây; cần Docker Desktop.

#### B. docker compose test stack bật sẵn
- Ưu: test chạy nhanh.
- Nhược: phải nhớ bật trước; dữ liệu có thể sót giữa các lần chạy.

### Thiếu fixture thật

#### A. Fail mặc định qua `requireFixture()`
- Ưu: không bao giờ báo pass khi thiếu dữ liệu; fixture đã ẩn thông tin được commit nên không có lý do thiếu.
- Nhược: clone mới mà thiếu fixture thì test đỏ ngay.

#### B. Skip có báo (`skipIf` + `console.warn`)
- Ưu: không chặn khi thiếu fixture.
- Nhược: vẫn dễ bị bỏ qua khi đọc nhanh kết quả.

## Quyết định

Runner giữ vitest của POC (+ `unplugin-swc` cho NestJS), property-based dùng fast-check. DB thật chọn A (Testcontainers). Thiếu fixture chọn A (fail). Lint cấm `.skip`, `.only`, `.todo`, `skipIf`.

## Hệ quả

- Được: integration test cô lập, lặp lại được; không còn skip ngầm.
- Mất / rủi ro: `pnpm test:int` cần Docker và chậm hơn; phải giữ phiên bản image test khớp `compose.yml`.
