# Tiệm Nhà Mio – Business Operations Platform

Web app nội bộ tự động hóa marketing cho Tiệm Nhà Mio. Thiết kế khái quát: `docs/project/`. Quy trình phát triển: `docs/process/2026-10-29-dev-process-skills-design.md`.

## Ưu tiên skill

- Trong repo này, skill của dự án (`.claude/skills/`) được ưu tiên hơn mọi skill khác, kể cả superpowers.
- Không dùng `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development` của superpowers cho công việc phát triển hệ thống. Dùng skill tương ứng của dự án.

## Vòng đời

Mỗi giai đoạn trong `docs/project/05-roadmap.md` đi theo thứ tự:

```text
/phase-kickoff
  → (từng tính năng) /detailed-design → /ui-design (nếu có màn hình, gọi /component-design khi cần)
     → /test-case-design → /design-review
  → /implementation-plan
  → (từng task) /implement-task → /review-code
  → (từng tính năng) /manual-test-run → [/feedback | /bug-fix → /manual-test-run --retest]
  → /acceptance-report
```

- Nhánh phụ dùng bất kỳ lúc nào: `/feedback`, `/change-request`, `/decision-log`, `/phase-status`.
- Nhóm khởi tạo chạy một lần trước giai đoạn 0: `/conventions-init` → `/ui-style-init` → `/test-viewpoints-init`. Đổi style về sau: `/ui-style-update`.
- Skill nào cũng kiểm tra điều kiện tiên quyết qua `docs/phases/phase-N/status.md` trước khi làm. Chưa thỏa thì dừng và báo, không tự nhảy bước.

## Điểm dừng

- Tại điểm dừng, dừng hẳn và chờ người dùng duyệt rõ ràng.
- Lần duyệt được ghi vào `## Nhật ký duyệt` của `status.md` kèm ngày.
- Duyệt một bước không có nghĩa là duyệt các bước sau.

## Ngôn ngữ và định dạng

- Tên file, tên skill, mã định danh: tiếng Anh. Nội dung tài liệu: tiếng Việt.
- Ưu tiên heading và gạch đầu dòng. Chỉ dùng bảng khi dữ liệu thật sự là bảng (cột DB, bảng đối chiếu).
- Trả lời người dùng ngắn gọn, tập trung vào thông tin quan trọng.

## Mã định danh

- Giai đoạn: `phase-0` … `phase-4`.
- Tính năng: kebab-case, ví dụ `group-settings`; mã 3 chữ in hoa, ví dụ `GRP`.
- Quy tắc trong thiết kế: `R-<ABC>-<nn>`, ví dụ `R-GRP-03`.
- Test case: `P<N>-<ABC>-<nnn>`, ví dụ `P0-GRP-012`.
- Task code: `T<nn>`, ví dụ `T06`.
- Quyết định: `NNNN-<slug>`, ví dụ `0003-https-via-caddy`.
- Lần chạy test: `YYYY-MM-DD-NN`, ví dụ `2026-11-10-01`.
- Vấn đề: `P<N>-ISS-<nnn>`, ví dụ `P0-ISS-007`.

## Ghi quyết định

- Ghi ADR (`/decision-log`) khi quyết định chọn giữa nhiều phương án **và** ảnh hưởng rộng hơn một tính năng: thư viện, kiến trúc, quy ước chung, style.
- Quyết định chỉ thuộc một tính năng: ghi trong file thiết kế của tính năng đó.

## Dữ liệu thật và evidence

- Evidence không che thông tin; người dùng tự xóa sau khi xác nhận.
- Không bao giờ commit: `docs/phases/*/test/runs/*/evidence/`, `docs/phases/*/acceptance/*.xlsx`, `docs/phases/*/acceptance/*.pdf`, `.local/`.

## Báo cáo kết thúc

Mỗi skill kết thúc bằng 3 phần:
- đã làm gì và ghi vào file nào;
- cần người dùng quyết gì;
- bước tiếp theo là lệnh nào.

## Cấu trúc tài liệu

```text
docs/
├── project/            # thiết kế khái quát
├── process/            # quy trình phát triển
├── decisions/          # ADR
├── testing/viewpoints.md
├── design/             # dùng chung cả app: db-schema.md, api/, ui-style.md, ui-tokens.css, components/, ui/
└── phases/phase-N/     # status.md, design/, plan.md, issues.md, test/, acceptance/
tools/                  # script dùng chung: kiểm tra skill, sinh token, chụp mockup
```

- Kiểm tra skill: `py tools/skills/validate_skills.py`.
- Test của script: `py -m pytest tools .claude/skills -q`.

## Quy ước

Chưa chốt. Chạy `/conventions-init`.
