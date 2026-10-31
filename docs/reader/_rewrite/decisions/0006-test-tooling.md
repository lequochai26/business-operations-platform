<!-- src-section: 0b0fa0b228 2a8a5b9b955b -->
# 0006 – Công cụ test tự động: vitest, fast-check, Testcontainers; thiếu fixture thì fail

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - CLAUDE.md mục Quy ước › Test tự động;
  - docs/process/2026-10-29-dev-process-skills-design.md mục 9;
  - skill tdd.

**Tóm tắt.** Test tự động dùng vitest, dùng fast-check cho property-based test và Testcontainers cho DB thật. Test thiếu fixture thật sẽ fail thay vì skip, để không bao giờ báo pass khi thiếu dữ liệu.

<!-- src-section: 0bc81167ac 61f4d94662d6 -->
## Bối cảnh

Spec mục 9 đặt ra các yêu cầu sau:
- đồng hồ được truyền vào;
- có property-based test;
- integration test chạy với Postgres và Redis thật trong Docker;
- có contract test;
- không skip ngầm.

POC dùng vitest. Trong POC, `story-parser.real.test.ts` bị skip khi thiếu fixture mà vẫn báo pass.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 1a666e1bf5 f18db2c83df3 -->
### DB thật cho integration test

#### A. Testcontainers

**Ưu**

- Test tự bật container sạch.
- Mỗi lần chạy đều chạy migration thật.
- Không cần bước chuẩn bị.

**Nhược**

- Khởi động chậm hơn vài giây.
- Cần Docker Desktop.

#### B. Test stack bằng docker compose, bật sẵn

**Ưu**

- Test chạy nhanh.

**Nhược**

- Phải nhớ bật stack trước.
- Dữ liệu có thể sót lại giữa các lần chạy.

<!-- src-section: a57cbf35bf f185a3861a33 -->
### Thiếu fixture thật

#### A. Mặc định fail qua `requireFixture()`

**Ưu**

- Không bao giờ báo pass khi thiếu dữ liệu.
- Fixture đã ẩn thông tin được commit vào repo, nên không có lý do để thiếu.

**Nhược**

- Clone mới mà thiếu fixture thì test đỏ ngay.

#### B. Skip có báo (`skipIf` kèm `console.warn`)

**Ưu**

- Không chặn khi thiếu fixture.

**Nhược**

- Vẫn dễ bị bỏ qua khi đọc lướt kết quả.

<!-- src-section: 254160d409 9701c6b8468b -->
## Quyết định

- Runner giữ vitest như POC, thêm `unplugin-swc` cho NestJS.
- Property-based test dùng fast-check.
- DB thật chọn phương án A (Testcontainers).
- Khi thiếu fixture chọn phương án A: test fail.
- Lint cấm `.skip`, `.only`, `.todo`, `skipIf`.

<!-- src-section: 58c5fdb1ed 275d15ea1b53 -->
## Hệ quả

**Được**

- Integration test cô lập và lặp lại được.
- Không còn skip ngầm.

**Mất và rủi ro**

- Lệnh `pnpm test:int` cần Docker và chạy chậm hơn.
- Phải giữ phiên bản image dùng trong test khớp với `compose.yml`.
