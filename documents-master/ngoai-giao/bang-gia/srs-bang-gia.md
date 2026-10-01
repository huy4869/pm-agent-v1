---
type: srs
feature: bang-gia
status: dang-review
updated: 2026-08-28
nguon:
  - docs/cuc-ql/brainstorming/brainstorm-bang-gia.md
  - docs/cuc-ql/user-flow/userflow-bang-gia.md
  - docs/cuc-ql/wireframe/bang-gia/wireframe-index-bang-gia.md
  - docs/cuc-ql/wireframe/bang-gia/screen-bang-gia-bg-lap.md
  - docs/cuc-ql/wireframe/bang-gia/screen-bang-gia-bg-ban-hanh.md
  - docs/cuc-ql/wireframe/bang-gia/screen-bang-gia-bg-tra-cuu.md
  - docs/cuc-ql/srs/srs-qdgctkh.md
  - docs/cuc-ql/srs/srs-hop-dong.md
---

# Đặc tả: Bảng giá SPMM

**Figma:** file **BCY(2)** · Page 1 · khu vực 6 — **7 màn**, đánh số `BG 01`–`BG 07`, khung 1440.

> **Luật nằm ở hai chỗ, không hơn.** Luật của một ô hay một nút nằm ngay tại ô hoặc nút đó ở **Mục 5**. Chỉ những gì **không thuộc màn nào** mới lên **Mục 6**.

## 1. Phạm vi

Bảng giá SPMM là **danh mục dùng chung** của phần mềm, không phải một bước trong chuỗi nghiệp vụ. Nó cấp **giá gợi ý** cho hai chỗ đang cần: cột *Đơn giá* của QĐGCTKH và cột *Đơn giá* của Hợp đồng.

Một bảng giá gồm *Thông tin chung* và một lưới **toàn bộ danh mục SPMM** kèm đơn giá. Cán bộ Cục QLKTNVMM đặt *Ngày bắt đầu hiệu lực*, gõ đơn giá, *Lưu* — hồ sơ ở trạng thái *Mới*. Sau khi có văn bản ban hành ký ngoài phần mềm thì nhập *Số chứng từ*, *Ngày chứng từ*, đính kèm bản chụp rồi bấm *Ban hành*. Từ đó bảng giá **khoá tuyệt đối**: không sửa, không xoá, không thu hồi, không huỷ. Đổi giá thì **nhân bản** bảng cũ, sửa, ban hành với ngày bắt đầu mới; phần mềm tự đóng ngày kết thúc của bảng liền trước.

**Giá chỉ là gợi ý.** QĐGCTKH và Hợp đồng chép giá vào hồ sơ của mình tại thời điểm lập và **sửa tay tự do**. Ban hành bảng giá mới **không sửa lại** hồ sơ đã lưu.

**Đơn vị tính** là thuộc tính của SPMM trong danh mục SPMM — một SPMM một đơn vị tính. Bảng giá chỉ **hiện lại** ở cột *ĐVT*, **không đặt lại**. Việc một *Hệ thống* được đếm như thế nào là vấn đề ở tầng danh mục SPMM, chưa chốt — xem Mục 8.

**Một loại tiền: VND.** Không có ô chọn loại tiền, không có tỉ giá. Đơn vị tiền ghi **đúng một chỗ** — tiêu đề cột *Đơn giá (VND)*.

**Bảng giá không chạm tới từng cái SPMM cụ thể.** Nó định giá theo **loại** SPMM, nên không có mã định danh 15 số và không có serial vật lý ở bất kỳ màn nào.

### 1.1 Bản triển khai

| Việc | Chạy ở bản |
|---|---|
| Lập · sửa · nhân bản · ban hành · xoá bảng giá — 7 màn `5.1`–`5.7` | **Cục QL** |
| Xem danh sách `5.1` và xem chi tiết `5.6` ở dạng **chỉ đọc** | **Cục QL** và **4 hệ đầu hệ** |

Bảng giá **đồng bộ một chiều từ Cục QL xuống 4 bản hệ đầu hệ**. Bản ở hệ **không lập, không sửa, không ban hành, không xoá** — mọi nút ghi bị ẩn. Tần suất và cơ chế đồng bộ **chưa chốt** — xem Mục 8.

### 1.2 Ngoài phạm vi

- **Soạn thảo, trình ký, ký số và phê duyệt pháp lý văn bản ban hành bảng giá** — nằm ở eOffice và quy trình riêng của Ban. Phần mềm chỉ **ghi nhận kết quả đã ký** qua *Số chứng từ*, *Ngày chứng từ* và tệp đính kèm.
- **Danh mục SPMM** — bảng giá chỉ **đọc** danh sách SPMM và *ĐVT*, không thêm sửa xoá SPMM tại đây.
- **Cách QĐGCTKH và Hợp đồng dùng giá gợi ý** — có đặc tả riêng ở `srs-qdgctkh.md` `5.4` `[23]` và `srs-hop-dong.md` `5.3` `[19]`. Tài liệu này chỉ khai **bảng nào là nguồn** và **đọc lúc nào** (`BR-bang-gia-007`).
- **Nguyên giá tài sản** trong module QLTS — chưa có ở đợt này.

### 1.3 Hai số hiệu

| Tên | Nguồn | Định dạng | Bắt buộc |
|---|---|---|---|
| ***Mã bảng giá*** | Phần mềm sinh khi *Lưu* lần đầu. Chỉ đọc, duy nhất, không đổi suốt vòng đời | `BG/<năm>/<4 số>` | Luôn có kể từ lần lưu đầu |
| ***Số chứng từ*** | Người dùng nhập tay, lấy từ văn bản ban hành đã ký | Theo số văn bản của Ban | Bắt buộc khi *Ban hành* |

***Mã bảng giá*** là khoá liên kết dữ liệu và là cột bấm để mở bảng giá. ***Số chứng từ*** không dùng làm khoá — lúc lập bảng giá thì văn bản chưa ký, chưa ký thì chưa có số.

## 2. Quy trình nghiệp vụ

