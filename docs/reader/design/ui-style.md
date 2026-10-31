> Bản đọc sinh từ docs/design/ui-style.md (phiên bản a6c6d45, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Style UI – Tiệm Nhà Mio

**Tóm tắt.** Đây là nguồn chính về style của toàn hệ thống. Hướng style là **kem ấm, sage nhấn, thanh điều hướng xanh đậm**.

**Cách dùng**
- File token CSS được sinh tự động từ [mục Tokens](#s-135863406d) bên dưới.
- Không sửa tay file token CSS. Muốn đổi giá trị thì sửa [mục Tokens](#s-135863406d) rồi sinh lại.

**Chi tiết kỹ thuật**
- `ui-tokens.css` được sinh từ khối `## Tokens` bằng `py tools/ui/gen_tokens.py`.
- Quyết định về hướng style: ADR `0008-ui-style-direction`.

<a id="s-e7e90ca7c2"></a>

## Nguyên tắc

**Tóm tắt.** Giao diện là giao diện vận hành trên máy tính. Giao diện ưu tiên dễ đọc, gọn, trạng thái rõ, và mọi giá trị đều lấy từ token.

**Nền tảng**
- Nền tảng hiện tại là web trên máy tính, với khung chuẩn 1440×900.
- Responsive và app native sẽ làm sau. Vì vậy token được đặt tên độc lập với nền tảng.

**Cách trình bày**
- Giao diện vận hành ưu tiên dễ đọc, dễ quét danh sách và trạng thái rõ ràng.
- Nhận diện của tiệm thể hiện ở màu, không thể hiện ở trang trí.
- Nền trang màu kem. Nội dung đặt trên thẻ trắng.
- Màu tiệm đậm nhất nằm ở thanh điều hướng và nút chính.
- Mật độ hiển thị gọn, vì danh sách và form cài đặt dài là loại màn hình chính.
- Mọi giá trị lấy từ token. Không viết cứng màu, cỡ chữ hay khoảng cách.

**Màu sage chỉ dùng để nhấn**
- Màu sage chỉ dùng để nhấn: gạch chân tab đang chọn, thanh tiến độ, vạch đánh dấu.
- Màu sage **không** dùng làm nền cho chữ.
- Vì sao: chữ trắng trên nền sage chỉ đạt độ tương phản 2.74:1.

**Chi tiết kỹ thuật**
- Màu sage là token `color-brand-primary`.

<a id="s-135863406d"></a>

## Tokens

**Tóm tắt.** Khối dưới đây là danh sách token gốc của toàn hệ thống: màu, font, cỡ chữ, khoảng cách, bo góc, viền, bóng, kích thước, độ mờ, thời lượng chuyển động và breakpoint. File `ui-tokens.css` được sinh từ khối này.

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

<a id="s-544f478473"></a>

## Typography

**Tóm tắt.** Mỗi loại chữ trên màn hình có font, cỡ và độ đậm riêng. Font tiêu đề Playfair chỉ dùng cho tiêu đề trang. Font trang trí chỉ dùng cho logo.

**Quy tắc**
- Mỗi màn hình chỉ có một tiêu đề dùng font Playfair, đó là tiêu đề trang.
- Không dùng Playfair cho số. Vì sao: chữ số old-style của Playfair khó đọc ("Q11", "18").
- Font trang trí chỉ dùng cho logo "Mio" ở thanh điều hướng và màn hình đăng nhập. Font này không dùng cho chữ cần đọc.

**Chi tiết kỹ thuật**
- Tiêu đề trang: `font-family-heading`, `font-size-xxl`, `font-weight-bold`.
- Tiêu đề khối (thẻ, nhóm cài đặt, hộp thoại): `font-family-body`, `font-size-lg`, `font-weight-bold`.
- Nội dung, ô nhập, mục điều hướng: `font-family-body`, `font-size-md`, `line-height-normal`.
- Nút, tab, chữ trong bảng dày: `font-size-sm` hoặc `font-size-md`. Nút dùng thêm `font-weight-semibold`.
- Chú thích, nhãn phụ, thời gian: `font-size-sm`, `color-text-muted`.
- Badge, nhãn cột: `font-size-xs`, `font-weight-semibold`.
- Số liệu lớn (số liệu nhanh): `font-family-body`, `font-size-xxl`, `font-weight-bold`.
- Logo: `font-family-decorative`, cỡ `font-size-logo`.

<a id="s-f30a0eaf89"></a>

## Bố cục và breakpoint

**Tóm tắt.** Màn hình chuẩn gồm thanh điều hướng cố định bên trái và vùng nội dung bên phải. Mọi khoảng cách theo lưới 4px.

**Cách bố trí**
- Khung chuẩn 1440×900 gồm hai phần:
  - thanh điều hướng bên trái, cố định khi cuộn;
  - vùng nội dung, có lề hai bên và giới hạn độ rộng tối đa.
- Đầu trang có tiêu đề trang và dòng phụ ở bên trái. Hành động chính của trang nằm bên phải.
- Lưới khoảng cách theo bội số 4px.

**Breakpoint**
- Breakpoint được định nghĩa sẵn cho giai đoạn responsive.
- Hiện chưa thiết kế giao diện cho màn hình hẹp hơn breakpoint desktop.
- Khi làm responsive, thanh điều hướng thu thành thanh dưới hoặc menu trượt. Màu vẫn giữ nguyên.

**Chi tiết kỹ thuật**
- Thanh điều hướng: rộng `size-nav-width`, nền `color-nav-background`.
- Vùng nội dung: nền `color-surface-page`, lề `space-xxl` hai bên, rộng tối đa `size-content-max`.
- Khoảng cách giữa các thẻ: `space-lg`.
- Đệm trong thẻ: `space-lg` theo chiều dọc, `space-xl` theo chiều ngang.
- Đơn vị lưới: `space-xs` (4px).
- Breakpoint chưa thiết kế: dưới `breakpoint-desktop`.

<a id="s-4f1091ba96"></a>

## Component cơ bản

**Tóm tắt.** Mục này mô tả các component dùng chung: thanh điều hướng, nút, ô nhập, công tắc và ô chọn, tab, thẻ, thông báo, badge, thanh tiến độ. Token cụ thể của từng component nằm trong phần Chi tiết kỹ thuật.

### Thanh điều hướng

- Đầu thanh có logo "Mio" (font trang trí) và một dòng phụ.
- Mục thường đổi nền khi hover.
- Mục đang chọn có nền và màu chữ riêng, chữ đậm vừa.
- Số việc chờ hiện trong một viên tròn cạnh mục.
- Nhóm Cài đặt và Nhật ký hệ thống được tách ra bằng một đường kẻ.

**Chi tiết kỹ thuật**
- Dòng phụ: `color-nav-text-muted`.
- Mục thường: chữ `color-nav-text`, hover nền `color-nav-item-hover`.
- Mục đang chọn: nền `color-nav-item-active-background`, chữ `color-nav-item-active-text`, `font-weight-semibold`.
- Viên số việc chờ: `color-nav-count-background` / `color-nav-count-text`.
- Đường kẻ tách nhóm: `color-nav-divider`.

### Nút

- Có 4 biến thể: primary, secondary, danger, ghost.
- Nút danger dùng cho Dừng khẩn cấp và xóa.
- Có 2 cỡ. Cỡ nhỏ dùng cho nút trong dòng danh sách.
- Nút có các trạng thái: bình thường, hover, focus, disabled, loading.

**Chi tiết kỹ thuật**
- `primary`: nền `color-brand-primary-strong`, chữ `color-text-on-primary`; hover nền `color-brand-primary-stronger`.
- `secondary`: nền thẻ, viền và chữ `color-brand-primary-strong`; hover nền `color-brand-primary-soft`.
- `danger`: nền `color-status-danger`; hover `color-status-danger-hover`.
- `ghost`: không nền, chữ `color-brand-primary-strong`; hover nền `color-brand-primary-soft`.
- Cỡ `md` cao `size-control-md`. Cỡ `sm` cao `size-control-sm`. Bo góc `radius-sm`.

### Ô nhập

- Các loại ô nhập: text, số, chọn, giờ, vùng văn bản.
- Nhãn nằm phía trên ô. Gợi ý nằm phía dưới ô, chữ nhỏ và nhạt.
- Giờ luôn hiển thị dạng 24 giờ, không phụ thuộc ngôn ngữ trình duyệt. Vì sao: ô giờ gốc của trình duyệt có thể hiện AM/PM.
- Ô nhập có các trạng thái: bình thường, hover, focus, lỗi, disabled.
- Khi lỗi, viền và thông báo chuyển màu danger. Thông báo lỗi nằm ngay dưới ô, thay chỗ gợi ý.

**Chi tiết kỹ thuật**
- Kích thước và viền: cao `size-control-md`, viền `color-control-border`, bo `radius-sm`.
- Gợi ý: `font-size-sm`, `color-text-muted`.
- Định dạng giờ: `HH:mm`.
- Hover: viền `color-control-border-hover`.
- Lỗi: viền và thông báo `color-status-danger`.
- Disabled: nền `color-control-background-disabled`.

### Công tắc và ô chọn

- Công tắc dùng cho bật/tắt có hiệu lực ngay, ví dụ trong cài đặt.
- Ô chọn dùng khi được chọn nhiều mục.

**Chi tiết kỹ thuật**
- Trạng thái bật: nền `color-brand-primary-strong`.

### Tab

- Tab thường có chữ nhạt. Tab đang chọn có chữ màu tiệm và gạch dưới màu sage.
- Bên cạnh nhãn tab có số đếm.

**Chi tiết kỹ thuật**
- Tab thường: chữ `color-text-muted`.
- Tab đang chọn: chữ `color-brand-primary-strong`, gạch dưới `border-width-focus` màu `color-brand-primary`.

### Thẻ

- Thẻ có nền trắng, viền mảnh, bo góc và bóng nhẹ.
- Ô trích dẫn nội dung trong thẻ (ví dụ comment đề xuất) dùng nền màu trang.

**Chi tiết kỹ thuật**
- Thẻ: nền `color-surface-card`, viền `color-surface-border`, bo `radius-md`, bóng `shadow-card`.
- Ô trích dẫn: nền `color-surface-page`.

### Thông báo

- Có hai loại: banner trong trang và toast.
- Banner có nền nhạt, chữ đậm màu và vạch màu ở cạnh trái, theo mức độ của thông báo.
- Toast hiện ở góc dưới bên phải, nền thẻ, có bóng và vạch trái như banner.
- Toast tự ẩn sau vài giây, trừ loại danger.
- Quy tắc đặt thông báo ở đâu nằm ở mục "Vị trí thông báo".

**Chi tiết kỹ thuật**
- Banner: nền `color-status-soft-*`, chữ `color-status-text-*`, vạch trái `border-width-accent` màu `color-status-*`.
- Toast: bóng `shadow-overlay`.

### Badge

- Badge có nền nhạt, chữ đậm màu và bo tròn hai đầu.
- Badge chia theo nhóm trạng thái:
  - success: đã xong, đang chạy;
  - warning: chờ duyệt, chờ thợ;
  - danger: thất bại, bị dừng;
  - info: loại bài, đã nhắc;
  - neutral: khung bận, bỏ qua.

**Chi tiết kỹ thuật**
- Badge: nền `color-status-soft-*`, chữ `color-status-text-*`, bo `radius-pill`.

### Thanh tiến độ

- Thanh gồm rãnh nền và phần đã dùng màu sage.
- Khi gần chạm giới hạn (từ 90% trở lên), phần đã dùng đổi sang màu warning.
- Thanh luôn kèm số, ví dụ "18 / 40".

**Chi tiết kỹ thuật**
- Rãnh: `color-surface-divider`.
- Phần đã dùng: `color-brand-primary`.
- Gần chạm giới hạn: `color-status-warning`.

<a id="s-a675c315d5"></a>

## Vị trí thông báo

**Tóm tắt.** Mục này quy định mỗi loại thông báo hiện ở đâu trên màn hình. Quy ước áp dụng chung cho mọi màn hình.

**Lỗi theo trường**
- Lỗi của một trường hiện ngay dưới ô, thay chỗ gợi ý (xem phần Ô nhập).

**Thông báo cấp form**
- Đây là kết quả gửi form không gắn với một trường cụ thể. Ví dụ: lỗi nghiệp vụ, bị khóa, lỗi hệ thống, mất mạng. Thông báo info hiện khi vừa chuyển tới trang cũng thuộc loại này.
- Mỗi form có một **vùng thông báo** duy nhất. Vùng này nằm ngay sau trường cuối cùng, trước hàng nút gửi.
- Vùng thông báo hiện mọi thông báo còn đúng. Mỗi thông báo là một banner.
- Các banner xếp theo mức độ: danger trước, rồi warning, rồi info. Giữa các banner có một khoảng cách nhỏ.
- Mỗi lần bấm gửi, toàn bộ banner cũ bị xóa trước khi hiện kết quả mới.
- Thông báo không lặp: cùng một nội dung chỉ có một banner.
- Banner được đánh dấu để trình đọc màn hình đọc ngay.

**Hộp thoại**
- Hộp thoại dùng cùng quy tắc với form. Vùng thông báo nằm ngay trên hàng nút.
- Nếu gửi bị lỗi khi hộp thoại đã đóng (ví dụ Đổi mật khẩu), thông báo hiện ở vùng thông báo của form gốc.

**Thông báo cấp trang**
- Đây là trạng thái hệ thống, không gắn với form nào. Ví dụ: "Đã tự dừng".
- Thông báo cấp trang là banner nằm dưới đầu trang, trên phần nội dung.

**Thành công**
- Thông báo thành công dùng toast.
- Không dùng banner success trong form, trừ khi thông báo phải ở lại trên trang.

**Lỗi khi thao tác không có form**
- Ví dụ: nút trong danh sách, công tắc có hiệu lực ngay.
- Lỗi loại này hiện bằng toast danger.

**Câu chữ**
- Một thông báo dùng chung cho nhiều màn hình hoặc nhiều endpoint phải đúng nghĩa ở mọi chỗ nó hiện.
- Nếu không đúng nghĩa ở mọi chỗ, cần viết câu trung tính hoặc tách thành câu riêng.

**Chi tiết kỹ thuật**
- Quyết định: ADR `0016-form-message-placement`.
- Mockup minh họa nằm trong `ui-style-preview.html`, mục "Vị trí thông báo".
- Khoảng cách giữa các banner: `space-sm`.
- Banner danger, warning có `role="alert"`. Banner info có `role="status"`.

<a id="s-adfcc4d297"></a>

## Trạng thái tương tác

**Tóm tắt.** Mục này quy định cách hiển thị bốn trạng thái tương tác chung: focus, hover, disabled và loading.

**Cách hiển thị**
- Focus: phần tử đang focus luôn nhìn thấy được nhờ một viền ngoài. Trên thanh điều hướng, viền này dùng màu riêng.
- Hover: nền đổi màu theo quy định của từng component ở trên. Màu chuyển nhanh.
- Disabled: phần tử bị làm mờ và con trỏ đổi sang dạng không cho bấm. Bố cục không thay đổi.
- Loading: nút giữ nguyên kích thước và hiện vòng xoay cạnh chữ. Chữ đổi sang dạng đang làm ("Đang lưu…"). Nút không bấm được trong lúc này.

**Chi tiết kỹ thuật**
- Focus: viền ngoài `border-width-focus` màu `color-focus-ring`, cách `space-xxs`; trên thanh điều hướng dùng `color-focus-ring-on-nav`.
- Hover: chuyển màu trong `duration-fast`.
- Disabled: độ mờ `opacity-disabled`, con trỏ `not-allowed`.
- Loading: vòng xoay cỡ `size-icon`.

<a id="s-2f0f72e8eb"></a>

## Khả năng truy cập

**Tóm tắt.** Giao diện phải đủ tương phản, có vùng bấm đủ lớn và không truyền đạt trạng thái chỉ bằng màu.

**Độ tương phản của chữ**
- Chữ thường cần độ tương phản tối thiểu 4.5:1. Chữ lớn cần tối thiểu 3:1.
- Các cặp màu chính đã được kiểm:
  - chữ trên nền trang, thẻ và nền phụ đạt 4.6–13.2:1;
  - chữ trên nút primary, nút danger, thanh điều hướng (kể cả chữ phụ và hover) và mục đang chọn đạt 4.9–8.9:1;
  - chữ của badge và banner trên nền status-soft đạt 6.4–9.0:1.

**Viền ô nhập**
- Viền ô nhập và thành phần điều khiển cần độ tương phản tối thiểu 3:1 so với nền.
- Màu viền trang trí của thẻ không dùng cho ô nhập.

**Vùng bấm**
- Vùng bấm tối thiểu 32×32px trên máy tính.
- Khi làm responsive, vùng bấm tối thiểu 44×44px.

**Không chỉ dùng màu**
- Trạng thái không được truyền đạt chỉ bằng màu.
- Badge luôn có chữ. Thanh tiến độ luôn có số.

**Chi tiết kỹ thuật**
- Viền ô nhập: `color-control-border` đạt 3.67:1.
- Viền chỉ để trang trí thẻ: `color-surface-border`.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-29: tạo mới.
- 2026-10-31: thêm mục "Vị trí thông báo". Token không thay đổi.
  - Lý do: góp ý khi duyệt UI của `auth`. Banner ở đầu form dễ bị bỏ qua. Câu thông báo dùng chung bị sai nghĩa ở màn khác.
  - Quyết định: ADR `0016-form-message-placement`.
