---
type: srs
feature: qdgctkh
goi_dev: qdgctkh
status: dang-review
updated: 2026-09-04
nguon:
  - docs/cuc-ql/srs/srs-qdgctkh-bo-sung.md
  - docs/cuc-ql/brainstorming/brainstorm-qdgctkh.md
  - docs/cuc-ql/user-flow/userflow-qdgctkh.md
  - docs/cuc-ql/wireframe/qdgctkh/screen-qdgctkh-lap-quyet-dinh.md
  - docs/cuc-ql/wireframe/qdgctkh/wireframe-index-qdgctkh.md
  - docs/ngoai-giao/srs/srs-de-nghi-spmm.md
  - docs/meetings/2026-07-30-2026-08-04-thong-nhat-quy-trinh-qlspmm.md
  - docs/reference/TongHop_DuAn_QLSPMM.md
  - docs/reference/PhuLuc_QDGCTKH_Nam_Mau.xlsx
---

# Đặc tả: Quyết định giao chỉ tiêu kế hoạch năm (QĐGCTKH năm)

**Figma:** file **BCY(2)** · Page 1 · khu vực 3 — **11 màn**, đánh số `01`–`11`, khung 1440.

> Quyết định loại ***Kế hoạch bổ sung*** đặc tả riêng ở [`srs-qdgctkh-bo-sung.md`](srs-qdgctkh-bo-sung.md). Tài liệu này giữ phần **Kế hoạch năm** và **ba tab xem kết quả sau điều chỉnh** (`5.12`–`5.14`) — ba tab đó là màn của quyết định năm nên sống ở đây, dù nội dung do quyết định bổ sung và QĐTK sinh ra.

## 1. Phạm vi

QĐGCTKH là **bước 2** của chuỗi nghiệp vụ QLSPMM: sau *Đăng ký nhu cầu* (phiếu đề nghị SPMM), trước *Ký hợp đồng sản xuất / mua sắm*.

Cục QLKTNVMM chọn các phiếu đề nghị **đã tiếp nhận** từ 4 hệ đầu hệ và từ chính Cục QL, chốt số lượng cấp cho từng dòng, nhập đơn giá dự trù, ban hành quyết định.

**Đơn vị tính** là thuộc tính của SPMM trong danh mục SPMM — một SPMM một đơn vị tính. *Bảng giá SPMM* lấy đơn vị tính từ cùng danh mục đó, nên *Đơn giá* luôn cùng đơn vị với *Tổng SL*.

### 1.1 Bản triển khai

| Việc | Chạy ở bản |
|---|---|
| Lập · sửa · chọn và bỏ chọn phiếu · nhập số lượng cấp và đơn giá · xuất phụ lục · ban hành · xoá | **Cục QL** |
| Xem quyết định **đã ban hành** | **Cục QL và các cơ yếu hệ đầu hệ**, phạm vi dữ liệu được xem refer Mục 3.1 |

Quyết định ở trạng thái *Mới* chỉ tồn tại trên bản Cục QL, không xuống các bản hệ. Sau khi ban hành, quyết định đi xuống các bản hệ qua **đồng bộ định kỳ hai chiều**: chiều xuống mang quyết định đã ban hành, chiều lên mang số hiện trạng của các hệ. Đồng bộ **không tức thời**; nhãn thời điểm dữ liệu hiện mốc đồng bộ gần nhất.

### 1.2 Ngoài phạm vi

- Danh mục **Bảng giá SPMM** — quyết định chỉ **đọc** giá gợi ý từ đó, không sửa được bảng giá tại đây. **Một bảng duy nhất, dùng chung với Hợp đồng sản xuất** (`FR-qdgctkh-002`); ⚠️ **bản đang chạy chưa có bảng này, phải làm mới**.
- Loại kế hoạch **Kế hoạch bổ sung** — đặc tả ở [`srs-qdgctkh-bo-sung.md`](srs-qdgctkh-bo-sung.md)
- **QĐTK** — tầng triển khai, đặc tả riêng. Ở đây chỉ ghi phần QĐTK chảy ngược lên *số hiện hành* (Mục 1.4)
- **Tạo thủ công** (lập quyết định không dựa vào phiếu đề nghị nào) — làm giai đoạn sau. Đợt này mọi quyết định đều tạo từ phiếu đề nghị SPMM, nên **trường *Phương thức tạo* không hiện trên màn**.
- **Lập công văn, trình ký, ký số, phê duyệt pháp lý** — nằm ở eOffice của Ban.

### 1.3 Hai số hiệu

| Tên | Nguồn | Định dạng | Bắt buộc |
|---|---|---|---|
| ***Số phiếu*** | Phần mềm sinh khi *Lưu* lần đầu. Chỉ đọc, duy nhất, không đổi suốt vòng đời | `QĐGCTKH/<mã đơn vị>/<năm>/<4 số>` | Luôn có |
| ***Số QĐGCTKH*** | Người dùng nhập tay, lấy từ quyết định giấy đã ký trên eOffice | Theo số QĐ của Ban | Bắt buộc khi *Ban hành* |

**Mã đơn vị lấy từ danh mục đơn vị lập, không phải hằng số.** Số thứ tự **đếm lại từ `0001` mỗi năm**, riêng theo từng đơn vị và **riêng theo từng loại quyết định** — quyết định loại *Kế hoạch bổ sung* mang tiền tố `QĐGCTKH-BS` và có dải đếm riêng; QĐTK sau này mang tiền tố `QĐTK`.

***Số phiếu*** là khoá liên kết dữ liệu và là cột bấm để mở quyết định. ***Số QĐGCTKH*** không dùng làm khoá.

### 1.4 Số gốc và số hiện hành

Quyết định năm đã ban hành **đóng băng vĩnh viễn** — không văn bản nào sửa được nó. Nhưng **con số thực tế đang có hiệu lực** thì đổi theo các văn bản ban hành sau. Hai khái niệm phải tách:

| | Nghĩa | Xem ở |
|---|---|---|
| ***Số gốc*** | Đúng con số trong bản quyết định năm đã ký | Tab *Kế hoạch năm* `5.13` |
| ***Số hiện hành*** | Số gốc **+** tổng mọi dòng điều chỉnh của các văn bản đã ban hành cùng năm | Tab *Kế hoạch hiện hành* `5.12` |

> **`số hiện hành(SPMM, địa điểm, năm)` = số của quyết định năm **+** tổng delta của mọi văn bản đã ban hành cùng năm đó.**

- Nguồn delta: **QĐGCTKH bổ sung** và **QĐTK**. Văn bản còn *Mới* không tính.
- **Cộng dồn khi xem, không lưu.** Không có cờ *Hiệu lực* / *Đã bị thay thế* ở mức dòng.
- Khoá tham chiếu là cặp `SPMM × địa điểm triển khai × năm`.
- **Phiếu điều chuyển và phiếu cấp phát lấy căn cứ là quyết định năm, đọc theo số hiện hành** — không trỏ vào quyết định bổ sung hay QĐTK nào.

**Tiền gắn với từng văn bản.** Đơn giá đổi giữa các thời điểm — có thể điều chỉnh giá, hoặc SPMM thêm mới ở một quyết định bổ sung lấy giá tại lúc đó. Tab *Kế hoạch hiện hành* vì thế **ẩn cột *Đơn giá*, chỉ để *Thành tiền***. Nghiệp vụ điều chỉnh đơn giá làm sau.

## 2. Quy trình nghiệp vụ

| # | Ai làm | Làm gì | Ở đâu |
|:--:|---|---|---|
| 1 | Các cấp trong hệ · Cục cơ yếu đầu hệ · Cục QLKTNVMM | Cấp dưới đề nghị lên cấp trên trực tiếp, lặp lại tới **Cục cơ yếu đầu hệ**; Cục đầu hệ tổng hợp thành **phiếu đề nghị của toàn hệ** gửi Cục QLKTNVMM. Cục QLKTNVMM tự lập phiếu cho nhu cầu của chính mình | `srs-de-nghi-spmm.md` |
| 2 | Cục QLKTNVMM | Tiếp nhận phiếu, đối chiếu bản giấy đã ký với dữ liệu. Chỉ phiếu ở trạng thái *Đã tiếp nhận* mới dùng được làm đầu vào | `srs-de-nghi-spmm.md` |
| 3 | Cục QLKTNVMM | Tạo quyết định, chọn *Loại kế hoạch* và *Năm áp dụng*, rồi **tích chọn các phiếu đề nghị** trong danh sách đã lọc theo hai giá trị đó | `5.3` · `5.4` |
| 4 | Phần mềm | Từ các phiếu đề nghị SPMM đã chọn, **tự đổ dòng chi tiết vào đúng tab của từng hệ**, rồi tự tính lên hai bảng *Phân bổ theo hệ* và *Tổng hợp kế hoạch toàn ngành* | `5.3` |
| 5 | Cục QLKTNVMM | Rà soát, **sửa *Số lượng cấp* thực tế** cho từng dòng. Nhập *Đơn giá* nếu cần — không bắt buộc | `5.3` |
| 6 | Cục QLKTNVMM | Xuất phụ lục, trình ký ngoài phần mềm (Vụ Tài chính, rồi Lãnh đạo Ban Cơ yếu) | `5.3` → eOffice |
| 7 | Cục QLKTNVMM | Đính kèm bản đã ký, nhập *Số QĐGCTKH* và *Ngày chứng từ*, bấm *Ban hành* | `5.3` · `5.5` |

*Xuất phụ lục* ở bước 6 **không** yêu cầu *Số QĐGCTKH*. Phần mềm **không đối chiếu** phụ lục đã xuất với số liệu hiện tại của quyết định.

## 3. Phân quyền

### 3.1 Phạm vi dữ liệu

Cắt theo **vị trí của người xem trong cây tổ chức**, độc lập với quyền chức năng ở Mục 3.2.

| Trạng thái quyết định | Ai thấy |
|---|---|
| ***Mới*** | Chỉ người dùng thuộc **Cục QLKTNVMM** |
| ***Đã ban hành*** | Người dùng ở **mọi cấp**, phạm vi dữ liệu theo bảng dưới |

| Người xem thuộc | Thấy dòng chi tiết của |
|---|---|
| Cục QLKTNVMM | **Toàn bộ** — đủ 5 tab, đủ mọi dòng |
| Một đơn vị bất kỳ trong cây (Cục đầu hệ hoặc cấp dưới) | **Chính đơn vị mình** và **mọi đơn vị cấp con**, đệ quy không giới hạn số tầng |

**Không thấy:** dòng của **cấp trên** mình · dòng của **đơn vị ngang hàng** (cùng đơn vị cha) · dòng của **hệ khác**.

Khối nào hiện với ai:

| Khối trên màn quyết định | Cục QLKTNVMM | Đơn vị khác trong cây |
|---|:--:|---|
| *Thông tin chung* | ✔ | ✔ |
| *Thông tin chi tiết* | ✔ | Chỉ dòng của đơn vị mình và cấp con |
| *Phân bổ theo hệ* | ✔ | **Ẩn** |
| *Tổng hợp kế hoạch toàn ngành* | ✔ | **Ẩn** |

**Đơn vị ngoài Cục QLKTNVMM chỉ xem, không sửa, không xoá** — quyết định là căn cứ để họ lập phiếu điều chuyển và phiếu cấp phát.

Phạm vi này áp cả cho **tệp phụ lục xuất ra**: người ngoài Cục QLKTNVMM xuất thì tệp **chỉ có sheet chi tiết**, đã cắt theo phạm vi.

### 3.2 Quyền theo vai trò

Quyền gán cho tài khoản ở chức năng **Quản trị người dùng**.

| Quyền | Cho phép |
|---|---|
| **Xem QĐGCTKH** | Mở màn danh sách `5.1`, mở xem chi tiết `5.2` / `5.7`, xuất phụ lục |
| **Lập QĐGCTKH** | Tạo mới, sửa *Thông tin chung*, chọn và bỏ chọn phiếu, sửa *Số lượng cấp*, thêm và xoá dòng chi tiết, nhập *Đơn giá*, đính kèm tài liệu |
| **Ban hành QĐGCTKH** | Bấm *Ban hành* |
| **Xoá QĐGCTKH** | Xoá quyết định |