| # | Ai làm | Làm gì | Ở đâu |
|:--:|---|---|---|
| 1 | Cán bộ Cục QLKTNVMM | Tạo bảng giá mới, hoặc nhân bản một bảng cũ để chép sẵn đơn giá. Phần mềm đổ **toàn bộ danh mục SPMM**. Điền *Tên bảng giá*, chọn *Ngày bắt đầu hiệu lực* (từ ngày mai trở đi), gõ đơn giá. Bấm *Lưu* — sinh *Mã bảng giá*, hồ sơ ở trạng thái *Mới* | `5.3` |
| 2 | Cán bộ Cục QLKTNVMM · người ký | **Ra văn bản ban hành bảng giá** theo quy trình riêng của Ban | **Ngoài phạm vi QLSPMM** |
| 3 | Cán bộ Cục QLKTNVMM | Nhập *Số chứng từ* và *Ngày chứng từ* lấy từ văn bản, đính kèm bản chụp, điền nốt các dòng còn trống đơn giá, bấm *Ban hành* — hồ sơ chuyển sang *Sắp áp dụng* và khoá lại | `5.3` · `5.5` |

**Điều kiện vào:** danh mục SPMM đã có dữ liệu.
**Điều kiện ra:** từ *Ngày bắt đầu hiệu lực*, bảng giá là nguồn giá gợi ý cho QĐGCTKH và Hợp đồng.

Bước 2 **không** phải điều kiện để *Lưu*. Bảng giá lưu được, sửa được nhiều lần trước khi có văn bản.

> **Không có sơ đồ luồng cho chức năng này** — ba bước, một vai trò trong phần mềm, không nhánh rẽ.

## 3. Phân quyền

Bảng giá chạy ở bản Cục QL với đủ chức năng, và ở 4 bản hệ đầu hệ ở dạng chỉ đọc. **Không cắt phạm vi dữ liệu theo đơn vị** — ai xem được thì xem được mọi bảng giá.

### 3.1 Quyền theo vai trò

Quyền gán cho tài khoản ở chức năng **Quản trị người dùng**, cùng cơ chế với QĐGCTKH (`srs-qdgctkh.md` Mục 3.2).

| Quyền | Cho phép | Có ở bản |
|---|---|---|
| **Xem bảng giá** | Mở `5.1`, mở `5.2` / `5.6`, mở và tải tệp đính kèm | Cục QL · 4 hệ |
| **Lập bảng giá** | Tạo mới, nhân bản, sửa bảng còn *Mới*, đính kèm tài liệu | Cục QL |
| **Ban hành bảng giá** | Bấm *Ban hành* | Cục QL |
| **Xoá bảng giá** | Xoá bảng còn *Mới* | Cục QL |

Phòng nào trong Cục QLKTNVMM giữ ba quyền *Lập* · *Ban hành* · *Xoá* thì **chưa chốt** — xem Mục 8.

### 3.2 Thao tác theo trạng thái

Một thao tác chạy được khi **tài khoản có quyền ở Mục 3.1** *và* **trạng thái bảng giá cho phép**. Thiếu một trong hai thì nút không hiện.

| Thao tác trên một bảng giá | *Mới* | *Sắp áp dụng* | *Hiệu lực* | *Hết hiệu lực* |
|---|:--:|:--:|:--:|:--:|
| Xem chi tiết | ✔ | ✔ | ✔ | ✔ |
| Sửa *Thông tin chung* | ✔ | ✘ | ✘ | ✘ |
| Sửa *Đơn giá* | ✔ | ✘ | ✘ | ✘ |
| Thêm và bớt *Tài liệu đính kèm* | ✔ | ✘ | ✘ | ✘ |
| Mở xem và tải tệp đính kèm | ✔ | ✔ | ✔ | ✔ |
| Nhân bản | ✔ | ✔ | ✔ | ✔ |
| Ban hành | ✔ | ✘ | ✘ | ✘ |
| Xoá | ✔ | ✘ | ✘ | ✘ |
| Là nguồn giá gợi ý cho QĐGCTKH và Hợp đồng | ✘ | ✘ | ✔ | ✘ |

`✔` được làm · `✘` phần mềm chặn

*Tạo bảng giá* và *Xem danh sách* không phụ thuộc trạng thái, chỉ cần quyền ở Mục 3.1.

## 4. Vòng đời trạng thái

### 4.1 Bốn trạng thái

Phần mềm **lưu ba thứ**: bảng giá ***đã ban hành hay chưa***, ***Ngày bắt đầu hiệu lực***, ***Ngày kết thúc hiệu lực*** (có thể còn trống).

**Trạng thái không lưu trong dữ liệu.** Mỗi lần mở màn, phần mềm đối chiếu ba thứ trên với **ngày hôm nay** rồi suy ra. Không có tác vụ chạy nền nào bật tắt trạng thái.

| Trạng thái | Điều kiện |
|---|---|
| ***Mới*** | Chưa ban hành |
| ***Sắp áp dụng*** | Đã ban hành **và** `Hôm nay < Ngày bắt đầu hiệu lực` |
| ***Hiệu lực*** | Đã ban hành **và** `Hôm nay ≥ Ngày bắt đầu hiệu lực` **và** *(Ngày kết thúc hiệu lực còn trống* **hoặc** `Hôm nay ≤ Ngày kết thúc hiệu lực`*)* |
| ***Hết hiệu lực*** | Đã ban hành **và** `Hôm nay > Ngày kết thúc hiệu lực` |

**Mốc giờ:** *Ngày bắt đầu hiệu lực* tính từ **00:00:00** của ngày đó; *Ngày kết thúc hiệu lực* kéo tới hết **23:59:59** của ngày đó. Bảng kết thúc 31/12/2026 vẫn cấp giá cho cả ngày 31/12/2026, bảng sau bắt đầu từ 01/01/2027.

**Ngày kết thúc còn trống = vô thời hạn.** Bảng đó ở *Hiệu lực* cho tới khi có bảng sau được ban hành và cắt ngày; khi ô này còn trống thì nó **không bao giờ vào *Hết hiệu lực***.

**Tại một thời điểm chỉ một bảng giá ở *Hiệu lực***. Đây là hệ quả của việc các khoảng ngày không chồng nhau, không phải một luật riêng cần kiểm.

### 4.2 Chuyển trạng thái

