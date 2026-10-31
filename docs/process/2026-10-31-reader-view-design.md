# Thiết kế bản cho người đọc (reader view)

- **Ngày:** 31/10/2026
- **Phạm vi:** tài liệu do bộ skill của dự án sinh ra (`docs/phases/`, `docs/design/`, `docs/decisions/`, `docs/testing/`)
- **Trạng thái:** chờ review
- **Liên quan:** `docs/process/2026-10-29-dev-process-skills-design.md`

---

## Tóm tắt

- Tài liệu do skill sinh ra hiện viết cho AI đọc: dùng mã số để tham chiếu (`R-AUT-06`, `P0-AUT-012`), văn kiểu ghi chú, tên biến chen vào câu. Người review phải tra mã qua lại giữa nhiều file và tốn nhiều thời gian.
- **Bản gốc giữ nguyên như hiện tại.** Mã số hoạt động như tên biến: một ý định nghĩa một lần, nơi khác trỏ tới bằng mã. Nhờ vậy AI tra cứu và cập nhật không bị sót.
- Mỗi tài liệu có thêm một **bản cho người đọc**, sinh tự động, không bao giờ sửa tay:
  - AI viết lại câu chữ theo một hướng dẫn viết chung;
  - script chèn ý nghĩa của mã ngay tại chỗ dùng, triển khai viết tắt, tạo link;
  - script kiểm tra bản đọc không thiếu mã, con số, câu nguyên văn nào của bản gốc;
  - xuất cả Markdown (commit) và HTML (rê chuột xem ý nghĩa mã, không commit).
- Skill mới `reader-view` làm việc này. 18 skill có ghi tài liệu gọi nó trước mỗi điểm dừng, nên lúc duyệt bản đọc luôn mới.
- Lần duyệt vẫn ghi cho bản gốc. Bản đọc chỉ là cách đọc bản gốc dễ hơn.

---

## 1. Vấn đề

Đọc `docs/phases/phase-0/design/auth.md` và `test/cases/auth.md` thấy hai nhóm vấn đề.

### Tra mã
- Mã thay cho ý nghĩa: `(R-AUT-01 … R-AUT-04, R-AUT-07)`, `Thiết kế: R-AUT-08, R-AUT-09, R-AUT-28`.
- Trỏ sang chỗ khác thay vì nói luôn: "mục Trạng thái và thuật toán", "câu hỏi mở 7", "ADR 0011".
- Viết tắt riêng của tài liệu: `<api>`, `<psql>`, `<id mio>`.

### Câu chữ và trình bày
1. Một câu nhồi nhiều ý, nối bằng dấu chấm phẩy và ngoặc lồng.
2. Văn kiểu ghi chú, thiếu chủ ngữ và động từ, dùng ký hiệu thay chữ ("đang khóa → trả khóa").
3. Tên biến chen dày vào câu tiếng Việt.
4. Chi tiết đứng trước tổng quan, thiếu lý do.
5. Danh sách lồng sâu, mỗi gạch đầu dòng dài.

### Vì sao không sửa thẳng bản gốc
Chép ý nghĩa của mã ra mọi chỗ dùng nghĩa là nhân bản thông tin. Khi một quy tắc đổi, `change-request` phải sửa mọi bản chép; sót một chỗ là tài liệu tự mâu thuẫn. Bản gốc vì vậy giữ kiểu chuẩn hóa như hiện tại.

---

## 2. Nguyên tắc

- **Bản gốc là nguồn duy nhất.** Mọi skill đọc và ghi bản gốc. Không skill nào đọc bản đọc làm input.
- **Bản đọc chỉ được sinh ra.** Muốn sửa nội dung thì sửa bản gốc rồi sinh lại. Đầu mỗi bản đọc ghi "Không sửa tay".
- **AI lo câu chữ, script lo phần cần chính xác.** Ý nghĩa của mã, link, viết tắt do script chèn theo quy tắc cố định. AI không tự chú thích mã.
- **Không mất thông tin.** Script kiểm tra độ trung thực sau mỗi lần sinh (mục 6).
- **Duyệt bản gốc qua bản đọc.** Lần duyệt ghi vào `status.md` như cũ.

---

## 3. Ví dụ

### Bản gốc (giữ nguyên)

