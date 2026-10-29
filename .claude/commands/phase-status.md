---
description: Xem tiến độ giai đoạn hiện tại - tính năng đang ở bước nào, task, test case, vấn đề đang mở, việc đang chặn và lệnh nên chạy tiếp. Chỉ đọc, không ghi file.
argument-hint: "[số giai đoạn]"
---

Báo tiến độ giai đoạn. **Chỉ đọc file, không ghi hay sửa bất kỳ file nào.**

Giai đoạn: nếu có tham số `$ARGUMENTS` thì dùng số đó; nếu không, chọn giai đoạn có số lớn nhất trong `docs/phases/` mà `## Nhật ký duyệt` trong `status.md` chưa có dòng `nghiệm thu`. Không có thư mục giai đoạn nào: báo "Chưa mở giai đoạn nào" và gợi ý lệnh nhóm khởi tạo còn thiếu (`/conventions-init`, `/ui-style-init`, `/test-viewpoints-init`) hoặc `/phase-kickoff 0`.

Đọc trong `docs/phases/phase-N/`:
- `status.md`: cột `Trạng thái` của bảng `## Tính năng`, mục `## Vấn đề đang chặn`;
- `plan.md` (nếu có): đếm task theo `- Trạng thái:` (`chưa làm`, `đang làm`, `xong`);
- `test/runs/*/results.md` (nếu có): với mỗi mã case lấy kết quả của lần chạy mới nhất; đếm `đạt`, `không đạt`, `bị chặn`, `bỏ qua`; số case chưa chạy = số case trong `test/cases/*.md` trừ số case đã có kết quả;
- `issues.md` (nếu có): đếm mục có `- Trạng thái: mở` hoặc `đang xử lý`.

In ra đúng dạng sau (không thêm phần khác):

```text
Giai đoạn N – <tên>
- Tính năng: <tổng> | <trạng thái>: <số>, … (chỉ liệt kê trạng thái có số > 0)
- Task: <xong>/<tổng> xong (<đang làm> đang làm) | chưa có plan
- Test case: <đạt> đạt, <không đạt> không đạt, <bị chặn> bị chặn, <bỏ qua> bỏ qua, <chưa chạy> chưa chạy
- Vấn đề đang mở: <số> (<mã>, …)
- Đang chặn: <từng vấn đề, ngăn bằng ;> | không có
Lệnh nên chạy tiếp: <lệnh>
```

Chọn "Lệnh nên chạy tiếp" theo thứ tự ưu tiên:
1. Có vấn đề `bug` đang mở → `/bug-fix <mã vấn đề>`.
2. Có tính năng chưa xong thiết kế → lệnh của bước tiếp theo cho tính năng đứng đầu trong thứ tự thiết kế (`/detailed-design`, `/ui-design`, `/test-case-design`, `/design-review`).
3. Mọi tính năng đã duyệt thiết kế mà chưa có `plan.md` → `/implementation-plan`.
4. Có task `chưa làm` mà phụ thuộc đã xong → `/implement-task <mã task>`.
5. Có tính năng `đã code` → `/manual-test-run <slug>`.
6. Mọi tính năng `đạt` → `/acceptance-report N`.