| Từ | Đến | Do đâu | Hệ quả |
|---|---|---|---|
| *(chưa có)* | ***Mới*** | Bấm *Lưu* lần đầu ở `5.3` | Phần mềm sinh ***Mã bảng giá***, không đổi về sau |
| ***Mới*** | ***Sắp áp dụng*** | Bấm *Ban hành* ở `5.2` / `5.3`, xác nhận ở `5.5` | **Khoá toàn bộ hồ sơ.** Đóng ngày kết thúc của bảng liền trước. Chụp lại mã · tên SPMM · ĐVT của mọi dòng. Ghi lại người bấm và thời điểm |
| ***Sắp áp dụng*** | ***Hiệu lực*** | **Không ai bấm** — tới ngày bắt đầu hiệu lực | Bảng liền trước rời khỏi *Hiệu lực* cùng lúc |
| ***Hiệu lực*** | ***Hết hiệu lực*** | **Không ai bấm** — qua ngày kết thúc hiệu lực | — |
| ***Mới*** | *(xoá hẳn)* | Icon xoá ở `5.1`, xác nhận ở `5.7` | Xoá bản ghi. Không đụng tới bảng giá nào khác |

> **Điều kiện để bấm được từng nút ghi ngay tại nút đó** — *Lưu* và *Ban hành* ở `5.3` `[14]` `[15]`, *Xoá* ở `5.1` `[13]`.

***Ban hành* luôn vào *Sắp áp dụng***, không bao giờ vào thẳng *Hiệu lực* — vì ngày bắt đầu hiệu lực luôn lớn hơn ngày hôm nay.

**Chuyển trạng thái bị CẤM:** đã ban hành thì **không quay lại *Mới***, **không thu hồi, không huỷ, không sửa, không xoá** — kể cả bảng *Hết hiệu lực*, vì nó là căn cứ giá của quãng thời gian đã qua. Ban hành nhầm thì ban hành một bảng đúng với ngày bắt đầu sau đó.

## 5. Màn hình

**7 mục.** `5.1`–`5.7` chạy ở **bản Cục QL**; `5.1` và `5.6` còn dùng lại ở 4 bản hệ đầu hệ ở dạng chỉ đọc.

Hai hộp thoại `5.5` `5.7` theo khuôn hộp thoại xác nhận dùng chung ở `docs/design.md` Mục 9.4.

### 5.1 Danh sách bảng giá

**Figma:** [BG 01 · Danh sách bảng giá](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-9778) · **Bước:** điểm vào · **Slug:** `danh-sach-bang-gia`

> Hàng lọc nằm trong lưới ngay dưới tiêu đề cột, áp dụng ngay khi nhập. Không có thẻ lọc riêng, không có nút *Tìm* / *Xoá lọc*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Ô chọn cột hiển thị | Multiselect | Danh sách cột | Bật tắt cột nào hiện trên lưới. Mặc định hiện đủ 9 cột. Chỉ đổi cách xem, không đổi dữ liệu |
| 2 | Tạo bảng giá | Button | — | Mở `5.3` với bảng chi tiết đã đổ **toàn bộ danh mục SPMM**, mọi ô đơn giá trống. Chỉ hiện với tài khoản có quyền *Lập bảng giá* |
| — | Bảng danh sách | Table | — | Chín cột: STT · **Mã bảng giá** · Trạng thái · Tên bảng giá · Bắt đầu hiệu lực · Kết thúc hiệu lực · Số chứng từ · SPMM có giá · Thao tác. Mặc định sắp theo *Bắt đầu hiệu lực* giảm dần. Không có nút *Xuất Excel* |
| 3 | Hàng lọc từng cột | Input · Dropdown | Theo cột | Lọc theo Mã bảng giá, Trạng thái, Tên bảng giá, hai ngày hiệu lực, Số chứng từ. Lọc không ra dòng nào thì bảng rỗng, không chuyển màn |
| 4 | Mã bảng giá | Link | Chuỗi | Phần mềm sinh khi *Lưu* lần đầu, dạng `BG/<năm>/<4 số>`, không đổi suốt vòng đời. Cột bấm để mở: dòng *Mới* mở `5.2`, dòng đã ban hành mở `5.6`. **Bấm mã là vào xem, bấm icon sửa `[11]` mới vào sửa** — cùng khuôn `BR-qdgctkh-007` |
| 5 | Trạng thái | Tag | Danh mục | Bốn giá trị: *Mới* · *Sắp áp dụng* · *Hiệu lực* · *Hết hiệu lực*, tính ra khi mở màn theo Mục 4.1 |
| 6 | Tên bảng giá | Text | Chuỗi | Tên do người lập đặt |
| 7 | Bắt đầu hiệu lực | Text | Ngày | Ngày đầu tiên bảng giá có hiệu lực. Luôn có giá trị kể từ lần lưu đầu |
| 8 | Kết thúc hiệu lực | Text | Ngày | Ngày **cuối cùng** còn hiệu lực. **Để trống** khi chưa có bảng sau — trống nghĩa là còn hiệu lực tới khi có bảng kế; không hiện dấu gạch, không hiện chữ *"không thời hạn"* |
| 9 | Số chứng từ | Text | Chuỗi | Số văn bản ban hành. **Để trống khi còn *Mới*** |
| 10 | SPMM có giá | Text | Chuỗi | Dạng `<số dòng đã có đơn giá> / <tổng số dòng>`, vd `126 / 132`. Bảng đã ban hành luôn ở dạng `n / n` |
| 11 | Sửa | Icon button | — | Chỉ hiện ở dòng *Mới* và với tài khoản có quyền *Lập*. Mở **thẳng `5.3`**, không qua màn chỉ xem |
| 12 | Nhân bản | Icon button | — | Hiện ở **mọi dòng, mọi trạng thái**. Mở `5.3` với bản sao ở trạng thái *Mới* — chép gì và không chép gì xem `BR-bang-gia-006`. Đây là **chỗ duy nhất** gọi được nhân bản |
| 13 | Xoá | Icon button | — | Chỉ hiện ở dòng còn ***Mới*** và với tài khoản có quyền *Xoá*. Mở `5.7` để xác nhận. Bảng đã ban hành không có nút này |
| 14 | Phân trang | Paginator | — | Mặc định 10 dòng một trang. Dòng chú thích ghi *"Hiển thị `<a>` – `<b>` / `<N>` bảng giá"* |

Ở **bản hệ đầu hệ**: ẩn `[2]` `[11]` `[12]` `[13]`, cột *Thao tác* không còn nút nào.

### 5.2 Bảng giá *Mới* — chỉ xem

