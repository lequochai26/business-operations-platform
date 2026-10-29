# Style UI – Tiệm Nhà Mio

Nguồn chính về style của toàn hệ thống. `ui-tokens.css` được sinh từ khối `## Tokens` bằng `py tools/ui/gen_tokens.py`. Không sửa tay `ui-tokens.css`.

Hướng style: **kem ấm, sage nhấn, thanh điều hướng xanh đậm** (ADR `0008-ui-style-direction`).

## Nguyên tắc

- Nền tảng hiện tại: web trên máy tính (khung chuẩn 1440×900). Responsive và app native làm sau, nên token đặt tên độc lập nền tảng.
- Giao diện vận hành: ưu tiên dễ đọc, dễ quét danh sách, trạng thái rõ ràng. Nhận diện của tiệm thể hiện ở màu, không ở trang trí.
- Nền trang màu kem, nội dung đặt trên thẻ trắng. Màu tiệm đậm nhất nằm ở thanh điều hướng và nút chính.
- Sage `color-brand-primary` chỉ dùng để nhấn (gạch chân tab đang chọn, thanh tiến độ, vạch đánh dấu), **không** dùng làm nền cho chữ: chữ trắng trên sage chỉ đạt 2.74:1.
- Mật độ gọn: danh sách và form cài đặt dài là loại màn hình chính.
- Mọi giá trị lấy từ token. Không viết cứng màu, cỡ chữ, khoảng cách.

## Tokens

```yaml
color:
  brand:
    primary: '#8FA284'
    primary-strong: '#4E6045'
    primary-stronger: '#3E4E37'
    primary-soft: '#E4EBDF'
    cream: '#FAF7F0'
  text:
    default: '#2B2B2B'
    muted: '#6B6B6B'
    on-primary: '#FFFFFF'
    link: '#4E6045'
  surface:
    page: '#FAF7F0'
    card: '#FFFFFF'
    subtle: '#F3EFE4'
    border: '#E2DED3'
    divider: '#ECE8DE'
    overlay: 'rgba(43, 43, 43, 0.4)'
  control:
    border: '#8A857A'
    border-hover: '#4E6045'
    background-disabled: '#F3EFE4'
  nav:
    background: '#4E6045'
    text: '#FAF7F0'
    text-muted: '#D6DDD0'
    item-hover: '#5B6E52'
    item-active-background: '#FAF7F0'
    item-active-text: '#3E4E37'
    divider: '#6A7A61'
    count-background: '#F1D9A8'
    count-text: '#4A3108'
  focus:
    ring: '#4E6045'
    ring-on-nav: '#FAF7F0'
  status:
    success: '#3C7A4A'
    warning: '#B7791F'
    danger: '#B23A3A'
    danger-hover: '#962F2F'
    info: '#3B6E8F'
    neutral: '#6B6B6B'
  status-soft:
    success: '#E2EFE4'
    warning: '#FBEBD0'
    danger: '#F7E0E0'
    info: '#E0EBF2'
    neutral: '#EEEBE3'
  status-text:
    success: '#2B5E36'
    warning: '#6F4A0E'
    danger: '#8A2B2B'
    info: '#2C5670'
    neutral: '#4A4A4A'
font:
  family:
    heading: "'Playfair Display', Georgia, serif"
    body: "'Be Vietnam Pro', system-ui, sans-serif"
    decorative: "'Dancing Script', cursive"
  size:
    xs: 12px
    sm: 13px
    md: 15px
    lg: 17px
    xl: 22px
    xxl: 32px
    logo: 40px
  weight:
    regular: '400'
    medium: '500'
    semibold: '600'
    bold: '700'
line-height:
  tight: '1.25'
  normal: '1.5'
space:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  xxxl: 48px
radius:
  sm: 6px
  md: 8px
  lg: 12px
  pill: 999px
border-width:
  default: 1px
  focus: 2px
  accent: 3px
shadow:
  card: 0 1px 2px rgba(0, 0, 0, 0.04)
  overlay: 0 8px 24px rgba(0, 0, 0, 0.16)
size:
  control-sm: 32px
  control-md: 36px
  icon: 16px
  nav-width: 232px
  content-max: 1200px
opacity:
  disabled: '0.5'
duration:
  fast: 120ms
  normal: 200ms
breakpoint:
  mobile: 480px
  tablet: 768px
  desktop: 1280px
```

## Typography

- Tiêu đề trang: `font-family-heading`, `font-size-xxl`, `font-weight-bold`. Chỉ một tiêu đề Playfair mỗi màn hình.
- Tiêu đề khối (thẻ, nhóm cài đặt, hộp thoại): `font-family-body`, `font-size-lg`, `font-weight-bold`.
- Nội dung, ô nhập, mục điều hướng: `font-family-body`, `font-size-md`, `line-height-normal`.
- Nút, tab, chữ trong bảng dày: `font-size-sm` hoặc `font-size-md`, `font-weight-semibold` cho nút.
- Chú thích, nhãn phụ, thời gian: `font-size-sm`, `color-text-muted`.
- Badge, nhãn cột: `font-size-xs`, `font-weight-semibold`.
- Số liệu lớn (số liệu nhanh): `font-family-body`, `font-size-xxl`, `font-weight-bold`. Không dùng Playfair cho số: chữ số old-style của Playfair khó đọc ("Q11", "18").
- `font-family-decorative` chỉ dùng cho logo "Mio" ở thanh điều hướng và màn hình đăng nhập (`font-size-logo`), không dùng cho chữ cần đọc.

## Bố cục và breakpoint

- Khung chuẩn 1440×900:
  - thanh điều hướng trái rộng `size-nav-width`, nền `color-nav-background`, cố định khi cuộn;
  - vùng nội dung nền `color-surface-page`, lề `space-xxl` hai bên, rộng tối đa `size-content-max`.
