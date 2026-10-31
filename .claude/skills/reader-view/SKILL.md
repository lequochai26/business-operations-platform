---
name: reader-view
description: Sinh bản cho người đọc (Markdown + HTML) từ tài liệu do skill sinh ra - AI viết lại câu chữ các mục đã đổi theo writing-guide, script chèn ý nghĩa của mã, triển khai viết tắt, kiểm tra độ trung thực và sinh HTML. Được các skill khác gọi trước điểm dừng, hoặc gọi tay. Use to generate human-readable reader views of generated docs.
argument-hint: "<file>… | phase-N | all"
---

# reader-view

## Mục đích

Tạo bản dễ đọc của tài liệu trong `docs/` mà không sửa bản gốc: người đọc thấy ngay ý nghĩa của mã, câu chữ rõ ràng, và không mất thông tin nào của bản gốc.

## Điều kiện tiên quyết

- Đã cài công cụ Python của dự án (`tools/requirements.txt`).
- Tham số là file trong phạm vi bản gốc (`docs/phases/`, `docs/design/`, `docs/decisions/`, `docs/testing/`), `phase-N` hoặc `all`. File ngoài phạm vi: báo và bỏ qua.

## Input

- Tham số: danh sách file, `phase-N` hoặc `all`.
- Bản gốc trong `docs/`.
- `docs/process/writing-guide.md`: cách viết lại.
- Bản viết lại cũ trong `docs/reader/_rewrite/` (nếu có).

## Các bước

1. Chạy `py tools/reader/cli.py todo <tham số>`. Lệnh in số mục cần viết lại của từng file và heading của chúng.
2. Đọc `docs/process/writing-guide.md`. Với mỗi file trong `docs/reader/_rewrite/` có khối chứa `<!-- TODO: viết lại mục này -->`:
   - viết lại phần thân của **chỉ những khối đó** theo hướng dẫn viết, rồi xóa dòng TODO;
   - giữ nguyên dòng marker `<!-- src-section: … -->`, không đụng các khối khác.
3. Rà câu chữ vừa viết theo skill `vietnamese-tech-writing`: văn phong khách quan, giữ thuật ngữ tiếng Anh quen dùng, không cụm dịch máy, Unicode NFC.
4. Chạy `py tools/reader/cli.py build <tham số>`.
   - Báo `bản đọc thiếu … mục`: bổ sung đúng phần tử bị thiếu vào khối tương ứng trong `_rewrite`, chạy lại `build`. Tối đa 3 vòng; vẫn thiếu thì dừng và báo người dùng danh sách còn thiếu.
   - Báo `chạy lại todo`: bản gốc vừa đổi, quay lại bước 1.
   - Báo `Cảnh báo: … không tìm thấy định nghĩa`: ghi vào báo cáo, không chặn.
5. Ghi nhận đường dẫn bản đọc Markdown và HTML mà `build` in ra.

## Điểm dừng

Không có điểm dừng riêng. Skill gọi `reader-view` tự dừng theo quy trình của nó. Khi gọi tay: dừng sau khi báo link.

## Output

- `docs/reader/_rewrite/<đường dẫn>`: bản viết lại (commit).
- `docs/reader/<đường dẫn>`: bản đọc Markdown (commit).
- `docs/reader/html/`: bản đọc HTML và `index.html` (không commit).

## Tự kiểm tra

- `build` kết thúc với mã thoát 0.
- Không còn khối TODO trong các file vừa xử lý (`py tools/reader/cli.py stale <tham số>` không báo `còn mục chưa viết lại`).
- Không sửa file nào trong `docs/` ngoài `docs/reader/`.

## Cập nhật status.md

Không áp dụng.

## Báo cáo kết thúc

- Danh sách bản đọc vừa sinh: link Markdown và HTML; số mục đã viết lại; cảnh báo mã không có định nghĩa (nếu có).
- Cần người dùng quyết: phần tử vẫn thiếu sau 3 vòng (nếu có).
- Bước tiếp theo: quay lại skill đã gọi, hoặc mở `docs/reader/html/index.html` để đọc.