**Figma:** [BG 02 · Bảng giá Mới — chỉ xem](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-14892) · **Bước:** 1 · 3 · **Slug:** `bg-chi-tiet`

> Cùng bộ trường với `5.3`, mọi ô ở dạng chỉ đọc. Bấm *Mã bảng giá* ở `5.1` vào đây.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Mới*, đứng ngay sau tiêu đề màn |
| 2 | Chuyển sang sửa | Icon button | — | Mở `5.3` với đúng bảng giá đang xem. Chỉ hiện ở trạng thái *Mới* và với tài khoản có quyền *Lập* |
| 3 | Toàn bộ trường của *Thông tin chung* | Text (chỉ đọc) | — | Cùng bộ trường và cùng thứ tự với `5.3`. Không sửa được tại chỗ |
| 4 | Bảng *Chi tiết đơn giá* | Text (chỉ đọc) | — | Cùng bốn cột với `5.3`. Dòng chưa có đơn giá vẫn nằm ở đầu lưới. **Vẫn có ô tìm SPMM** như `5.3` `[16]` và chạy y hệt — tìm chỉ đổi cách xem nên màn chỉ đọc dùng được |
| 5 | Ban hành | Button | — | Kiểm **đúng bộ điều kiện của nút *Ban hành* ở `5.3` `[15]`**. Đủ thì mở `5.5`. **Thiếu bất kỳ mục nào thì phần mềm mở thẳng `5.3` với các mục còn thiếu đã tô đỏ** — xem `5.4`. Màn này không sửa được tại chỗ nên không báo lỗi tại đây, và **không có thông báo nổi nào** |
| — | *Huỷ* · *Lưu* · *Xoá* | — | — | **Không có**. Xoá gọi từ icon trên dòng ở `5.1` |

### 5.3 Tạo / sửa bảng giá

**Figma:** [BG 03 · Tạo / sửa bảng giá](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-10266) · **Bước:** 1 · 3 · **Slug:** `bg-nhap`

> **Hai khối gập** xếp dọc trên một màn, gọi thẳng bằng tên: *Thông tin chung* · *Chi tiết đơn giá*.
>
> Khối *Chi tiết đơn giá* là **bảng đóng theo danh mục SPMM**: phần mềm đổ đủ, không thêm được dòng, không xoá được dòng — nên **không có nút *Thêm dòng*, không có hộp thoại chọn SPMM, không có cột *Thao tác***.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Mã bảng giá | Text (chỉ đọc) | Chuỗi | Phần mềm sinh khi *Lưu* lần đầu, dạng `BG/<năm>/<4 số>`. Trước lần lưu đầu để trống. Không sửa được, không đổi suốt vòng đời |
| 2 | Số chứng từ | Input | Chuỗi | Mang dấu `*`. **Bắt buộc khi *Ban hành*, không bắt buộc khi *Lưu***. Lấy từ văn bản đã ký, phần mềm không sinh. Chữ mờ trong ô: *"Nhập khi ban hành"*. Trống lúc bấm *Ban hành* → tô đỏ ô, câu lỗi *"Chưa có Số chứng từ."* dưới ô. **Chặn** |
| 3 | Ngày chứng từ | Date | Ngày | Mang dấu `*`. **Bắt buộc khi *Ban hành*, không bắt buộc khi *Lưu***; trống lúc bấm *Ban hành* → *"Chưa có Ngày chứng từ."* dưới ô, **chặn**. Ngày ghi trên văn bản đã ký — **chọn được ngày quá khứ**, nhưng phải **nhỏ hơn hoặc bằng *Ngày bắt đầu hiệu lực***; lớn hơn thì tô đỏ, *"Ngày chứng từ phải trước hoặc bằng Ngày bắt đầu hiệu lực."*, chặn **ngay từ khi *Lưu***. **Không mặc định ngày hôm nay** |
| 4 | Tên bảng giá | Input | Chuỗi | Mang dấu `*`. **Bắt buộc khi *Lưu***. Trống → tô đỏ, *"Chưa có Tên bảng giá."* dưới ô. **Chặn** |
| 5 | Ngày bắt đầu hiệu lực | Date | Ngày | Mang dấu `*`. **Bắt buộc khi *Lưu***; trống → tô đỏ, *"Chưa có Ngày bắt đầu hiệu lực."*, chặn. Ô chọn ngày **chỉ mở từ ngày mai trở đi** — ngày hôm nay và mọi ngày quá khứ **không chọn được**, nên không có câu lỗi cho ca này. Hồ sơ có thể nằm chờ qua ngày nên giá trị này được **kiểm lại lúc bấm *Ban hành*** — xem `[15]` |
| 6 | Ngày kết thúc hiệu lực | Date (chỉ đọc) | Ngày | **Người dùng không nhập bao giờ**, không mang dấu `*`. Để trống cho tới khi có bảng sau; ban hành bảng sau thì phần mềm điền = ngày bắt đầu bản mới **trừ một ngày**. Là ngày **cuối cùng** còn hiệu lực |
| 7 | Ghi chú | Textarea | Chuỗi | Không bắt buộc. Chiếm trọn một hàng |
| 8 | Tài liệu đính kèm | Button + badge | Tệp | Mở hộp thoại quản lý tệp. Badge đếm số tệp đang có. **Bắt buộc khi *Ban hành*** — chưa có tệp nào thì câu lỗi *"Chưa đính kèm văn bản ban hành."* hiện đỏ **cạnh nút, cùng hàng**, **chặn**. Ban hành **không kiểm nội dung tệp** |
| 9 | STT | Text | Số | Phần mềm đánh theo thứ tự đang bày |
| 10 | SPMM | Text | Chuỗi | Một cột `Mã - Tên`. **Đóng theo danh mục SPMM** — phần mềm đổ đủ toàn bộ danh mục, không thêm được dòng, không xoá được dòng |
| 11 | ĐVT | Text (chỉ đọc) | Danh mục | Đơn vị tính **đi theo SPMM trong danh mục**, bảng giá chỉ hiện lại chứ không đặt lại |
| 12 | Đơn giá (VND) | Input trong ô bảng | Số tiền | Tiêu đề cột mang dấu `*`. **Bắt buộc ở MỌI dòng khi *Ban hành***; lúc *Lưu* thì để trống được. **Nhận `0`** — `0` là giá đúng bằng không, khác hẳn ô trống là chưa nhập. **Số âm thì chặn ngay khi *Lưu***, câu lỗi *"Đơn giá không được âm."* dưới ô |
| — | Thứ tự dòng trên lưới | — | — | **Dòng chưa có đơn giá xếp lên đầu**, phần còn lại theo mã SPMM. Tính lại mỗi lần mở màn. **Không có dòng đếm hay câu cảnh báo nào lúc *Lưu*** |
| 13 | Huỷ | Button | — | Rời màn, bỏ thay đổi chưa lưu. Còn thay đổi chưa lưu thì hỏi lại trước khi rời |
| 14 | Lưu | Button | — | **Kiểm bốn điều:** *Tên bảng giá* `[4]` có giá trị · *Ngày bắt đầu hiệu lực* `[5]` có giá trị · *Ngày chứng từ* `[3]` không lớn hơn *Ngày bắt đầu hiệu lực* nếu cả hai đã điền · không dòng nào có *Đơn giá* âm `[12]`. Sai thì **tô đỏ tại ô**, con trỏ nhảy về ô sai đầu tiên, **chặn**. **Không kiểm dòng trống đơn giá.** Qua được thì lần lưu đầu sinh *Mã bảng giá* và đưa hồ sơ vào *Mới*; lưu lại nhiều lần vẫn **giữ nguyên *Mới*** |
| 15 | Ban hành | Button | — | **Lưu phần đang sửa trước** — lưu không qua bốn điều ở `[14]` thì dừng, không kiểm tiếp. Rồi **kiểm sáu điều**: *Số chứng từ* `[2]` có giá trị · *Ngày chứng từ* `[3]` có giá trị · có ít nhất một tệp đính kèm `[8]` · **mọi dòng có *Đơn giá*** `[12]` · *Ngày bắt đầu hiệu lực* `[5]` **vẫn lớn hơn ngày hôm nay** tại thời điểm bấm, sai thì *"Ngày bắt đầu hiệu lực phải sau ngày hôm nay."* · *Ngày bắt đầu hiệu lực* **lớn hơn ngày bắt đầu của bảng đã ban hành gần nhất trên trục**, sai thì *"Ngày bắt đầu phải sau ngày bắt đầu của bảng giá `<mã>` (`<ngày>`)."* — **chưa có bảng nào đã ban hành thì bỏ qua điều cuối**. Đủ sáu thì mở `5.5`; thiếu thì **ở lại màn này**, tô đỏ mọi chỗ thiếu cùng lúc — xem `5.4` |
| 16 | Ô tìm SPMM | Input | Chuỗi | **Một ô nhập nằm trong lưới *Chi tiết đơn giá*, thuộc cột *SPMM*** — ba cột còn lại không có ô nào. Chữ mờ trong ô: *"Tìm mã hoặc tên SPMM"*. **Thu hẹp lưới ngay khi gõ**, khớp một phần cả **mã** lẫn **tên**, không phân biệt hoa thường; không có nút *Tìm*, xoá hết chữ thì lưới hiện lại đủ dòng. **Chỉ đổi cách xem, không đổi dữ liệu** — đơn giá đã gõ ở dòng đang bị ẩn **giữ nguyên và vẫn được *Lưu***, thứ tự dòng không tính lại. Không khớp dòng nào thì lưới rỗng, không chuyển màn và không báo gì. **Không thu hẹp phạm vi kiểm** — *Lưu* `[14]` và *Ban hành* `[15]` luôn xét **mọi dòng của bảng giá**, kể cả dòng đang bị ẩn |
| — | Danh mục sinh SPMM mới | — | — | Bảng còn *Mới* mà danh mục SPMM có thêm mã mới thì lần mở màn sau phần mềm **tự bổ sung dòng** cho mã đó, ô đơn giá trống nên dòng nằm ở đầu lưới. Bảng đã ban hành **không đổi** |