- Đầu trang: tiêu đề trang + dòng phụ bên trái, hành động chính của trang bên phải.
- Khoảng cách giữa các thẻ: `space-lg`. Đệm trong thẻ: `space-lg` dọc, `space-xl` ngang.
- Lưới khoảng cách theo bội số `space-xs` (4px).
- Breakpoint định nghĩa sẵn cho giai đoạn responsive; hiện chưa thiết kế giao diện dưới `breakpoint-desktop`. Khi làm responsive: thanh điều hướng thu thành thanh dưới hoặc menu trượt, giữ nguyên màu.

## Component cơ bản

- **Thanh điều hướng:**
  - logo "Mio" (decorative) và dòng phụ `color-nav-text-muted`;
  - mục thường chữ `color-nav-text`, hover nền `color-nav-item-hover`;
  - mục đang chọn nền `color-nav-item-active-background`, chữ `color-nav-item-active-text`, `font-weight-semibold`;
  - số việc chờ: viên `color-nav-count-background` / `color-nav-count-text`;
  - nhóm Cài đặt, Nhật ký hệ thống tách bằng đường `color-nav-divider`.
- **Nút:** biến thể
  - `primary`: nền `color-brand-primary-strong`, chữ `color-text-on-primary`; hover nền `color-brand-primary-stronger`;
  - `secondary`: nền thẻ, viền và chữ `color-brand-primary-strong`; hover nền `color-brand-primary-soft`;
  - `danger`: nền `color-status-danger`; hover `color-status-danger-hover`. Dùng cho Dừng khẩn cấp, xóa;
  - `ghost`: không nền, chữ `color-brand-primary-strong`; hover nền `color-brand-primary-soft`;
  - cỡ `md` cao `size-control-md`, cỡ `sm` cao `size-control-sm` (nút trong dòng danh sách); bo `radius-sm`;
  - trạng thái: bình thường, hover, focus, disabled, loading.
- **Ô nhập:** text, số, chọn, giờ, vùng văn bản; cao `size-control-md`, viền `color-control-border`, bo `radius-sm`.
  - Nhãn phía trên ô, gợi ý phía dưới (`font-size-sm`, `color-text-muted`).
  - Giờ luôn hiển thị dạng 24 giờ `HH:mm`, không phụ thuộc ngôn ngữ trình duyệt (ô giờ gốc của trình duyệt có thể hiện AM/PM).
  - Trạng thái: bình thường, hover (viền `color-control-border-hover`), focus, lỗi (viền và thông báo `color-status-danger`, thông báo ngay dưới ô thay chỗ gợi ý), disabled (nền `color-control-background-disabled`).
- **Công tắc và ô chọn:** công tắc cho bật/tắt có hiệu lực ngay (cài đặt), ô chọn cho chọn nhiều. Bật: nền `color-brand-primary-strong`.
- **Tab:** chữ `color-text-muted`; tab đang chọn chữ `color-brand-primary-strong`, gạch dưới `border-width-focus` màu `color-brand-primary`. Có số đếm bên cạnh nhãn.
- **Thẻ:** nền `color-surface-card`, viền `color-surface-border`, bo `radius-md`, bóng `shadow-card`. Ô trích dẫn nội dung trong thẻ (comment đề xuất) nền `color-surface-page`.
- **Thông báo:**
  - banner trong trang: nền `color-status-soft-*`, chữ `color-status-text-*`, vạch trái `border-width-accent` màu `color-status-*`;
  - toast: góc dưới phải, nền thẻ, bóng `shadow-overlay`, vạch trái như banner; tự ẩn sau vài giây trừ loại danger.
- **Badge:** nền `color-status-soft-*`, chữ `color-status-text-*`, bo `radius-pill`. Nhóm: success (đã xong, đang chạy), warning (chờ duyệt, chờ thợ), danger (thất bại, bị dừng), info (loại bài, đã nhắc), neutral (khung bận, bỏ qua).
- **Thanh tiến độ:** rãnh `color-surface-divider`, phần đã dùng `color-brand-primary`; gần chạm giới hạn (≥ 90%) đổi sang `color-status-warning`. Luôn kèm số "18 / 40".

## Trạng thái tương tác

- Focus luôn nhìn thấy được: viền ngoài `border-width-focus` màu `color-focus-ring`, cách `space-xxs`; trên thanh điều hướng dùng `color-focus-ring-on-nav`.
- Hover: đổi nền theo từng component ở trên, chuyển màu trong `duration-fast`.
- Disabled: độ mờ `opacity-disabled`, con trỏ `not-allowed`, không đổi bố cục.
- Loading: giữ kích thước nút, hiện vòng xoay cỡ `size-icon` cạnh chữ, chữ đổi sang dạng đang làm ("Đang lưu…"), không bấm được.

## Khả năng truy cập

- Tương phản chữ thường tối thiểu 4.5:1, chữ lớn 3:1. Đã kiểm các cặp chính:
  - chữ trên nền trang, thẻ, nền phụ: 4.6–13.2:1;
  - chữ trên nút primary, danger, thanh điều hướng (kể cả chữ phụ, hover), mục đang chọn: 4.9–8.9:1;
  - chữ badge, banner trên nền status-soft: 6.4–9.0:1.
- Viền ô nhập và thành phần điều khiển tối thiểu 3:1 với nền (`color-control-border` 3.67:1). `color-surface-border` chỉ để trang trí thẻ, không dùng cho ô nhập.
- Vùng bấm tối thiểu 32×32px trên máy tính (44×44px khi làm responsive).
- Không truyền đạt trạng thái chỉ bằng màu: badge luôn có chữ, thanh tiến độ luôn có số.

## Lịch sử thay đổi

- 2026-10-29: tạo mới
