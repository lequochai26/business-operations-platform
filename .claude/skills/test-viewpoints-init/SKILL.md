---
name: test-viewpoints-init
description: Tạo bảng khía cạnh test dùng chung cho mọi tính năng (docs/testing/viewpoints.md), là đầu vào bắt buộc của test-case-design. Dùng một lần trước giai đoạn 0 hoặc khi cần bổ sung khía cạnh. Use to create the shared manual test viewpoint checklist.
argument-hint: ""
---

# test-viewpoints-init

## Mục đích

Tạo `docs/testing/viewpoints.md`: danh sách khía cạnh mà mọi lần thiết kế test case đều phải xét, để không bỏ sót loại tình huống nào.

## Điều kiện tiên quyết

- Chưa có `docs/testing/viewpoints.md`, **hoặc** người dùng muốn bổ sung/sửa. Nếu đã có: đọc file hiện tại và chỉ sửa phần được yêu cầu, ghi `## Lịch sử thay đổi`.

## Input

- `docs/process/2026-10-29-dev-process-skills-design.md` mục 8 (phạm vi manual test, 12 khía cạnh, nhóm thao tác tay).
- `docs/project/`: đặc thù của hệ thống (Facebook, Messenger, AI, lịch, phanh an toàn), và mục 5 của `01-overview.md` (những điều tuyệt đối không được xảy ra).

## Các bước

1. Tạo file theo `templates/viewpoints.md`, giữ đúng 12 khía cạnh và thứ tự.
2. Với mỗi khía cạnh, viết:
   - **Câu hỏi gợi ý**: 4–8 câu hỏi người thiết kế test phải tự trả lời;
   - **Ví dụ**: 2–4 ví dụ cụ thể của hệ thống này, lấy từ `docs/project/`.
3. Thêm mục `## Lằn ranh đỏ`: chép các điều trong `01-overview.md` mục 5, mỗi điều ghi khía cạnh nào giữ nó.
4. Trình bày cho người dùng, hỏi có muốn thêm khía cạnh riêng không.

## Điểm dừng

Người dùng duyệt nội dung `viewpoints.md` trước khi kết thúc.

## Output

`docs/testing/viewpoints.md` theo `templates/viewpoints.md` (ví dụ một khía cạnh đã điền: `templates/example-viewpoint.md`).

## Tự kiểm tra

- Đủ 12 khía cạnh, đúng tên và thứ tự như mẫu.
- Mỗi khía cạnh có ít nhất 4 câu hỏi và 2 ví dụ.
- Mục `## Lằn ranh đỏ` đủ các điều trong `01-overview.md` mục 5.
- Không có câu hỏi đòi can thiệp vào luồng xử lý của code (thay giá trị lúc chạy, breakpoint) — đó là việc của test tự động.

## Cập nhật status.md

Không áp dụng (chạy trước khi có giai đoạn).

## Báo cáo kết thúc

- Đã tạo hoặc cập nhật `docs/testing/viewpoints.md`.
- Cần người dùng quyết: khía cạnh muốn bổ sung (nếu có).
- Bước tiếp theo: `/phase-kickoff 0` (nếu `/conventions-init` và `/ui-style-init` đã xong).