### 5.4 Ban hành bị chặn ở màn sửa

**Figma:** [BG 04 · Ban hành bị chặn (lỗi tại ô)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-15696) · **Bước:** 3 · **Slug:** `ban-hanh-chan`

> **Không phải một màn riêng** — đây là chính `5.3` sau khi bấm *Ban hành* mà thiếu điều kiện. Danh sách điều kiện và nguyên văn từng câu lỗi ở `5.3` `[15]`; mục này chỉ nói **cách báo**.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Báo lỗi tại từng mục | Label (lỗi) | — | Thiếu mục nào thì tô đỏ ô đó và hiện câu lỗi **ngay dưới ô** — riêng *Tài liệu đính kèm* thì cạnh nút, cùng hàng. Báo **đồng thời cho mọi mục còn thiếu**, không báo lần lượt |
| 2 | Ô đơn giá còn trống | — | — | **Mọi ô đơn giá còn trống tô đỏ cùng lúc**, và dòng của chúng đã nằm sẵn ở đầu lưới. **Không có câu lỗi kèm theo** |
| 3 | Vị trí con trỏ | — | — | Nhảy về **mục thiếu đầu tiên** theo thứ tự trên màn |
| 4 | Hệ quả | — | — | `5.5` **không mở**, bảng giá giữ nguyên *Mới*, không bảng nào bị đóng ngày kết thúc. Bổ sung đủ tại chỗ rồi bấm *Ban hành* lại thì mở `5.5` |
| 5 | Ô tìm SPMM đang có chữ | — | — | Phần mềm **tự xoá ô tìm `5.3` `[16]`** trước khi tô đỏ, để mọi ô đơn giá còn trống hiện đủ trên lưới thay vì nằm trong phần đang bị ẩn |

**Vào màn này từ `5.2`:** bấm *Ban hành* ở màn chỉ xem mà thiếu điều kiện thì phần mềm mở thẳng `5.3` ở đúng trạng thái này.

### 5.5 Hộp thoại ban hành

