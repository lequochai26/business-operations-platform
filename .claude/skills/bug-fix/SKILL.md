---
name: bug-fix
description: Sửa lỗi có kiểm chứng - đọc kết quả và evidence lần test không đạt, tái hiện, tìm nguyên nhân gốc, viết test tự động tái hiện lỗi rồi sửa (tdd), gắn cờ regression và cập nhật issues.md; lỗi do thiết kế thì chuyển change-request. Use to fix a bug or failed test case.
argument-hint: "<mã case | mã vấn đề | mô tả lỗi>"
---

# bug-fix

## Mục đích

Sửa đúng nguyên nhân gốc của lỗi, có test chứng minh lỗi đã hết và không quay lại.

## Điều kiện tiên quyết

- Có mã case không đạt, mã vấn đề trong `issues.md`, hoặc mô tả lỗi đủ để tái hiện. Thiếu: hỏi bước tái hiện.
- Cây làm việc git sạch.

## Input

- Tham số: mã case (`P<N>-<ABC>-<nnn>`), mã vấn đề (`P<N>-ISS-<nnn>`) hoặc mô tả.
- Lần chạy không đạt gần nhất của case trong `docs/phases/phase-N/test/runs/*/results.md`: kết quả thực tế, evidence.
- Mục vấn đề trong `docs/phases/phase-N/issues.md` (nếu có).
- Thiết kế chi tiết và case: hành vi đúng phải như thế nào.
- `CLAUDE.md` mục `## Quy ước`: nhánh, lệnh test.

## Các bước

1. Đọc kết quả, evidence, thiết kế. Nêu rõ: hành vi mong đợi (trích thiết kế) và hành vi thực tế.
2. Nếu lỗi do **thiết kế sai hoặc thiếu** (code làm đúng thiết kế): dừng, chuyển sang `change-request`.
3. Nếu chưa có mục trong `issues.md`: tạo mục (`- Phân loại: bug`, `- Trạng thái: mở`) theo `.claude/skills/feedback/templates/issues.md`.
4. Tạo nhánh sửa lỗi theo quy ước (ví dụ `phase-<N>/fix-<mã vấn đề>`). Đặt vấn đề `đang xử lý`.
5. Tái hiện lỗi trên môi trường thật hoặc bằng test. Không tái hiện được: báo người dùng, hỏi thêm thông tin, không sửa mò.
6. Tìm nguyên nhân gốc: lần ngược từ triệu chứng tới chỗ dữ liệu/hành vi sai đầu tiên. Không sửa triệu chứng.
7. Gọi `tdd`: test tự động tái hiện đúng lỗi, thấy thất bại → sửa → pass → chạy toàn bộ test.
8. Gắn `- Regression: có` cho case liên quan trong file test case.
9. Commit. Cập nhật mục vấn đề: `- Trạng thái: đã xong`, `- Xử lý: <commit>, test <tên test>`. **Không sửa** `results.md` của lần chạy cũ; kết quả mới ghi ở lần test lại.
10. Merge theo `/review-code` như mọi thay đổi code.

## Điểm dừng

- Bước 2: lỗi do thiết kế → dừng, xác nhận với người dùng trước khi chuyển `change-request`.
- Bước 5: không tái hiện được → dừng, hỏi người dùng.

## Output

- Test tự động tái hiện lỗi, code sửa, commit.
- Case gắn cờ regression; mục `issues.md` đã cập nhật.

## Tự kiểm tra

- Test mới thất bại trên code cũ và pass trên code mới (đã thấy cả hai).
- Toàn bộ test pass.
- Nguyên nhân gốc được nêu rõ trong báo cáo, không chỉ triệu chứng.

## Cập nhật status.md

Không đổi trạng thái tính năng.

## Báo cáo kết thúc

- Nguyên nhân gốc, cách sửa, test đã thêm, commit, mục vấn đề.
- Cần người dùng quyết: merge (qua `/review-code`).
- Bước tiếp theo: `/review-code`, sau đó `/manual-test-run --retest <mã case>`.