Ba quyền *Lập* · *Ban hành* · *Xoá* chỉ gán cho tài khoản thuộc **Cục QLKTNVMM** — các bản hệ đầu hệ không có ba chức năng này.

### 3.3 Thao tác theo trạng thái

Một thao tác chạy được khi **tài khoản có quyền ở Mục 3.2** *và* **trạng thái quyết định cho phép**. Thiếu một trong hai thì nút không hiện.

| Thao tác trên một quyết định | *Mới* | *Đã ban hành* |
|---|:--:|:--:|
| Xem chi tiết | ✔ | ✔ |
| Sửa *Thông tin chung* | ✔ | ✘ |
| Chọn thêm phiếu · bỏ chọn phiếu | ✔ | ✘ |
| Sửa *Số lượng cấp* · thêm và xoá dòng chi tiết | ✔ | ✘ |
| Nhập *Đơn giá* | ✔ | ✘ |
| Thêm và bớt *Tài liệu đính kèm* | ✔ | ✘ |
| Xuất phụ lục | ✔ | ✔ |
| Ban hành | ✔ | ✘ |
| Xoá | ✔ | ✘ |

`✔` được làm · `✘` phần mềm chặn

*Tạo quyết định* và *Xem danh sách* không phụ thuộc trạng thái, chỉ cần quyền ở Mục 3.2.

## 4. Vòng đời trạng thái

Hai trạng thái: ***Mới*** → ***Đã ban hành***. Không có nấc trung gian, không có đường lùi.

| Trạng thái | Nghĩa |
|---|---|
| ***Mới*** | Đang soạn trên bản Cục QL. Chưa xuống các bản hệ |
| ***Đã ban hành*** | Đã có quyết định giấy ký. **Trạng thái cuối** |

| Từ | Đến | Kích hoạt bằng | Điều kiện | Hệ quả |
|---|---|---|---|---|
| *(chưa có)* | ***Mới*** | *Lưu* lần đầu ở `5.3` | Đủ trường bắt buộc khi lưu, xem `5.3` `[3]` | **Sinh *Số phiếu***, không đổi về sau. **Chiếm các phiếu đang tích** |
| ***Mới*** | ***Đã ban hành*** | *Ban hành* ở `5.2` / `5.3`, xác nhận ở `5.5` | Đủ **ba mục**: *Số QĐGCTKH* · *Ngày chứng từ* · tệp **bản đã ký** ở *Tài liệu đính kèm* | **Đóng băng HẾT** — `NFR-qdgctkh-004`. Khoá ba bảng, *Đơn giá*, việc chọn và bỏ chọn phiếu, việc đính kèm. Phiếu đã chọn **giữ nguyên liên kết**. Ghi lại người bấm và thời điểm. Quyết định bắt đầu đi xuống các bản hệ ở đợt đồng bộ kế tiếp |
| ***Mới*** | *(xoá hẳn)* | Icon xoá ở `5.1`, xác nhận ở `5.8` | — | Xoá bản ghi. **Mọi phiếu đã chọn được thả ra, dùng lại được cho quyết định khác**, chọn lại được ở `5.4`. Mọi *Số lượng cấp* đã sửa và mọi dòng thủ công mất theo |

Quyết định đã ban hành **không thu hồi, không thay thế, không xoá**. Đổi chỉ tiêu thì lập quyết định loại *Kế hoạch bổ sung*.

**Đóng băng là đóng băng bản ghi của quyết định, không phải đóng băng con số đang có hiệu lực.** Sau khi ban hành, *số gốc* của quyết định giữ nguyên vĩnh viễn, còn *số hiện hành* đổi theo từng quyết định bổ sung và từng QĐTK được ban hành sau đó (Mục 1.4). Hai con số xem ở hai tab khác nhau, `5.13` và `5.12`.

## 5. Màn hình

**15 mục**. Việc lập, sửa, ban hành và xoá chạy ở **bản Cục QL**; các màn chỉ xem quyết định **đã ban hành** — `5.7` và ba tab `5.12`–`5.14` — chạy cả ở bản của các cơ yếu đầu hệ theo phạm vi dữ liệu Mục 3.1. **Toàn bộ 15 mục đã vẽ trên Figma.**

Mọi thành phần dùng lại từ phiếu đề nghị SPMM — lưới chi tiết và ba hộp thoại ***Thêm hàng loạt***, ***Nhập Excel***, ***Điền một số cho nhiều dòng*** — đặc tả ở `docs/ngoai-giao/srs/srs-de-nghi-spmm.md`.

### 5.1 Danh sách quyết định

**Figma:** [QĐGCTKH 01 · Danh sách quyết định](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=320-16422) · **Bước:** điểm vào · **Slug:** `danh-sach-qd`

> Lọc áp dụng ngay khi nhập, không có nút *Tìm* / *Xoá lọc*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Ô chọn cột hiển thị | Multiselect | Danh sách cột | Bật tắt cột hiện trên lưới. Mặc định hiện đủ 8 cột. Chỉ đổi cách xem, không đổi dữ liệu |
| 2 | Tạo QĐGCTKH | Button | — | Mở `5.3` với quyết định trắng: *Loại kế hoạch* mặc định *Kế hoạch năm*, ba bảng rỗng. Chỉ hiện với tài khoản có quyền *Lập QĐGCTKH* |
| — | Bảng danh sách | Table | — | Cột: STT · **Số phiếu** · Trạng thái · **Số QĐGCTKH** · Loại kế hoạch · Năm áp dụng · Ngày chứng từ · Thao tác. **Không có nút *Xuất Excel*** |
| 3 | Hàng lọc từng cột | Input · Dropdown · Date | Theo cột | Lọc theo Số phiếu, Trạng thái, Số QĐGCTKH, Loại kế hoạch, Năm áp dụng, Ngày chứng từ. Lọc không ra dòng nào thì bảng rỗng, không chuyển màn |
| 4 | Số phiếu | Link | Chuỗi | Hệ sinh, luôn có kể cả khi còn *Mới*. Cột bấm để mở: dòng *Mới* mở `5.2` chỉ xem, dòng *Đã ban hành* mở `5.7` chỉ đọc |
| 5 | Trạng thái | Tag | Danh mục | Hai giá trị: *Mới* · *Đã ban hành* |
| 6 | Số QĐGCTKH | Text | Chuỗi | Số trên bản giấy đã ký. **Để trống khi còn *Mới*** |
| 7 | Loại kế hoạch | Text | Danh mục | Hai giá trị — *Kế hoạch năm* và *Kế hoạch bổ sung* (`srs-qdgctkh-bo-sung.md`). Lọc được ở hàng lọc |
| 8 | Năm áp dụng | Text | Số | Năm kế hoạch mà quyết định giao chỉ tiêu, **không phải năm lập** |
| 9 | Ngày chứng từ | Text | Ngày | Ngày ghi trên bản giấy, **không phải ngày tạo bản ghi**. Để trống khi còn *Mới* |
| 10 | Sửa | Icon button | — | Chỉ hiện ở dòng *Mới* và với tài khoản có quyền *Lập*. Mở **thẳng `5.3`**, không qua màn chỉ xem |
| 11 | Xoá | Icon button | — | Chỉ hiện ở dòng *Mới* và với tài khoản có quyền *Xoá*. Mở `5.8` trước khi xoá |
| 12 | Phân trang | Paginator | — | Mặc định 10 dòng một trang |

**Không có icon nhân bản.**

### 5.2 Quyết định *Mới* — chỉ xem

**Figma:** [QĐGCTKH 02 · Quyết định Mới — chỉ xem](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=340-33968) · **Bước:** 3–7 · **Slug:** `qd-xem`

> Cùng bố cục `5.3`, mọi ô khoá. Bấm *Số phiếu* ở `5.1` vào đây.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Mới* |
| 2 | Chuyển sang sửa | Icon button | — | Mở `5.3` với đúng quyết định đang xem. Chỉ hiện ở trạng thái *Mới* và với tài khoản có quyền *Lập* |
| 3 | Xuất phụ lục | Button | — | Hành vi như `5.3` `[15]` |
| 4 | Ban hành | Button | — | Đủ ba điều kiện ở Mục 4 thì mở `5.5`. **Thiếu bất kỳ mục nào thì phần mềm mở thẳng màn sửa `5.3` với các mục còn thiếu đã tô đỏ** — xem `5.6`. Màn này không sửa được tại chỗ nên không báo lỗi tại đây, và **không có thông báo nổi nào** |
| — | *Hủy* · *Lưu* | — | — | **Không có** |
| 5 | Nội dung bốn khối | — | — | Hiện đủ *Thông tin chung* · *Thông tin chi tiết* · *Phân bổ theo hệ* · *Tổng hợp kế hoạch toàn ngành*, **mọi ô chỉ đọc**. Ô *Phiếu đề nghị SPMM* không xổ được bảng chọn, không có icon xoá dòng, không có hàng thêm nhanh. Đổi tab và đổi *Xem theo* vẫn dùng được |

### 5.3 Tạo / sửa quyết định

**Figma:** [QĐGCTKH 03 · Tạo / sửa quyết định](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=320-17239) · **Bước:** 3–7 · **Slug:** `qd-nhap`

