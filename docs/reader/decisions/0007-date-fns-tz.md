> Bản đọc sinh từ docs/decisions/0007-date-fns-tz.md (phiên bản 5e6aa4d, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0007 – date-fns + @date-fns/tz cho xử lý ngày giờ

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - CLAUDE.md mục Quy ước › Test tự động (Đồng hồ, Ngày giờ);
  - docs/project/04-technical.md mục 3, 8.

**Tóm tắt.** Xử lý ngày giờ dùng date-fns và @date-fns/tz. Lý do là hai thư viện này dùng `Date` gốc, nên một kiểu `Date` đi xuyên suốt từ `Clock` tới DB.

<a id="s-0bc81167ac"></a>

## Bối cảnh

Nghiệp vụ có nhiều phép tính ngày giờ:
- tìm khung trống;
- chống trùng lịch;
- quy đổi ngày tương đối như "mai", "T3", "tối nay";
- giờ nghỉ của phanh an toàn.

Mọi lịch dùng múi giờ `Asia/Ho_Chi_Minh`. Đồng hồ phải được truyền vào qua `Clock`.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-3b426ad02d"></a>

### A. date-fns và @date-fns/tz

**Ưu**

- Hàm thuần, tree-shake được.
- Dùng `Date` gốc nên hợp với `Clock` và Drizzle.

**Nhược**

- API múi giờ hơi rời rạc.

<a id="s-3f43e9347e"></a>

### B. Luxon

**Ưu**

- `DateTime` bất biến.
- Múi giờ rõ ràng.

**Nhược**

- Phải chuyển qua lại với `Date` ở biên DB và ở `Clock`.

<a id="s-8a42b0cfc6"></a>

### C. Temporal (polyfill)

**Ưu**

- Là chuẩn của tương lai và chính xác nhất.

**Nhược**

- Polyfill nặng.
- Drizzle và zod chưa hỗ trợ sẵn.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A. Múi giờ lấy từ một hằng số dùng chung. DB lưu thời gian kiểu `timestamptz`.

**Chi tiết kỹ thuật**

- Hằng múi giờ: `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Một kiểu `Date` dùng xuyên suốt từ `Clock` tới DB.

**Mất và rủi ro**

- `Date` thay đổi được (mutable), nên phải dùng hàm của date-fns thay vì sửa trực tiếp.
- Khi Temporal phổ biến thì có thể cần chuyển sang.
