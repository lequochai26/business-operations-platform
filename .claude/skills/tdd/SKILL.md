---
name: tdd
description: Viết code theo vòng đỏ → xanh → refactor với quy ước test của dự án (đồng hồ truyền vào, property-based, DB thật trong Docker, không skip ngầm). Được implement-task và bug-fix gọi, hoặc gọi tay cho một hành vi. Use for test-driven development of a behavior.
argument-hint: "<hành vi cần hiện thực>"
---

# tdd

## Mục đích

Mọi code nghiệp vụ đều có test được viết trước và đã thấy thất bại đúng lý do.

## Điều kiện tiên quyết

- Hành vi cần làm được mô tả rõ (từ task trong `plan.md`, từ lỗi cần sửa, hoặc tham số). Chưa rõ: hỏi trước.
- `CLAUDE.md` mục `## Quy ước` đã chốt (công cụ test, vị trí file, lệnh chạy).

## Input

- Hành vi cần hiện thực (tham số hoặc từ skill gọi).
- Thiết kế liên quan (`docs/phases/phase-N/design/<slug>.md`): giá trị, thông báo, mã lỗi nguyên văn.
- `CLAUDE.md` mục `## Quy ước` → `### Test tự động`.
- `docs/process/2026-10-29-dev-process-skills-design.md` mục 9.

## Các bước

Lặp cho từng hành vi nhỏ:

1. **Đỏ – viết một test**: một hành vi, tên mô tả hành vi, giá trị lấy nguyên văn từ thiết kế. Trước khi viết, nói rõ thay đổi nào trong code sẽ làm test này thất bại.
2. **Chạy và thấy thất bại**: chạy đúng test đó. Phải thất bại vì thiếu tính năng (assert sai, hàm chưa có), không phải vì lỗi cú pháp hay import sai. Test pass ngay từ đầu = test sai hoặc hành vi đã có: sửa test.
3. **Xanh – code tối thiểu** để test pass. Không thêm tính năng ngoài test.
4. **Chạy lại**: test pass; chạy cả bộ test nhanh của dự án, mọi test khác vẫn pass.
5. **Refactor** khi đang xanh: bỏ trùng lặp, đặt tên rõ. Chạy lại test sau refactor.

Quy ước bắt buộc:
- **Cấm** viết code nghiệp vụ khi chưa có test thất bại cho nó. Lỡ viết trước: xóa và làm lại từ bước 1.
- Logic phụ thuộc thời gian nhận đồng hồ từ ngoài (interface trong `## Quy ước`); không gọi giờ hệ thống trực tiếp.
- Bất biến quan trọng (lịch không trùng, khung đề xuất luôn trống, không comment hai lần) dùng thêm property-based test.
- Ràng buộc DB, giao dịch, hàng đợi, migration: integration test với PostgreSQL/Redis thật trong Docker, không mock.
- Adapter bên ngoài (Facebook, Messenger, Gemini): test với fixture đã lưu và bản giả của interface; không gọi dịch vụ thật trong test tự động.
- Test bỏ qua (skip) phải in lý do; thiếu fixture thật phải báo rõ, không được báo pass.
- Mock chỉ khi không tránh được; assert trên hành vi thật, không assert trên mock.

## Điểm dừng

Không có điểm dừng riêng. Nếu thấy thiết kế sai hoặc thiếu trong lúc viết test: dừng, báo người dùng (có thể cần `/change-request`).

## Output

- File test và code theo vị trí trong `## Quy ước`.
- Kết quả chạy test (lệnh + số pass/fail) của lần đỏ và lần xanh.

## Tự kiểm tra

- Mọi hàm/hành vi mới có test.
- Đã thấy từng test thất bại đúng lý do trước khi code.
- Bộ test nhanh pass toàn bộ, không có cảnh báo mới.
- Không có skip không lý do.

## Cập nhật status.md

Không áp dụng trực tiếp (skill gọi `tdd` tự cập nhật).

## Báo cáo kết thúc

- Các hành vi đã làm, test tương ứng, kết quả đỏ → xanh.
- Cần người dùng quyết: chỗ thiết kế chưa rõ (nếu có).
- Bước tiếp theo: quay lại skill gọi (`implement-task` hoặc `bug-fix`).