> Bốn khối gập xếp dọc trên một màn theo chiều thao tác: *Thông tin chung* · *Thông tin chi tiết* · *Phân bổ theo hệ* · *Tổng hợp kế hoạch toàn ngành*. Lưới chi tiết là nơi nhập; hai bảng dưới tự tính, chỉ có một ô nhập là *Đơn giá*.
>
> **Chọn và bỏ chọn phiếu làm chung ở một chỗ** — bảng chọn `5.4` xổ ra từ ô *Phiếu đề nghị SPMM*. Không có bảng liệt kê phiếu đã chọn riêng trên màn.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Mới* cho tới khi ban hành |
| 2 | Hủy | Button | — | Rời màn, bỏ thay đổi chưa lưu. Còn thay đổi chưa lưu thì hỏi lại trước khi rời |
| 3 | Lưu | Button | — | Lưu số liệu, **giữ nguyên trạng thái *Mới***. Lần lưu đầu sinh *Số phiếu* và **chiếm các phiếu đang tích** — trước lần lưu này phiếu chưa bị chiếm. Kiểm khi lưu: *Loại kế hoạch*, *Năm áp dụng*, *Phiếu đề nghị SPMM*, và *Số đề nghị* · *Số lượng cấp* của mọi dòng chi tiết. Thiếu thì báo đỏ ngay dưới trường thiếu, con trỏ nhảy về trường thiếu đầu tiên, **chặn**. Phiếu đang tích vừa bị quyết định khác chiếm → thông báo nổi *"Phiếu đề nghị `<số phiếu đề nghị>` — công văn `<số công văn>` đã được chọn vào QĐGCTKH khác."*, phần mềm **tự bỏ tích phiếu đó và xoá các dòng của nó**, lần lưu này **không thành công**, bấm lại được. Bỏ hết phiếu thì ô *Phiếu đề nghị SPMM* `[11]` trở về trống và báo lỗi bắt buộc tại ô |
| 4 | Ban hành | Button | — | **Lưu phần đang sửa trước, rồi mới kiểm điều kiện ban hành.** Ba điều kiện: *Số QĐGCTKH* `[6]`, *Ngày chứng từ* `[7]`, tệp bản đã ký ở *Tài liệu đính kèm* `[13]`. Đủ ba thì mở `5.5`; thiếu thì báo lỗi tại từng mục, xem `5.6` |
| 5 | Số phiếu | Input (chỉ đọc) | Chuỗi | Hệ sinh khi lưu lần đầu, dạng `QĐGCTKH/<mã đơn vị>/<năm>/<4 số>` (Mục 1.3), không đổi suốt vòng đời. Hiện ở cột đầu `5.1` |
| 6 | Số QĐGCTKH | Textbox | Chuỗi | Số quyết định của Ban trên bản giấy đã ký. **Bắt buộc khi *Ban hành*, không bắt buộc khi *Lưu*** — đánh dấu `*` kèm chú thích *"Bắt buộc khi Ban hành"*. Còn *Mới* thì để trống, hiện chữ mờ *"Nhập khi ban hành"*. **Đây là nơi duy nhất nhập số này**; `5.5` chỉ xác nhận. Thiếu lúc bấm *Ban hành* → báo đỏ ngay dưới ô: *"Chưa có Số QĐGCTKH."*, con trỏ nhảy về ô. **Chặn** |
| 7 | Ngày chứng từ | Datepicker | Ngày | **Bắt buộc khi *Ban hành*, không bắt buộc khi *Lưu***. Thiếu lúc bấm *Ban hành* → báo đỏ dưới ô: *"Chưa có Ngày chứng từ."*. **Chặn** |
| 8 | Loại kế hoạch | Dropdown | Danh mục | Bắt buộc khi *Lưu*, mặc định *Kế hoạch năm*. Chọn *Kế hoạch bổ sung* thì màn chuyển sang bố cục ở `srs-qdgctkh-bo-sung.md` `5.2`. **Là một trong hai điều kiện lọc danh sách phiếu ở `5.4`**. **Chỉ đổi được khi quyết định còn *Mới***; đang có phiếu được chọn thì đổi phải qua `5.11` |
| 9 | Năm áp dụng | Dropdown | Số | Bắt buộc khi *Lưu*. Năm kế hoạch mà quyết định giao chỉ tiêu, **không phải năm lập**. **Là điều kiện lọc thứ hai của danh sách phiếu ở `5.4`**. Đổi giá trị: cùng luật với `[8]` |
| 10 | Phương thức tạo | — | — | **Không hiện trên màn đợt này.** Mọi quyết định đều tạo từ phiếu đề nghị SPMM; *Tạo thủ công* làm giai đoạn sau (Mục 1.2) |
| 11 | Phiếu đề nghị SPMM | Dropdown chọn nhiều | Danh sách | **Bắt buộc.** Bấm mở bảng chọn `5.4` ngay bên dưới — **nơi duy nhất chọn và bỏ chọn phiếu**. **Chưa điền *Loại kế hoạch* và *Năm áp dụng* thì chưa mở được bảng chọn** — hai giá trị đó là điều kiện lọc danh sách. Chưa chọn thì hiện chữ mờ *"Chọn phiếu đã tiếp nhận…"*; đã chọn thì ghi ***"Đã chọn N phiếu"***, không bày thành thẻ |
| 12 | Mô tả | Textarea | Chuỗi | Không bắt buộc |
| 13 | Tài liệu đính kèm | Button | Tệp | Nút kèm số đếm tệp. **Bắt buộc có tệp bản quyết định đã ký khi *Ban hành***, không bắt buộc khi *Lưu*. Thiếu lúc bấm *Ban hành* → báo đỏ ngay dưới nút: *"Chưa đính kèm bản quyết định đã ký."*. **Chặn**. Phần mềm không kiểm nội dung tệp |
| 14 | Dải tab hệ | Tabs | — | Năm tab cố định: *Cơ yếu Đảng chính quyền* · *Cơ yếu Bộ Công an* · *Cơ yếu Quân đội* · *Cơ yếu Bộ ngoại giao* · *Cục QLKTNVMM*. Số trong ngoặc là số dòng chi tiết của tab. Mở mặc định tab đầu tiên |
| 15 | Xuất phụ lục | Button | — | Một nút, ra **một tệp Excel 7 sheet** — lưới chi tiết không có nút xuất riêng. Thứ tự sheet: *1. Tổng hợp toàn ngành* · *2. Phân bổ theo hệ* · **5 sheet chi tiết, mỗi hệ một sheet** theo đúng thứ tự tab `[14]`. Mọi sheet lặp lại khối đầu trang *Số phiếu · Số QĐGCTKH · Ngày chứng từ · Loại kế hoạch · Năm áp dụng*. Trong phụ lục, **SPMM tách thành hai cột *Mã* và *Tên*, địa điểm triển khai cũng vậy** — khác màn hình, nơi mỗi thứ là một cột gộp. Sheet chi tiết **không có *Đơn giá* và *Thành tiền***. Khuôn mẫu của **quyết định năm**: [`PhuLuc_QDGCTKH_Nam_Mau.xlsx`](PhuLuc_QDGCTKH_Nam_Mau.xlsx). **Dùng được ngay ở *Mới*, không cần *Số QĐGCTKH***. **Lưu trước rồi mới xuất**. Không đổi trạng thái, không khoá gì. Quyết định **đã có văn bản điều chỉnh** thì bấm nút mở `5.15` chọn bản xuất trước |
| 16 | Lưới *Thông tin chi tiết* | Table | — | **Dùng lại nguyên lưới chi tiết của phiếu đề nghị SPMM** — cùng ô *Xem theo* với **ba cách xem** (*Nhóm theo SPMM* mặc định · *Nhóm theo địa điểm triển khai* · *Trải phẳng*), cùng hàng công cụ (*+ Thêm hàng loạt* · *Nhập Excel* · *Tải xuống tệp mẫu*), cùng hàng lọc trong lưới, cùng bộ cột (SPMM · Địa điểm triển khai · ĐVT · Hiện trạng · Số đề nghị · Ghi chú mục đích), cùng icon xoá dòng, cùng hàng thêm nhanh, cùng dòng đếm chân lưới. Hành vi từng thành phần đặc tả ở `docs/ngoai-giao/srs/srs-de-nghi-spmm.md`. **Mọi thao tác áp cho tab đang mở.** Hai chỗ khác phiếu đề nghị: **thêm cột *Số lượng cấp*** `[17]`, và **dòng đếm chân lưới có thêm nhãn *"Hiện trạng cập nhật đến `<ngày>`"*** |
| 17 | Số lượng cấp | Input số | Số nguyên | **Cột duy nhất quyết định thêm vào lưới.** Chỉ nhập ở dòng con, dòng nhóm để trống. Nhận **số nguyên từ `0` trở lên**; `0` nghĩa là *đợt này không cấp* và **phần mềm không tự xoá dòng** — dòng vẫn giữ để lưu dấu vết đề nghị. Số âm hoặc số thập phân → báo đỏ dưới ô: *"Số lượng cấp phải là số nguyên không âm."* Mặc định bằng *Số đề nghị* của cùng dòng, kể cả **dòng thêm tay** — gõ *Số đề nghị* thì số đó đổ sang. **Không kiểm gì so với *Số đề nghị*** — lớn hơn, bằng hay nhỏ hơn đều được. **Bắt buộc có giá trị khi *Lưu***; thiếu → báo đỏ tại ô: *"Chưa có Số lượng cấp."*, **chặn**. Đây là con số chảy lên hai bảng dưới |
| 18 | Xoá dòng chi tiết | Icon button | — | Ở cuối mỗi dòng con **và ở dòng nhóm**. **Xoá được cả dòng đến từ phiếu lẫn dòng thêm thủ công.** **Dòng con xoá thẳng, không hỏi**; **dòng nhóm mở `5.9` xác nhận** vì xoá một lượt nhiều dòng. Luật này áp cho cả hai cách xem có nhóm. Xoá dòng của phiếu **không tách phiếu khỏi quyết định**, trừ khi đó là **dòng cuối cùng của phiếu đó** — khi đó phiếu tự được bỏ chọn và nhả ra, kèm thông báo nổi *"Đã bỏ chọn phiếu đề nghị `<số phiếu đề nghị>` vì không còn dòng chi tiết nào."* |
| 19 | *Phân bổ theo hệ* — cột | Table | — | SPMM (`Mã - Tên`) · ĐVT · bốn cột hệ · hai cột của Cục QLKTNVMM là ***Triển khai*** và ***Dự phòng*** · Tổng · dòng Tổng cộng. **Không tách triển khai / dự phòng thành cột riêng cho 4 hệ** |
| 20 | *Phân bổ theo hệ* — số | Table | Số nguyên | **Tự cộng từ lưới chi tiết, không có ô nhập nào.** Bấm vào số thì nhảy sang tab tương ứng ở lưới chi tiết và lọc sẵn đúng SPMM đó. Hệ chưa có dữ liệu trong đợt **để trống ô**, không điền `–` cũng không điền `0` |
| 21 | *Tổng hợp toàn ngành* — cột | Table | — | SPMM (`Mã - Tên`) · ĐVT · Tổng SL · Đơn giá · Thành tiền |
| 22 | *Tổng hợp* — Tổng SL | Text | Số nguyên | Tự tính, không sửa trực tiếp |
| 23 | *Tổng hợp* — Đơn giá | Input số | Số tiền | **Không bắt buộc.** Gợi ý mặc định từ **bảng giá đang ở trạng thái *Hiệu lực***. **SPMM chưa có trong bảng giá thì để trống**, không điền `0` — ô trống là *"chưa có giá"*, `0` là *"giá bằng không"*. Nhận `0`; số âm → báo đỏ dưới ô: *"Đơn giá không được là số âm."* Sửa tay tự do cho tới khi ban hành. **Để trống không chặn ban hành** |
| 24 | *Tổng hợp* — Thành tiền | Text | Số tiền | Tổng SL nhân Đơn giá, tự tính. *Đơn giá* để trống thì *Thành tiền* cũng để trống |
| 25 | Tổng tiền ngân sách dự trù | Table footer | Số tiền | Cộng cột Thành tiền, **bỏ qua dòng chưa có đơn giá**. **Không gọi là *"Tổng cộng thành tiền"*** |

### 5.4 Bảng chọn phiếu đề nghị

**Figma:** [QĐGCTKH 04 · Bảng chọn phiếu đề nghị](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=320-18394) · **Bước:** 3 · **Slug:** `gom-phieu`

> **Bảng xổ xuống của ô *Phiếu đề nghị SPMM***, không phải hộp thoại — không có nút đóng riêng, thoát bằng *Hủy*. Mở lại được nhiều lần.
>
> **Đây là nơi làm cả hai việc chọn và bỏ chọn.** Bảng hiện đồng thời phiếu **đã chọn cho quyết định đang mở** (tích sẵn) và phiếu **chưa thuộc quyết định nào** (chưa tích). Tích thêm một dòng là chọn, bỏ tích một dòng đang tích là bỏ chọn.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Hàng lọc trong bảng | Input · Dropdown | Theo cột | Ngay dưới tiêu đề cột: lọc theo Số phiếu đề nghị, Số công văn, Đơn vị đề nghị, Năm áp dụng. Không có ô tìm chung, không có dải lọc theo hệ |
| 2 | Ô tích chọn | Checkbox | Boolean | Tích nhiều phiếu một lượt. **Phiếu đã chọn cho quyết định đang mở thì mở bảng ra là đã tích sẵn.** Ô tích ở hàng tiêu đề chọn hết những dòng **đang hiện** |
| 3 | Số phiếu đề nghị | Link | Chuỗi | Số hệ sinh của phiếu đề nghị, dạng `PDN/<mã đơn vị>/<năm>/<4 số>`. **Gọi là *Số phiếu đề nghị*, không gọi tắt là *Số phiếu*** — trên màn này *Số phiếu* đã là số của quyết định |
| 4 | Số công văn | Text | Chuỗi | Số công văn giấy đã ký đi kèm phiếu |
| 5 | Đơn vị đề nghị | Text | Chuỗi | Đơn vị đứng tên phiếu. Phiếu tự đề nghị của Cục QLKTNVMM thì đơn vị đề nghị là Cục QLKTNVMM |
| 6 | Năm áp dụng | Text | Số | Năm kế hoạch của phiếu. **Luôn bằng *Năm áp dụng* của quyết định** — phiếu khác năm đã bị lọc khỏi danh sách |
| 7 | Dòng đếm chân bảng | Label | — | *"N / M phiếu đang chọn"*. Cập nhật ngay khi tích hoặc bỏ tích |
| 8 | Hủy | Button | — | Đóng bảng, giữ nguyên danh sách phiếu đang chọn — mọi thay đổi tích chưa xác nhận đều bỏ |
| 9 | Xác nhận | Button | — | Áp thay đổi tích vào quyết định. **Phiếu vừa tích thêm**: dòng của phiếu đổ vào đúng tab của hệ tương ứng, hai bảng dưới tính lại. **Phiếu chưa bị chiếm ở bước này** — chiếm ở lần *Lưu*, xem `5.3` `[3]`. **Phiếu vừa bỏ tích**: tách khỏi quyết định, dùng lại được cho quyết định khác — mọi dòng của phiếu đó ở lưới chi tiết mất theo, **kể cả dòng đã sửa *Số lượng cấp***; dòng thủ công và dòng của phiếu khác không bị đụng. **Có bỏ tích thì mở `5.10` xác nhận trước khi áp** |