```markdown
- R-AUT-06: Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên không tồn tại, để không lộ tên nào có thật):
  - 5 lần sai trong cửa sổ 15 phút (tính từ lần sai đầu của cửa sổ) → khóa 15 phút; lần sai thứ 5 trả ngay 429;
  - đang khóa: mọi lần đăng nhập tên đó (kể cả đúng mật khẩu) → 429 `LOGIN_LOCKED`, "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (cùng câu cho màn Đăng nhập và Đổi mật khẩu, R-AUT-20), …
```

### Bản đọc (Markdown)

Phần *nghiêng trong ngoặc* sau mã do script chèn.

```markdown
### R-AUT-06: Giới hạn số lần đăng nhập sai

**Tóm tắt.** Một tên đăng nhập bị nhập sai mật khẩu 5 lần trong vòng 15 phút thì bị khóa 15 phút.

**Vì sao.** Để chặn việc đoán mật khẩu bằng cách thử liên tục. Bộ đếm áp dụng cả với tên đăng nhập không tồn tại, nên người dò không biết được tên nào có thật.

**Cách hoạt động**
- Bộ đếm tính theo tên đăng nhập đã chuẩn hóa, xem R-AUT-07 *(Tên đăng nhập được chuẩn hóa)*.
- Trong thời gian bị khóa, mọi lần đăng nhập bằng tên đó đều bị từ chối, kể cả khi nhập đúng mật khẩu. …

**Chi tiết kỹ thuật**
- Lỗi trả về: 429 `LOGIN_LOCKED`. …
```

Bản HTML có cùng nội dung; ý nghĩa của mã hiện khi rê chuột, mã là link tới chỗ định nghĩa.

---

## 4. Hướng dẫn viết (`docs/process/writing-guide.md`)

AI đọc file này mỗi lần viết bản đọc.

### Trình bày
- Mỗi mục lớn (quy tắc, test case, task, vấn đề, quyết định) mở đầu bằng **Tóm tắt** một đến hai câu.
- Có **Vì sao** khi bản gốc nêu lý do. Không tự bịa lý do bản gốc không có.
- Thứ tự: tóm tắt → vì sao → cách hoạt động → chi tiết kỹ thuật.
- Tên hàm, class, lệnh SQL, header HTTP, cấu hình dồn vào phần **Chi tiết kỹ thuật** của mục đó.
- Danh sách lồng tối đa hai cấp.
- Test case: "Kiểm tra điều gì", "Chuẩn bị", "Các bước", mỗi bước tách "thao tác" và "Mong đợi".

### Câu chữ
- Mỗi câu một ý. Câu có chủ ngữ và động từ.
- Không dùng ký hiệu thay chữ: không "→", "≈", "…" trong câu văn (vẫn giữ trong `code` và câu nguyên văn).
- Viết tắt riêng của tài liệu (`<api>`, `<psql>`…) không xuất hiện trong bản đọc; script triển khai chúng (mục 5.3).
- Theo `vietnamese-tech-writing`: văn phong khách quan, không xưng "bạn" trong tài liệu thiết kế; giữ thuật ngữ tiếng Anh mà kỹ sư Việt quen dùng (`transaction`, `cookie`, `deploy`); Unicode NFC.

### Bất biến (script kiểm tra)
- Giữ nguyên mọi mã, con số, câu trong ngoặc kép, đoạn `code`, đường dẫn của bản gốc.
- Không thêm thông tin bản gốc không có.
- Không tự chú thích ý nghĩa của mã.

---

## 5. Script (`tools/reader/`)

Python, có pytest như các script khác trong `tools/`.

### 5.1 `id_index`: bảng mã → ý nghĩa
Quét mọi bản gốc trong phạm vi, lập bảng: mã → ý nghĩa ngắn, file, anchor.

Các loại mã:
- quy tắc `R-<ABC>-<nn>`: dòng `- R-<ABC>-<nn>: …`;
- test case `P<N>-<ABC>-<nnn>`, vấn đề `P<N>-ISS-<nnn>`: heading `## <mã> <tiêu đề>`;
- task `T<nn>`: heading `### T<nn> <tiêu đề>` trong `plan.md` (phạm vi một giai đoạn);
- quyết định `ADR NNNN` / `NNNN-<slug>`: tiêu đề file trong `docs/decisions/`;
- điểm review `RV-<nn>`, "câu hỏi mở <n>": phạm vi một file;
- khoảng mã `R-AUT-01 … R-AUT-04`: triển khai thành từng mã.

