---
name: test-case-design
description: Thiết kế manual test case cho một tính năng từ thiết kế chi tiết và mockup, dùng bảng khía cạnh test chung và các kỹ thuật thiết kế test (giá trị biên, bảng quyết định, chuyển trạng thái, đoán lỗi); cập nhật bảng đối chiếu traceability. Use to design manual test cases.
argument-hint: "<slug tính năng>"
---

# test-case-design

## Mục đích

Sinh bộ manual test case đầy đủ, truy vết được tới từng quy tắc của thiết kế, trước khi code.

## Điều kiện tiên quyết

- Trạng thái tính năng là `test case` trong `status.md` (đã duyệt thiết kế chi tiết, và UI nếu có màn hình).
- Đã có `docs/testing/viewpoints.md`. Chưa có: dừng, gợi ý `/test-viewpoints-init`.

## Input

- Tham số: slug tính năng.
- `docs/phases/phase-N/design/<slug>.md`: quy tắc `R-<ABC>-<nn>`, trường, tham số, trạng thái, phân quyền, tích hợp.
- `docs/design/ui/<màn hình>/` (nếu có): mockup và `notes.md` (luồng thao tác).
- `docs/testing/viewpoints.md`: 12 khía cạnh và câu hỏi gợi ý.
- `docs/phases/phase-N/test/traceability.md` (nếu có).
- `docs/process/2026-10-29-dev-process-skills-design.md` mục 8: phạm vi manual test, nhóm thao tác tay.

## Các bước

1. Đọc thiết kế và mockup. Lập danh sách: mọi `R-…`, mọi trường nhập, mọi tham số, mọi trạng thái và bước chuyển, mọi vai trò.
2. Với **từng** khía cạnh trong `viewpoints.md`: trả lời các câu hỏi gợi ý cho tính năng này → danh sách điều cần kiểm chứng. Khía cạnh không áp dụng: ghi lý do vào đầu file case.
3. Sinh case bằng kỹ thuật phù hợp:
   - **phân vùng tương đương và giá trị biên**: mỗi trường/tham số có khoảng → dưới biên, đúng biên dưới, đúng biên trên, trên biên, sai kiểu, rỗng;
   - **bảng quyết định**: quy tắc nhiều điều kiện → mỗi tổ hợp có kết quả khác nhau là một case;
   - **chuyển trạng thái**: mỗi bước chuyển hợp lệ một case, và các bước chuyển không hợp lệ quan trọng;
   - **đoán lỗi và tình huống thực tế**: theo nhóm thao tác tay (trình duyệt, cookie/phiên, DB, Facebook, Messenger, thiết bị thật).
4. Gộp các điều kiện trùng, đánh mã `P<N>-<ABC>-<nnn>` tăng dần từ `001`. Viết theo `templates/test-cases.md`.
   - Mỗi bước có kết quả mong đợi cụ thể (thông báo nguyên văn, giá trị trong DB, trạng thái hiển thị).
   - Bước cần evidence đánh dấu `[evidence]`.
   - `Người thực hiện: Claude` nếu làm được bằng Playwright, lệnh SQL, sửa cookie; `người` nếu cần Facebook thật, thiết bị thật, đánh giá bằng mắt.
   - Gắn `Regression: có` cho case cốt lõi (đường chính, phân quyền, lằn ranh đỏ).
   - Không viết case đòi can thiệp vào luồng xử lý của code.
5. Cập nhật `docs/phases/phase-N/test/traceability.md` (tạo từ `templates/traceability.md` nếu chưa có): mỗi `R-…` của tính năng → các case.
6. Chạy checklist `checklists/test-case-design.md`, bổ sung case còn thiếu.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

Không có điểm dừng riêng: bộ case được duyệt cùng thiết kế ở `/design-review`.

## Output

- `docs/phases/phase-N/test/cases/<slug>.md` theo `templates/test-cases.md` (ví dụ: `templates/example-test-cases.md`).
- `docs/phases/phase-N/test/traceability.md` theo `templates/traceability.md`.

## Tự kiểm tra

Chạy `checklists/test-case-design.md`; mọi mục phải đạt.

## Cập nhật status.md

Không đổi trạng thái (vẫn `test case` cho tới khi `/design-review` duyệt).

## Báo cáo kết thúc

- Số case theo khía cạnh, số case Claude làm / người làm, số case regression; khía cạnh không áp dụng.
- Cần người dùng quyết: tình huống nào thiết kế chưa nói rõ hành vi đúng (nếu có).
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: `/design-review <slug>`.
