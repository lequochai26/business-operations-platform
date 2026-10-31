---
name: feedback
description: Cửa vào chung cho mọi phản hồi trong lúc test (thấy bug, thấy chỗ chưa hợp lý, thắc mắc) - đối chiếu với thiết kế để phân loại (bug, thiết kế chưa hợp lý, thiếu test case, câu hỏi), ghi vào issues.md rồi chuyển sang skill xử lý. Use when the user reports a problem, bug, or feedback during testing.
argument-hint: "<nội dung phản hồi>"
---

# feedback

## Mục đích

Nhận mọi phản hồi của người dùng trong lúc test, phân loại đúng, ghi sổ và chuyển sang đúng cách xử lý.

## Điều kiện tiên quyết

- Có giai đoạn đang mở (`docs/phases/phase-N/status.md`). Chưa có: trả lời trực tiếp, không ghi sổ.
- Có nội dung phản hồi. Thiếu: hỏi.

## Input

- Tham số: nội dung phản hồi; ảnh chụp người dùng gửi (nếu có).
- Tính năng liên quan: tự đoán từ nội dung và `status.md` (tính năng đang `đang manual test` hoặc vừa được nhắc tới); đoán không ra thì hỏi.
- `docs/phases/phase-N/design/<slug>.md`, mockup `docs/design/ui/<màn hình>/`, `docs/phases/phase-N/test/cases/<slug>.md`: để đối chiếu.
- `docs/phases/phase-N/issues.md` (tạo từ `templates/issues.md` nếu chưa có).

## Các bước

1. Xác định tính năng và đoạn thiết kế/mockup/case liên quan.
2. Phân loại bằng cách đối chiếu hành vi người dùng thấy với thiết kế:
   - **bug**: app chạy khác thiết kế hoặc mockup;
   - **thiết kế chưa hợp lý**: app chạy đúng thiết kế nhưng thiết kế chưa tốt hoặc thiếu;
   - **thiếu test case**: tình huống hợp lệ chưa có case nào bao phủ (có thể kèm bug hoặc không);
   - **câu hỏi**: người dùng hiểu nhầm hoặc cần giải thích.
   Phản hồi chứa nhiều ý: tách thành nhiều mục.
3. Trình bày: phân loại, dẫn chứng (trích thiết kế/mockup/case), hướng xử lý đề xuất.
4. Sau khi người dùng xác nhận: thêm mục vào `issues.md` theo `templates/issues.md` (mã `P<N>-ISS-<nnn>` tiếp theo, `- Nguồn: feedback`, `- Trạng thái: mở`). Ảnh người dùng gửi lưu vào `evidence/` của lần chạy test gần nhất (hoặc `.local/feedback/` nếu chưa có lần chạy), ghi tên file vào `- Evidence:`.
5. Xử lý theo phân loại:
   - bug → gọi `bug-fix` với mã vấn đề;
   - thiết kế chưa hợp lý → gọi `change-request`;
   - thiếu test case → thêm case vào `docs/phases/phase-N/test/cases/<slug>.md` và `traceability.md` theo mẫu của `test-case-design`; đặt `- Trạng thái: đã xong`, `- Xử lý: thêm case <mã>`;
   - câu hỏi → trả lời kèm dẫn chứng; đặt `- Trạng thái: đã xong`, `- Xử lý:` tóm tắt câu trả lời.
6. Khi skill xử lý kết thúc: cập nhật `- Trạng thái:` và `- Xử lý:` của mục (commit, phiên bản thiết kế, mã case mới).

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

Sau bước 3: người dùng xác nhận phân loại và hướng xử lý trước khi ghi sổ và chuyển skill.

## Output

- Mục mới trong `docs/phases/phase-N/issues.md` theo `templates/issues.md`.
- Kết quả của skill xử lý (bug đã sửa, thiết kế đã đổi, case mới, câu trả lời).

## Tự kiểm tra

- Mỗi ý trong phản hồi có đúng một mục và một phân loại.
- Phân loại có dẫn chứng từ thiết kế/mockup/case, không dựa vào cảm tính.
- Mục có đủ các dòng của mẫu; mã không trùng.

## Cập nhật status.md

Không đổi trực tiếp. `change-request` có thể lùi trạng thái tính năng; `bug-fix` không đổi trạng thái.

## Báo cáo kết thúc

- Mã vấn đề đã tạo, phân loại, đã chuyển sang skill nào, kết quả.
- Cần người dùng quyết: các vấn đề còn chờ quyết.
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: `/manual-test-run --retest <mã case>` sau khi sửa, hoặc tiếp tục test.
