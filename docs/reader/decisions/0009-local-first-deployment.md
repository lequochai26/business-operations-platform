> Bản đọc sinh từ docs/decisions/0009-local-first-deployment.md (phiên bản 7cdfee8, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0009 – Chạy trên máy local trước, giữ khả năng dời lên Oracle

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - docs/project/04-technical.md mục 1, 3, 7;
  - docs/project/05-roadmap.md giai đoạn 0 và mục "Triển khai lên máy chủ";
  - CLAUDE.md mục Quy ước – Docker;
  - phase-0: app-skeleton, fb-account-session, backup.

**Tóm tắt.** Giai đoạn 0 chạy bằng Docker trên máy local thay vì chờ có Oracle Cloud Free. Image và cấu hình được ràng buộc ngay từ đầu để sau này dời lên Oracle chỉ là việc triển khai, không phải sửa code.

<a id="s-0bc81167ac"></a>

## Bối cảnh

- Thiết kế khái quát chọn Oracle Cloud Free (Ampere A1, linux/arm64) làm nơi chạy 24/7. Thiết kế này cũng đặt việc dựng VM, HTTPS và tên miền vào giai đoạn 0.
- Hiện chưa đăng ký được Oracle Free. Người dùng muốn chạy giai đoạn 0 bằng Docker trên máy của mình trước. Sau này hệ thống sẽ dời lên Oracle mà không phải sửa code.
- Máy dev chạy Windows x64, tức là linux/amd64 trong Docker. Oracle A1 là linux/arm64.
- Giai đoạn 0 không cần HTTPS, vì web app chỉ truy cập qua `localhost`. Giai đoạn 1 có web push trên iPhone, giai đoạn 2 có webhook Messenger. Cả hai giai đoạn này bắt buộc có HTTPS và tên miền cố định.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-54e1e273f4"></a>

### A. Local trước, image đa kiến trúc, cấu hình theo môi trường

**Ưu**

- Bắt đầu được ngay và không tốn tiền.
- IP nhà mạng ít bị Facebook nghi ngờ hơn IP datacenter.
- Muốn dời lên Oracle chỉ cần build image arm64, đổi biến môi trường và đăng nhập lại.

**Nhược**

- Máy dev không chạy 24/7, nên tiêu chí "chạy liên tục 3 ngày" phải nới.
- Chưa kiểm chứng được rủi ro IP datacenter và tài nguyên của Oracle A1.
- Phải giữ image chạy được trên cả amd64 và arm64.

<a id="s-89c9d390a7"></a>

### B. Chờ có Oracle rồi mới làm giai đoạn 0

**Ưu**

- Giữ nguyên roadmap.
- Kiểm chứng đúng môi trường thật ngay từ đầu.

**Nhược**

- Bị chặn vô thời hạn, không làm được gì.

<a id="s-4fe2507198"></a>

### C. Thuê VPS trả phí (x64) ngay

**Ưu**

- Chạy 24/7.
- Có IP cố định để làm HTTPS sớm.

**Nhược**

- Tốn tiền hằng tháng, trái với ưu tiên "không tốn tiền máy chủ".
- IP datacenter vẫn có rủi ro như Oracle.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A.

**Vì sao.** Phương án A không bị chặn và không tốn tiền. Nếu ràng buộc tính khả chuyển ngay từ `app-skeleton` thì việc dời lên Oracle chỉ còn là việc triển khai.

**Ràng buộc kèm theo**

- Image Docker build được cho `linux/amd64` và `linux/arm64`. Base image phải là loại đa kiến trúc, kể cả image Playwright. Không dùng thứ gì chỉ có trên một kiến trúc.
- Mọi khác biệt giữa các máy nằm ở biến môi trường và volume. Đó là đường dẫn dữ liệu (ảnh, debug dump, profile trình duyệt), đích sao lưu và URL công khai. Code và `compose.yml` không chứa giá trị phụ thuộc máy.
- Sao lưu ghi ra một thư mục cấu hình được. Việc đẩy bản sao lưu lên Object Storage (giao thức tương thích S3) là bước tuỳ chọn, bật bằng biến môi trường.
- HTTPS và reverse proxy (Caddy) là một lớp tách riêng. Lớp này được thêm vào khi triển khai lên máy chủ và không làm thay đổi app.
- Khi dời máy, DB được khôi phục từ bản sao lưu. **Không copy profile trình duyệt.** Thay vào đó, đăng nhập lại trên máy mới qua noVNC (04-technical.md mục 4.2).

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Giai đoạn 0 làm được ngay.
- App và hạ tầng được tách rõ.
- Có sẵn quy trình dời máy: sao lưu, khôi phục, rồi đăng nhập lại.

**Mất và rủi ro**

- Rủi ro IP datacenter và mức tài nguyên trên Oracle A1 chưa được kiểm chứng. Phải kiểm chứng lại khi dời lên Oracle.
- Phải có HTTPS và tên miền cố định trước khi bật web push ở giai đoạn 1. Nếu lúc đó vẫn chưa có Oracle thì cần phương án tạm, ví dụ Cloudflare Tunnel có tên miền. Phương án tạm này sẽ được ghi thành ADR riêng.
- Build arm64 trên máy amd64 cần buildx hoặc QEMU, nên chậm hơn build thường.