Ý nghĩa ngắn lấy cố định:
- heading: phần tiêu đề sau mã;
- dòng định nghĩa: phần sau dấu hai chấm, bỏ mọi đoạn trong ngoặc đơn, cắt ở ký tự đầu tiên trong `→ : ; . ,`, tối đa 60 ký tự (dài hơn thì cắt và thêm "…").
- Ví dụ: `R-AUT-28: Chưa đăng nhập (GET … trả 401) mà mở trang cần đăng nhập → chuyển …` thành "Chưa đăng nhập mà mở trang cần đăng nhập".

Mã được dùng mà không tìm thấy định nghĩa: ghi cảnh báo, không chèn ý nghĩa.

### 5.2 `sections`: chia mục và băm
- Chia bản gốc theo heading cấp 2 và 3. Mỗi mục có hash nội dung.
- Bản viết lại của AI lưu trong `docs/reader/_rewrite/<đường dẫn>.md`, mỗi mục kèm dòng ẩn `<!-- src: <hash mục gốc> -->`.
- Lần sau chỉ những mục có hash đổi (hoặc mục mới) phải viết lại. Mục bị xóa ở bản gốc thì xóa khỏi bản viết lại.

### 5.3 `expand`: sinh bản đọc Markdown
Từ `_rewrite` sinh `docs/reader/<đường dẫn>.md`:
- sau mỗi mã chèn ` *(<ý nghĩa ngắn>)*`, mỗi mã một lần trong một đoạn;
- mã và "mục X" thành link Markdown tới file bản đọc chứa định nghĩa;
- viết tắt khai báo trong bản gốc (dạng `` `<tên>` = `<giá trị>` ``) được thay bằng giá trị đầy đủ;
- dòng đầu: `> Bản đọc sinh từ <đường dẫn gốc> (phiên bản <hash 7 ký tự>, <thời điểm>). Không sửa tay.`

`expand` luôn chạy lại cho mọi bản đọc mỗi lần `reader-view` chạy, vì ý nghĩa của mã ở file khác có thể đã đổi. Việc này không cần AI.

### 5.4 `fidelity`: kiểm tra độ trung thực
So bản gốc với bản đọc. Mọi phần tử sau của bản gốc phải có trong bản đọc (so sau khi chuẩn hóa NFC và khoảng trắng):
- mã (mọi loại ở 5.1);
- con số (kể cả số có đơn vị: `15 phút`, `429`, `32 ký tự`);
- chuỗi trong ngoặc kép;
- đoạn `code`;
- đường dẫn file và URL.

Thiếu thì in danh sách theo mục và trả mã lỗi 1. Ví dụ:
```text
design/auth.md – bản đọc thiếu 2 mục so với bản gốc:
- con số "128" (mục R-AUT-04)
- chuỗi "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (mục R-AUT-06)
```

### 5.5 `stale`: phát hiện bản đọc cũ
Liệt kê bản gốc chưa có bản đọc, hoặc có hash khác hash ghi ở dòng đầu bản đọc.

### 5.6 `render_html`: sinh HTML
- Từ `docs/reader/**/*.md` sinh `docs/reader/html/**/*.html` và `index.html` (danh sách tài liệu theo thư mục).
- Ý nghĩa chèn trong ngoặc được đổi thành tooltip trên mã; mã và tham chiếu là link.
- Bản đọc cũ (theo `stale`) có dải cảnh báo ở đầu trang.
- Dùng màu và font từ `docs/design/ui-tokens.css`.

---

## 6. Skill `reader-view`

- **Lệnh:** `/reader-view <file> [<file>…]`, `/reader-view phase-N` (mọi tài liệu của giai đoạn), `/reader-view all`.
- **Các bước:**
  1. Chạy `sections` để biết mục nào cần viết lại.
  2. AI viết lại các mục đó theo `writing-guide.md`, ghi vào `_rewrite`.
  3. Kiểm tra câu chữ theo `vietnamese-tech-writing` (văn phong, thuật ngữ, NFC).
  4. Chạy `expand` cho mọi bản đọc.
  5. Chạy `fidelity`. Lỗi thì AI sửa mục bị thiếu trong `_rewrite`, quay lại bước 4. Tối đa 3 vòng; vẫn lỗi thì dừng và báo.
  6. Chạy `render_html`.
  7. Báo link bản đọc Markdown và HTML của các file vừa sinh.
