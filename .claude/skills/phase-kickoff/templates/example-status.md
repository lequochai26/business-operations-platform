# Giai đoạn 0 – Nền móng

## Phạm vi

- Mục tiêu: có khung app chạy được trên Oracle và kiểm chứng những điều kiện kỹ thuật lớn.
- Ngoài phạm vi: phân loại bài bằng AI (giai đoạn 1).

## Tiêu chí Xong khi

- Chạy quét liên tục ít nhất 3 ngày trên Oracle bằng tài khoản phụ mà không bị đăng xuất, hoặc nếu bị thì app tự dừng và báo đúng.
- Bài mới trong group xuất hiện trong cơ sở dữ liệu trong vòng 1 chu kỳ quét.
- Ghi lại mức RAM và CPU thực tế.

## Tính năng

Thứ tự thiết kế đề xuất: auth → group-settings → group-crawl-job → emergency-stop → backup

| Slug | Mã | Có màn hình | Tài liệu liên quan | Trạng thái |
|---|---|---|---|---|
| auth | AUT | có | 07-screens-and-settings.md mục chung | đã duyệt thiết kế |
| group-settings | GRP | có | 07 mục 2; 01 mục 2; 03 mục 2 | test case |
| group-crawl-job | CRW | không | 01 mục 2; 04-technical.md mục 2 | chưa bắt đầu |
| emergency-stop | STP | có | 01 mục 8; 07 mục 1.1 | chưa bắt đầu |
| backup | BAK | không | 04-technical.md mục 7 | chưa bắt đầu |

## Vấn đề đang chặn

- Chưa có VM Oracle Free — ảnh hưởng: group-crawl-job, backup — người xử lý: Hải
- Chưa có group riêng tư để test — ảnh hưởng: group-crawl-job — người xử lý: chủ tiệm

## Nhật ký duyệt

- 2026-11-01 | giai đoạn | mở giai đoạn | Hải
- 2026-11-03 | auth | đã duyệt thiết kế | Hải
