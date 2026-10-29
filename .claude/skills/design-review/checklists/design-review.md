# Checklist – design-review

## Khớp yêu cầu
- [ ] Mọi yêu cầu, quy tắc, con số trong các mục `docs/project/` liên quan đều có trong thiết kế hoặc trong `## Câu hỏi mở`.
- [ ] Không có yêu cầu nào bị làm sai nghĩa hoặc tự thêm ngoài phạm vi giai đoạn.
- [ ] Mọi `## Câu hỏi mở` đã có câu trả lời.

## Nhất quán
- [ ] Không mâu thuẫn với `docs/design/db-schema.md`, `docs/design/api/*.md`, thiết kế đã duyệt của tính năng khác.
- [ ] Tên bảng, cột, endpoint, mã lỗi theo `CLAUDE.md` mục `## Quy ước`.
- [ ] Mockup khớp thiết kế: trường, thông báo lỗi nguyên văn, phân quyền.

## Rõ ràng
- [ ] Không có câu hiểu được theo hai cách (ví dụ "thông báo phù hợp", "xử lý lỗi").
- [ ] Mọi trường nhập có kiểu, bắt buộc, khoảng/định dạng, thông báo lỗi nguyên văn.
- [ ] Mọi tham số có mặc định và khoảng hợp lệ.

## Đủ trường hợp
- [ ] Có xử lý cho lỗi mạng, lỗi hệ thống bên ngoài, dữ liệu không tồn tại, thao tác đồng thời.
- [ ] Trạng thái và bước chuyển đầy đủ, có quy định cho bước chuyển không hợp lệ.
- [ ] Phân quyền nêu rõ cho từng vai trò.

## Test case
- [ ] Mọi `R-…` có case trong `traceability.md`.
- [ ] Đã đạt mọi mục trong `.claude/skills/test-case-design/checklists/test-case-design.md`.

## Lằn ranh đỏ (`docs/project/01-overview.md` mục 5)
- [ ] Không nói sai với khách: giá, giờ, địa chỉ chỉ lấy từ nguồn thật; AI không tự sinh.
- [ ] Không thể nhận trùng lịch qua luồng tự động.
- [ ] Không comment giống spam, không comment hai lần vào một bài (kể cả khi retry).
- [ ] Có cơ chế dừng và cảnh báo khi tài khoản Facebook có dấu hiệu bị khóa.
- [ ] Ảnh chỉnh bằng AI không bị ghi là ảnh thật.
- [ ] Không vi phạm nguyên tắc minh bạch (review giả, từ tuyệt đối, "trọn bộ như hình" khi chưa rõ).
- [ ] Không trả lời chen ngang khi người thật đang nói chuyện với khách.