- **Không có điểm dừng riêng**; skill gọi nó tự dừng như cũ.

---

## 7. Tích hợp vào bộ skill

- 18 skill có ghi tài liệu thêm bước "gọi `reader-view` cho các file vừa ghi" ngay trước `## Điểm dừng`, và báo link bản đọc trong báo cáo kết thúc: `conventions-init`, `ui-style-init`, `ui-style-update`, `test-viewpoints-init`, `phase-kickoff`, `decision-log`, `detailed-design`, `ui-design`, `component-design`, `test-case-design`, `design-review`, `implementation-plan`, `implement-task`, `bug-fix`, `change-request`, `feedback`, `manual-test-run`, `acceptance-report`.
- `tdd` và `review-code` không ghi tài liệu, không đổi.
- `validate_skills.py` thêm kiểm tra: skill trong danh sách trên phải nhắc tới `reader-view`.
- `/phase-status` thêm dòng `Bản đọc đã cũ: <danh sách>` (dùng `stale`).
- `CLAUDE.md` thêm mục ngắn: bản đọc là gì, không sửa tay, không dùng làm input.
- `docs/process/skills-usage-guide.md` thêm mục hướng dẫn đọc bản đọc.

---

## 8. Phạm vi, lưu trữ, chuyển đổi

- **Bản gốc trong phạm vi:** mọi `.md` trong `docs/phases/`, `docs/design/`, `docs/decisions/`, `docs/testing/`. Không gồm `docs/project/`, `docs/process/`, `docs/story/` (người viết), `openapi.yaml`, `ui-tokens.css`, mockup HTML.
- **Lưu:**
  - `docs/reader/<đường dẫn tương đối so với docs/>`: bản đọc Markdown, commit;
  - `docs/reader/_rewrite/`: bản viết lại chưa chèn ý nghĩa, commit (cần cho viết lại từng phần);
  - `docs/reader/html/`: không commit, thêm vào `.gitignore`.
- **Tài liệu đã có** (39 file lúc viết spec): sau khi merge nhánh `process/reader-view` vào `main`, chạy `/reader-view all` một lần trên `main`. Chạy thử ngày 31/10/2026 với `design/auth.md` và `test/cases/auth.md` thật: `build` đạt kiểm tra trung thực, bản đọc Markdown và HTML đúng như ví dụ mục 3.
- **Chi phí:** mỗi điểm dừng tốn thêm token cho các mục vừa đổi. Viết lại theo mục (5.2) giữ chi phí tỷ lệ với lượng thay đổi.

---

## 9. Kiểm thử

- pytest cho từng script:
  - `id_index`: mọi loại mã ở 5.1, khoảng mã, mã phạm vi một file, quy tắc lấy ý nghĩa ngắn (ngoặc, ký tự cắt, 60 ký tự), mã không có định nghĩa;
  - `sections`: mục đổi, mục mới, mục bị xóa, CRLF/BOM;
  - `expand`: chèn một lần mỗi đoạn, link, triển khai viết tắt, dòng đầu;
  - `fidelity`: bắt thiếu mã, số, chuỗi, `code`, đường dẫn; không báo nhầm khi chỉ khác khoảng trắng hoặc NFC/NFD;
  - `stale`: thiếu bản đọc, hash khác;
  - `render_html`: tooltip, link, dải cảnh báo bản cũ.
- Validator: test cho kiểm tra mới ở mục 7.
- Chạy thử thật: `/reader-view all` trên 39 tài liệu hiện có; người dùng đọc thử `design/auth.md` và `test/cases/auth.md` bản đọc.

---

## 10. Quyết định và giả định

- Bản gốc giữ nguyên định dạng hiện tại (người dùng chốt).
- Bản đọc gồm Markdown và HTML (người dùng chốt).
- Bản đọc sinh qua skill `reader-view`, được gọi trước mỗi điểm dừng (người dùng chọn phương án A).
- Phần "lần này cần duyệt gì" nói trong chat ở điểm dừng, không lưu file.
- Quy tắc lấy ý nghĩa ngắn ở 5.1 là giả định của người viết; có thể chỉnh sau lần chạy thử.
- Viết lại tối đa 3 vòng khi `fidelity` báo lỗi (giả định của người viết).