**Figma:** [BG 05 · Hộp thoại ban hành](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-16098) · **Bước:** 3 · **Slug:** `xac-nhan-ban-hanh`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Ban hành bảng giá"* |
| 2 | Dòng nhận diện | Label | — | *"Bảng giá `<mã>` — Số chứng từ `<số>`."* |
| 3 | Câu hệ quả | Label | — | Đã có bảng trước trên trục: *"Ban hành rồi không sửa được nữa. Bảng giá `<mã bảng trước>` sẽ hết hiệu lực từ `<ngày kết thúc mới>`."* Chưa có bảng nào: bỏ hẳn câu thứ hai, chỉ còn *"Ban hành rồi không sửa được nữa."* |
| 4 | Huỷ | Button | — | Đóng hộp thoại, giữ trạng thái *Mới*, không đụng vào bảng nào khác. Bấm `(x)` tương đương |
| 5 | Ban hành bảng giá | Button | — | Khoá hồ sơ, đóng ngày kết thúc của bảng liền trước, **chụp lại mã · tên SPMM · ĐVT** của mọi dòng, rồi mở `5.6`. Ghi lại **người bấm và thời điểm** |
| 6 | Bảng khác vừa được ban hành ở phiên khác | Label | — | Người khác vừa ban hành một bảng làm ngày bắt đầu của bảng này không còn lớn hơn bảng cuối trên trục → câu hệ quả `[3]` **đổi thành** *"Vừa có bảng giá khác được ban hành, ngày bắt đầu của bảng này không còn hợp lệ."*, nút chính `[5]` đổi thành *Đóng*. Đóng xong màn nạp lại ở `5.3` với ô ngày tô đỏ. **Báo ngay trong hộp thoại đang mở**, không đẻ thêm hộp thoại và không dùng thông báo nổi |

### 5.6 Bảng giá đã ban hành — chỉ đọc

**Figma:** [BG 06 · Bảng giá đã ban hành (chỉ đọc)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-16500) · **Bước:** sau 3 · **Slug:** `bg-da-ban-hanh`

> Dùng chung cho cả ba trạng thái sau ban hành: *Sắp áp dụng* · *Hiệu lực* · *Hết hiệu lực*. Ba trạng thái đó chỉ khác nhau ở nhãn và ở việc bảng có đang là nguồn giá gợi ý hay không — nội dung màn giống hệt.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Sắp áp dụng* · *Hiệu lực* · *Hết hiệu lực*, tính ra khi mở màn theo Mục 4.1 |
| 2 | Toàn màn | — | — | Cùng bộ trường và cùng bốn cột với `5.3`, **mọi ô ở trạng thái vô hiệu hoá**. Không sửa được trường nào, không sửa được đơn giá dòng nào. **Riêng ô tìm SPMM `5.3` `[16]` vẫn gõ được** — nó là cách xem, không phải ô dữ liệu |
| 3 | Mã SPMM · tên SPMM · ĐVT | Text (chỉ đọc) | — | Đọc từ **bản chụp lúc ban hành**, không đọc lại danh mục hiện hành — `NFR-bang-gia-001` |
| 4 | Ngày kết thúc hiệu lực | Text (chỉ đọc) | Ngày | **Để trống** khi chưa có bảng sau. Có bảng sau thì phần mềm đã điền, và giá trị đó **không sửa được** |
| 5 | Tài liệu đính kèm | Button + badge | Tệp | Mở được để **xem và tải** văn bản ban hành. **Không thêm, không xoá tệp** |
| — | Icon sửa · *Lưu* · *Ban hành* · *Xoá* · icon nhân bản | — | — | **Không có**. Nhân bản gọi từ icon trên dòng ở `5.1` |

### 5.7 Hộp thoại xoá bảng giá

**Figma:** [BG 07 · Cảnh báo xoá bảng giá](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=860-16902) · **Bước:** ngoài luồng chính · **Slug:** `xoa-bg-canh-bao`

> Mở từ icon xoá trên dòng ở `5.1`. **Chỉ mở được với bảng giá còn *Mới*.**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xoá bảng giá"* |
| 2 | Dòng nhận diện | Label | — | *"Bảng giá `<mã>`."* Chỉ một giá trị — bảng còn *Mới* thì **chưa có Số chứng từ**, nên bỏ hẳn đoạn sau gạch dài thay vì để nhãn với ô trống |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Xoá rồi không khôi phục được."* |
| 4 | Huỷ | Button | — | Đóng hộp thoại, không xoá gì. Bấm `(x)` tương đương |
| 5 | Xoá bảng giá | Button | — | Xoá hẳn hồ sơ rồi quay lại `5.1`. Không đụng tới bảng giá nào khác |

## 6. Quy tắc chung

**12 quy tắc.** Chỉ những gì **không thuộc màn nào** hoặc **xuyên nhiều màn**. Luật của từng ô và từng nút nằm ở Mục 5, không lặp lại ở đây.

