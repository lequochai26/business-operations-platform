---
name: manual-test-run
description: Chạy manual test case của một tính năng (hoặc test lại một case, hoặc chạy bộ regression) và thu evidence - Claude tự chạy case làm được bằng Playwright/SQL/cookie, hướng dẫn người dùng làm case cần Facebook hay thiết bị thật; ghi results.md, tạo vấn đề cho case không đạt. Use to run manual tests and capture evidence.
argument-hint: "<slug> | --retest <mã case> | --regression"
---

# manual-test-run

## Mục đích

Chạy manual test có evidence, ghi kết quả theo định dạng cố định để báo cáo nghiệm thu xuất được.

## Điều kiện tiên quyết

- `<slug>`: tính năng ở trạng thái `đã code` hoặc `đang manual test`, code đã merge (hoặc người dùng chỉ định nhánh).
- `--retest <mã case>`: case có kết quả `không đạt` hoặc `bị chặn` ở lần chạy trước, và vấn đề liên quan ở trạng thái `chờ test lại` (do `bug-fix` đặt sau khi sửa).
- `--regression`: chạy mọi case có `- Regression: có` của giai đoạn.
- Có file case `docs/phases/phase-N/test/cases/<slug>.md`.

## Input

- Tham số (một trong ba dạng ở trên).
- Các case cần chạy trong `docs/phases/phase-N/test/cases/`.
- Từ người dùng: môi trường (máy dev hay Oracle) và URL. Commit tự lấy bằng `git rev-parse --short HEAD`.
- Từ người dùng, với case `Người thực hiện: người`: ảnh chụp và kết quả quan sát.
- Lần chạy trước (khi test lại): `docs/phases/phase-N/test/runs/*/results.md`.

## Các bước

1. Xác định danh sách case (bỏ qua case có dòng `- Đã bỏ:`). Hỏi môi trường và URL. Đặt tính năng `đang manual test` (nếu đang `đã code`).
2. Tạo `docs/phases/phase-N/test/runs/<YYYY-MM-DD-NN>/` (NN tăng dần trong ngày) và thư mục `evidence/` bên trong. Viết phần đầu `results.md` theo `templates/results.md`.
3. Với từng case, theo thứ tự trong file:
   - **Claude làm**: thực hiện từng bước bằng Playwright (trình duyệt), lệnh SQL (DB), sửa cookie; tại bước `[evidence]` chụp ảnh vào `evidence/` tên `<mã case>_<bước 2 chữ số>_<mô tả ngắn tiếng Anh>.png`; so kết quả với mong đợi.
   - **Người làm**: in từng bước và kết quả mong đợi; chờ người dùng làm và gửi ảnh + kết quả; lưu ảnh vào `evidence/` đúng quy tắc tên.
   - Ghi mục case vào `results.md` ngay sau khi xong case đó (không đợi cuối), đúng định dạng mẫu; `- Kết quả:` chỉ dùng `đạt`, `không đạt`, `bị chặn`, `bỏ qua`.
   - Case `không đạt` (lần chạy thường, không phải test lại): tạo mục trong `docs/phases/phase-N/issues.md` theo `.claude/skills/feedback/templates/issues.md` (`- Nguồn: manual test <mã lần chạy>`, `- Phân loại: bug` hoặc theo đối chiếu thiết kế), điền mã vào `- Vấn đề:`.
   - Người dùng phản hồi giữa chừng điều không nằm trong case: chuyển qua `feedback`.
4. Test lại: lần chạy mới chỉ chứa các case chạy lại; không sửa `results.md` cũ. Với vấn đề `chờ test lại` của case:
   - case **đạt**: vấn đề → `đã xong`, `- Xử lý:` thêm "đạt ở lần chạy <mã>";
   - case **không đạt**: **mở lại vấn đề cũ** (→ `mở`, `- Xử lý:` thêm "vẫn lỗi ở lần chạy <mã>: <thực tế>"), điền mã vấn đề cũ vào `- Vấn đề:`; **không** tạo vấn đề mới.
5. Tổng kết: số case theo kết quả, danh sách vấn đề mới.

## Điểm dừng

- Mỗi case `người`: chờ người dùng gửi kết quả.
- Cuối lần chạy: nếu có case không đạt, đề xuất `/bug-fix <mã>` và chờ người dùng chọn.

## Output

- `docs/phases/phase-N/test/runs/<mã lần chạy>/results.md` theo `templates/results.md` (ví dụ: `templates/example-results.md`).
- `evidence/` (không commit, nằm trong `.gitignore`).
- Mục mới trong `issues.md` cho case không đạt.

## Tự kiểm tra

- Mọi case trong danh sách có mục trong `results.md`.
- Mọi tên file trong `- Evidence:` tồn tại trong `evidence/`.
- Mọi case `không đạt` có `- Vấn đề:` trỏ tới mục có thật trong `issues.md`.
- Đã `git status` xác nhận `evidence/` không bị đưa vào commit.

## Cập nhật status.md

- Bắt đầu: tính năng `đã code` → `đang manual test`.
- Mọi case của tính năng có kết quả mới nhất `đạt` (hoặc `bỏ qua` có lý do được người dùng chấp nhận): `đạt`; ghi `- <ngày> | <slug> | manual test đạt | <người duyệt>` vào `## Nhật ký duyệt`.

## Báo cáo kết thúc

- Mã lần chạy, số case đạt / không đạt / bị chặn / bỏ qua, vấn đề mới.
- Cần người dùng quyết: sửa lỗi nào trước; chấp nhận case `bỏ qua` không.
- Bước tiếp theo: `/bug-fix <mã>` nếu có lỗi; `/acceptance-report N` nếu mọi tính năng đã `đạt`; ngược lại `/manual-test-run <slug tiếp theo>`.