**Bốn điều kiện lọc danh sách** — phiếu phải thoả cả bốn mới hiện:

| # | Điều kiện |
|:--:|---|
| 1 | Trạng thái phiếu là ***Đã tiếp nhận*** — phiếu ở *Mới*, *Chờ tiếp nhận*, *Trả lại* không lên |
| 2 | ***Loại kế hoạch* của phiếu trùng *Loại kế hoạch* của quyết định** — quyết định *Kế hoạch năm* chỉ thấy phiếu *Kế hoạch năm* |
| 3 | ***Năm áp dụng* của phiếu trùng *Năm áp dụng* của quyết định** |
| 4 | Phiếu **chưa bị quyết định nào khác chiếm**, hoặc **thuộc chính quyết định đang mở** (dòng này hiện tích sẵn) |

Điều kiện 4 tính theo **liên kết đã lưu**, không theo trạng thái của quyết định kia: phiếu đã lưu vào một quyết định khác thì không lên đây **dù quyết định đó mới chỉ ở trạng thái *Mới*** — xem `BR-qdgctkh-002`. Điều kiện này **kiểm lại lúc *Lưu***; phiếu bị chiếm trong lúc bảng đang mở thì xử theo `5.3` `[3]`.

Đổi *Loại kế hoạch* hoặc *Năm áp dụng* ở `5.3` thì **danh sách lọc lại theo giá trị mới**.

**Tra một phiếu không thấy trong bảng:** mở chính phiếu đó ở màn phiếu đề nghị — phiếu mang thông tin *"đã dùng trong `<số phiếu quyết định>`"*.

### 5.5 Hộp thoại xác nhận ban hành

**Figma:** [QĐGCTKH 05 · Popup xác nhận ban hành](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=334-29753) · **Bước:** 7 · **Slug:** `ban-hanh`

> Hộp thoại xác nhận, **không phải biểu mẫu nhập**. Mọi trường đã điền ở `5.3`.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xác nhận ban hành quyết định"* |
| 2 | Nội dung nhắc lại | Label | — | Nhắc lại **Số phiếu**, **Số QĐGCTKH**, **Ngày chứng từ**, **tên tệp bản đã ký** và **Tổng tiền ngân sách dự trù**. Không nhập lại gì |
| 3 | Hệ quả | Label | — | Nêu rõ: ban hành thì **khoá** ba bảng, *Đơn giá*, việc chọn và bỏ chọn phiếu, việc đính kèm; và **không thu hồi, không thay thế, không xoá được** |
| 4 | Hủy | Button | — | Đóng hộp thoại, quyết định **giữ trạng thái *Mới***, sửa tiếp được |
| 5 | Xác nhận ban hành | Button | — | Chuyển sang *Đã ban hành*, mở `5.7`. Ghi lại **người bấm và thời điểm** |

### 5.6 Ban hành bị chặn ở màn sửa

**Figma:** [QĐGCTKH 06 · Ban hành bị chặn (lỗi tại ô)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=334-30768) · **Bước:** 7 · **Slug:** `ban-hanh-thieu-dieu-kien`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Báo lỗi tại từng mục | Label (lỗi) | — | Bấm *Ban hành* ở `5.3` — hoặc bấm ở `5.2`, khi đó phần mềm mở thẳng `5.3` ở đúng trạng thái này — mà thiếu điều kiện nào thì **hiện lỗi ngay dưới mục đó**, đồng thời cho mọi mục còn thiếu: dưới ô *Số QĐGCTKH* — *"Chưa có Số QĐGCTKH."* · dưới ô *Ngày chứng từ* — *"Chưa có Ngày chứng từ."* · dưới nút *Tài liệu đính kèm* — *"Chưa đính kèm bản quyết định đã ký."* |
| 2 | Vị trí con trỏ | — | — | Nhảy về **mục thiếu đầu tiên** theo thứ tự trên màn |
| 3 | Hệ quả | — | — | `5.5` **không mở**, quyết định giữ nguyên *Mới*. **Chặn** |

### 5.7 Quyết định đã ban hành

**Figma:** [QĐGCTKH 07 · Quyết định đã ban hành (chỉ đọc)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=334-24984) · **Bước:** sau 7 · **Slug:** `qd-da-ban-hanh`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Đã ban hành* |
| 2 | Toàn màn | — | — | Cùng bố cục `5.3` ở chế độ **chỉ đọc**: không sửa bảng nào, không sửa *Đơn giá*, ô *Phiếu đề nghị SPMM* không xổ được bảng chọn nên không chọn thêm cũng không bỏ chọn được, không có icon xoá dòng, không có hàng thêm nhanh. Đổi tab và đổi *Xem theo* vẫn dùng được. **Khối nào hiện và dòng nào hiện cắt theo Mục 3.1** — người ngoài Cục QLKTNVMM không thấy *Phân bổ theo hệ* và *Tổng hợp kế hoạch toàn ngành* |
| 3 | Xuất phụ lục | Button | — | Dùng được. **Đã có văn bản điều chỉnh thì mở `5.15` chọn bản xuất trước**; chưa có thì xuất thẳng bản gốc, không hỏi. Cục QLKTNVMM xuất ra tệp **7 sheet**; đơn vị khác xuất ra tệp **chỉ có sheet chi tiết của chính hệ mình**, cắt theo phạm vi |
| 4 | Tài liệu đính kèm | Button | Tệp | Mở xem bản đã ký. **Không thêm, không bớt tệp** |
| 5 | Dải tab bản kế hoạch | Tabs | — | Ba tab, đặt ngay trên khối *Thông tin chi tiết*: ***Kế hoạch hiện hành*** `5.12` (mặc định) · ***Kế hoạch năm*** `5.13` · ***Lịch sử điều chỉnh*** `5.14`. **Chưa có văn bản điều chỉnh nào thì cả dải tab không hiện** — màn chỉ có ba bảng của bản gốc. Dải tab dùng **đúng thành phần tab của khối *Thông tin chi tiết*** |
| — | *Thông tin chung* | — | — | **Nằm ngoài dải tab, luôn hiện.** Nó là danh tính văn bản, không đổi theo cách xem |
| — | *Hủy* · *Lưu* · *Ban hành* | — | — | **Không có** |

### 5.8 Hộp thoại xoá quyết định

**Figma:** [QĐGCTKH 08 · Cảnh báo xoá quyết định](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=334-25984) · **Bước:** ngoài luồng chính · **Slug:** `xoa-qd-canh-bao`

> Bốn hộp thoại `5.8`–`5.11` theo khuôn hộp thoại xác nhận ở `docs/design.md` Mục 9.4: tiêu đề là cụm động từ hành động · dòng nhận diện · câu hệ quả · nút chính mang đúng chữ của tiêu đề. **`5.9` gom thành hộp thoại *Xoá nhóm* dùng chung cho cả hai cách xem có nhóm** — tiêu đề và câu hệ quả không nói nhóm theo gì, dòng nhận diện lấy đúng nhãn dòng nhóm đang xoá. Thêm tệp khuôn mẫu `PhuLuc_QDGCTKH_HienHanh_Mau.xlsx` cho bản xuất *Kế hoạch hiện hành* — 7 sheet, số hiện hành, sheet Tổng hợp không có cột *Đơn giá*, khối đầu trang ghi mốc thời điểm.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xoá quyết định"* |
| 2 | Dòng nhận diện | Label | — | *"Số phiếu `<số phiếu>` — Số QĐGCTKH `<giá trị>`."*. Quyết định còn *Mới* thì *Số QĐGCTKH* trống, dòng chỉ còn *"Số phiếu `<số phiếu>`."* |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi xoá, quyết định không khôi phục được. Vui lòng xác nhận."* |
| 4 | Hủy | Button | — | Đóng, không xoá gì |
| 5 | Xoá quyết định | Button | — | Xoá hẳn quyết định. **Mọi phiếu đã chọn được thả ra, dùng lại được cho quyết định khác**, hiện lại ở `5.4` |

Chỉ xoá được quyết định ở trạng thái *Mới*.

### 5.9 Hộp thoại xoá nhóm

**Figma:** [QĐGCTKH 12 · Xoá nhóm — xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1178-63851) · **Bước:** 5 · **Slug:** `xoa-nhom-canh-bao`

> Chỉ mở khi xoá ở **dòng nhóm** — xoá một lượt mọi dòng con của nhóm đó. Xoá **một dòng con lẻ** thì xoá thẳng, không hỏi. **Dùng chung cho cả hai cách xem có nhóm** (*Nhóm theo SPMM* và *Nhóm theo địa điểm triển khai*); cách xem *Trải phẳng* không có dòng nhóm nên không có ca này.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xoá nhóm"* — **không nói nhóm theo gì**, vì cùng một hộp thoại dùng cho cả hai cách xem |
| 2 | Dòng nhận diện | Label | — | *"Nhóm `<nhãn của dòng nhóm đang xoá>`."* — lấy **đúng chữ đang hiện trên dòng nhóm**: cách xem *Nhóm theo SPMM* ra `Mã - Tên SPMM`, cách xem *Nhóm theo địa điểm triển khai* ra tên địa điểm |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi xoá, toàn bộ dòng con của nhóm này không khôi phục được. Vui lòng xác nhận."* |
| 4 | Hủy | Button | — | Đóng, không xoá gì |
| 5 | Xoá nhóm | Button | — | Xoá, hai bảng dưới tính lại. Phiếu nào hết sạch dòng thì tự bỏ chọn theo `5.3` `[18]` |

### 5.10 Hộp thoại bỏ chọn phiếu

**Figma:** [QĐGCTKH 13 · Bỏ chọn phiếu — xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1178-65891) · **Bước:** 3 · **Slug:** `bo-chon-phieu-canh-bao`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Bỏ chọn phiếu đề nghị"* |
| 2 | Dòng nhận diện | Label | — | Một dòng cho mỗi phiếu vừa bỏ tích: *"Số phiếu đề nghị `<số>`."* |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi bỏ chọn, mọi dòng chi tiết của phiếu mất theo. Vui lòng xác nhận."* |
| 4 | Hủy | Button | — | Đóng, giữ nguyên phiếu đang chọn — không áp thay đổi tích nào |
| 5 | Bỏ chọn phiếu đề nghị | Button | — | Áp thay đổi tích ở `5.4`. Phiếu bị bỏ chọn dùng lại được cho quyết định khác. Dòng thủ công và dòng của phiếu khác không bị đụng |

### 5.11 Hộp thoại đổi trường lọc

**Figma:** [QĐGCTKH 14 · Đổi trường lọc — cảnh báo](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1178-65017) · **Bước:** 3 · **Slug:** `doi-truong-loc-canh-bao`