| ID | Quy tắc | Cách kiểm |
|---|---|---|
| `BR-bang-gia-001` | **Trạng thái tính ra khi mở màn** theo bảng điều kiện ở Mục 4.1 — **không lưu cờ trạng thái**, **không có tác vụ chạy nền** nào bật tắt | Ban hành một bảng có ngày bắt đầu là ngày mai → hôm nay là *Sắp áp dụng*; đổi ngày hệ thống sang ngày mai, mở lại danh sách → thành *Hiệu lực*, không chạy tác vụ gì |
| `BR-bang-gia-002` | **Phần mềm sinh *Mã bảng giá* ở lần *Lưu* đầu tiên**, dạng `BG/<năm>/<4 số>`, duy nhất trong toàn hệ, **không đổi và không tái sử dụng** kể cả khi bảng giá bị xoá | Lưu một bảng giá mới → có mã; xoá nó rồi lưu bảng khác → mã mới, không trùng mã vừa xoá |
| `BR-bang-gia-003` | **Bảng chi tiết luôn chứa toàn bộ danh mục SPMM.** Tạo mới hay nhân bản đều đổ đủ danh mục **hiện tại**; không thêm dòng, không xoá dòng. Bảng còn *Mới* thì mỗi lần mở màn **bổ sung dòng** cho SPMM mới sinh trong danh mục. Bảng đã ban hành **không đổi** | Lưu một bảng giá, thêm một SPMM vào danh mục, mở lại → có thêm đúng một dòng, đơn giá trống, nằm ở đầu lưới. Làm lại với một bảng đã ban hành → không có dòng nào thêm |
| `BR-bang-gia-004` | **Ban hành đóng ngày kết thúc của đúng MỘT bảng.** Bảng bị đóng là bảng đã ban hành có ngày bắt đầu lớn nhất; ngày kết thúc của nó = ngày bắt đầu bản mới **trừ một ngày**. Chưa có bảng đã ban hành nào thì không đóng bảng nào | Có bảng A hiệu lực từ 01/10/2026, ngày kết thúc trống. Ban hành bảng B từ 01/01/2027 → A có ngày kết thúc 31/12/2026, không bảng nào khác đổi |
| `BR-bang-gia-005` | **Ban hành là khoá tuyệt đối.** Không sửa trường nào, không sửa đơn giá, không thay tệp, không xoá, **không thu hồi, không huỷ**. Đổi giá phải đi đường **nhân bản**; ban hành nhầm thì ban hành bảng đúng với ngày bắt đầu sau đó | Mở một bảng đã ban hành → không ô nào sửa được, không có nút *Lưu* / *Xoá* / *Thu hồi* / *Huỷ*; gọi thẳng địa chỉ màn sửa → bị chặn |
| `BR-bang-gia-006` | **Nhân bản chép** đơn giá của mọi dòng, *Tên bảng giá* và ghi chú; **không chép** *Mã bảng giá*, hai ngày hiệu lực, *Số chứng từ*, *Ngày chứng từ*, tệp đính kèm. Bản sao ở trạng thái *Mới*, danh sách dòng lấy theo **danh mục SPMM hiện tại**. Gọi được ở **mọi trạng thái**, chỉ từ màn danh sách | Nhân bản một bảng đã ban hành → bản mới ở *Mới*, sáu trường trên trống, mọi dòng có đúng đơn giá của bản gốc, và có thêm dòng cho SPMM sinh sau khi bản gốc được ban hành |
| `BR-bang-gia-007` | **QĐGCTKH và Hợp đồng đọc giá gợi ý từ bảng ở trạng thái *Hiệu lực* tại thời điểm mở màn.** SPMM không có dòng trong bảng đó, hoặc **chưa có bảng nào ở *Hiệu lực***, thì ô *Đơn giá* **để trống** — người lập gõ tay, **không chặn, không báo gì**, và **không điền `0` thay cho trống**. Đổi bảng giá **không sửa lại** hồ sơ đã lưu. Cùng một yêu cầu với `FR-qdgctkh-002` và `FR-hop-dong-002` | Lập một hợp đồng, ghi lại giá gợi ý; ban hành bảng giá mới với giá khác → mở lại hợp đồng cũ: giá giữ nguyên; lập hợp đồng mới: lấy giá mới. Xoá hết bảng giá *Hiệu lực* → ô đơn giá trống, hợp đồng vẫn lưu được |
| `BR-bang-gia-008` | **Cục QL độc quyền ghi.** Bốn bản hệ đầu hệ nhận bảng giá đã đồng bộ ở dạng **chỉ đọc** — mọi nút ghi bị ẩn, không có đường nào lập hay sửa bảng giá ở bản hệ. ⚠️ **Tần suất và cơ chế đồng bộ chưa chốt** — xem Mục 8 | Ở bản hệ, mở màn danh sách → không có nút *Tạo bảng giá*, không có icon sửa / nhân bản / xoá; gọi thẳng địa chỉ màn sửa → bị chặn |
| `NFR-bang-gia-001` | **Ban hành là mốc đóng băng — đóng băng HẾT, không riêng con số.** Bảng giá đã ban hành giữ nguyên vĩnh viễn *đơn giá*, **mã SPMM, tên SPMM và ĐVT** — đọc từ **bản chụp lúc ban hành**, không đọc lại danh mục hiện hành. Cùng khuôn `NFR-qdgctkh-004` | Ban hành một bảng giá, rồi đổi tên một SPMM và đổi ĐVT của nó trong danh mục → mở lại bảng giá: tên cũ và ĐVT cũ giữ nguyên, đơn giá không đổi |
| `NFR-bang-gia-002` | **Mọi hành động đổi trạng thái ghi lại được ai làm và lúc nào** — lưu lần đầu, ban hành, xoá. Người tạo và thời điểm tạo **không bày trên màn nào** nhưng vẫn tra ra được | Ban hành một bảng giá → tra ra được người bấm và thời điểm; mở lại màn thì không thấy trường nào bày hai thông tin đó |
| `NFR-bang-gia-003` | **Không hai người cùng ban hành được hai bảng giá chồng khoảng.** Phần mềm chỉ nhận lần bấm đầu tiên; lần bấm sau bị chặn với câu báo ở `5.5` `[6]`, **không sinh hai lần chuyển trạng thái** và **không đóng nhầm ngày kết thúc của bảng nào**. Cùng khuôn `NFR-hop-dong-003` | Mở hai bảng giá *Mới* có ngày bắt đầu khác nhau ở hai phiên, bấm *Ban hành* ở cả hai gần như cùng lúc → chỉ một qua được; bảng còn lại phải sửa ngày mới ban hành được, trục thời gian không có hai bảng chồng khoảng |
| `NFR-bang-gia-004` | **Ghi dữ liệu thất bại thì không mất gì.** Áp cho *Lưu*, *Ban hành*, *Xoá*: máy chủ lỗi hoặc mất kết nối thì dữ liệu đang nhập **giữ nguyên trên màn**, bảng giá **giữ nguyên trạng thái cũ**, và **không bảng nào bị đóng ngày kết thúc**, bấm lại được | Ngắt kết nối rồi bấm *Ban hành* → đơn giá đang gõ còn nguyên, trạng thái không đổi, bảng liền trước vẫn có ngày kết thúc trống, có thông báo lỗi, bấm lại được |

## 7. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|:--:|---|---|
| 1 | **Tại mọi thời điểm tra được đúng một bảng giá đang hiệu lực**, không cần ai bấm gì để bật tắt | Ban hành ba bảng giá nối tiếp nhau; đổi ngày hệ thống về ba mốc khác nhau, mỗi lần mở danh sách → đúng một dòng mang nhãn *Hiệu lực* |
| 2 | **Tra được giá của một SPMM tại một mốc thời gian trong quá khứ** | Mở bảng giá *Hết hiệu lực* phủ ngày 15/03 → đọc được đơn giá của SPMM X đúng như lúc đó, kể cả khi SPMM X đã đổi tên từ đó tới nay |
| 3 | **Không có quãng thời gian nào không có bảng giá**, kể từ bảng đầu tiên | Ban hành ba bảng nối tiếp; ghép ba khoảng hiệu lực lại → liền mạch, không hở ngày nào, không chồng ngày nào |
| 4 | **Đổi giá không làm xáo trộn hồ sơ đã lập** | Lập một QĐGCTKH và một hợp đồng; ban hành bảng giá mới với giá khác hẳn → mở lại cả hai: mọi con số giữ nguyên |
| 5 | **Bảng giá đã ban hành phủ hết danh mục SPMM tại thời điểm ban hành** | Mở bảng giá bất kỳ ở trạng thái đã ban hành → cột *SPMM có giá* ở `5.1` luôn ở dạng `n / n`, không dòng nào trống đơn giá |

