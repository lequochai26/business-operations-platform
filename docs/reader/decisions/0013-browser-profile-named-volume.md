> Bản đọc sinh từ docs/decisions/0013-browser-profile-named-volume.md (phiên bản 0d828e0, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0013 – Profile trình duyệt nằm trong named volume riêng

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton ([R-SKL-20](../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*, biến `BROWSER_PROFILE_DIR`), fb-account-session, backup;
  - docs/project/04-technical.md mục 4.2, 7;
  - [ADR 0009](0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*;
  - review `docs/phases/phase-0/design/reviews/app-skeleton-review.md` RV-06.

**Tóm tắt.** Profile trình duyệt được đặt trong một named volume riêng của Docker, tách khỏi thư mục dữ liệu bind mount trên ổ Windows. Cách này giữ quyền truy cập và phiên đăng nhập Facebook ổn định mà không đổi cách làm việc hằng ngày.

<a id="s-0bc81167ac"></a>

## Bối cảnh

- Giai đoạn 0 chạy Docker Desktop trên Windows ([ADR 0009](0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*). `MIO_DATA_DIR` nhiều khả năng là một thư mục trên ổ NTFS, gắn vào container qua bind mount.
- Bind mount từ ổ Windows không giữ quyền Unix, nên `chmod 700` cho thư mục profile không có tác dụng. Truy cập file qua bind mount chậm. Khoá file SQLite, nơi Chromium lưu cookie và phiên đăng nhập, kém tin cậy. Điều này ảnh hưởng tới bài chạy quét 24 giờ không bị đăng xuất.
- Tài liệu 04 mục 7 yêu cầu profile chỉ người chạy dịch vụ được đọc và không được đưa vào bản sao lưu công khai. [ADR 0009](0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)* quy định khi dời máy thì không copy profile mà đăng nhập lại.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-a5d3a4f400"></a>

### A. Profile trong named volume riêng; ảnh và debug dump vẫn ở `MIO_DATA_DIR`

Profile nằm trong named volume `mio-browser-profile`, gắn vào đường dẫn `/browser-profile`.

**Ưu**

- Volume nằm trên ext4 trong máy ảo Docker. Quyền `700` có hiệu lực, SQLite ổn định và nhanh.
- Chạy giống nhau trên Windows và Linux.
- Profile tự tách khỏi thư mục sao lưu.

**Nhược**

- Không mở trực tiếp profile được từ Windows Explorer. Muốn xem thì phải dùng `docker`.
- Thêm một biến `BROWSER_PROFILE_DIR`.
- Nếu xoá nhầm bằng `docker compose down -v` thì mất phiên. Khi đó phải đăng nhập lại qua noVNC.

<a id="s-9d21cf0ebe"></a>

### B. Giữ cả `MIO_DATA_DIR` (kể cả profile) là bind mount trên ổ Windows

**Ưu**

- Không phải thêm gì.
- Mọi dữ liệu nằm một chỗ và xem được bằng Explorer.

**Nhược**

- Quyền `700` bị vô hiệu.
- Có rủi ro hỏng hoặc mất phiên do khoá file.
- Chậm.

<a id="s-9c60aa661b"></a>

### C. Chạy Docker từ WSL2, `MIO_DATA_DIR` đặt trong filesystem của WSL2

**Ưu**

- Quyền Unix và hiệu năng tốt cho mọi dữ liệu, không chỉ profile.

**Nhược**

- Đổi cách làm việc hằng ngày: chạy lệnh từ WSL2 và dùng đường dẫn kiểu Linux.
- Thêm bước cài đặt cho máy dev.
- Không giúp gì khi đã lên máy chủ Linux.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A.

**Vì sao.** Phương án A giải quyết đúng phần nhạy cảm nhất là phiên đăng nhập Facebook. Phương án này không đổi cách làm việc và chạy giống nhau trên máy local lẫn máy chủ.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Quyền `700` có hiệu lực thật.
- Phiên đăng nhập ổn định hơn.
- Profile không lẫn vào bản sao lưu.
- Khi dời máy chỉ cần tạo volume mới và đăng nhập lại.

**Mất và rủi ro**

- Lệnh `docker compose down -v` xoá profile, sau đó phải đăng nhập lại.
- Muốn xem file trong profile thì phải dùng `docker`.
- browser-worker có thêm biến môi trường `BROWSER_PROFILE_DIR`.