> Dùng chung cho **hai trường** *Loại kế hoạch* `[8]` · *Năm áp dụng* `[9]`. Chỉ hiện khi **đang có phiếu được chọn**; không có phiếu nào thì đổi thẳng, không hỏi.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Đổi `<tên trường>`"* |
| 2 | Dòng nhận diện | Label | — | *"`<tên trường>`: `<giá trị cũ>` → `<giá trị mới>`."* |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi đổi, mọi phiếu đã chọn và dòng đi theo phiếu bị bỏ. Vui lòng xác nhận."* |
| 4 | Hủy bỏ | Button | — | Đóng, **giữ nguyên giá trị cũ** của trường |
| 5 | Đồng ý | Button | — | Đổi giá trị trường, **bỏ toàn bộ phiếu đã chọn và mọi dòng đi theo phiếu**; **dòng thêm tay giữ nguyên**. Phiếu vừa bỏ dùng lại được. Danh sách ở `5.4` lọc lại theo giá trị mới. Cặp nút *Hủy bỏ* / *Đồng ý* thay vì lấy động từ của tiêu đề — đây là hộp thoại hỏi *có đi tiếp không*, không phải nấc chốt một hành động (`design.md` Mục 9.4) |

### 5.12 Tab *Kế hoạch hiện hành*

**Figma:** [QĐGCTKH 09 · Kế hoạch hiện hành (sau điều chỉnh)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=834-2415) · **Bước:** sau 7 · **Slug:** `qd-nam-hien-hanh`

> **Tab mặc định** khi mở một quyết định năm đã có ít nhất một văn bản điều chỉnh. Trả lời câu *"đến hôm nay chỉ tiêu còn bao nhiêu"*. Ba bảng cùng bộ khung với `5.7`, chỉ đổi con số và bỏ hai cột.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Lưới *Thông tin chi tiết* | Table | — | **Không thêm cột nào so với bản gốc**, dù có bao nhiêu văn bản điều chỉnh. Cột *Số lượng cấp* hiện ***số hiện hành*** theo công thức Mục 1.4. Cùng năm tab hệ, cùng ba cách xem, cùng hàng lọc, cùng khung cuộn. **Chỉ đọc** — không có hàng thêm nhanh, không có icon xoá dòng, không có hàng công cụ |
| 2 | Số lượng cấp | Text (chỉ đọc) | Số nguyên | Số hiện hành của cặp `SPMM × địa điểm × năm`. Dòng nhóm hiện tổng của các dòng con. **Cặp mới mọc ra từ một quyết định bổ sung cũng là một dòng bình thường ở đây** — không đánh dấu gì thêm |
| — | Cột *Hiện trạng* | — | — | **Không hiện** — `BR-qdgctkh-bo-sung-023` |
| 3 | *Phân bổ theo hệ* | Table | Số nguyên | Cùng bộ cột với `5.3` `[19]`. Hiện **số hiện hành** của từng hệ, **không có dấu cộng trừ** |
| 4 | *Tổng hợp kế hoạch toàn ngành* — cột | Table | — | SPMM (`Mã - Tên`) · ĐVT · ***Tổng SL*** · ***Thành tiền (VND)***. **Không có cột *Đơn giá*** — Mục 1.4 |
| 5 | Thành tiền | Text | Số tiền | **Cộng dồn *Thành tiền* của quyết định năm và của mọi văn bản điều chỉnh đã ban hành** cho SPMM đó, không phải `Tổng SL × một đơn giá nào` |
| 6 | Tổng cộng | Table footer | Số | Một dòng, cộng cột *Tổng SL* và cột *Thành tiền* |
| 7 | Xuất phụ lục | Button | — | Nút nằm ngoài dải tab. Bấm thì mở `5.15` chọn bản xuất, **radio chọn sẵn *Kế hoạch hiện hành*** vì đang đứng ở tab này |

### 5.13 Tab *Kế hoạch năm*

**Figma:** [QĐGCTKH 10 · Kế hoạch năm (bản ban hành gốc)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1113-48464) · **Bước:** sau 7 · **Slug:** `qd-nam-ban-goc`

> Đúng bản đã ký, **không bao giờ đổi**. Trả lời câu *"lúc ký thì giao bao nhiêu"*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Toàn bộ ba bảng | Table | — | **Y hệt `5.7`** — bản chụp lúc ban hành, đọc từ bản ghi đóng băng (`NFR-qdgctkh-004`), kể cả tên SPMM, ĐVT và tên địa điểm |
| 2 | *Tổng hợp kế hoạch toàn ngành* | Table | — | **Có đủ cột *Đơn giá***, khác `5.12` |
| 3 | Dòng đếm chân lưới | Label | — | Kèm hậu tố ***"bản ban hành ngày `<ngày chứng từ>`"*** |
| 4 | Số dòng chi tiết | — | — | **Ít hơn `5.12`** nếu quyết định bổ sung đã thêm cặp `SPMM × địa điểm` mới. Số trong ngoặc ở dải tab hệ đếm theo **tab bản kế hoạch đang mở** |

### 5.14 Tab *Lịch sử điều chỉnh*

**Figma:** [QĐGCTKH 11 · Lịch sử điều chỉnh](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=835-5633) · **Bước:** sau 7 · **Slug:** `qd-nam-lich-su`

> Danh sách **mọi văn bản đã tác động lên kế hoạch của năm này**, xếp theo *Ngày chứng từ* tăng dần. Trả lời câu *"năm nay đã có những văn bản nào"*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Bảng *Các văn bản điều chỉnh* | Table | — | Năm cột: **Số phiếu · Số quyết định · Loại văn bản · Phạm vi · Ngày chứng từ**. Không có cột tóm tắt tăng giảm và không có cột tiền — muốn xem thì bấm mở văn bản |
| 2 | Mốc đầu tiên | — | — | **Chính quyết định năm gốc**, luôn là dòng đầu |
| 3 | Số phiếu | Link | Chuỗi | Bấm mở văn bản đó **ở tab trình duyệt mới** |
| 4 | Số quyết định | Text | Chuỗi | *Số QĐGCTKH* của văn bản đó |
| 5 | Loại văn bản | Text | Danh mục | Ba giá trị: *Kế hoạch năm* · *Kế hoạch bổ sung* · *Quyết định triển khai* |
| 6 | Phạm vi | Text | Chuỗi | **Điền cho mọi dòng, không để trống dòng nào.** *Kế hoạch năm* và *Kế hoạch bổ sung* → ***Toàn ngành***. *Quyết định triển khai* → **tên cơ yếu đầu hệ** mà nó tác động, ví dụ *Cơ yếu ĐCQ*; QĐTK rút hàng từ kho Cục QLKTNVMM thì ghi ***`Cục QLKTNVMM → <tên hệ>`*** |
| 7 | Ngày chứng từ | Text | Ngày | Ngày trên bản giấy của văn bản đó |
| — | Dòng *Tổng cộng* | — | — | **Không có.** Cộng *Thành tiền* của các văn bản là việc của `5.12` `[5]` |
| — | Văn bản còn *Mới* | — | — | **Không lên bảng này.** Chỉ văn bản **đã ban hành** mới có mặt |


### 5.15 Hộp thoại chọn bản xuất phụ lục

**Figma:** [QĐGCTKH 15 · Chọn bản xuất phụ lục](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1178-67679) · **Bước:** 6 và sau 7 · **Slug:** `chon-ban-xuat-phu-luc`

> Chỉ mở khi quyết định năm **đã có ít nhất một văn bản điều chỉnh**. Chưa có thì nút *Xuất phụ lục* xuất thẳng bản gốc.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xuất phụ lục"* |
| 2 | Chọn bản xuất | Radio button | Chọn một | Hai lựa chọn: ***Kế hoạch năm*** — bản gốc đã ký, đúng nội dung `5.13` · ***Kế hoạch hiện hành*** — số sau khi cộng mọi văn bản điều chỉnh đã ban hành, đúng nội dung `5.12`. **Chọn sẵn theo tab đang đứng**; đứng ở tab *Lịch sử điều chỉnh* thì chọn sẵn *Kế hoạch hiện hành* |
| 3 | Huỷ | Button | — | Đóng, không xuất gì |
| 4 | Xuất phụ lục | Button | — | Xuất tệp theo bản đã chọn. Không đổi trạng thái, không khoá gì |
| — | Nội dung tệp *Kế hoạch năm* | — | — | Đúng như `5.3` `[15]` — 7 sheet, số của bản gốc, sheet *Tổng hợp* có đủ *Đơn giá* và *Thành tiền* |
| — | Nội dung tệp *Kế hoạch hiện hành* | — | — | Cùng 7 sheet và cùng bộ cột, khác hai chỗ: cột số là **số hiện hành**, và sheet *Tổng hợp* **không có cột *Đơn giá*** (Mục 1.4). Khối đầu trang có thêm dòng ***"Số hiện hành tính đến `<ngày giờ>`"*** — là **thời điểm bấm xuất**, vì số hiện hành tính khi đọc chứ không lưu. Khuôn mẫu `PhuLuc_QDGCTKH_HienHanh_Mau.xlsx` **đang hoàn thiện, chưa giao kèm gói này** |
| — | Phạm vi dữ liệu | — | — | Cắt theo Mục 3.1 cho **cả hai bản** — người ngoài Cục QLKTNVMM xuất ra tệp chỉ có sheet chi tiết của hệ mình |
| — | Tab *Lịch sử điều chỉnh* | — | — | **Không có bản xuất riêng.** Danh sách văn bản xem trên màn, bấm từng dòng để mở |

## 6. Yêu cầu chức năng không thuộc màn hình nào

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `FR-qdgctkh-001` | **Ba bảng tính một chiều:** lưới chi tiết → *Phân bổ theo hệ* → *Tổng hợp kế hoạch toàn ngành*. Không có đường tính ngược. Ô nhập duy nhất ở hai bảng sau là *Đơn giá* | Sửa một ô *Số lượng cấp* → số ở cả hai bảng dưới đổi theo ngay; không có cách nào sửa hai bảng dưới để làm đổi lưới chi tiết |
| `FR-qdgctkh-002` | **Chỉ có MỘT Bảng giá SPMM, dùng chung cho cả QĐGCTKH và Hợp đồng sản xuất.** Cả hai **chỉ lấy giá gợi ý** rồi **sửa tay tự do** — không bên nào bị buộc bằng giá trong bảng, và **hợp đồng không lấy giá từ quyết định** mà lấy thẳng từ bảng giá. Đổi bảng giá **không sửa lại** đơn giá của quyết định đã lưu. Quyết định giữ đơn giá **ở mức SPMM toàn ngành** (bảng *Tổng hợp*, `5.3` `[23]`), **không giữ đơn giá trên từng dòng chi tiết**. ⚠️ **Bản đang chạy chưa có bảng giá nào — phải làm mới** | Đổi giá một SPMM trong bảng giá → quyết định đã lưu giữ số cũ, quyết định tạo mới lấy giá mới. Mở màn lập Hợp đồng sản xuất cho cùng SPMM → giá gợi ý **giống hệt** giá gợi ý của quyết định, và sửa tay được |
| `FR-qdgctkh-003` | **Danh mục địa điểm triển khai dựng từ cây tổ chức**, thêm hai mục `— Triển khai` và `— Dự phòng` của chính **đơn vị lập** — **không giới hạn ở Cơ yếu đầu hệ**. Mục `— Dự phòng` **sinh theo cờ ở Quản lý đơn vị**, không tạo bản ghi đơn vị mới | Bật cờ cho một đơn vị → danh sách địa điểm của đơn vị đó có thêm mục `— Dự phòng`; cây tổ chức ở các chức năng khác không xuất hiện đơn vị nào tên *Dự phòng* |
| `FR-qdgctkh-004` | **Ghi dữ liệu thất bại thì không mất gì.** Áp cho *Lưu*, *Ban hành*, chọn phiếu, bỏ chọn phiếu, xoá: máy chủ lỗi hoặc mất kết nối thì dữ liệu đang nhập **giữ nguyên trên màn**, quyết định **giữ nguyên trạng thái cũ**, bấm lại được | Ngắt kết nối rồi bấm *Lưu* → số đang gõ còn nguyên, trạng thái không đổi, có thông báo lỗi, bấm lại được |
| `FR-qdgctkh-005` | **Trạng thái nguồn là điều kiện của mọi thao tác đổi trạng thái.** *Ban hành* và *Xoá* chỉ chạy khi quyết định còn *Mới*. Quyết định đã rời trạng thái đó thì lần bấm sau **không có tác dụng**, màn hiện lại trạng thái mới nhất | Mở cùng một quyết định ở hai phiên, ban hành ở phiên thứ nhất, bấm *Ban hành* ở phiên thứ hai → không ban hành lần hai, màn hiện *Đã ban hành* |
| `FR-qdgctkh-006` | **Phân quyền ở Mục 3.1, 3.2 và 3.3 phải chặn được ở mọi đường truy cập**, không chỉ ẩn nút hoặc ẩn khối trên màn. Áp cho cả ba lớp: phạm vi dữ liệu, quyền theo vai trò, thao tác theo trạng thái | Đăng nhập bằng tài khoản một đơn vị cấp dưới rồi gọi thẳng tới một quyết định *Mới*, tới dòng chi tiết của đơn vị ngang hàng, và tới thao tác *Ban hành* → cả ba đều bị từ chối |
| `FR-qdgctkh-007` | **Số hiện hành tính bằng cộng dồn khi xem, không lưu**, và **quyết định năm không bị văn bản nào sửa vào bản ghi**. Nguồn delta là quyết định bổ sung và QĐTK **đã ban hành** | Ban hành một quyết định bổ sung → tab `5.12` đổi đúng phần chênh, tab `5.13` không đổi một con số nào. Xoá quyết định bổ sung khi còn *Mới* → cả hai tab không đổi. Ban hành hai quyết định bổ sung cùng chạm một SPMM → cột *Thành tiền* ở `5.12` bằng đúng tổng *Thành tiền* của quyết định năm và của cả hai quyết định bổ sung đó |