## 8. Câu hỏi mở

| Mức | Câu hỏi | Vì sao quan trọng | Người chốt |
|:--:|---|---|---|
| 🟡 | ***Số chứng từ* có phải duy nhất trong toàn hệ không**, và có định dạng bắt buộc nào không | Nếu duy nhất thì cần thêm một điều kiện vào nút *Lưu* hoặc *Ban hành*; nếu không thì hai bảng giá mang cùng số chứng từ là hợp lệ và không tra ngược được về văn bản gốc. Ảnh hưởng `5.3` `[2]` | @quynhdtn17 |
| 🟡 | **Có ràng buộc khoảng hiệu lực tối thiểu không** — hai bảng ban hành cách nhau một ngày là hợp lệ hay bất thường | Điều kiện ở `5.3` `[15]` chỉ đòi ngày bắt đầu *lớn hơn* bảng trước, nên một bảng có thể chỉ sống đúng một ngày. Chưa chốt thì không biết đó là ca cần chặn hay ca bình thường | Cục QLKTNVMM |
| 🟡 | **Phòng nào trong Cục QLKTNVMM giữ ba quyền *Lập* · *Ban hành* · *Xoá*** | Chưa chốt thì Mục 3.1 chỉ khai được tên quyền, không khai được ai giữ | Cục QLKTNVMM |
| 🟡 | **Tần suất và cơ chế đồng bộ bảng giá** từ bản Cục QL xuống 4 bản hệ đầu hệ | Quyết định bao lâu sau khi ban hành thì hệ đầu hệ nhìn thấy giá mới. Bảng giá đổi ở Cục mà hệ còn đọc bảng cũ thì hai bên nói hai con số. Ảnh hưởng `BR-bang-gia-008` | BCY *(thừa hưởng bất biến I7)* |
| 🟡 | **Đơn vị tính *Hệ thống* và bộ/thiết bị đơn lẻ** — đơn giá của một *Hệ thống* và đơn giá của từng thiết bị trong đó là hai con số khác hẳn | Chưa chốt thì chưa xác định được *Đơn giá* của bảng này đang tính cho dạng nào. Trên màn bảng giá thì cột *ĐVT* chỉ hiện lại giá trị của danh mục nên **không chặn việc dựng màn**; nó chặn ở tầng danh mục SPMM | Cục QLKTNVMM *(thừa hưởng bất biến I2)* |
| 🟢 | **Hệ đầu hệ có cần màn xem bảng giá riêng không**, hay chỉ dùng ngầm ở các màn nghiệp vụ của hệ | Đợt này chưa có nghiệp vụ nào ở hệ đọc giá. Tới lúc làm QLTS (tài sản có nguyên giá) thì câu này mới có đáp án thật | Cục QLKTNVMM |

## 9. Chưa làm ở đợt này

- **Nhập đơn giá hàng loạt bằng Excel.** Đợt này gõ tay từng dòng trên lưới.
- **Xuất bảng giá ra Excel.** Chưa có nhu cầu đối chiếu ngoài phần mềm.
- **Loại tiền khác VND và tỉ giá.**
- **Sơ đồ vòng đời trạng thái.** Trạng thái của bảng giá **tính ra từ ngày** chứ không do người dùng bấm, nên sơ đồ máy trạng thái chỉ vẽ được đúng hai mũi tên do người bấm — hai bảng ở Mục 4 đúng hình dạng của logic hơn.

## 📝 Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|---|---|---|---|---|
| 2026-08-27 | thêm mới | `docs/cuc-ql/brainstorming/brainstorm-bang-gia.md` Mục 3 và Mục 5 · `docs/cuc-ql/user-flow/userflow-bang-gia.md` · ba file `screen-bang-gia-*.md` · 7 frame Figma khu vực 6 file BCY(2) | @quynhdtn17 | Bản đầu tiên: Mục 4 vòng đời trạng thái, Mục 5 gồm 7 màn, Mục 6 quy tắc chung |
| 2026-08-27 | cập nhật | @quynhdtn17 chốt 27/08/2026 | @quynhdtn17 | **Gộp luật về hai chỗ.** Mục 4 viết lại bằng lời, bỏ ký hiệu tắt và bỏ cột *Điều kiện* của bảng chuyển trạng thái — điều kiện bấm nút chuyển hết về nút tương ứng ở Mục 5. Bỏ bảng kiểm `L1`–`B6` và bảng đọc giá `G1`–`G3`; nội dung nhập vào nút *Lưu* / *Ban hành* ở `5.3` và vào `BR-bang-gia-007`. Gộp ba mục *Yêu cầu chức năng* · *Quy tắc nghiệp vụ* · *Yêu cầu phi chức năng* thành một Mục 6, **30 quy tắc còn 12**. Mục 4.1 viết lại thành bảng điều kiện `Hôm nay` so với hai mốc ngày, thêm mốc giờ 00:00:00 và 23:59:59. **Gỡ phần hình thức khỏi SRS** — cách tô đỏ báo lỗi, vị trí icon sửa, biểu tượng lịch, chữ in đậm trong hộp thoại, màu nút xoá: đã có ở `docs/design.md` Mục 9.1 và 9.4 |
| 2026-08-28 | cập nhật | 5 frame Figma BG 02 · BG 03 · BG 04 · BG 05 · BG 06 file BCY(2) | @quynhdtn17 | Thêm ô tìm theo mã hoặc tên SPMM vào cột *SPMM* của lưới *Chi tiết đơn giá* — `5.3` `[16]`, dùng chung ở hai màn chỉ đọc `5.2` và `5.6`; ban hành bị chặn thì tự xoá ô tìm (`5.4` `[5]`) |
