> Bản đọc sinh từ docs/phases/phase-0/design/reviews/app-skeleton-review.md (phiên bản 04ac225, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Review thiết kế – Khung ứng dụng (`app-skeleton`)

**Tóm tắt.** Bản review này soát thiết kế chi tiết và test case của khung ứng dụng. Tính năng này không có mockup. Review tìm ra 19 điểm (1 chặn, 13 nên sửa, 5 gợi ý), và tất cả đều đã được sửa.

- Ngày: 2026-10-29
- Đối tượng: thiết kế chi tiết, test case (không có mockup)
- Tổng: 19 điểm (1 chặn, 13 nên sửa, 5 gợi ý)

<a id="s-d56738b7bd"></a>

### RV-01 Job bị stalled vẫn được BullMQ chạy lại một lần

- Mức độ: chặn
- Vị trí: design/app-skeleton.md [R-SKL-07](../app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*, [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*, [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*; test [P0-SKL-060](../../test/cases/app-skeleton.md#s-2c9a4efd46 "Quá thời gian ân hạn: job dở dang thất bại, không chạy lại") *(Quá thời gian ân hạn: job dở dang thất bại, không chạy lại)*, [P0-SKL-061](../../test/cases/app-skeleton.md#s-43c4e46785 "Một worker chết giữa job, worker còn lại không chạy lại job…") *(Một worker chết giữa job, worker còn lại không chạy lại job…)*

**Tóm tắt.** Thiết kế cho rằng job dở dang bị stalled sẽ không chạy lại. Thực tế BullMQ vẫn chạy lại job đó một lần, nên có nguy cơ comment hai lần vào một bài.

**Vấn đề**
- Thiết kế viết rằng job dở dang bị đánh dấu stalled "không tự chạy lại vì `attempts: 1`".
- Thực tế, cấu hình số lần thử không áp dụng cho job stalled. Worker của BullMQ mặc định cho phép stalled 1 lần. Job stalled lần đầu được đưa lại hàng chờ và chạy lại. Chỉ khi stalled lần thứ hai, job mới chuyển sang thất bại.
- Với job comment ở giai đoạn 1, đây là đường dẫn tới comment hai lần vào một bài. Điều này vi phạm lằn ranh đỏ "kể cả khi retry".
- Nếu implement theo thiết kế hiện tại, [P0-SKL-060](../../test/cases/app-skeleton.md#s-2c9a4efd46 "Quá thời gian ân hạn: job dở dang thất bại, không chạy lại") *(Quá thời gian ân hạn: job dở dang thất bại, không chạy lại)* và [P0-SKL-061](../../test/cases/app-skeleton.md#s-43c4e46785 "Một worker chết giữa job, worker còn lại không chạy lại job…") *(Một worker chết giữa job, worker còn lại không chạy lại job…)* sẽ không đạt.

**Đề xuất**
- [R-SKL-07](../app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)* thêm quy tắc: mọi Worker (browser-worker và api) tắt cơ chế chạy lại job stalled. Job stalled chuyển thẳng sang thất bại, không quay về hàng chờ.
- Để thời gian giữ khóa của job ở mặc định (30 giây, tự gia hạn). Processor không được chặn event loop, để tránh stalled giả khi job vẫn đang chạy.
- Sửa câu trong [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)* và [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)* cho đúng cơ chế.
- Thêm test tự động (integration) "job stalled → failed, không chạy lần hai".

**Kết quả.** Đã sửa ([R-SKL-07](../app-skeleton.md#s-0f1edd606c "tùy chọn mặc định của mọi hàng đợi") *(tùy chọn mặc định của mọi hàng đợi)*, [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*, [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*; [P0-SKL-057](../../test/cases/app-skeleton.md#s-a8527a39a1 "Tùy chọn job mặc định") *(Tùy chọn job mặc định)*, Ghi chú chạy: test tự động).

**Chi tiết kỹ thuật**
- Cấu hình số lần thử: `attempts`.
- Số lần stalled cho phép: `maxStalledCount`, mặc định 1. Đề xuất đặt `maxStalledCount: 0`.
- Job stalled lần đầu quay về trạng thái `wait`. Lần thứ hai chuyển sang `failed`.
- Thời gian giữ khóa: `lockDuration`.

<a id="s-5fc3149518"></a>

### RV-02 Một job gốc có thể sinh hai tín hiệu kết quả

- Mức độ: nên sửa
- Vị trí: [R-SKL-28](../app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)*, [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*

**Tóm tắt.** Một job gốc có thể vừa gửi kết quả vừa bị báo thất bại. Thiết kế chưa quy định cách xử lý, nên thao tác ghi lên Facebook có thể bị làm hai lần.

**Vấn đề**
- Thiết kế chưa quy định trường hợp một job gốc có cả job kết quả lẫn sự kiện thất bại.
- Trường hợp này xảy ra theo hai cách:
  - processor ném lỗi sau khi đã gửi kết quả;
  - stalled giả: worker vẫn chạy nhưng mất lock. Api nhận lỗi worker sập, rồi sau đó worker vẫn gửi kết quả thật.
- Nếu tính năng coi lỗi worker sập là "chưa làm" và tự xếp lại việc, thao tác ghi lên Facebook (comment) có thể bị làm hai lần.

**Đề xuất.** Thêm vào [R-SKL-28](../app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)* và [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)* các quy tắc sau:
- Processor bắt mọi lỗi và luôn gửi job kết quả. Lỗi chưa phân loại được gửi với loại lỗi bất ngờ. Sau đó processor kết thúc job gốc bình thường.
- Job gốc chỉ thất bại khi không gửi được kết quả, tức là khi worker chết hoặc job bị stalled.
- Api xử lý kết quả theo mã job gốc và idempotent. Kết quả từ hàng đợi kết quả luôn thắng lỗi worker sập, dù kết quả tới sau.
- Lỗi worker sập nghĩa là "không rõ đã làm tới đâu". Tính năng có thao tác ghi lên Facebook không được coi đó là chưa làm để tự làm lại.

**Kết quả.** Đã sửa ([R-SKL-28](../app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)*, [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*; Ghi chú chạy: test tự động).

**Chi tiết kỹ thuật**
- Sự kiện thất bại: `failed`.
- Lỗi worker sập: `WorkerCrashedError`.
- Loại lỗi chưa phân loại: `type: 'UnexpectedError'`.
- Mã job gốc: `sourceJobId`.

<a id="s-3b1a2be3ca"></a>

### RV-03 R-SKL-29 dựa vào sự kiện nên mất tín hiệu khi api tắt

- Mức độ: nên sửa
- Vị trí: [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*; mục Job và hàng đợi

**Tóm tắt.** [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)* chỉ nghe sự kiện thất bại, nên sẽ bỏ lỡ tín hiệu nếu api đang tắt đúng lúc đó. Đề xuất thêm bước đối soát định kỳ.

**Vấn đề**
- [R-SKL-28](../app-skeleton.md#s-0f1edd606c "browser-worker trả kết quả bằng cách thêm job vào hàng đợi…") *(browser-worker trả kết quả bằng cách thêm job vào hàng đợi…)* bỏ cách dùng sự kiện hoàn thành vì "api tắt đúng lúc đó sẽ bỏ lỡ sự kiện".
- Nhưng [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)* lại dựa vào sự kiện thất bại. Mặc định, bộ nghe sự kiện chỉ đọc sự kiện mới.
- Nếu worker chết trong lúc api đang khởi động lại, job gốc thất bại mà không tính năng nào biết. Job quét group có thể chờ kết quả mãi.
- Ngoài ra, việc kiểm tra stalled chỉ do Worker chạy. Khi không còn browser-worker nào sống, job nằm ở trạng thái đang chạy vô thời hạn.

**Đề xuất.** Thêm vào [R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*:
- Ngoài việc nghe sự kiện, api đối soát lúc khởi động và mỗi 5 phút.
- Job thất bại của hàng đợi trình duyệt và hàng đợi inbox mà chưa được xử lý thì được xử lý như lỗi worker sập. Bước này dùng chung đường xử lý idempotent của [RV-02](#s-5fc3149518 "Một job gốc có thể sinh hai tín hiệu kết quả") *(Một job gốc có thể sinh hai tín hiệu kết quả)*.
- Job đang chạy khi khóa nhịp sống đã hết hạn: ghi rõ rằng cơ chế dừng khẩn cấp sẽ phát hiện và báo.
- Thêm test case: dừng api, giết worker giữa job, chạy lại api. Lượt quét phải ghi thất bại đúng một lần.

**Kết quả.** Đã sửa ([R-SKL-29](../app-skeleton.md#s-0f1edd606c "job gốc failed") *(job gốc failed)*, mục Tham số; [P0-SKL-069](../../test/cases/app-skeleton.md#s-3c1666c6f9 "Worker chết khi api đang tắt: job vẫn được ghi thất bại sau…") *(Worker chết khi api đang tắt: job vẫn được ghi thất bại sau…)*).

**Chi tiết kỹ thuật**
- Sự kiện hoàn thành: `completed`. Sự kiện thất bại: `failed`. Bộ nghe sự kiện: QueueEvents.
- Job quét group: `group-crawl-job`.
- Trạng thái đang chạy: `active`.
- Hàng đợi cần đối soát: `fb-browser` / `fb-inbox`.
- Lỗi worker sập: `WorkerCrashedError`.
- Cơ chế dừng khẩn cấp: `emergency-stop`.

<a id="s-3d8984a91b"></a>

### RV-04 Docker không tự khởi động lại container unhealthy; thiếu tham số healthcheck

- Mức độ: nên sửa
- Vị trí: mục Xử lý lỗi ("browser-worker chết → healthcheck không đạt, Compose khởi động lại"); [R-SKL-18](../app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*; mục Khởi động

**Tóm tắt.** Thiết kế cho rằng Docker Compose tự khởi động lại container không khỏe, nhưng điều này sai. Thiết kế cũng thiếu tham số healthcheck và khóa nhịp sống chưa tách theo tiến trình.

**Vấn đề**
- Restart policy hiện tại chỉ khởi động lại khi tiến trình thoát. Container bị treo, báo không khỏe nhưng vẫn chạy, sẽ không được Docker Compose khởi động lại. Câu trong thiết kế là sai.
- Chưa có tham số healthcheck cho 4 dịch vụ.
- Chưa có lệnh healthcheck cho api. Image Node bản slim không có sẵn công cụ gọi HTTP.
- Khóa nhịp sống dùng chung một tên. Khi chạy 2 browser-worker ([P0-SKL-058](../../test/cases/app-skeleton.md#s-d9052f5a3d "Hai tiến trình browser-worker vẫn chỉ chạy một job fb-brows…") *(Hai tiến trình browser-worker vẫn chỉ chạy một job fb-brows…)*), worker bị treo sẽ bị worker còn sống che đi và vẫn báo khỏe.

**Đề xuất**
- Sửa câu trong thiết kế:
  - tiến trình thoát thì restart policy chạy lại;
  - tiến trình treo thì container báo không khỏe nhưng không tự chạy lại;
  - khóa nhịp sống hết hạn là tín hiệu cho cơ chế dừng khẩn cấp.
- Thêm bảng healthcheck cho từng dịch vụ:
  - postgres, redis, api và browser-worker mỗi dịch vụ có lệnh kiểm tra riêng;
  - interval 10 giây, timeout 5 giây, retries 3, start_period 30 giây (api 60 giây vì chạy migration).
- Khóa nhịp sống đặt theo từng tiến trình. Healthcheck đọc khóa của chính container đó.

**Kết quả.** Đã sửa ([R-SKL-18](../app-skeleton.md#s-0f1edd606c "mỗi tiến trình browser-worker ghi khóa riêng mio") *(mỗi tiến trình browser-worker ghi khóa riêng mio)*, thêm [R-SKL-31](../app-skeleton.md#s-0f1edd606c "healthcheck và khởi động lại trong Compose") *(healthcheck và khởi động lại trong Compose)*, mục Tham số; [P0-SKL-032](../../test/cases/app-skeleton.md#s-53c1e1ab68 "browser-worker ghi nhịp sống đều đặn") *(browser-worker ghi nhịp sống đều đặn)*, [P0-SKL-033](../../test/cases/app-skeleton.md#s-843cfc11a7 "Khóa nhịp sống hết hạn khi worker dừng; healthcheck chỉ đọc…") *(Khóa nhịp sống hết hạn khi worker dừng; healthcheck chỉ đọc…)*, [P0-SKL-066](../../test/cases/app-skeleton.md#s-81fdea9a0b "Hai browser-worker: worker treo không bị worker kia che") *(Hai browser-worker: worker treo không bị worker kia che)*, [P0-SKL-071](../../test/cases/app-skeleton.md#s-63f466f034 "Cấu hình healthcheck; container unhealthy không bị khởi độn…") *(Cấu hình healthcheck; container unhealthy không bị khởi độn…)*).

**Chi tiết kỹ thuật**
- Restart policy: `restart: unless-stopped`. Trạng thái không khỏe: `unhealthy`.
- Tham số healthcheck: `interval`, `timeout`, `retries`, `start_period`.
- Image `node:*-slim` không có `curl`.
- Lệnh healthcheck:
  - postgres: `pg_isready`;
  - redis: `redis-cli ping`;
  - api: `node dist/healthcheck.js` gọi `/api/v1/health`;
  - browser-worker: `node dist/healthcheck.js`.
- Tên khóa nhịp sống theo tiến trình: `mio:heartbeat:browser-worker:<hostname>`.
- Cơ chế dừng khẩn cấp: `emergency-stop`.

<a id="s-70a62c3166"></a>

### RV-05 api và browser-worker có thể chạy bằng user khác nhau trên cùng thư mục dữ liệu

- Mức độ: nên sửa
- Vị trí: [R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*; mục Tham số (base image)

**Tóm tắt.** Hai container dùng hai image khác nhau, nên có thể chạy bằng hai user khác nhau trên cùng thư mục dữ liệu. Điều này dễ gây lỗi quyền trên máy Linux.

**Vấn đề**
- Api và browser-worker dùng hai image khác nhau, mỗi image có user mặc định riêng. Uid của hai user có thể khác nhau.
- Cả hai container ghi chung vào thư mục dữ liệu.
- Api cần đọc file chẩn đoán do worker ghi, ví dụ ảnh chụp khi tự dừng khẩn cấp.
- Trên máy Linux (Oracle), cách bố trí này dễ gây lỗi quyền.

**Đề xuất**
- [R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)* chốt cả hai container chạy cùng uid và gid (1000:1000).
- Thư mục và file trong thư mục ảnh và thư mục chẩn đoán phải cho nhóm đọc được.
- [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)* thêm bước kiểm tra: uid và gid của hai container bằng nhau, và api đọc được file worker ghi trong thư mục chẩn đoán.

**Kết quả.** Đã sửa ([R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*; [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)*; 05-roadmap.md mục Triển khai lên máy chủ thêm bước chown).

**Chi tiết kỹ thuật**
- Image của api: `node:26-bookworm-slim`, user `node`.
- Image Playwright của browser-worker: user `pwuser`.
- Thư mục dữ liệu chung: `MIO_DATA_DIR`.
- Thư mục chẩn đoán: `debug-dumps/`. Ảnh tự dừng được ghi bởi `emergency-stop`.
- Thư mục ảnh: `images/`.
- Cặp uid và gid: `uid:gid`.
- Lệnh kiểm tra trong [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)*: `id -u`, `id -g`.

<a id="s-56f6dffb8d"></a>

### RV-06 Profile trình duyệt trên ổ Windows: quyền 700 không có tác dụng, rủi ro hỏng phiên

- Mức độ: nên sửa
- Vị trí: [R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*; bảng biến Compose (`MIO_DATA_DIR`); [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)* bước 3

**Tóm tắt.** Ở giai đoạn 0, profile trình duyệt nằm trên ổ Windows nên quyền 700 không có tác dụng và phiên dễ bị hỏng. Đề xuất chuyển profile sang một named volume riêng.

**Vấn đề**
- Giai đoạn 0 chạy trên Windows. Thư mục dữ liệu nhiều khả năng nằm trên ổ NTFS và được gắn vào container qua Docker Desktop.
- Bind mount kiểu này không giữ quyền Unix. Lệnh đặt quyền 700 không có tác dụng, nên [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)* bước 3 sẽ không đạt.
- Bind mount kiểu này còn chậm.
- Khóa file SQLite trong profile Chromium kém tin cậy trên bind mount này. Điều đó ảnh hưởng trực tiếp tới bài chạy 24 giờ không bị đăng xuất.

**Đề xuất**
- Tách profile trình duyệt ra một named volume riêng. Volume này nằm trên ext4 trong máy ảo Docker, nên quyền 700 có hiệu lực.
- Thư mục ảnh và thư mục chẩn đoán vẫn giữ trong thư mục dữ liệu.
- Cách làm này phù hợp [ADR 0009](../../../../decisions/0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*, vì khác biệt giữa các máy nằm ở volume.
- Cách làm này cũng phù hợp 04 mục 7: profile không đưa vào bản sao lưu công khai và không copy khi dời máy.
- Cập nhật [R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*, [P0-SKL-011](../../test/cases/app-skeleton.md#s-e686545008 "Thư mục con, profile trong named volume, cùng user không ph…") *(Thư mục con, profile trong named volume, cùng user không ph…)*, [P0-SKL-039](../../test/cases/app-skeleton.md#s-908a22103a "Chuyển máy chỉ bằng biến môi trường và volume") *(Chuyển máy chỉ bằng biến môi trường và volume)*.

**Kết quả.** Đã sửa ([R-SKL-20](../app-skeleton.md#s-0f1edd606c "thư mục dữ liệu và quyền") *(thư mục dữ liệu và quyền)*, biến BROWSER_PROFILE_DIR, named volume mio-browser-profile; [ADR 0013](../../../../decisions/0013-browser-profile-named-volume.md "Profile trình duyệt nằm trong named volume riêng") *(Profile trình duyệt nằm trong named volume riêng)*; [P0-SKL-008](../../test/cases/app-skeleton.md#s-1630bac11e "DATA_DIR, BROWSER_PROFILE_DIR là đường dẫn tương đối") *(DATA\_DIR, BROWSER\_PROFILE\_DIR là đường dẫn tương đối)* … [P0-SKL-012](../../test/cases/app-skeleton.md#s-84afd4755e "Khởi động lại không làm mất dữ liệu có sẵn trong DATA_DIR") *(Khởi động lại không làm mất dữ liệu có sẵn trong DATA\_DIR)*, [P0-SKL-039](../../test/cases/app-skeleton.md#s-908a22103a "Chuyển máy chỉ bằng biến môi trường và volume") *(Chuyển máy chỉ bằng biến môi trường và volume)*).

**Chi tiết kỹ thuật**
- Thư mục dữ liệu: `MIO_DATA_DIR`, ví dụ `D:\mio-data`.
- Lệnh đặt quyền không có tác dụng: `chmod 700`.
- Thư mục profile: `browser-profile`.
- Named volume mới: `mio-browser-profile`, gắn vào `/data/browser-profile`.
- Thư mục giữ lại trong thư mục dữ liệu: `images/`, `debug-dumps/`.

<a id="s-612295d598"></a>

### RV-07 Phiên bản Node của browser-worker chưa chốt, test case giả định Node 26

- Mức độ: nên sửa
- Vị trí: mục Tham số (phiên bản hạ tầng); [P0-SKL-038](../../test/cases/app-skeleton.md#s-5676b654ee "Build image đa kiến trúc và chạy được trên arm64") *(Build image đa kiến trúc và chạy được trên arm64)* bước 2

**Tóm tắt.** Browser-worker dùng Node đi kèm image Playwright, chưa chắc là Node 26, trong khi test case lại giả định Node 26. Cần chốt phiên bản Node cho browser-worker.

**Vấn đề**
- Image Playwright mang sẵn phiên bản Node riêng, không chắc là 26.
- [P0-SKL-038](../../test/cases/app-skeleton.md#s-5676b654ee "Build image đa kiến trúc và chạy được trên arm64") *(Build image đa kiến trúc và chạy được trên arm64)* bước 2 lại mong cả api và browser-worker đều chạy Node 26.
- Code dùng chung phải chạy được trên cả hai phiên bản Node.

**Đề xuất**
- Phương án A:
  - ghi rõ browser-worker dùng Node đi kèm image Playwright; phiên bản cụ thể ghi vào `plan.md` lúc implement;
  - package dùng chung và browser-worker chỉ dùng tính năng có trên phiên bản đó;
  - [P0-SKL-038](../../test/cases/app-skeleton.md#s-5676b654ee "Build image đa kiến trúc và chạy được trên arm64") *(Build image đa kiến trúc và chạy được trên arm64)* bước 2 đổi thành "api `v26.x.x`, browser-worker đúng phiên bản Node của image Playwright".
- Phương án khác: build browser-worker từ image Node 26 rồi cài Chromium của Playwright vào. Khi đó chỉ có một phiên bản Node.

**Kết quả.** Đã sửa theo phương án A (mục Tham số; [ADR 0014](../../../../decisions/0014-browser-worker-playwright-image.md "browser-worker dùng image Playwright chính thức kèm Node củ…") *(browser-worker dùng image Playwright chính thức kèm Node củ…)*; [P0-SKL-038](../../test/cases/app-skeleton.md#s-5676b654ee "Build image đa kiến trúc và chạy được trên arm64") *(Build image đa kiến trúc và chạy được trên arm64)*).

**Chi tiết kỹ thuật**
- Image Playwright: `mcr.microsoft.com/playwright:v1.63.0-noble`.
- Phiên bản test case mong đợi: `v26.x.x`.
- Package dùng chung: `@mio/shared`. Thư mục browser-worker: `apps/browser-worker`.
- Phương án khác: image `node:26-bookworm-slim` + `playwright install --with-deps chromium`.

<a id="s-1542d9f71c"></a>

### RV-08 Mã lỗi API dùng chung chưa đủ và chưa nằm ở chỗ dùng chung

- Mức độ: nên sửa
- Vị trí: [R-SKL-10](../app-skeleton.md#s-0f1edd606c "get / set với khóa không có trong SETTINGS") *(get / set với khóa không có trong SETTINGS)*, [R-SKL-11](../app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*, [R-SKL-12](../app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*, [R-SKL-15](../app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*; `docs/design/api/system.md`; `openapi.yaml`; [P0-SKL-049](../../test/cases/app-skeleton.md#s-de70ed5af5 "Khóa cài đặt không tồn tại") *(Khóa cài đặt không tồn tại)*

**Tóm tắt.** Một số mã lỗi API dùng cho nhiều tính năng nhưng chưa được khai báo ở tài liệu dùng chung. Thiết kế cũng chưa quy định lỗi thân JSON sai cú pháp và thân quá lớn.

**Vấn đề**
- Lỗi dữ liệu không hợp lệ (400) và lỗi cài đặt đã lưu không hợp lệ (409) dùng cho mọi endpoint cài đặt của nhiều tính năng. Hai mã này chưa có trong tài liệu API hệ thống và chưa có response dùng chung trong file OpenAPI.
- Thiết kế chưa quy định khi thân JSON sai cú pháp hoặc quá lớn. Mặc định NestJS trả về một dạng lỗi riêng, trái với [R-SKL-15](../app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*.
- Mã lỗi không tìm thấy cài đặt không bao giờ tới được qua HTTP. Mỗi khóa cài đặt có route cố định ([ADR 0010](../../../../decisions/0010-settings-storage.md "Lưu cài đặt nghiệp vụ dạng mục JSON có schema") *(Lưu cài đặt nghiệp vụ dạng mục JSON có schema)*), nên khóa lạ rơi vào lỗi 404 chung. [P0-SKL-049](../../test/cases/app-skeleton.md#s-de70ed5af5 "Khóa cài đặt không tồn tại") *(Khóa cài đặt không tồn tại)* phải chú thích "[câu hỏi mở 3](../app-skeleton.md#s-505f20bb78 "Giá trị cài đặt trong DB không còn hợp lệ thì làm gì? — đã…") *(Giá trị cài đặt trong DB không còn hợp lệ thì làm gì? — đã…)*", nhưng câu hỏi này không tồn tại.

**Đề xuất**
- [R-SKL-15](../app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")* và tài liệu API hệ thống thêm các mã lỗi chung:
  - lỗi dữ liệu không hợp lệ (400), kèm danh sách trường lỗi;
  - lỗi JSON sai cú pháp (400) với câu "Dữ liệu gửi lên không đúng định dạng JSON";
  - lỗi thân quá lớn (413) với câu "Dữ liệu gửi lên quá lớn", giới hạn thân 1 MB;
  - lỗi cài đặt đã lưu không hợp lệ (409).
- Thêm response dùng chung vào file OpenAPI, sinh lại và lint.
- Bỏ mã lỗi không tìm thấy cài đặt. Khóa cài đặt lạ là lỗi lập trình, vì khóa có kiểu riêng và typecheck đã chặn. Nếu lỗi này xảy ra lúc chạy thì trả 500. [P0-SKL-049](../../test/cases/app-skeleton.md#s-de70ed5af5 "Khóa cài đặt không tồn tại") *(Khóa cài đặt không tồn tại)* bỏ chú thích.
- Thêm test case JSON sai cú pháp và thân quá 1 MB. Case này cần một endpoint nhận thân, nên chạy khi đã có tính năng cài đặt quét.

**Kết quả.** Đã sửa ([R-SKL-10](../app-skeleton.md#s-0f1edd606c "get / set với khóa không có trong SETTINGS") *(get / set với khóa không có trong SETTINGS)*, [R-SKL-15](../app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*; api/system.md; openapi.yaml sinh lại, lint sạch; [P0-SKL-049](../../test/cases/app-skeleton.md#s-de70ed5af5 "Khóa cài đặt không tồn tại") *(Khóa cài đặt không tồn tại)*, [P0-SKL-065](../../test/cases/app-skeleton.md#s-352c976967 "Thân request sai JSON hoặc quá lớn") *(Thân request sai JSON hoặc quá lớn)*).

**Chi tiết kỹ thuật**
- Mã lỗi hiện có: `VALIDATION_ERROR` (400), `INVALID_STORED_SETTING` (409); chưa có trong `api/system.md`, chưa có response dùng chung trong `openapi.yaml`.
- Dạng lỗi mặc định của NestJS: `{ statusCode, message, error }`.
- Mã lỗi không tìm thấy cài đặt: `SETTING_NOT_FOUND`. Khóa lạ rơi vào 404 `NOT_FOUND`.
- Mã chung thêm vào [R-SKL-15](../app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")* và `system.md`:
  - `400 VALIDATION_ERROR` (có `fields`);
  - `400 INVALID_JSON`;
  - `413 PAYLOAD_TOO_LARGE`;
  - `409 INVALID_STORED_SETTING`.
- Lỗi lập trình: `UnknownSettingKeyError`; khóa có kiểu `SettingKey`; lúc chạy trả 500 `INTERNAL_ERROR`.
- Tính năng cần có trước khi chạy case: `crawl-settings`.

<a id="s-e162a936e5"></a>

### RV-09 Thông báo lỗi biến môi trường chưa nguyên văn; "biến rỗng coi như thiếu" chưa có trong thiết kế

- Mức độ: nên sửa
- Vị trí: bảng Biến môi trường; [R-SKL-01](../app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*, [R-SKL-02](../app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*; [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)*, [P0-SKL-006](../../test/cases/app-skeleton.md#s-6ba381391d "DATABASE_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…") *(DATABASE\_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…)*

**Tóm tắt.** Thiết kế chưa ghi nguyên văn thông báo lỗi cho từng biến môi trường. Test case cũng dựa vào một quy tắc mà thiết kế chưa có.

**Vấn đề**
- [R-SKL-02](../app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)* chỉ có ví dụ cho một biến (Redis). Phần yêu cầu của các biến còn lại chỉ xuất hiện trong test case.
- [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)* dựa vào quy tắc "biến rỗng coi như thiếu", nhưng thiết kế không có quy tắc này.
- Test case dẫn "[câu hỏi mở 1](../app-skeleton.md#s-505f20bb78 "browser-worker chỉ kết nối Redis") *(browser-worker chỉ kết nối Redis)*, 2", nhưng các câu hỏi này không tồn tại ở cả hai file.

**Đề xuất**
- Thêm cột "Yêu cầu (in trong thông báo)" vào bảng biến môi trường, với nội dung:
  - biến kết nối DB: "phải là URL postgres:// hoặc postgresql://";
  - biến kết nối Redis: "phải là URL redis://";
  - biến thư mục dữ liệu: "phải là đường dẫn tuyệt đối";
  - biến URL công khai: "phải là URL http:// hoặc https://, không có / cuối".
- [R-SKL-01](../app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)* thêm quy tắc "giá trị rỗng hoặc chỉ có khoảng trắng coi như thiếu".
- Xóa chú thích "câu hỏi mở" trong [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)* và [P0-SKL-006](../../test/cases/app-skeleton.md#s-6ba381391d "DATABASE_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…") *(DATABASE\_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…)*.

**Kết quả.** Đã sửa (bảng Biến môi trường, [R-SKL-01](../app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)*, [R-SKL-02](../app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*; [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)*, [P0-SKL-006](../../test/cases/app-skeleton.md#s-6ba381391d "DATABASE_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…") *(DATABASE\_URL: phân vùng hợp lệ / không hợp lệ và không lộ m…)*).

**Chi tiết kỹ thuật**
- Biến có ví dụ trong [R-SKL-02](../app-skeleton.md#s-0f1edd606c "biến sai định dạng") *(biến sai định dạng)*: `REDIS_URL`.
- Phần `<yêu cầu>` của `DATABASE_URL`, `DATA_DIR`, `PUBLIC_URL` chỉ có trong test case.

<a id="s-b3be1e1532"></a>

### RV-10 `SettingsService` còn chỗ hiểu hai cách

- Mức độ: nên sửa
- Vị trí: [R-SKL-11](../app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*, [R-SKL-12](../app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*; mục Đọc / ghi cài đặt; [P0-SKL-051](../../test/cases/app-skeleton.md#s-80c5c4bf4c "Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài") *(Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài)*

**Tóm tắt.** Dịch vụ cài đặt còn vài chỗ mơ hồ: lưu giá trị nào, xử lý trường lạ ra sao, ghi đường dẫn lỗi thế nào và in giá trị đang lưu ra sao. Đề xuất chốt từng điểm.

**Vấn đề**
- Thiết kế chưa nói lưu giá trị gửi lên hay giá trị sau khi parse.
- Thiết kế chưa nói trường lạ (không có trong schema) bị bỏ hay bị báo lỗi, ở cả lúc ghi lẫn lúc đọc.
- Định dạng đường dẫn trong danh sách trường lỗi chỉ được nêu ở [R-SKL-12](../app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*.
- Chưa có cách ghi lỗi ở gốc (khi thân không phải object) và cách ghi trường có nhiều lỗi.
- Thông báo "đang lưu: <giá trị>" chưa nói in giá trị thế nào (chuỗi có ngoặc kép không). Cũng chưa nói việc cắt 100 ký tự tính trên gì.

**Đề xuất**
- Lưu kết quả sau khi parse.
- Trường lạ bị bỏ, theo mặc định của zod, ở cả lúc ghi và lúc đọc. Nhờ vậy, bỏ một trường khỏi schema không làm giá trị cũ thành lỗi.
- [R-SKL-11](../app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)* và [R-SKL-12](../app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)* dùng chung một định dạng đường dẫn.
- Lỗi ở gốc dùng một khóa riêng. Một trường có nhiều lỗi thì lấy lỗi đầu tiên.
- Giá trị được in ở dạng JSON, nên chuỗi có ngoặc kép. Giá trị bị cắt khi chuỗi JSON dài hơn 100 ký tự.
- [P0-SKL-051](../../test/cases/app-skeleton.md#s-80c5c4bf4c "Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài") *(Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài)* đổi giá trị biên:
  - chuỗi 98 ký tự (JSON 100) không bị cắt;
  - chuỗi 99 ký tự (JSON 101) bị cắt.

**Kết quả.** Đã sửa ([R-SKL-11](../app-skeleton.md#s-0f1edd606c "set với giá trị không qua zod schema của khóa") *(set với giá trị không qua zod schema của khóa)*, [R-SKL-12](../app-skeleton.md#s-0f1edd606c "giá trị trong DB không qua schema hiện tại") *(giá trị trong DB không qua schema hiện tại)*; [P0-SKL-048](../../test/cases/app-skeleton.md#s-808ee36bcc "Ghi cài đặt sai schema thì báo lỗi theo trường, không ghi DB") *(Ghi cài đặt sai schema thì báo lỗi theo trường, không ghi DB)*, [P0-SKL-051](../../test/cases/app-skeleton.md#s-80c5c4bf4c "Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài") *(Giá trị đang lưu sai nhiều trường: thiếu, lồng, quá dài)*, [P0-SKL-068](../../test/cases/app-skeleton.md#s-25d0a70d96 "Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc") *(Trường lạ trong cài đặt bị bỏ khi ghi và khi đọc)*).

**Chi tiết kỹ thuật**
- Danh sách trường lỗi: `fields`.
- Thao tác ghi và đọc: `set`, `get`.
- Ví dụ định dạng đường dẫn: `goldenHours[1].end`.
- Khóa của lỗi ở gốc: `_root`.
- Cách in giá trị: `JSON.stringify`, ví dụ `"abc"`.

<a id="s-29b2eef86a"></a>

### RV-11 `created_at` lấy giờ DB, `updated_at` lấy `CLOCK`

- Mức độ: nên sửa
- Vị trí: `docs/design/db-schema.md` mục `app_settings` và Quy ước chung; mục Đọc / ghi cài đặt

**Tóm tắt.** Thời điểm tạo lấy giờ của DB, còn thời điểm cập nhật lấy giờ của app. Trong test, thời điểm cập nhật có thể sớm hơn thời điểm tạo. Đề xuất để app đặt cả hai cột.

**Vấn đề**
- Ở lần ghi đầu, thời điểm tạo lấy giờ của DB. Thời điểm cập nhật lấy giờ của app, hoặc cũng lấy giờ DB, vì thiết kế không nói nhánh INSERT.
- Trong test dùng đồng hồ giả, thời điểm cập nhật có thể nhỏ hơn thời điểm tạo.
- Các bảng sau sẽ lặp lại cùng vấn đề.

**Đề xuất**
- Quy ước chung của db-schema thêm: app đặt cả hai cột thời điểm bằng đồng hồ của app khi ghi.
- Giá trị mặc định lấy giờ DB chỉ là dự phòng cho SQL viết tay.
- Mục Đọc / ghi cài đặt ghi rõ nhánh INSERT đặt cả hai cột.

**Kết quả.** Đã sửa (db-schema.md Quy ước chung; mục Đọc / ghi cài đặt; [P0-SKL-046](../../test/cases/app-skeleton.md#s-b548d2ba78 "Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục") *(Ghi cài đặt hợp lệ: tạo mới rồi thay cả mục)*).

**Chi tiết kỹ thuật**
- Hai cột: `created_at`, `updated_at`.
- Giờ DB: `now()`. Giờ app: `CLOCK.now()`.
- Đồng hồ giả trong test: `FakeClock`.

<a id="s-87064be426"></a>

### RV-12 Mất kết nối DB/Redis: "thư viện tự kết nối lại" còn mơ hồ

- Mức độ: nên sửa
- Vị trí: mục Xử lý lỗi; mục Khởi động; [R-SKL-13](../app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*

**Tóm tắt.** Thiết kế chưa nói rõ api xử lý thế nào khi mất kết nối PostgreSQL hoặc Redis, lúc khởi động cũng như lúc đang chạy. Kiểm tra sức khỏe cũng có thể quá chậm.

**Vấn đề**
- Chưa quy định trường hợp khởi động mà không kết nối được PostgreSQL hoặc Redis, ví dụ api khởi động lại lúc DB đang dừng.
- Khi đang chạy, pool kết nối PostgreSQL phát sự kiện lỗi. Nếu không ai bắt sự kiện này, tiến trình sẽ sập. [P0-SKL-017](../../test/cases/app-skeleton.md#s-8c19408dd1 "Health khi PostgreSQL dừng rồi chạy lại") *(Health khi PostgreSQL dừng rồi chạy lại)* lại kiểm số lần khởi động lại không đổi.
- Kiểm tra sức khỏe chạy tuần tự thì tổng thời gian có thể tới 4 giây, trái [P0-SKL-020](../../test/cases/app-skeleton.md#s-04badc4434 "Health khi DB hoặc Redis treo (không trả lời)") *(Health khi DB hoặc Redis treo (không trả lời))* (2–3 giây).
- Nếu kiểm tra sức khỏe dùng chung kết nối với BullMQ (thử lại vô hạn), lệnh ping sẽ phải xếp hàng phía sau.

**Đề xuất.** Thêm các quy tắc sau:
- Khi khởi động:
  - thử kết nối mỗi 2 giây, tối đa 30 giây;
  - không kết nối được thì thoát mã 1 với thông báo "Không kết nối được PostgreSQL" / "Không kết nối được Redis".
- Khi đang chạy:
  - bắt sự kiện lỗi của pool PostgreSQL và client Redis, ghi log mức cảnh báo, không thoát;
  - client Redis thử lại không giới hạn, theo yêu cầu của BullMQ;
  - request cần DB trong lúc mất kết nối nhận lỗi 500.
- Kiểm tra sức khỏe kiểm DB và Redis song song, dùng kết nối riêng. Mỗi lần kiểm có timeout 2 giây.
- Thêm test case: chạy lại api khi PostgreSQL đang dừng.

**Kết quả.** Đã sửa ([R-SKL-13](../app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*, thêm [R-SKL-30](../app-skeleton.md#s-0f1edd606c "kết nối PostgreSQL và Redis") *(kết nối PostgreSQL và Redis)*; [P0-SKL-020](../../test/cases/app-skeleton.md#s-04badc4434 "Health khi DB hoặc Redis treo (không trả lời)") *(Health khi DB hoặc Redis treo (không trả lời))*, [P0-SKL-070](../../test/cases/app-skeleton.md#s-9153860e30 "Khởi động khi PostgreSQL hoặc Redis chưa sẵn sàng") *(Khởi động khi PostgreSQL hoặc Redis chưa sẵn sàng)*).

**Chi tiết kỹ thuật**
- Pool kết nối PostgreSQL: `pg`; sự kiện lỗi: `error`.
- [P0-SKL-017](../../test/cases/app-skeleton.md#s-8c19408dd1 "Health khi PostgreSQL dừng rồi chạy lại") *(Health khi PostgreSQL dừng rồi chạy lại)* kiểm `RestartCount`.
- Endpoint kiểm tra sức khỏe: `/health`.
- Mức log: `warn`.
- Client Redis: ioredis, cấu hình `maxRetriesPerRequest: null`.
- Lỗi khi mất kết nối: 500 `INTERNAL_ERROR`.

<a id="s-fe4f3abe69"></a>

### RV-13 `container_stats.py` thiếu khoảng tham số và phạm vi container

- Mức độ: nên sửa
- Vị trí: [R-SKL-24](../app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*; mục Đo RAM/CPU từng container; [P0-SKL-040](../../test/cases/app-skeleton.md#s-3cac25e098 "Đo RAM/CPU: ghi CSV theo chu kỳ") *(Đo RAM/CPU: ghi CSV theo chu kỳ)* … [P0-SKL-042](../../test/cases/app-skeleton.md#s-86263041a9 "Đo RAM/CPU khi Docker không chạy") *(Đo RAM/CPU khi Docker không chạy)*

**Tóm tắt.** Script đo RAM và CPU đang lấy cả container ngoài app, và các tham số chưa có khoảng hợp lệ hay giá trị mặc định. Đề xuất giới hạn phạm vi container và chốt từng tham số.

**Vấn đề**
- Lệnh đo của Docker liệt kê mọi container trên máy, kể cả container của Testcontainers và container khác. Điều này làm lẫn số liệu nghiệm thu.
- Tham số khoảng đo chưa có khoảng hợp lệ.
- Tham số file kết quả chưa rõ là bắt buộc hay có mặc định.
- Giá trị CPU trên 100% chưa được giải thích.
- Lệnh tổng hợp chưa quy định khi file không tồn tại.

**Đề xuất**
- Chỉ lấy container có nhãn project của app.
- Khoảng đo là số nguyên 5–3600, mặc định 60. Giá trị sai thì thoát mã 2 với thông báo "--interval phải là số nguyên từ 5 đến 3600".
- File kết quả có đường dẫn mặc định đặt theo ngày giờ Việt Nam.
- Giá trị CPU tính theo Docker. 100% tương ứng 1 lõi.
- Lệnh tổng hợp gặp file không có thì thoát mã 1 với thông báo "Không tìm thấy file: <đường dẫn>".
- Thêm test case biên cho khoảng đo (4, 5, 3600, 3601, `abc`), và case container ngoài project bị bỏ qua.

**Kết quả.** Đã sửa ([R-SKL-24](../app-skeleton.md#s-0f1edd606c "tools/ops/container_stats") *(tools/ops/container\_stats)*, mục Đo RAM/CPU; [P0-SKL-040](../../test/cases/app-skeleton.md#s-3cac25e098 "Đo RAM/CPU: ghi CSV theo chu kỳ") *(Đo RAM/CPU: ghi CSV theo chu kỳ)*, [P0-SKL-067](../../test/cases/app-skeleton.md#s-8ea6efe961 "Đo RAM/CPU: tham số --interval, --out và file tổng hợp khôn…") *(Đo RAM/CPU: tham số --interval, --out và file tổng hợp khôn…)*).

**Chi tiết kỹ thuật**
- Lệnh đo: `docker stats`.
- Nhãn lọc container: `com.docker.compose.project`.
- Tham số khoảng đo: `--interval`.
- Tham số file kết quả: `--out`, mặc định `.local/metrics/<YYYY-MM-DD-HHmm>.csv` theo giờ `Asia/Ho_Chi_Minh`.
- Cột CPU: `cpu_percent`.
- Lệnh tổng hợp: `summary`.

<a id="s-d3c790701c"></a>

### RV-14 Case về "không tự chạy lại job" chưa gắn regression

- Mức độ: nên sửa
- Vị trí: test/cases/app-skeleton.md [P0-SKL-057](../../test/cases/app-skeleton.md#s-a8527a39a1 "Tùy chọn job mặc định") *(Tùy chọn job mặc định)*

**Tóm tắt.** Case kiểm việc không tự chạy lại job gắn với một lằn ranh đỏ nhưng chưa gắn cờ regression. Đề xuất gắn cờ.

**Vấn đề**
- [P0-SKL-057](../../test/cases/app-skeleton.md#s-a8527a39a1 "Tùy chọn job mặc định") *(Tùy chọn job mặc định)* kiểm cấu hình chỉ thử một lần. Case này gắn với lằn ranh đỏ "không comment hai lần (kể cả khi retry)".
- Nhưng case đang ghi `Regression: không`.
- Checklist test case yêu cầu mọi case của lằn ranh đỏ phải có `Regression: có`.

**Đề xuất**
- Đổi thành `Regression: có`.
- Nếu nhận [RV-01](#s-d56738b7bd "Job bị stalled vẫn được BullMQ chạy lại một lần") *(Job bị stalled vẫn được BullMQ chạy lại một lần)* thì thêm bước kiểm số lần stalled cho phép của worker, qua log khởi động hoặc cấu hình.

**Kết quả.** Đã sửa ([P0-SKL-057](../../test/cases/app-skeleton.md#s-a8527a39a1 "Tùy chọn job mặc định") *(Tùy chọn job mặc định)* Regression: có).

**Chi tiết kỹ thuật**
- Cấu hình chỉ thử một lần: `attempts: 1`.
- Số lần stalled cho phép: `maxStalledCount`.

<a id="s-a668a80529"></a>

### RV-15 Đăng ký hàng đợi của giai đoạn sau ngay trong khung

- Mức độ: gợi ý
- Vị trí: mục Job và hàng đợi; [R-SKL-05](../app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)*; [P0-SKL-037](../../test/cases/app-skeleton.md#s-6dc6f07c19 "Hàng đợi đăng ký đúng tên, global concurrency 1") *(Hàng đợi đăng ký đúng tên, global concurrency 1)*

**Tóm tắt.** Khung ứng dụng đang đăng ký worker cho cả các hàng đợi giai đoạn 0 chưa dùng. Đề xuất giai đoạn 0 chỉ khai báo tên và chỉ đăng ký hàng đợi trình duyệt.

**Vấn đề**
- Khung đăng ký worker cho hàng đợi inbox, render, AI và các hàng đợi khác, dù giai đoạn 0 không dùng.
- Theo 04 mục 4.3, nếu inbox dùng chung tài khoản vận hành thì hàng đợi inbox gộp vào hàng đợi trình duyệt, với inbox có ưu tiên cao nhất. Chủ tiệm chưa chọn phương án này.
- Hai hàng đợi riêng cùng mở một thư mục profile trình duyệt sẽ xung đột.

**Đề xuất**
- Giai đoạn 0 chỉ khai báo tên hàng đợi. Giai đoạn này chỉ đăng ký hàng đợi trình duyệt và hàng đợi kết quả của nó.
- Tính năng của giai đoạn sau tự đăng ký hàng đợi của mình.
- [R-SKL-05](../app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)* ghi chú: việc gộp hay tách hàng đợi inbox được quyết ở giai đoạn 3, theo 04 mục 4.3.
- [P0-SKL-037](../../test/cases/app-skeleton.md#s-6dc6f07c19 "Hàng đợi đăng ký đúng tên, global concurrency 1") *(Hàng đợi đăng ký đúng tên, global concurrency 1)* bỏ phần hàng đợi inbox.

**Kết quả.** Đã sửa ([R-SKL-05](../app-skeleton.md#s-0f1edd606c "fb-browser có global concurrency = 1") *(fb-browser có global concurrency = 1)*, mục Job và hàng đợi; [P0-SKL-037](../../test/cases/app-skeleton.md#s-6dc6f07c19 "Hàng đợi đăng ký đúng tên, global concurrency 1") *(Hàng đợi đăng ký đúng tên, global concurrency 1)*).

**Chi tiết kỹ thuật**
- Hàng đợi chưa dùng ở giai đoạn 0: `fb-inbox`, `render`, `ai-*`…
- Hàng đợi trình duyệt: `fb-browser`. Hàng đợi kết quả: `fb-browser-results`.
- Thư mục profile trình duyệt: `browser-profile/`.
- Danh sách tên hàng đợi: `QUEUE_NAMES`.

<a id="s-45783c65ae"></a>

### RV-16 pino không che được khóa "ở mọi độ sâu"

- Mức độ: gợi ý
- Vị trí: [R-SKL-17](../app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*; [ADR 0012](../../../../decisions/0012-structured-logging-pino.md "Log JSON bằng pino (nestjs-pino)") *(Log JSON bằng pino (nestjs-pino))*

**Tóm tắt.** Thư viện log pino không hỗ trợ che khóa bí mật ở mọi độ sâu của object. Đề xuất chốt danh sách đường dẫn cụ thể cần che.

**Vấn đề**
- Tính năng che dữ liệu của pino nhận đường dẫn cụ thể và wildcard một cấp. Pino không có wildcard đệ quy.
- Yêu cầu che "ở mọi độ sâu" buộc phải viết serializer duyệt cả object cho mỗi dòng log.

**Đề xuất**
- Chốt danh sách đường dẫn cần che:
  - header của request và response liên quan tới xác thực và cookie;
  - các khóa mật khẩu, token, khóa bí mật và cookie, tới độ sâu 3.
- Giữ yêu cầu "không lộ" bằng test tự động cho từng đường dẫn.

**Kết quả.** Đã sửa ([R-SKL-17](../app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*).

**Chi tiết kỹ thuật**
- Tính năng che dữ liệu của pino: `redact`.
- Header cần che: `authorization`, `cookie`, `set-cookie`.
- Khóa cần che: `password`, `token`, `secret`, `cookie`.
- Đường dẫn theo độ sâu: `*.x`, `*.*.x`, `*.*.*.x`.

<a id="s-0284a2f356"></a>

### RV-17 Compose nên báo thiếu biến ngay thay vì truyền chuỗi rỗng

- Mức độ: gợi ý
- Vị trí: bảng biến Compose; [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)*

**Tóm tắt.** Khi thiếu biến URL công khai, Compose chỉ cảnh báo và truyền chuỗi rỗng, làm api khởi động lại liên tục. Đề xuất để Compose dừng ngay với thông báo rõ.

**Vấn đề**
- Nếu file môi trường thiếu biến URL công khai, Compose chỉ cảnh báo và truyền chuỗi rỗng.
- Khi đó api rơi vào vòng khởi động lại.

**Đề xuất**
- Khai báo biến URL công khai theo dạng bắt buộc, giống các biến mật khẩu PostgreSQL và thư mục dữ liệu. Khi thiếu biến, lệnh khởi động Compose dừng ngay với thông báo rõ.
- [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)* đổi kết quả mong đợi theo hành vi mới.
- [R-SKL-01](../app-skeleton.md#s-0f1edd606c "thiếu biến môi trường bắt buộc") *(thiếu biến môi trường bắt buộc)* vẫn giữ nguyên, cho trường hợp chạy image trực tiếp.

**Kết quả.** Đã sửa (bảng biến Compose; [P0-SKL-004](../../test/cases/app-skeleton.md#s-b90f0e9e0f "Biến bắt buộc thiếu hoặc rỗng trong .env và trong container") *(Biến bắt buộc thiếu hoặc rỗng trong .env và trong container)*).

**Chi tiết kỹ thuật**
- Biến URL công khai: `MIO_PUBLIC_URL`, trong file `.env`.
- Cú pháp bắt buộc: `${MIO_PUBLIC_URL:?Thiếu MIO_PUBLIC_URL trong .env}`.
- Các biến đã dùng cú pháp này: `POSTGRES_PASSWORD`, `MIO_DATA_DIR`.
- Lệnh khởi động: `docker compose up`.

<a id="s-c30cf1755c"></a>

### RV-18 Vài chi tiết implement nên ghi rõ

- Mức độ: gợi ý
- Vị trí: [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*; mục `apps/web`; mục `apps/api` (`core/db`)

**Tóm tắt.** Một số chi tiết implement cần được ghi rõ: cách chạy Node trong Dockerfile, file token CSS sinh ra, vị trí thư mục DB, và khóa migration khi chạy nhiều bản api.

**Vấn đề và đề xuất**
- [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*: Dockerfile phải chạy Node trực tiếp ở dạng exec, không qua pnpm hay shell. Nếu không, tín hiệu dừng sẽ không tới được Node.
- File token CSS được "chép lúc build": ghi rõ bản chép là file sinh ra và bị gitignore, để không có hai nguồn.
- Có hai thư mục DB: module DB và thư mục schema (theo `CLAUDE.md`). Cần ghi rõ schema và hàm chạy migration nằm ở đâu.
- Api chạy một bản. Nếu sau này chạy nhiều bản, migration cần có khóa.

**Kết quả.** Đã sửa ([R-SKL-03](../app-skeleton.md#s-0f1edd606c "chỉ api chạy migration") *(chỉ api chạy migration)*, [R-SKL-22](../app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)*, mục apps/web, core/db; [P0-SKL-034](../../test/cases/app-skeleton.md#s-f8ea86b185 "Dừng bình thường khi không có job") *(Dừng bình thường khi không có job)*).

**Chi tiết kỹ thuật**
- Lệnh chạy trong Dockerfile: `CMD ["node", "dist/main.js"]` dạng exec, không qua `pnpm` hay `sh`; nếu không thì `SIGTERM` không tới Node.
- File token CSS: `ui-tokens.css`.
- Module DB: `core/db` (DbModule). Thư mục schema: `src/db/schema/`.
- Hàm chạy migration: `runMigrations`.
- Khóa migration: `pg_advisory_lock`.

<a id="s-9291000e68"></a>

### RV-19 Bổ sung vài test case

- Mức độ: gợi ý
- Vị trí: test/cases/app-skeleton.md

**Tóm tắt.** Đề xuất thêm test case kiểm việc truy cập file nằm ngoài thư mục build của web qua đường dẫn tĩnh.

**Vấn đề**
- Chưa có case thử truy cập file ngoài `apps/web/dist` qua đường dẫn tĩnh có `../`.

**Đề xuất**
- Thêm case gọi hai đường dẫn đi ngược lên thư mục cha.
- Server phải trả `index.html` hoặc 404. Server không được trả nội dung file nằm ngoài `dist`.

**Kết quả.** Đã sửa ([R-SKL-14](../app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*; [P0-SKL-072](../../test/cases/app-skeleton.md#s-2de6c30b01 "File tĩnh không lộ file ngoài apps/web/dist") *(File tĩnh không lộ file ngoài apps/web/dist)*).

**Chi tiết kỹ thuật**
- Lệnh thử 1: `curl --path-as-is http://127.0.0.1:3000/../package.json`.
- Lệnh thử 2: đường dẫn `/%2e%2e/package.json`.