## 7. Quy tắc nghiệp vụ

Chỉ những quy tắc **xuyên nhiều màn** hoặc **không thuộc màn nào**. Luật của từng ô nằm trong bảng mô tả màn ở Mục 5.

| ID | Quy tắc | Áp ở | Căn cứ |
|---|---|---|---|
| `BR-qdgctkh-001` | **Một phiếu đề nghị chỉ vào MỘT quyết định.** Thể hiện bằng **liên kết**, **không đổi trạng thái phiếu** — *Đã tiếp nhận* vẫn là trạng thái cuối của phiếu | `5.3`, `5.4`, `5.8` | brainstorming Mục 7 |
| `BR-qdgctkh-002` | **Phiếu bị chiếm ngay khi *Lưu* quyết định đang *Mới***, không đợi ban hành. Nên phiếu đã lưu vào một quyết định khác thì **không lên danh sách chọn dù quyết định đó còn *Mới***. Tích ô ở `5.4` mà chưa *Lưu* thì **chưa chiếm gì**. Bỏ tích thì phiếu dùng lại được; **xoá hẳn quyết định đang *Mới*** thì mọi phiếu của nó nhả ra | `5.3` `[3]`, `5.4` | brainstorming Mục 7 · @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-004` | ***Ban hành* thực hiện *Lưu* trước.** Bấm *Ban hành* khi đang sửa dở thì phần vừa sửa được lưu trước, không ban hành bản cũ | `5.2`, `5.3` | @quynhdtn17 chốt 21/08/2026 |
| `BR-qdgctkh-005` | **Ba điều kiện ban hành:** *Số QĐGCTKH* · *Ngày chứng từ* · tệp **bản quyết định đã ký** ở *Tài liệu đính kèm*. Thiếu bất kỳ mục nào thì chặn. **Ngoài ba mục đó, ban hành không kiểm gì thêm** — không kiểm nội dung tệp đính lên, không kiểm số liệu ba bảng, không đòi quyết định phải có dòng chi tiết | `5.2`, `5.3`, `5.5`, `5.6` | @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-006` | ***Xuất phụ lục* dùng được ở mọi trạng thái**, kể cả *Mới* và khi chưa có *Số QĐGCTKH*; **lưu trước rồi mới xuất**. Nội dung tệp ở `5.3` `[15]`; người ngoài Cục QLKTNVMM xuất ra tệp **chỉ có sheet chi tiết của hệ mình** (`BR-qdgctkh-018`) | `5.2`, `5.3`, `5.7` | @quynhdtn17 chốt 21/08/2026, sửa 25/08/2026 theo `PhuLuc_QDGCTKH_Nam_Mau.xlsx` |
| `BR-qdgctkh-007` | **Vào xem và vào sửa là hai đường khác nhau.** Bấm *Số phiếu* ở danh sách → màn chỉ xem, có icon chuyển sang sửa. Bấm icon sửa trên dòng → thẳng màn sửa | `5.1`, `5.2`, `5.3` | @quynhdtn17 chốt 21/08/2026 |
| `BR-qdgctkh-009` | **Giá trong quyết định là số dự trù.** Biến động giá khi ký hợp đồng **không sửa lại** quyết định đã ban hành. SPMM chưa có trong bảng giá thì *Đơn giá* để trống và **không chặn ban hành** (`5.3` `[23]`) | `5.3` `[23]`–`[25]` | brainstorming Mục 8 · @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-010` | **Cột *Hiện trạng* bắt buộc kèm nhãn *"Hiện trạng cập nhật đến `<ngày>`"*** ở dòng đếm chân lưới. Quyết định còn *Mới*: nhãn là **mốc đồng bộ gần nhất**, số thả trôi theo từng đợt đồng bộ. Quyết định **đã ban hành**: cả số lẫn nhãn **đóng băng ở mốc ban hành** (`NFR-qdgctkh-004`) | `5.2`, `5.3` `[16]`, `5.7` | brainstorming Mục 8 · @quynhdtn17 chốt 24/08/2026 |
| `BR-qdgctkh-011` | **Chi tiết địa điểm triển khai giữ nguyên xuyên suốt các tầng gom**, không rút gọn ở bất kỳ cấp nào — *địa điểm triển khai* là một cấp đơn vị trong cây tổ chức | Bước 1, `5.3` | brainstorming Mục 5 · `BR-de-nghi-spmm-036` |
| `BR-qdgctkh-012` | **Hai nghĩa của chữ *Dự phòng* phải khác nhãn:** dự phòng 1-1 tại một điểm (lẫn trong *Số đề nghị*, giải thích ở *Ghi chú mục đích*) · **phần chưa gán điểm triển khai nào của một đơn vị** (`<Đơn vị> — Dự phòng`). Nghĩa thứ hai dùng **chung một khuôn nhãn cho mọi đơn vị**, kể cả Cục QLKTNVMM — **không đặt tên riêng** | `5.3`, `5.4` | brainstorming Mục 4 · @quynhdtn17 chốt 21/08/2026, sửa 24/08/2026 |
| `BR-qdgctkh-016` | **Quyết định đã ban hành không thu hồi, không thay thế, không xoá.** Đổi chỉ tiêu thì lập quyết định loại *Kế hoạch bổ sung* | `5.7`, `5.8` | @quynhdtn17 chốt 21/08/2026 |
| `BR-qdgctkh-018` | **Hai bảng *Phân bổ theo hệ* và *Tổng hợp kế hoạch toàn ngành* chỉ hiện với Cục QLKTNVMM**, ẩn hoàn toàn với mọi đơn vị khác — kể cả Cục cơ yếu đầu hệ. Áp cả cho tệp phụ lục: người ngoài Cục QLKTNVMM xuất ra tệp **chỉ có sheet chi tiết** | Mục 3.1, `5.7` | @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-019` | **Quyết định chỉ lấy được phiếu cùng loại và cùng năm.** Danh sách phiếu ở `5.4` lọc theo **bốn điều kiện đồng thời**: phiếu ở trạng thái *Đã tiếp nhận* · *Loại kế hoạch* trùng quyết định · *Năm áp dụng* trùng quyết định · chưa bị quyết định nào khác chiếm. Đổi *Loại kế hoạch* hoặc *Năm áp dụng* ở `5.3` thì danh sách lọc lại. **Không có đường nào lấy phiếu khác loại hay khác năm** — không phải cảnh báo rồi cho qua, mà là không hiện ra để chọn | `5.3` `[8]` `[9]` `[11]`, `5.4` | @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-020` | **Đổi một trong hai trường đầu biểu mẫu — *Loại kế hoạch*, *Năm áp dụng* — thì bỏ toàn bộ phiếu đã chọn và mọi dòng đi theo phiếu; *dòng thêm tay giữ nguyên*.** Chỉ đổi được khi quyết định còn ***Mới***. Đang có phiếu được chọn thì phải qua hộp thoại `5.11`; không có phiếu nào thì đổi thẳng, không hỏi | `5.3` `[8]` `[9]`, `5.11` | @quynhdtn17 chốt 22/08/2026, sửa 25/08/2026 |
| `BR-qdgctkh-024` | **Hai người chọn cùng một phiếu thì người *Lưu* trước được.** Cách phần mềm xử người sau ở `5.3` `[3]` | `5.3` `[3]` `[11]`, `5.4` | @quynhdtn17 chốt 22/08/2026 |
| `BR-qdgctkh-030` | **Phụ lục có hai bản: *Kế hoạch năm* (bản gốc đã ký) và *Kế hoạch hiện hành*.** Người dùng chọn ở `5.15`, radio chọn sẵn theo tab đang đứng. **Chưa có văn bản điều chỉnh nào thì không hỏi**, xuất thẳng bản gốc. Bản gốc **luôn khớp bản giấy đã ký**, không văn bản nào làm đổi được | `5.7` `[3]`, `5.12` `[7]` | @quynhdtn17 chốt 27/08/2026 |

## 8. Yêu cầu phi chức năng

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `NFR-qdgctkh-001` | **Ba bảng tính lại trong vòng 1 giây** sau khi sửa một ô *Số lượng cấp*, kể cả khi quyết định đã chọn vài chục phiếu | Chọn đủ số phiếu cho một quyết định năm thật, sửa một ô, đo thời gian tới lúc *Tổng tiền ngân sách dự trù* đổi |
| `NFR-qdgctkh-002` | **Khuôn phụ lục xuất ra sửa được** — thêm và bớt cột, đổi nhãn — mà không phải phát hành bản phần mềm mới | Đổi khuôn → tệp phụ lục xuất ra đổi theo ngay, không build lại |
| `NFR-qdgctkh-003` | **Mọi hành động đổi trạng thái ghi lại được ai làm và lúc nào** — ban hành, xoá, chọn phiếu, bỏ chọn phiếu | Ban hành một quyết định → tra ra được người bấm và thời điểm |
| `NFR-qdgctkh-004` | **Ban hành là mốc đóng băng — đóng băng HẾT, không riêng con số.** Quyết định đã ban hành giữ nguyên vĩnh viễn cả số lượng, *Đơn giá*, *Thành tiền*, cột *Hiện trạng* kèm nhãn ngày, lẫn **tên SPMM, ĐVT, tên địa điểm triển khai và dòng đó thuộc hệ nào** — đọc từ **bản chụp lúc ban hành**, KHÔNG đọc lại danh mục hiện hành. Đổi tên một SPMM, hay chuyển một đơn vị sang cha khác, **không làm đổi quyết định cũ** và **không làm dòng nhảy sang tab hệ khác**; mở lại sau nhiều năm vẫn khớp bản giấy đã ký | Ban hành một quyết định, rồi đổi tên một SPMM, đổi tên một địa điểm và chuyển một đơn vị sang hệ khác trong cây tổ chức → mở lại quyết định: **tên cũ giữ nguyên, dòng vẫn ở tab cũ, số *Hiện trạng* và nhãn ngày không đổi** |

## 9. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|:--:|---|---|
| 1 | **Mở lại quyết định còn *Mới* để chọn thêm phiếu** mà không mất phần đã làm | Mở lại một quyết định *Mới* đã chọn phiếu trước đó, tích thêm phiếu mới → dòng cũ và *Số lượng cấp* đã sửa còn nguyên |
| 2 | **Phụ lục xuất ra dùng thẳng được cho hồ sơ trình ký**, không phải chỉnh tay | Xuất phụ lục ở trạng thái *Mới* → đủ 7 sheet, số liệu khớp ba bảng trên màn, in riêng từng tờ được |
| 3 | **Không có phiếu nào lọt vào hai quyết định** | Chọn một phiếu vào quyết định A rồi lưu → mở quyết định B, phiếu đó không còn trong danh sách chọn, kể cả khi A vẫn ở trạng thái *Mới* |
| 4 | **Cấp dưới xem được phần chỉ tiêu của mình sau khi quyết định ban hành**, và không xem được phần của đơn vị khác hay số toàn ngành | Đăng nhập bằng tài khoản một đơn vị cấp dưới → thấy dòng của mình và cấp con; không thấy dòng của đơn vị ngang hàng và của hệ khác; không thấy *Phân bổ theo hệ* và *Tổng hợp kế hoạch toàn ngành* |

## 10. Chưa làm ở đợt này

- **Định mức.** `brainstorm-de-nghi-spmm.md` chốt 18/08 rằng định mức *"thuộc khâu QĐGCTKH"*, nhưng đợt này chưa làm — chưa có cột đối chiếu trong lưới chi tiết, chưa có danh mục riêng. Bổ sung sau.
- **Cột *Học viện* ở bảng *Tổng hợp kế hoạch toàn ngành*** và **loại quyết định *Dự trữ Quốc gia* riêng** — biên bản 30/07–04/08 đã chốt là có, nhưng chưa làm đợt này. Làm dần theo thứ tự triển khai các hệ.

## 📝 Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|---|---|---|---|---|
| 2026-09-04 | cập nhật | `docs/reference/PhuLuc_QDGCTKH_Nam_Mau.xlsx` · @quynhdtn17 chốt 04/09/2026 | @quynhdtn17 | Khuôn mẫu phụ lục quyết định năm đổi tên thành `PhuLuc_QDGCTKH_Nam_Mau.xlsx`; `5.3` `[11]` và `5.15` sửa theo. `5.15` chốt khối đầu trang bản *Kế hoạch hiện hành* **chỉ có một dòng mốc thời gian** — thời điểm bấm xuất; khuôn mẫu `PhuLuc_QDGCTKH_HienHanh_Mau.xlsx` chưa giao kèm gói này **Bảng *Phân bổ theo hệ* bỏ hẳn dấu `–`** — hệ không có số thì để trống ô, sửa cả trên Figma (185 ô). |
| 2026-09-03 | cập nhật | `docs/cuc-ql/srs/srs-qdgctkh-bo-sung.md` · 3 frame Figma khu vực 3 file BCY(2) · @quynhdtn17 chốt 02–03/09/2026 | @quynhdtn17 | **Thêm ba tab xem kết quả sau điều chỉnh — `5.12`–`5.14`**, Mục 5 từ 11 lên **14 mục**. Mục 1 thêm **1.4 Số gốc và số hiện hành** (cộng dồn khi xem, không lưu; nguồn delta là quyết định bổ sung và QĐTK đã ban hành). Mục 4 nói rõ **đóng băng là đóng băng bản ghi quyết định, không phải đóng băng con số đang có hiệu lực**. `5.7` thêm dải ba tab, *Thông tin chung* nằm ngoài tab, chưa có văn bản điều chỉnh thì dải tab không hiện. Thêm `FR-qdgctkh-007` và `BR-qdgctkh-026`–`031`: **tab hiện hành có *Thành tiền* nhưng không có *Đơn giá*** (đơn giá không cộng được giữa các văn bản), **phụ lục luôn xuất theo bản gốc**, **cột *Phạm vi* ở tab lịch sử điền cho mọi dòng**. Mục 10 thêm câu hỏi mở về việc QĐTK có đẩy chênh lệch vào số hiện hành không. Loại *Kế hoạch bổ sung* **tách sang `srs-qdgctkh-bo-sung.md`** thay cho dòng "làm giai đoạn sau"; `5.1` `[7]`, `5.3` `[5]` `[8]` và câu phạm vi Mục 5 sửa theo. **Chốt hết câu hỏi mở, xoá Mục 10** — còn 10 mục. Soát câu chữ toàn file: cắt câu giải thích lý do và mô tả hình thức. **Đổi tên tệp thành `srs-qdgctkh-nam.md`** cho khỏi lẫn với bản bổ sung (slug feature giữ nguyên `qdgctkh`). Mục 1.4 viết lại lý do tab hiện hành ẩn cột *Đơn giá*; bỏ định dạng của *Số QĐGCTKH*; Mục 2 gọi *Cục QLKTNVMM* thay cho *Phòng Kế hoạch*; Mục 3.1 thêm câu hệ chỉ xem, không sửa không xoá. **Thêm `5.15` — hộp thoại chọn bản xuất phụ lục**, Mục 5 lên 15 mục: nút *Xuất phụ lục* mở hai radio *Kế hoạch năm* / *Kế hoạch hiện hành*, chọn sẵn theo tab đang đứng, chưa có văn bản điều chỉnh thì xuất thẳng bản gốc không hỏi; `BR-030` viết lại theo đó. **Vẽ Figma bốn hộp thoại `QĐGCTKH 12`–`15`** — Mục 5 hết chỗ "chưa vẽ". Chuẩn hoá câu hệ quả của mọi hộp thoại về đúng khuôn `design.md` Mục 9.4 (một câu, không liệt kê nhiều hệ quả, không đếm số dòng) và cho nút chính mang đúng chữ của tiêu đề. **Xoá một dòng chi tiết lẻ không hỏi nữa** — `5.9` đổi thành hộp thoại xoá cả nhóm SPMM, chỉ mở khi bấm icon xoá ở dòng nhóm. **Mục 7 từ 31 quy tắc còn 16** — bỏ những quy tắc chỉ chép lại luật đã có nguyên vẹn ở bảng mô tả màn (`BR-008`, `BR-013`–`BR-015`, `BR-017`, `BR-021`–`BR-023`, `BR-025`–`BR-029`, `BR-031`), gộp `BR-003` vào `BR-002` |
| 2026-08-26 | cập nhật | `docs/ngoai-giao/srs/srs-de-nghi-spmm.md` `BR-de-nghi-spmm-026` · @quynhdtn17 chốt 26/08/2026 | @quynhdtn17 | **Chốt định dạng *Số phiếu*** — `QĐGCTKH/<mã đơn vị>/<năm>/<4 số>`, mã đơn vị lấy từ danh mục thay cho hằng số `QLKT`; mỗi loại quyết định một dải đếm riêng, bổ sung mang tiền tố `QĐGCTKH-BS`. **Thống nhất tên loại kế hoạch — *Bổ sung – đột xuất* đổi thành *Kế hoạch bổ sung*** ở cả 3 chỗ (Mục 1.2, Mục 4, `BR-qdgctkh-016`), cho khớp phiếu đề nghị SPMM — `BR-qdgctkh-019` lọc phiếu bằng so khớp đúng chữ nên lệch một chữ là bảng chọn phiếu rỗng |
| 2026-08-26 | cập nhật | @quynhdtn17 chốt 26/08/2026 | @quynhdtn17 | **Cắt gọn `5.4` `[7]` *Ngày chứng từ*** — chỉ giữ luật bắt buộc khi *Ban hành* và câu lỗi; bỏ phần mô tả giá trị hiển thị (*không mặc định ngày hôm nay*, *chữ mờ khi còn Mới*, *không gọi là Ngày lập*). Trên Figma: **ẩn trường *Phương thức tạo* ở cả 7 màn** có trường đó, và **thêm icon ⓘ vào nhãn *Ngày chứng từ*** cho đồng bộ với *Số QĐGCTKH* — hai trường cùng một luật |
| 2026-08-25 | cập nhật | `docs/reference/PhuLuc_QDGCTKH_Nam_Mau.xlsx` (bản người dùng sửa 25/08/2026) · @quynhdtn17 chốt 25/08/2026 | @quynhdtn17 | **Phụ lục từ 3 sheet lên 7 sheet** — *Tổng hợp toàn ngành* · *Phân bổ theo hệ* · **5 sheet chi tiết, mỗi hệ một sheet**; mọi sheet lặp khối đầu trang, trong phụ lục Mã và Tên của SPMM và của địa điểm tách thành hai cột, sheet chi tiết không có đơn giá và thành tiền. Sửa `5.3` `[15]`, `5.7` `[3]`, `BR-006`, tiêu chí 2, và trỏ tới tệp khuôn mẫu. **Bỏ trường *Phương thức tạo* khỏi màn đợt này** — *Tạo thủ công* chuyển sang Mục 1.2 làm giai đoạn sau; `5.3` `[10]` `[11]`, `5.11`, `BR-020`, `BR-021` sửa theo, ô *Phiếu đề nghị SPMM* luôn hiện và luôn bắt buộc. Trên Figma: ẩn trường *Phương thức tạo*, giãn ô *Phiếu đề nghị SPMM* kín hàng, ô *Ngày chứng từ* bỏ giá trị mẫu về chữ mờ *"Nhập khi ban hành"* cho khớp `5.3` `[7]` |
| 2026-08-24 | cập nhật | `docs/ngoai-giao/srs/srs-de-nghi-spmm.md` `BR-de-nghi-spmm-012` · @quynhdtn17 chốt 24/08/2026 | @quynhdtn17 | **Đồng bộ nghĩa chữ *Dự phòng* với phiếu đề nghị SPMM.** `BR-012` **bỏ chữ *"đệm toàn ngành"*** — ba tầng nghĩa rút còn **hai**, vì phần chưa gán điểm triển khai của một hệ và của Cục QLKTNVMM là **cùng một cơ chế, chỉ khác ai lập phiếu**; nghĩa thứ hai định nghĩa lại là *"phần chưa gán điểm triển khai nào của một đơn vị"*. `FR-003` ghi rõ hai mục `— Triển khai` / `— Dự phòng` là của **đơn vị lập**, **không giới hạn ở Cơ yếu đầu hệ** — cờ ở Quản lý đơn vị quyết định, cơ chế không đổi. **Không đụng `5.3` `[16]`**: lưới chi tiết dùng chung, luật *"điểm `— Dự phòng` để TRỐNG ở cột Hiện trạng"* viết một lần ở `srs-de-nghi-spmm.md` theo đúng `BR-qdgctkh-023`. `5.3` `[19]` *Phân bổ theo hệ* **giữ nguyên** — việc có tách cột Triển khai/Dự phòng cho cả 4 hệ hay không vẫn chờ Cục QLKTNVMM |
| 2026-08-22 | cập nhật | @quynhdtn17 chốt 22/08/2026 · `docs/design.md` Mục 9.4 · `docs/meetings/2026-07-30-2026-08-04-thong-nhat-quy-trinh-qlspmm.md` | @quynhdtn17 | **Bít 7 lỗ hổng logic tìm ra khi soát lại tài liệu.** (1) **Chiếm phiếu chuyển sang lần *Lưu*** — tích ô ở `5.4` chưa chiếm gì; hai người chọn cùng phiếu thì ai lưu trước được, người sau nhận thông báo nổi và phần mềm tự bỏ tích phiếu bị chiếm — `BR-024`, sửa `BR-002`, `5.3` `[3]`, `5.4` `[9]` và điều kiện lọc 4. (2) ***Ban hành* không kiểm gì ngoài ba mục giấy tờ** — ghi rõ để QC không kỳ vọng có chặn, kể cả với quyết định không có dòng chi tiết; sửa `BR-005`. (3) ***Số lượng cấp* bắt buộc khi *Lưu***, nhận số nguyên từ `0`, `0` nghĩa là *không cấp* và phần mềm không tự xoá dòng; dòng thêm tay cũng được gợi ý từ *Số đề nghị* — sửa `5.3` `[17]`. Thêm vế chặn số âm cho *Đơn giá* `[23]`. (4) **Đổi ba trường đầu biểu mẫu chỉ bỏ dòng đi theo phiếu, *dòng thêm tay giữ nguyên*** — sửa `BR-020`, `5.11`; hộp thoại chỉ hiện khi đang có phiếu được chọn. (5) **Xoá dòng cuối của một phiếu thì phiếu tự bỏ chọn**, cơ chế là đếm dòng còn lại chứ không đối chiếu nội dung — `BR-025`, sửa `5.3` `[18]`, `5.9`. (6) **Đơn vị tính là thuộc tính của SPMM trong danh mục**, bảng giá lấy cùng nguồn nên *Đơn giá* luôn cùng đơn vị với *Tổng SL* — thêm vào Mục 1. (7) **Bước 1 Mục 2 viết lại theo dạng đệ quy** `cấp N → cấp trên trực tiếp N+1`, Cục đầu hệ tổng hợp thành phiếu toàn hệ. Kèm theo: **bốn hộp thoại `5.8`–`5.11` viết lại theo khuôn `design.md` Mục 9.4** (tiêu đề · dòng nhận diện · câu hệ quả · nút chính mang chữ tiêu đề); `FR-006` viết theo kết quả và phủ cả ba lớp phân quyền thay vì chỉ Mục 3.1; **đồng bộ ghi rõ là hai chiều, không tức thời**; `BR-010` sửa tham chiếu `[28]` → `[16]`; xếp lại `BR-018` `BR-019` về đúng số; xoá hàng tiêu đề lặp ở Mục 10; ghi nhận **cột *Học viện*** và **loại *Dự trữ Quốc gia*** chưa làm đợt này ở Mục 11 |
| 2026-08-22 | cập nhật | @quynhdtn17 chốt 22/08/2026 | @quynhdtn17 | **Chốt 6 câu hỏi mở, Mục 10 từ 7 câu còn 2.** (1) *Tạo thủ công* → ô *Phiếu đề nghị SPMM* **ẩn hẳn**; ba trường *Loại kế hoạch* · *Năm áp dụng* · *Phương thức tạo* **chỉ đổi được khi còn *Mới***, đổi thì bỏ hết phiếu đã chọn và dòng chi tiết, qua hộp thoại mới `5.11` — `BR-020`, `BR-021`. (2) **Định mức chưa làm đợt này**, chuyển xuống Mục 11 mới thay vì đưa vào phạm vi. (3) **Lưới chi tiết dùng lại nguyên lưới phiếu đề nghị** với **ba cách xem** (chốt có *Trải phẳng*) — gộp 11 dòng mô tả `[18]`–`[28]` thành **một dòng tham chiếu** `[16]`, chỉ giữ riêng cột *Số lượng cấp*; `5.3` từ 35 xuống **25 dòng** — `BR-023`. (5) **SPMM chưa có trong Bảng giá thì *Đơn giá* để trống**, không điền `0`; *Thành tiền* trống theo và không cộng vào tổng — sửa `BR-009`. (6) **Xoá được cả dòng đến từ phiếu**, qua hộp thoại mới `5.9`; xoá dòng không tách phiếu khỏi quyết định — `BR-022`. Thêm hộp thoại `5.10` cho việc bỏ chọn phiếu (trước đó chỉ ghi "hỏi lại" mà không đặc tả). **Mục 5 từ 9 lên 12 mục**, ba mục cuối chưa vẽ Figma |
| 2026-08-22 | cập nhật | @quynhdtn17 chốt 22/08/2026 · `docs/ngoai-giao/srs/srs-de-nghi-spmm.md` (phiếu có *Loại kế hoạch* và *Năm áp dụng*) | @quynhdtn17 | **Thêm luật lọc danh sách phiếu — `BR-qdgctkh-019`.** Bảng chọn `5.4` lọc theo **bốn điều kiện đồng thời**: phiếu *Đã tiếp nhận* · *Loại kế hoạch* trùng quyết định · *Năm áp dụng* trùng quyết định · chưa thuộc quyết định nào khác. Phiếu đã thuộc quyết định khác **không lên dù quyết định đó còn *Mới*** (hệ quả của `BR-002`, ghi rõ ra). Đổi *Loại kế hoạch* / *Năm áp dụng* ở `5.3` thì danh sách lọc lại; chưa điền hai ô đó thì chưa mở được bảng chọn. Gỡ câu hỏi mở 🟡 về chặn phiếu khác năm — đã có lời giải; gộp hai câu hỏi về *đổi Loại* và *đổi Năm* thành một. **Đổi thuật ngữ toàn tài liệu: "gom / gỡ phiếu" → "chọn / bỏ chọn phiếu"** cho khớp thao tác thật là tích ô chọn. Viết lại tiêu chí thành công 1 và 3 |
| 2026-08-22 | cập nhật | @quynhdtn17 góp ý 22/08/2026 | @quynhdtn17 | Viết lại ba bước của Mục 2. Bước 3 **bỏ vế *"Lặp lại nhiều lần"*** — thao tác thật chỉ là tích chọn phiếu. Bước 4 nói rõ **đầu vào là các phiếu đã chọn** và phần mềm tự đổ dòng vào đúng tab của từng hệ trước khi tính hai bảng trên. Bước 5 nêu rõ *Số lượng cấp* là **số cấp thực tế**, còn ***Đơn giá* không bắt buộc** — ghi thêm vào `5.3` `[33]` |
| 2026-08-22 | cập nhật | Sửa trực tiếp trên frame Figma `320:18394` file BCY(2) | @quynhdtn17 | **Sửa ba chỗ trên bản vẽ rồi đồng bộ tài liệu.** (1) Ô lọc SPMM `Tất cả (5 loại)` → `Tất cả (4 loại)` cho khớp dòng đếm chân lưới. (2) Ô *Ngày chứng từ* bỏ giá trị `20/08/2026`, thành chữ mờ *"Nhập khi ban hành"* — **chốt không mặc định ngày hôm nay**, gỡ câu hỏi mở 🟡 tương ứng và sửa `5.3` `[7]`. (3) Nhãn ***"Hiện trạng cập nhật đến `<ngày>`"*** ghép vào **dòng đếm chân lưới** thay vì để trống như trước; sửa `5.3` `[22]` `[28]` và `BR-010` theo. Kiểm lại bố cục sau khi sửa: không có ô nào tràn, cắt chữ hay chồng nhau |
| 2026-08-22 | cập nhật | Đối soát trực tiếp frame Figma `320:18394` file BCY(2) | @quynhdtn17 | **Sửa Mục 5 cho khớp bản vẽ.** (1) **Bỏ hẳn bảng *Phiếu đề nghị đã gom*** ở `5.3` — bản vẽ không có bảng này; 7 dòng `[14]`–`[20]` gỡ đi, `5.3` còn **35 dòng**. (2) `5.4` viết lại theo cơ chế thật: bảng chọn hiện **cả phiếu đã gom vào quyết định đang mở (tích sẵn) lẫn phiếu còn tự do** — tích là gom, **bỏ tích là gỡ**; phiếu đã gom vào quyết định *khác* mới không lên. Sửa `BR-003` theo. (3) Cột `[3]` đổi tên thành ***Số phiếu đề nghị*** cho khỏi lẫn với *Số phiếu* của quyết định. (4) Thêm **cột ĐVT** vào lưới chi tiết (`[21]`). (5) Dòng đếm chân bảng chọn bỏ vế *"K dòng chi tiết"*, sửa cả trên Figma. (6) **Không vẽ sơ đồ luồng và sơ đồ trạng thái** cho feature này — một tác nhân, không nhánh rẽ, hai trạng thái; gỡ hai dòng ⚠️ ở Mục 2 và Mục 4. Sửa tham chiếu chéo `5.2` `[3]`, `BR-013`, `5.2` `[5]`, `5.7` `[2]`, bảng phạm vi Mục 3.1 |
| 2026-08-22 | cập nhật | @quynhdtn17 chốt 22/08/2026 | @quynhdtn17 | Chốt hai điểm còn treo: (1) ***Ngày chứng từ* chỉ bắt buộc khi *Ban hành***, không bắt buộc khi *Lưu*. (2) **Hai bảng *Phân bổ theo hệ* và *Tổng hợp kế hoạch toàn ngành* chỉ hiện với Cục QLKTNVMM**, ẩn hoàn toàn với mọi đơn vị khác kể cả Cục cơ yếu đầu hệ; đơn vị ngoài Cục QLKTNVMM xem *Thông tin chung*, *Phiếu đề nghị đã gom* và *Thông tin chi tiết* đã cắt theo cây tổ chức, và xuất phụ lục ra tệp một sheet. Thêm `BR-018`, thêm bảng "khối nào hiện với ai" ở Mục 3.1, sửa `BR-006`, `5.7`, tiêu chí 4; gỡ câu hỏi mở 🔴 tương ứng |
| 2026-08-22 | cập nhật | @quynhdtn17 góp ý 22/08/2026 · `docs/cuc-ql/wireframe/qdgctkh/screen-qdgctkh-lap-quyet-dinh.md` | @quynhdtn17 | Sửa **bốn lỗi nội dung**: (1) *Mã quyết định* → ***Số phiếu*** trên toàn tài liệu, khớp bản mô tả màn và màn phiếu đề nghị. (2) Điều kiện ban hành bỏ chữ *"duy nhất"*, thành **ba mục — *Số QĐGCTKH* · *Ngày chứng từ* · tệp bản đã ký**; kéo theo `BR-005`, `5.3`, `5.3` `[4]` `[7]` `[13]`, `5.5`, `5.6`. (3) **Mục 3.1 viết lại**: quyết định *Mới* chỉ Cục QLKTNVMM thấy; đã ban hành thì mọi cấp thấy nhưng chỉ dòng của **đơn vị mình và cấp con**, không thấy cấp trên · đơn vị ngang hàng · hệ khác — thêm `BR-017`, `FR-006`, tiêu chí 4. (4) **Bảng phân quyền tách làm hai**: quyền theo vai trò (Mục 3.2) và thao tác theo trạng thái (Mục 3.3); *Tạo quyết định* ra khỏi bảng trạng thái. Bổ sung **bước 1** vào bảng quy trình (bảng cũ hỏng, mất bước 1 và bị dòng trống ngắt). Thêm 1 câu hỏi mở 🔴 về phạm vi hai bảng tổng hợp. **Soát câu chữ toàn file:** cắt mọi câu giải thích lý do, câu so sánh với phiếu đề nghị và câu kể lại nội dung đã bỏ ở bản trước; gộp *Mục 1a* thành *Mục 1.3*; sửa tham chiếu sai `5.2` `[3]` từ `[20]` sang `[24]` |
| 2026-08-22 | thêm mới | `docs/cuc-ql/brainstorming/brainstorm-qdgctkh.md` · `docs/cuc-ql/wireframe/qdgctkh/screen-qdgctkh-lap-quyet-dinh.md` · 9 frame Figma khu vực 3 file BCY(2) | @quynhdtn17 | Bản đầu tiên. Mục 5 gồm 9 màn theo bản vẽ hiện tại. Ghi các quyết định ngày 21–22/08: *Ban hành* thực hiện *Lưu* trước, *Xuất phụ lục* một nút ba sheet dùng được ở *Mới*, hai đường vào một quyết định *Mới*, bỏ *Xuất Excel* ở màn danh sách, nhãn *Dự phòng* bỏ chữ *toàn ngành*. Feature chưa có sơ đồ luồng và sơ đồ trạng thái |
| 2026-08-24 | cập nhật | Dev hỏi lại 24/08/2026 | @quynhdtn17 | **Ban hành đóng băng HẾT**, kể cả tên SPMM, ĐVT, tên địa điểm và dòng thuộc hệ nào — `NFR-004` mới, sửa Mục 4 và `BR-010`. **Bảng giá SPMM là một bảng dùng chung với Hợp đồng sản xuất**, chỉ để gợi ý và sửa được; bản đang chạy chưa có bảng này — sửa `FR-002`, Mục 1.2, thêm một câu hỏi mở |
| 2026-08-26 | cập nhật | @quynhdtn17 chốt 26/08/2026 | @quynhdtn17 | **Bỏ màn thông báo nổi khi ban hành bị chặn.** Thiếu điều kiện thì tô đỏ ngay tại trường thiếu — bấm *Ban hành* ở màn chỉ xem `5.2` nay mở thẳng màn sửa `5.3` với các mục còn thiếu đã tô đỏ. Mục 5 còn **11 màn**, các mục từ `5.4` cũ trở đi lùi một số |
