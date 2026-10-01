---
type: srs
feature: nhap-kho
status: dang-review
updated: 2026-09-04
nguon:
  - Figma BCY(2) · Page 1 · khu vực 6 — 16 khung NK 01–16
  - docs/cuc-ql/srs/srs-hop-dong.md
---

# Đặc tả: Phiếu nhập kho SPMM

**Figma:** file **BCY(2)** · Page 1 · khu vực 6 — **16 khung**, đánh số `NK 01`–`NK 16`, khung 1440 (riêng `NK 03` rộng 1801 để thấy đủ lưới).

## 1. Phạm vi

Nhập kho là **bước 4** của chuỗi nghiệp vụ QLSPMM: sau *Hợp đồng*, trước *Quyết định triển khai*.

Cán bộ kho lập phiếu trên căn cứ **một hợp đồng *Đã xác nhận***. Chọn hợp đồng xong, phần mềm đổ đủ danh sách SPMM của hợp đồng kèm số còn lại chưa nhập. Người lập gõ *SL nhập kho* thực nhận theo chứng từ giao hàng, rồi mở hộp thoại serial của từng dòng để quét hoặc gõ mã định danh của từng cái. Bấm *Lưu* — phần mềm sinh *Mã phiếu*, hồ sơ ở trạng thái *Mới*, serial được giữ chỗ trong hệ. Kiểm đếm xong, nhập *Số phiếu nhập kho* lấy từ chứng từ giấy rồi bấm *Xác nhận* — hàng vào tồn kho, hồ sơ khoá lại.

**Một hợp đồng nhập nhiều đợt.** Mỗi đợt một phiếu, phần mềm trừ dần vào số đã đặt của hợp đồng.

**Đây là nơi SPMM lần đầu tồn tại thành từng cái.** Trước bước này, hợp đồng và quyết định chỉ đếm theo **loại** SPMM. Từ bước này trở đi, mỗi cái có một mã định danh riêng và theo được suốt vòng đời.

**Đơn vị tính** đi theo SPMM trong danh mục, phiếu chỉ hiện lại ở cột *ĐVT*. Việc một *Hệ thống* được đếm như thế nào là vấn đề ở tầng danh mục SPMM, chưa chốt.

**Một loại tiền duy nhất: VND.** Không có ô chọn loại tiền, không có tỉ giá. Đơn vị tiền ghi ở đúng hai chỗ — ô *Tổng tiền (VND)* trong *Thông tin chung* và hàng *Tổng cộng (VND)* ở chân lưới.

### 1.1 Bản triển khai

| Việc | Chạy ở bản |
|---|---|
| Toàn bộ 16 màn — lập · sửa · chọn hợp đồng · gõ số nhận · quét serial · xác nhận · xoá · tra cứu | **Cục QL** |

Nhập kho theo hợp đồng **không đi xuống các bản hệ đầu hệ** và **không nằm trong luồng đồng bộ** giữa Cục QL và 4 hệ. Cả cán bộ kho của Cục lẫn cán bộ kho của nhà máy thuộc Ban đều dùng **cùng một bản trên máy chủ Cục QL**, chỉ khác phạm vi dữ liệu ở Mục 3.

### 1.2 Ngoài phạm vi

- **Biên bản giao nhận, biên bản kiểm đếm và mọi thủ tục giấy** giữa bên giao và bên nhận — nằm ở eOffice và quy trình riêng của đơn vị. Phần mềm chỉ **ghi nhận kết quả đã nhận**.
- **Cấp mã định danh SPMM.** Mã do đơn vị sản xuất đánh lên từng cái trước khi giao; phần mềm phía kho **không sinh mã**, chỉ ghi lại mã quét được. Tab *Nhập số Serial theo dải* `5.6` **không phải là cấp mã** — nó gõ hộ một dải mã nhà máy đã đánh liên tiếp, người lập vẫn phải đối chiếu với hàng thật.
- **Serial vật lý của linh kiện** — xem Mục 1.3.
- **Danh mục kho và vị trí cất giữ**, **cây đơn vị**, **danh mục *Nguồn kinh phí*** — phiếu chỉ đọc, quản lý ở chức năng riêng.
- **Điều chuyển từ kho nhà máy về kho Cục** — chức năng riêng, có đặc tả riêng.
- **Xuất kho, cấp phát, kiểm kê** — chức năng riêng.

### 1.3 Hai con số trên một SPMM

| Tên | Nguồn | Có ở đợt này |
|---|---|---|
| ***Mã định danh SPMM*** — 15 số | Đơn vị sản xuất đánh lên từng cái theo quy cách của Ban. **Cố định suốt vòng đời**, không đổi kể cả khi thiết bị được sửa chữa | **Có.** Đây là con số quét vào ở hộp thoại serial `5.5` / `5.6`, và là khoá theo dõi từng cái từ đây về sau |
| ***Serial vật lý* của linh kiện** | Nhà sản xuất linh kiện đánh. **Đổi được** khi thay bo mạch chính, CPU | **Không.** Phiếu nhập kho không ghi, không đối chiếu |

Hai con số này **không được gộp làm một**. Cột trên màn tên là *Số serial* theo cách gọi quen của người dùng, nhưng thứ ghi vào là **mã định danh 15 số**.

**Khuôn mã định danh 15 chữ số** — sáu phần ghép liền, không dấu ngăn, toàn chữ số:

| Thứ tự | Phần | Số chữ số | Lấy từ |
|---|---|---|---|
| 1 | Mã *Nguồn kinh phí* | 1 | hợp đồng của phiếu |
| 2 | Mã *Đơn vị sản xuất* | 1 | hợp đồng của phiếu |
| 3 | Mã nhóm SPMM | 2 | danh mục SPMM |
| 4 | Mã SPMM | 4 | danh mục SPMM |
| 5 | Số chạy | 5 | nhà máy tự đánh |
| 6 | Năm sản xuất, hai số cuối | 2 | nhà máy tự đánh |

Bốn phần đầu **chỉ phụ thuộc vào hợp đồng và SPMM**, nên **tám chữ số đầu** của một mã đủ để biết mã đó thuộc dòng SPMM nào trên phiếu. Đây là căn cứ để ô *Quét/Nhập serial* `5.2` `[28]` tự đưa mã vừa quét về đúng dòng, và cũng là căn cứ để kiểm mã có hợp lệ hay không.

> ⚠️ **Hai điều kiện phải xong trước khi bật ô quét chung.** Chưa xong thì mã định danh sinh ra không đủ 15 chữ số và mọi lần quét đều bị chặn.
>
> **1. Mã nhóm SPMM phải đúng hai chữ số.** Ở danh mục hiện còn nhận cả chữ cái và dài bao nhiêu cũng được. Phải ép đúng hai chữ số, và **rà lại các nhóm đang có**.
>
> **2. Nhà máy phải có một số hiệu đúng một chữ số.** *Hợp đồng sản xuất* lấy *Đơn vị sản xuất* từ **cây đơn vị**, mà ô *Mã* của cây đơn vị dùng chung cho mọi đơn vị của Ban — **không được ép ô đó xuống một chữ số**: đơn vị sử dụng cần mã dài hơn, và mã đơn vị còn nằm trong *Mã phiếu* (Mục 1.4). Số hiệu này phải **không trùng giữa các nhà máy** và **không đổi sau khi đã có mã định danh sinh theo nó** — đổi là mọi mã cũ mất căn cứ tra ngược. Lấy số đó ra bằng cách nào là việc thiết kế của Dev.
>
> Mã *Nguồn kinh phí* đã ràng buộc đúng một chữ số và mã SPMM đã ràng buộc đúng bốn chữ số — hai phần này không phải làm gì thêm.

### 1.4 Hai số hiệu của phiếu

| Tên | Nguồn | Định dạng | Bắt buộc |
|---|---|---|---|
| ***Mã phiếu*** | Phần mềm sinh khi *Lưu* lần đầu. Chỉ đọc, duy nhất, không đổi suốt vòng đời | `PNK/<mã đơn vị>/<năm>/<4 số>` | Luôn có kể từ lần lưu đầu |
| ***Số phiếu nhập kho*** | Người dùng nhập tay, lấy từ chứng từ giấy | Theo số phiếu của đơn vị | Bắt buộc khi *Xác nhận*, và **không trùng trong cùng đơn vị cùng năm** |

***Mã phiếu*** là khoá liên kết dữ liệu và là cột bấm để mở phiếu. ***Số phiếu nhập kho*** không dùng làm khoá — lúc lập phiếu chưa kiểm đếm xong thì chưa có chứng từ, chưa có chứng từ thì chưa có số.

## 2. Quy trình nghiệp vụ

| # | Ai làm | Làm gì | Ở đâu |
|:--:|---|---|---|
| 1 | Bên giao · Bên nhận | **Giao hàng, kiểm đếm, ký biên bản giao nhận** theo quy trình riêng của đơn vị | **Ngoài phạm vi QLSPMM** |
| 2 | Cán bộ kho | Tạo phiếu, chọn **một** hợp đồng *Đã xác nhận*. Phần mềm đổ đủ danh sách SPMM của hợp đồng kèm cột *SL còn lại theo HĐ*. Gõ *SL nhập kho* cho những SPMM nhận trong đợt này | `5.2` · `5.3` |
| 3 | Cán bộ kho | Mở hộp thoại serial của từng dòng, quét hoặc gõ mã định danh của từng cái. Bấm *Lưu* — sinh *Mã phiếu*, hồ sơ ở trạng thái *Mới*, serial được giữ chỗ | `5.5` · `5.6` |
| 4 | Cán bộ kho | Nhập *Số phiếu nhập kho* lấy từ chứng từ giấy, đính kèm biên bản, bấm *Xác nhận* — hàng vào tồn kho, hồ sơ khoá sửa | `5.7` · `5.9` |

**Điều kiện vào:** đã có một hợp đồng ở trạng thái *Đã xác nhận* và chưa *Kết thúc*.
**Điều kiện ra:** SPMM đã có mặt trong tồn kho theo từng mã định danh, sẵn sàng cho điều chuyển và cấp phát.

## 3. Phân quyền

Nhập kho chỉ chạy ở bản Cục QL. Phạm vi dữ liệu cắt theo **đơn vị của người đăng nhập**, độc lập với quyền chức năng ở Mục 3.1.

**Mỗi đơn vị chỉ thấy phiếu nhập kho của chính đơn vị mình.** Danh sách `5.1`, ô chọn hợp đồng `5.3` và mọi màn chi tiết đều cắt theo đơn vị này.

Đơn vị sản xuất có ký hợp đồng thì **thấy hợp đồng đó** để lập phiếu nhập kho theo nó — cùng một chức năng nhập kho, cùng một bộ màn, chỉ khác kho nhận và khác phạm vi dữ liệu.

**Một hợp đồng chỉ có một bên nhập kho.** Hợp đồng ký với một nhà máy thì nhà máy đó nhập; không có chuyện hai đơn vị cùng lập phiếu trên một hợp đồng.

> ⚠️ **Chưa chốt: nhà máy có tài khoản trên phần mềm hay không.** Hai khả năng đang để ngỏ — nhà máy tự lập phiếu cho kho của mình, hoặc nhà máy không có tài khoản và **cán bộ Cục lập phiếu cho cả hàng về kho nhà máy**.
>
> **Đợt này dựng cho cả hai khả năng đều chạy được**, chốt xong mới chỉnh. Chỉ hai chỗ phải sửa khi chốt, còn lại giữ nguyên: ô *Kho nhập* `5.2` `[4]` (đang liệt kê kho của đơn vị người đăng nhập — nếu Cục lập hộ thì phải cho chọn cả kho nhà máy) và phạm vi dữ liệu ở mục này. Màn hình, luồng và mọi quy tắc khác không đổi theo hướng nào.
>
> Chốt hướng nào là việc của Cục QLKTNVMM.

### 3.1 Quyền theo vai trò

| Quyền | Cho phép |
|---|---|
| **Xem phiếu nhập kho** | Mở màn danh sách `5.1`, mở xem chi tiết `5.7` / `5.13`, mở xem serial |
| **Lập phiếu nhập kho** | Tạo mới, sửa *Thông tin chung*, chọn và đổi hợp đồng, gõ *SL nhập kho* · *Vị trí* · *Ghi chú*, quét serial, đính kèm tài liệu |
| **Xác nhận phiếu nhập kho** | Bấm *Xác nhận* |
| **Xoá phiếu nhập kho** | Xoá phiếu còn *Mới* |

### 3.2 Thao tác theo trạng thái

Một thao tác chạy được khi **tài khoản có quyền ở Mục 3.1** *và* **trạng thái phiếu cho phép**. Thiếu một trong hai thì nút không hiện.

| Thao tác trên một phiếu | *Mới* | *Đã xác nhận* |
|---|:--:|:--:|
| Xem chi tiết | ✔ | ✔ |
| Sửa *Thông tin chung* | ✔ | ✘ |
| Đổi *Số hợp đồng* | ✔ | ✘ |
| Sửa *SL nhập kho* · *Vị trí* · *Ghi chú* | ✔ | ✘ |
| Thêm và bớt serial | ✔ | ✘ |
| Xem danh sách serial của một dòng | ✔ | ✔ |
| Thêm và bớt *Tài liệu đính kèm* | ✔ | ✘ |
| Mở xem và tải tệp đính kèm | ✔ | ✔ |
| Xuất phụ lục | ✔ | ✔ |
| Xác nhận | ✔ | ✘ |
| Xoá | ✔ | ✘ |

`✔` được làm · `✘` phần mềm chặn

*Tạo phiếu* và *Xem danh sách* không phụ thuộc trạng thái, chỉ cần quyền ở Mục 3.1.

## 4. Vòng đời trạng thái

Hai trạng thái: ***Mới*** → ***Đã xác nhận***. Không có nấc phê duyệt trung gian, không có nhánh *Trả lại*, không có đường lùi.

| Trạng thái | Nghĩa |
|---|---|
| ***Mới*** | Đang nhập liệu, hàng chưa vào tồn kho. Sửa và xoá được. Serial đã quét **đã bị giữ chỗ** trong hệ nhưng chưa thành tồn |
| ***Đã xác nhận*** | Hàng đã vào tồn kho theo từng mã định danh. Khoá hẳn. **Trạng thái cuối** |

| Từ | Đến | Kích hoạt bằng | Điều kiện | Hệ quả |
|---|---|---|---|---|
| *(chưa có)* | ***Mới*** | *Lưu* lần đầu ở `5.2` | Đủ trường bắt buộc khi lưu, xem `5.2` `[30]` | **Sinh *Mã phiếu***, không đổi về sau. Serial đã quét bị giữ chỗ — phiếu khác quét trùng thì bị chặn. **Chưa trừ vào hợp đồng** |
| ***Mới*** | ***Đã xác nhận*** | *Xác nhận* ở `5.7`, xác nhận lại ở `5.9` | *Số phiếu nhập kho* đã nhập và không trùng, và **mọi dòng có *SL nhập kho* đều đã quét đủ serial** | **Khoá sửa toàn bộ**. Sinh tồn kho theo từng mã định danh vào đúng *Kho nhập* và *Vị trí* của dòng. Trừ vào *SL còn lại theo HĐ* của hợp đồng và cập nhật *Tiến độ nhập kho* của hợp đồng. Ghi lại người bấm và thời điểm |
| ***Mới*** | *(xoá hẳn)* | Icon xoá ở `5.1`, xác nhận ở `5.12` | — | Xoá bản ghi. **Toàn bộ serial phiếu đó đang giữ chỗ được nhả ra ngay**, phiếu khác quét lại được |

**Chuyển trạng thái bị CẤM:** phiếu *Đã xác nhận* **không quay lại *Mới***, **không huỷ xác nhận, không sửa, không xoá**. Nhập sai thì xử lý bằng nghiệp vụ điều chỉnh kho ngoài phạm vi đợt này.

Phiếu có hai trạng thái nối thẳng một chiều, một tác nhân, không nhánh rẽ — bảng trên là đủ, không dựng sơ đồ vòng đời riêng.

## 5. Màn hình

**13 mục**, toàn bộ chạy ở **bản Cục QL**, toàn bộ đã vẽ trên Figma.

Bốn hộp thoại `5.4` `5.9` `5.11` `5.12` theo khuôn dùng chung ở `docs/design.md` Mục 9.4: tiêu đề là cụm động từ hành động · dòng nhận diện · câu hệ quả · nút chính mang đúng chữ của tiêu đề.

**Một cách báo thiếu điều kiện duy nhất: tô đỏ tại trường** — `BR-nhap-kho-013`.

**SPMM luôn là MỘT cột `Mã - Tên`**, không tách Mã và Tên thành hai cột.

**Lưới chi tiết rộng hơn khung nên cuộn ngang, cột *Thao tác* ghim ở mép phải** — `docs/design.md` Mục 9.3. Mười hai cột kia trượt, cột ghim đứng yên.

### 5.1 Danh sách phiếu nhập kho

**Figma:** [NK 01 · Danh sách phiếu nhập kho](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1064-26778) · [NK 02 · Danh sách rỗng](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1079-41390) · **Bước:** điểm vào · **Slug:** `danh-sach-pnk`

> Hàng lọc nằm trong lưới ngay dưới tiêu đề cột, áp dụng ngay khi nhập. Không có thẻ lọc riêng, không có nút *Tìm* / *Xoá lọc*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Ô chọn cột hiển thị | Multiselect | Danh sách cột | Bật tắt cột nào hiện trên lưới. Chỉ đổi cách xem, không đổi dữ liệu |
| 2 | Thêm mới | Button | — | Mở `5.2` với phiếu trắng: *Ngày nhập kho* mặc định ngày hôm nay, *Loại hợp đồng* mặc định *Hợp đồng sản xuất*, lưới rỗng cho tới khi chọn *Số hợp đồng*. Chỉ hiện với tài khoản có quyền *Lập phiếu nhập kho* |
| — | Bảng danh sách | Table | — | Cột: STT · **Mã phiếu** · Trạng thái · Số phiếu nhập kho · Kho nhập · Loại HĐ · Số hợp đồng · Đơn vị sản xuất · Ngày nhập kho · Thao tác. Chỉ liệt kê phiếu của **đơn vị người đăng nhập** |
| 3 | Hàng lọc từng cột | Input · Dropdown · Date | Theo cột | Lọc theo Mã phiếu, Trạng thái, Số phiếu, Kho nhập, Loại HĐ, Số hợp đồng, Đơn vị sản xuất, Ngày nhập kho. Lọc không ra dòng nào thì bảng rỗng, không chuyển màn |
| 4 | Mã phiếu | Link | Chuỗi | Phần mềm sinh khi *Lưu* lần đầu, dạng `PNK/<mã đơn vị>/<năm>/<4 số>`, không đổi suốt vòng đời. Cột bấm để mở: dòng *Mới* mở `5.7`, dòng *Đã xác nhận* mở `5.13` chỉ đọc |
| 5 | Trạng thái | Tag | Danh mục | Hai giá trị: *Mới* · *Đã xác nhận* |
| 6 | Số phiếu nhập kho | Text | Chuỗi | Số trên chứng từ giấy. **Để trống khi còn *Mới*** — chỉ nhập lúc xác nhận |
| 7 | Kho nhập | Text | Chuỗi | Kho nhận hàng của đợt này |
| 8 | Loại HĐ | Text | Danh mục | *HĐ sản xuất* hoặc *HĐ thương mại* |
| 9 | Số hợp đồng | Text | Chuỗi | Số của hợp đồng mà phiếu neo vào. Một phiếu neo **đúng một** hợp đồng |
| 10 | Ngày nhập kho | Text | Ngày | Ngày hàng thực nhận, lấy từ `5.2` `[3]` |
| 11 | Sửa | Icon button | — | Chỉ hiện ở dòng *Mới* và với tài khoản có quyền *Lập*. Mở `5.7` |
| 12 | Xoá | Icon button | — | Chỉ hiện ở dòng *Mới* và với tài khoản có quyền *Xoá*. Mở `5.12` trước khi xoá |
| 13 | Phân trang | Paginator | — | Mặc định 10 dòng một trang. Dòng chú thích ghi *"Hiển thị `<a>` – `<b>` / `<N>` phiếu"* |
| 14 | Trạng thái rỗng | Empty state | — | Chưa có phiếu nào thì thân bảng thay bằng dòng *"Chưa có phiếu nhập kho nào"* và câu phụ *"Bấm Thêm mới để lập phiếu đầu tiên."*. **Hàng tiêu đề cột và hàng lọc vẫn giữ nguyên**. Lọc ra rỗng thì không dùng trạng thái này — bảng chỉ rỗng thân |

### 5.2 Lập phiếu nhập kho

**Figma:** [NK 03 · Lập phiếu nhập kho](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1065-27254) · **Bước:** 2–3 · **Slug:** `pnk-lap`

> **Hai khối gập** xếp dọc trên một màn: *Thông tin chung* · *Thông tin chi tiết*. Khung Figma của màn này rộng 1801 để thấy đủ lưới; trên khung thật 1440 thì lưới cuộn ngang.
>
> Khối *Thông tin chi tiết* là **bảng đóng theo hợp đồng**: không thêm được SPMM ngoài hợp đồng, không xoá được dòng — nên **không có hàng thêm nhanh, không có ô tích đầu dòng**. Cột *Thao tác* chỉ chứa nút mở hộp thoại serial.
>
> Màn chưa lưu **chỉ có hai nút *Hủy* · *Lưu*** ở hàng tiêu đề trang, và **không có hàng công cụ lưới** — chưa lưu thì chưa có gì để xuất.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Mã phiếu | Text (chỉ đọc) | Chuỗi | Phần mềm sinh khi *Lưu* lần đầu. Trước lần lưu đầu để trống. Không sửa được, không đổi suốt vòng đời |
| 2 | Số phiếu nhập kho | Input | Chuỗi | **Bắt buộc khi *Xác nhận*, không bắt buộc khi *Lưu***. Lấy từ chứng từ giấy — phần mềm không sinh. Chữ mờ trong ô: *"Nhập khi xác nhận"*. Bấm *Xác nhận* mà trống → tô đỏ ô, câu lỗi *"Chưa có Số phiếu nhập kho."* ngay dưới ô, con trỏ nhảy vào đây. **Chặn**. **Không được trùng** với phiếu khác **của cùng đơn vị trong cùng năm** — năm tính theo *Ngày nhập kho* `[3]`, và chỉ đối chiếu với phiếu ***Đã xác nhận***. Trùng → tô đỏ ô, câu lỗi *"Số phiếu này đã dùng."*, **chặn**. Kiểm ngay lúc bấm *Xác nhận*, không kiểm lúc *Lưu* vì lúc đó ô còn trống |
| 3 | Ngày nhập kho | Date | Ngày | **Bắt buộc khi *Lưu***. Ngày hàng thực nhận. **Mặc định ngày hôm nay**, sửa được. **Không nhận ngày sau hôm nay** — chọn ngày tương lai thì ô tô đỏ, câu lỗi *"Không nhận ngày sau hôm nay."*. **Lùi ngày về quá khứ thì cho**, nhưng **không được trước *Ngày chứng từ* của hợp đồng đã chọn** — hàng không thể về trước khi hợp đồng được ký. Vi phạm thì ô tô đỏ, câu lỗi *"Ngày nhập kho không được trước ngày ký hợp đồng."*. Kiểm lúc *Lưu*, và kiểm lại khi đổi sang hợp đồng khác. Đây là ngày phát sinh của dòng tồn kho, nên phiếu lùi ngày vào tháng đã báo cáo làm báo cáo tháng đó đổi số — `BR-nhap-kho-016` |
| 4 | Kho nhập | Dropdown | Danh mục | **Bắt buộc khi *Lưu***. Chỉ liệt kê kho của **đơn vị người đăng nhập**. Đổi kho sau khi đã quét serial thì serial giữ nguyên, chỉ đổi kho đích |
| 5 | Thủ kho | Dropdown | Danh mục | Không bắt buộc. Người chịu trách nhiệm giữ hàng, chọn trong danh sách người dùng của đơn vị |
| 6 | Loại hợp đồng | Dropdown | Danh mục | **Bắt buộc khi *Lưu***. Hai giá trị: ***Hợp đồng sản xuất*** (mặc định) và ***Hợp đồng thương mại***. Lọc danh sách ở ô chọn hợp đồng `[8]`. Đổi giá trị này thì **xoá giá trị ô `[8]` và làm trắng lưới**. *Hợp đồng thương mại* **chưa làm ở đợt này** |
| 7 | Đơn vị sản xuất | Text (chỉ đọc) | Chuỗi | Bên giao hàng, **ăn theo hợp đồng đã chọn**. Chưa chọn hợp đồng thì để trống |
| 8 | Số hợp đồng | Dropdown | Danh mục | **Bắt buộc khi *Lưu***, là căn cứ của phiếu. Bấm mở bảng chọn `5.3`. Chọn xong phần mềm **đổ đủ danh sách SPMM** của hợp đồng kèm cột *SL còn lại theo HĐ*, và điền *Đơn vị sản xuất* `[7]` cùng *Nguồn kinh phí* `[9]`. Đổi sang hợp đồng khác khi lưới đã có số thì mở `5.4` trước. Một phiếu neo **đúng một** hợp đồng; một hợp đồng nhập được **nhiều** phiếu |
| 9 | Nguồn kinh phí | Text (chỉ đọc) | Chuỗi | **Ăn theo hợp đồng đã chọn**, không sửa được tại đây. Giá trị này **đi theo SPMM suốt vòng đời** kể từ khi nhập kho — `BR-hop-dong-017` |
| 10 | Tổng tiền (VND) | Text (chỉ đọc) | Số tiền | Phần mềm cộng cột *Thành tiền sau thuế* của mọi dòng trong lưới, bằng đúng con số ở hàng *Tổng cộng (VND)* `[27]`. Tính lại ngay mỗi lần sửa *SL nhập kho*. Không nhập tay, không sửa được. **Dòng đang bị ẩn bởi ô tìm kiếm SPMM vẫn cộng vào** — `BR-nhap-kho-014`. Chưa chọn hợp đồng thì lưới rỗng nên ô để trống |
| 11 | Mô tả | Textarea | Chuỗi | Không bắt buộc. Chiếm trọn một hàng, có bộ đếm ký tự dưới ô |
| 12 | Tài liệu đính kèm | Button + badge | Tệp | Mở hộp thoại quản lý tệp. Badge đếm số tệp đang có. Tính năng dùng chung — như bản hiện tại đang làm. **Không phải điều kiện xác nhận** |
| 13 | Ô tìm kiếm SPMM | Input | Chuỗi | Nằm **trong lưới**, ở hàng ngay dưới tiêu đề cột và **đúng cột *SPMM***. Chữ mờ: *"Tìm SPMM"*. Gõ tới đâu lọc dòng tới đó, khớp **cả mã lẫn tên**, không phân biệt hoa thường; xoá hết chữ thì hiện lại đủ dòng. **Không có nút *Tìm*, không có nút *Xoá lọc***. Chỉ đổi cách xem, **không đổi dữ liệu** — `BR-nhap-kho-014` |
| 14 | STT | Text | Số | Số thứ tự dòng, phần mềm đánh |
| 15 | SPMM | Text | Chuỗi | Một cột `Mã - Tên`. **Đóng theo hợp đồng** — phần mềm đổ đủ, không thêm được SPMM ngoài hợp đồng, không xoá được dòng. **Mỗi SPMM đúng một dòng**, không bao giờ có hai dòng cùng một SPMM trên một phiếu — nhờ đó tám chữ số đầu của mã định danh chỉ ra đúng một dòng, là điều kiện để ô quét `[28]` tra ngược được |
| 16 | ĐVT | Text (chỉ đọc) | Danh mục | Đơn vị tính **đi theo SPMM trong danh mục**, phiếu chỉ hiện lại chứ không đặt lại |
| 17 | SL còn lại theo HĐ | Text (chỉ đọc) | Số | *SL đặt hàng* của hợp đồng trừ phần đã nhập ở các phiếu ***Đã xác nhận*** cùng hợp đồng cùng SPMM. **Phiếu còn *Mới* của người khác không trừ vào đây**, nên đây là **trần** của ô `[18]`. **Rê chuột** vào ô hiện bảng tra bốn dòng xếp dọc, nguyên văn: *"SL đặt hàng (theo hợp đồng): `<số>`"* · *"Đã nhập (đã xác nhận): `<số>`"* · *"Đang lập (chưa xác nhận): `<số>`"* · **"Còn lại: `<số>` — tối đa `<số>` nếu phiếu đang lập không được Xác nhận"**. Bảng tra **không liệt kê mã phiếu của người khác**. **Cột này chỉ có trên phiếu còn *Mới*** — phiếu *Đã xác nhận* không có cột này, cũng không có bảng tra (`5.13` `[3]`) |
| 18 | SL nhập kho | Input trong ô bảng | Số | **Ít nhất một dòng phải có số** thì mới lưu được. Số thực nhận theo chứng từ giao hàng. **Phần mềm điền sẵn bằng dòng *Còn lại* của bảng tra `[17]`** — tức đã trừ cả phần đang lập ở phiếu khác, âm thì lấy `0`. Sửa tự do, kể cả sửa lên tới trần *SL còn lại theo HĐ*. Chỉ điền sẵn **một lần lúc nạp lưới theo hợp đồng**; mở lại phiếu đã lưu hoặc nạp lại qua `5.11` thì **giữ nguyên số người dùng đã gõ**, không điền đè. Đợt này không nhận SPMM nào thì gõ `0` cho dòng đó. Phần mềm **không tự cộng ô này theo serial quét được**. Không nhận số âm. **Phải gõ ô này trước rồi mới quét serial được** cho dòng đó — xem `[26]`. **Vượt *SL còn lại theo HĐ* thì CHẶN**: ô tô đỏ, câu lỗi *"Tối đa `<số còn lại>`."* ngay dưới ô. **Hạ xuống thấp hơn số serial đã quét thì CHẶN**: câu lỗi *"Tối thiểu `<số serial đã quét>`."* — muốn hạ thật thì vào hộp thoại serial xoá bớt trước, không để phiếu rơi vào cảnh quét 300 mà khai 250. Đây cũng là con số tính tiền ở `[23]` `[24]` |
| 19 | Số serial đã nhập ⓘ | Text (chỉ đọc) | Số | Phần mềm đếm theo serial đã ghi nhận ở hộp thoại `5.5`, hiện dạng `<đã quét> / <SL nhập kho>`. Biểu tượng ⓘ cạnh nhãn cột ghi *"Số lượng đếm theo serial đã nhập"*. **Luôn hiện đủ hai số bằng chữ thường, kể cả khi lệch** — đây là con số để người lập liếc qua biết còn thiếu bao nhiêu, không phải lỗi. **Chỉ tô đỏ khi bấm *Xác nhận*** mà còn lệch — xem `5.8` `[3]` |
| 20 | Vị trí | Dropdown | Danh mục | Không bắt buộc. Vị trí cất giữ trong *Kho nhập*. Phần mềm điền sẵn **vị trí cất giữ mặc định của SPMM đó trong kho đã chọn**; SPMM chưa khai vị trí mặc định thì **để trống**, không hiện giá trị nào. Sửa lại được |
| 21 | Đơn giá | Text (chỉ đọc) | Số tiền | Lấy nguyên từ hợp đồng, **không sửa tại phiếu**. Đổi bảng giá sau đó không sửa lại phiếu đã lưu |
| 22 | % Thuế | Text (chỉ đọc) | Số | Mức thuế của dòng đó trên hợp đồng, **không sửa tại phiếu** |
| 23 | Thành tiền trước thuế | Text | Số tiền | Phần mềm tính: *SL nhập kho* × *Đơn giá* |
| 24 | Thành tiền sau thuế | Text | Số tiền | Phần mềm tính: *Thành tiền trước thuế* cộng phần thuế theo *% Thuế* **của chính dòng đó** |
| 25 | Ghi chú | Input trong ô bảng | Chuỗi | Ghi chú tự do cho dòng. Không bắt buộc. Đây là chỗ ghi lại lý do khi hàng nhận thiếu so với chứng từ |
| 26 | Thao tác — mở serial | Icon button | — | **Cột ghim ở mép phải lưới**, không trượt khi cuộn ngang. Mở hộp thoại serial `5.5` cho **đúng dòng đó**. **Nút không hiện khi dòng chưa khai *SL nhập kho*** — chưa khai nhận bao nhiêu thì chưa quét được. Khai số xong nút mới hiện ra |
| 27 | Tổng cộng (VND) | Table footer | Số | Hàng chân lưới, cộng dồn theo cột: *SL nhập kho*, *Số serial đã nhập*, *Thành tiền trước thuế*, *Thành tiền sau thuế*. **Chữ *(VND)* chỉ xuất hiện ở đây và ở ô *Tổng tiền (VND)* `[10]`** |
| 28 | Quét/Nhập serial | Input | Chuỗi | **Đường quét nhanh cho cả phiếu, không phải đường bắt buộc** — quét trong hộp thoại của từng dòng (`5.5`, `5.6`) vẫn dùng được y như cũ. Nằm ở hàng công cụ trên lưới. Chữ mờ *"Trỏ chuột vào đây và quét tem…"*. Máy quét bắn xong tự xuống dòng, gõ tay rồi Enter cũng vậy. **Phần mềm tự tìm dòng SPMM theo tám chữ số đầu của mã** (Mục 1.3) rồi ghi vào đúng dòng đó — người dùng không phải chọn dòng. Kiểm lần lượt, sai ở bước nào thì **dừng ở đó, không ghi gì vào lưới**, câu lỗi hiện ngay dưới ô quét và ô vẫn giữ con trỏ để quét tiếp: **đủ 15 chữ số, không ký tự nào khác** → *"Số serial phải là 15 chữ số."* · **tám chữ số đầu khớp một dòng SPMM trên phiếu** → *"Số serial này không thuộc SPMM nào trong phiếu."* · **hai số cuối không lớn hơn năm hiện tại** → *"Năm trong số serial lớn hơn năm hiện tại."* · **dòng khớp đã khai *SL nhập kho*** → *"Chưa khai SL nhập kho cho dòng này."* · **dòng khớp chưa quét đủ** → *"Dòng này đã quét đủ `<SL nhập kho>` serial."* · **chưa trùng serial nào trong phiếu** → *"Số serial này đã có trong phiếu."* · **chưa trùng serial nào trong hệ** → *"Số serial này đã tồn tại trong hệ thống."*. Qua hết thì ghi serial vào dòng đó, *Số serial đã nhập* `[19]` cộng 1, ô quét làm trắng, và phần mềm **kêu một tiếng báo nhận** kèm một dòng báo ngắn ngay dưới ô quét: *"Đã thêm serial cho `<Mã - Tên SPMM>` — `<đã quét>`/`<SL nhập kho>`."*. Dòng SPMM đang hiện trên lưới thì tô sáng trong chốc lát; **đang bị ô tìm kiếm `[13]` lọc mất thì cứ để nguyên bộ lọc, không cuộn, không xoá lọc** — tiếng báo và dòng báo đã đủ cho người quét biết mã rơi vào đâu. Chỉ có trên phiếu còn *Mới* |
| 29 | Hủy | Button | — | Rời màn, bỏ thay đổi chưa lưu. Còn thay đổi chưa lưu thì hỏi lại trước khi rời |
| 30 | Lưu | Button | — | Lần lưu đầu sinh *Mã phiếu* và đưa hồ sơ vào trạng thái *Mới*. Sửa lại được nhiều lần, **giữ nguyên trạng thái *Mới***. Kiểm khi lưu: *Ngày nhập kho* `[3]`, *Kho nhập* `[4]`, *Loại hợp đồng* `[6]`, *Số hợp đồng* `[8]`, ít nhất một dòng có *SL nhập kho* `[18]`, không dòng nào vượt *SL còn lại theo HĐ*, và **không serial nào trùng với serial đã có trong hệ**. **Lưu KHÔNG kiểm số serial: không chặn và cũng không cảnh báo gì** khi số đã quét chưa bằng *SL nhập kho* — phiếu vài trăm cái quét nhiều buổi mới xong, chặn ở đây là mất trắng công đang làm. Thiếu hoặc sai những mục kể trên thì **tô đỏ ngay tại ô**, con trỏ nhảy về ô sai đầu tiên, **chặn** |

### 5.3 Bảng chọn hợp đồng

**Figma:** [NK 04 · Chọn hợp đồng](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1071-38557) · **Bước:** 2 · **Slug:** `chon-hop-dong`

> **Bảng xổ xuống của ô *Số hợp đồng***, không phải hộp thoại chặn — không có nền mờ, không có nút *Hủy* / *Xác nhận*. **Bấm một dòng là chọn xong** và bảng đóng lại, vì chỉ chọn **một** hợp đồng.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Bảng hợp đồng | Table | — | **Hai cột: *Mã hợp đồng* · *Số hợp đồng***. Không có cột *Đơn vị sản xuất* — đã có ô riêng trên biểu mẫu. Không có cột tiến độ và không có cột trạng thái — bảng chỉ liệt kê hợp đồng còn nhập được nên hai cột đó không mang thông tin nào |
| 2 | Hàng lọc | Input | Chuỗi | Hai ô tìm nằm **trong bảng**, ngay dưới tiêu đề cột, chữ mờ *"Tìm mã"* và *"Tìm số"*. Gõ tới đâu lọc tới đó |
| 3 | Một dòng hợp đồng | Row | — | Bấm là chọn xong, bảng đóng, phần mềm nạp lưới SPMM của hợp đồng đó. Danh sách chỉ gồm hợp đồng **của đơn vị người đăng nhập**, trạng thái ***Đã xác nhận***, **chưa *Kết thúc***, đúng *Loại hợp đồng* đang chọn, và **còn ít nhất một SPMM chưa nhập đủ**. Không hợp đồng nào thoả thì bảng rỗng |

### 5.4 Hộp thoại đổi hợp đồng

**Figma:** [NK 05 · Cảnh báo đổi hợp đồng](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1087-43457) · **Bước:** 2 · **Slug:** `doi-hop-dong`

> Mở khi bấm chọn một hợp đồng khác ở `5.3` mà lưới **đã có số hoặc đã có serial**. Lưới còn trắng thì đổi thẳng, không hỏi.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Text | — | *"Đổi hợp đồng"* |
| 2 | Dòng nhận diện | Text | — | *"Hợp đồng `<số cũ>` → `<số mới>`."* |
| 3 | Câu hệ quả | Text | — | *"Sau khi đổi, toàn bộ serial đã quét trên phiếu bị bỏ. Vui lòng xác nhận."* |
| 4 | Hủy bỏ | Button | — | Đóng hộp thoại, **giữ nguyên hợp đồng cũ** và toàn bộ số đã nhập |
| 5 | Đồng ý | Button | — | Nạp lại lưới theo hợp đồng mới. Số đã gõ và serial đã quét **mất hẳn, không khôi phục được**. Nút **nền tối như mọi hộp thoại xác nhận** — không tô đỏ; đỏ chỉ dành cho hộp thoại xoá hẳn bản ghi |

### 5.5 Hộp thoại serial — tab *Nhập / Scan số serial*

**Figma:** [NK 06 · Serial một dòng — tab Nhập/Scan](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1071-39161) · **Bước:** 3 · **Slug:** `serial-dong`

> Mở từ nút ở cột *Thao tác* của **một dòng SPMM** — nút chỉ hiện khi dòng đó đã khai *SL nhập kho*. Serial luôn thuộc về đúng dòng đã mở. Muốn quét một mạch cho cả phiếu thì dùng ô *Quét/Nhập serial* ở `5.2` `[28]` — phần mềm tự đưa mã về đúng dòng, không phải mở từng hộp thoại.
>
> Hộp thoại có **hai tab**: *Nhập/ Scan số serial* (mục này) và *Nhập số Serial theo dải* (`5.6`). Hai tab dùng **chung một bảng serial** bên dưới — thêm bằng đường nào cũng đổ vào cùng một danh sách.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Text | — | *"Cập nhật số serial SPMM"*, có nút đóng ✕ ở góc |
| 2 | Thông tin SPMM | Text (chỉ đọc) | — | Bốn ô: *Mã SPMM* · *Tên SPMM* · *SL nhập kho* · *Số serial đã nhập*. **Không hiện *SL còn lại theo HĐ*** — trần đã kiểm ở lưới |
| 3 | Ô quét / gõ serial | Input | Chuỗi | Chữ mờ: *"Đặt con trỏ vào đây rồi quét"*. Máy quét bắn xong tự xuống dòng, phần mềm **thêm ngay một dòng vào bảng và làm trắng ô** để quét cái tiếp theo. Gõ tay rồi Enter cũng vậy. Ô luôn giữ con trỏ sau mỗi lần thêm. Kiểm khuôn trước khi thêm: **đủ 15 chữ số** → *"Số serial phải là 15 chữ số."* · **tám chữ số đầu đúng SPMM của dòng đang mở** (Mục 1.3) → *"Số serial này không thuộc SPMM của dòng."* · **hai số cuối không lớn hơn năm hiện tại** → *"Năm trong số serial lớn hơn năm hiện tại."*. Sai thì không thêm dòng, câu lỗi hiện đỏ dưới ô quét |
| 4 | Serial trùng trong danh sách | Error | — | Serial vừa quét đã có trong bảng của hộp thoại này → **không thêm dòng**, câu lỗi *"Serial này đã có trong danh sách."* hiện đỏ dưới ô quét, ô vẫn giữ con trỏ để quét tiếp |
| 5 | Serial trùng trong hệ | Error | — | Serial vừa quét đã thuộc một phiếu khác — kể cả phiếu còn *Mới* → **không thêm dòng**, câu lỗi *"Serial này đã tồn tại trong hệ thống."* hiện đỏ dưới ô quét |
| 6 | Vượt số đã khai | Error | — | Đã quét đủ bằng *SL nhập kho* mà còn quét tiếp → **không thêm dòng**, câu lỗi *"Đã quét đủ `<SL nhập kho>` serial."* dưới ô quét. Muốn nhận thêm thì đóng hộp thoại, sửa *SL nhập kho* ở lưới rồi quay lại. **Đây là chỗ duy nhất chặn được ngay lúc quét** — quét thiếu thì chưa phân biệt được là thiếu thật hay chưa quét xong, nên để tới bước *Xác nhận* |
| 7 | Ô tìm serial | Input | Chuỗi | Nằm **trong bảng**, ngay dưới tiêu đề cột *Số serial*, chữ mờ *"Tìm serial"*. Gõ tới đâu lọc tới đó. Chỉ đổi cách xem, không đổi dữ liệu |
| 8 | Bảng serial | Table | — | Ba cột: *STT* · *Số serial* · *Thao tác*. **Cuộn dọc trong hộp thoại, KHÔNG phân trang** |
| 9 | Xoá một serial | Icon button | — | Ở cột *Thao tác* của từng dòng. Bấm là xoá ngay, không hỏi lại — dòng vừa xoá quét lại được ngay |
| 10 | Chân bảng | Text | Số | Ghi tổng số dòng đang có, dạng *"`<N>` serial"* |
| 11 | Hủy | Button | — | Đóng hộp thoại, **bỏ mọi thay đổi trong lần mở này** |
| 12 | Lưu | Button | — | Ghi danh sách serial vào dòng SPMM đó rồi đóng hộp thoại. **KHÔNG đòi quét đủ *SL nhập kho*** — quét dở vẫn đóng được, cột *Số serial đã nhập* ở lưới hiện `<đã quét> / <SL nhập kho>` và tô đỏ để biết còn thiếu. Điều kiện đủ chỉ kiểm ở bước *Xác nhận* |

### 5.6 Hộp thoại serial — tab *Nhập số Serial theo dải*

**Figma:** [NK 07 · Serial một dòng — tab Nhập theo dải](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1088-46070) · **Bước:** 3 · **Slug:** `serial-dong-dai`

> Cùng hộp thoại với `5.5`, đổi tab. Phần trên đổi thành bộ ô sinh dải, **bảng serial và cụm nút bên dưới giữ nguyên**. Dùng khi nhà máy giao một lô đánh số liên tiếp.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Giá trị tiền tố | Text (chỉ đọc) | Chuỗi | **Tám chữ số đầu của khuôn mã định danh** (Mục 1.3), phần mềm tính theo hợp đồng của phiếu và SPMM của dòng đang mở rồi điền sẵn. **Không sửa được** — sửa là dải sinh ra rơi sang SPMM khác |
| 2 | Giá trị hậu tố | Input | Chuỗi | Hai số cuối của **năm sản xuất**. Phần mềm điền sẵn hai số cuối của năm hiện tại, **sửa được** — lô sản xuất năm trước thì gõ đè. Lớn hơn năm hiện tại thì tô đỏ, câu lỗi *"Năm trong số serial lớn hơn năm hiện tại."*, chặn *Tạo dải* |
| 3 | Giá trị từ | Input | Số | Số đầu của dải. Bắt buộc |
| 4 | Giá trị đến | Input | Số | Số cuối của dải. Bắt buộc. Nhỏ hơn *Giá trị từ* thì tô đỏ, câu lỗi *"Giá trị đến phải lớn hơn hoặc bằng Giá trị từ."* |
| 5 | Độ dài dải | Text (chỉ đọc) | Số | **Cố định `5`** — số chữ số của phần số chạy trong khuôn mã định danh, thiếu thì đệm số `0` ở đầu. Không sửa được |
| 6 | Tạo dải | Button | — | Sinh các serial `<tiền tố><số đã đệm 0><hậu tố>` từ *Giá trị từ* tới *Giá trị đến* rồi **đổ vào bảng serial bên dưới**. Ghép đủ ba phần thì mỗi mã ra đúng 15 chữ số. Dải sinh ra vẫn qua đủ ba lần kiểm ở `5.5` `[4]` `[5]` `[6]`: cái nào trùng hoặc vượt số đã khai thì **bỏ qua cái đó**, các cái còn lại vẫn vào bảng, câu lỗi ghi rõ đã bỏ bao nhiêu và vì sao |
| 7 | Bảng serial · cụm nút | — | — | Giống hệt `5.5` `[7]`–`[12]`. Sinh dải xong sửa tay tiếp được: xoá dòng thừa, sang tab kia quét bù |

### 5.7 Xem và sửa phiếu *Mới*

**Figma:** [NK 11 · Xem và sửa phiếu Mới](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1071-37426) · **Bước:** 3–4 · **Slug:** `pnk-sua`

> Cùng bố cục và cùng bộ trường với `5.2`. Khác ba chỗ: có **nhãn trạng thái *Mới*** cạnh tiêu đề màn, hàng tiêu đề trang có thêm nút ***Xác nhận***, và lưới có thêm hàng công cụ với nút ***Xuất phụ lục***.
>
> **Ba nút, đúng thứ tự trái sang phải: *Hủy* · *Lưu* · *Xác nhận*.** Không có *Quay lại*, không có *Xoá* trên màn — xoá làm ở danh sách `5.1`.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Mới*, cạnh tiêu đề màn |
| 2 | Toàn bộ trường và lưới | — | — | Cùng bộ với `5.2` `[1]`–`[28]`, sửa được hết. *Mã phiếu* nay đã có giá trị |
| 3 | Xuất phụ lục | Button | — | Nút của hàng công cụ lưới, đứng cạnh ô *Quét/Nhập serial*. Ra một tệp Excel danh sách SPMM và serial của phiếu. Chỉ hiện sau khi phiếu đã lưu |
| 4 | Hủy | Button | — | Rời màn, bỏ thay đổi chưa lưu |
| 5 | Lưu | Button | — | Như `5.2` `[30]`, giữ nguyên trạng thái *Mới* |
| 6 | Xác nhận | Button | — | **Lưu phần đang sửa trước, rồi mới kiểm điều kiện xác nhận** — `BR-nhap-kho-009`. Hai điều kiện riêng: *Số phiếu nhập kho* `[2]` đã nhập và không trùng, và **mọi dòng có *SL nhập kho* đều đã quét đủ serial**. Đủ thì mở `5.9`; thiếu thì **ở lại màn này**, các ô thiếu tô đỏ tại chỗ — xem `5.8` |

### 5.8 Báo lỗi tại ô *SL nhập kho*

**Figma:** [NK 08 · gõ vượt số còn lại](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1087-44772) · [NK 09 · gõ nhỏ hơn số serial đã quét](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1087-45396) · [NK 10 · chưa quét đủ serial](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1091-47779) · **Slug:** `pnk-loi`

> **Không phải màn riêng** — đây là chính `5.7` khi ô *SL nhập kho* của một dòng không hợp lệ. Ô tô viền đỏ, câu lỗi đỏ hiện **ngay dưới ô đó trong lòng lưới**, dòng cao thêm để chứa câu lỗi. Không có thông báo nổi, không có hộp thoại liệt kê.

| # | Tình huống | Khi nào hiện | Câu lỗi | Chặn gì |
|---|---|---|---|---|
| 1 | Gõ vượt số còn lại theo hợp đồng | Ngay khi rời ô | *"Tối đa `<SL còn lại theo HĐ>`."* | Chặn *Lưu* và *Xác nhận* |
| 2 | Hạ xuống thấp hơn số serial đã quét | Ngay khi rời ô | *"Tối thiểu `<số serial đã quét>`."* | Chặn *Lưu* và *Xác nhận*. Muốn hạ thật thì vào `5.5` xoá bớt serial trước |
| 3 | Chưa quét đủ serial | **Chỉ khi bấm *Xác nhận*** | *"Chưa quét đủ serial."* | **Chặn *Xác nhận*. *Lưu* không chặn và không cảnh báo gì.** Trước lúc bấm *Xác nhận* thì cột *Số serial đã nhập* chỉ hiện `297 / 300` bằng chữ thường; bấm rồi thì cả ô `[18]` lẫn cột đó tô đỏ, và **không mở hộp thoại `5.9`** — chưa qua cửa thì chưa tới bước hỏi lại. Gỡ bằng đúng hai cách: quét bù cho đủ, hoặc hạ *SL nhập kho* xuống bằng số đã quét |
| 4 | Nhiều dòng cùng sai | — | — | **Tô đỏ tất cả cùng lúc**, con trỏ nhảy về dòng sai đầu tiên |

### 5.9 Hộp thoại xác nhận nhập kho

**Figma:** [NK 12 · Hộp thoại xác nhận nhập kho](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1071-39858) · **Bước:** 4 · **Slug:** `xac-nhan-pnk`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Text | — | *"Xác nhận nhập kho"* |
| 2 | Dòng nhận diện | Text | — | *"Số phiếu `<Mã phiếu>` — Số phiếu nhập kho `<Số phiếu nhập kho>`."* |
| 3 | Câu hệ quả | Text | — | *"Sau khi xác nhận, phiếu không sửa và không xoá được nữa. Vui lòng xác nhận."* |
| 4 | Hủy | Button | — | Đóng hộp thoại, phiếu giữ nguyên *Mới* |
| 5 | Xác nhận nhập kho | Button | — | Chuyển phiếu sang *Đã xác nhận*, sinh tồn kho theo từng mã định danh, trừ vào hợp đồng. Đóng hộp thoại và nạp lại màn ở dạng chỉ đọc `5.13` |
| 6 | Trùng phiên | Error | — | Người khác vừa xác nhận phiếu này trước → hộp thoại **đổi thành `5.10` ngay tại chỗ**, không đóng và không mở thêm hộp thoại nào |
| 7 | Hợp đồng vừa đổi | Error | — | Hợp đồng căn cứ vừa bị đổi số → hộp thoại **đổi thành `5.11` ngay tại chỗ** |

### 5.10 Phiếu đã được xác nhận bởi người khác

**Figma:** [NK 13 · Phiếu đã được xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1087-44133) · **Slug:** `xac-nhan-trung`

> **Không phải hộp thoại mới** — là chính `5.9` sau khi phát hiện người khác đã xác nhận trước. Câu hệ quả và cụm nút đổi tại chỗ.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề · dòng nhận diện | Text | — | Giữ nguyên như `5.9` `[1]` `[2]` |
| 2 | Câu thông báo | Text | — | *"Phiếu đã được xác nhận, Vui lòng kiểm tra lại."* Chữ **không tô đỏ** — đây là thông báo kết quả, không phải lỗi nhập liệu |
| 3 | Đóng | Button | — | **Nút duy nhất**, thay cả *Hủy* lẫn *Xác nhận nhập kho*. Đóng xong màn nạp lại ở trạng thái *Đã xác nhận* `5.13` |

### 5.11 Hợp đồng đã thay đổi thông tin

**Figma:** [NK 14 · Hợp đồng đã thay đổi thông tin](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1088-46872) · **Slug:** `hop-dong-doi`

> Cũng là chính `5.9` đổi tại chỗ. Xảy ra khi phiếu mở lâu, trong lúc đó một phiếu khác của cùng hợp đồng được xác nhận làm *SL còn lại theo HĐ* tụt xuống.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề · dòng nhận diện | Text | — | Giữ nguyên như `5.9` `[1]` `[2]` |
| 2 | Câu thông báo | Text | — | *"Hợp đồng `<số hợp đồng>` đã thay đổi thông tin, mở lại phiếu nhập kho để cập nhật."* |
| 3 | Đồng ý | Button | — | **Nút duy nhất.** Đóng hộp thoại và **nạp lại phiếu với số mới**. Dòng nào có *SL nhập kho* lớn hơn *SL còn lại theo HĐ* mới thì **tô đỏ và hiện câu lỗi *"Tối đa `<số còn lại>`."*** ngay dưới ô, đúng cách báo ở `5.8` `[1]`. Phiếu vẫn ở *Mới*, sửa lại rồi xác nhận tiếp |

### 5.12 Hộp thoại xoá phiếu

**Figma:** [NK 15 · Hộp thoại xoá phiếu](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1067-36210) · **Slug:** `xoa-pnk`

> Mở từ icon xoá trên dòng ở `5.1`. Nút chính **nền đỏ** — đây là hộp thoại xoá hẳn bản ghi, loại duy nhất được dùng màu đỏ.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Text | — | *"Xoá phiếu nhập kho"* |
| 2 | Dòng nhận diện | Text | — | *"Số phiếu `<Mã phiếu>`."* |
| 3 | Câu hệ quả | Text | — | *"Sau khi xoá, phiếu không khôi phục được. Vui lòng xác nhận."* |
| 4 | Hủy | Button | — | Đóng hộp thoại, không xoá gì |
| 5 | Xoá phiếu nhập kho | Button | — | Xoá bản ghi và **nhả toàn bộ serial phiếu đó đang giữ chỗ** — phiếu khác quét lại được ngay. Chỉ bấm được khi phiếu còn *Mới* |

### 5.13 Phiếu *Đã xác nhận* — chỉ đọc

**Figma:** [NK 16 · Phiếu Đã xác nhận (chỉ đọc)](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1071-37989) · **Slug:** `pnk-da-xac-nhan`

> Cùng bố cục và cùng bộ trường với `5.7`, mọi ô ở dạng chỉ đọc — **giữ nguyên hình thức của ô gốc**: ô chọn vẫn có mũi tên xổ, ô ngày vẫn có biểu tượng lịch, chỉ khác ở chỗ bấm không mở.
>
> **Hàng tiêu đề trang không có nút nào.** Không *Hủy*, không *Lưu*, không *Xác nhận*, không *Quay lại*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Đã xác nhận*, cạnh tiêu đề màn |
| 2 | Toàn bộ trường của *Thông tin chung* | Text (chỉ đọc) | — | Cùng bộ mười một trường và cùng thứ tự với `5.7`. **Không có dấu `*` bắt buộc** ở nhãn nào — hồ sơ đã chốt thì không còn gì để nhập |
| 3 | Lưới chi tiết | Text (chỉ đọc) | — | Cùng bộ cột với `5.7` nhưng **bỏ cột *SL còn lại theo HĐ*** — trần theo hợp đồng chỉ dùng lúc đang lập, không hiện trên hồ sơ đã chốt. Các ô nhập hiện thành chữ trơn không khung. Cột *Thao tác* vẫn ghim và vẫn mở được hộp thoại serial ở **dạng chỉ xem** — giữ nguyên bảng serial và ô tìm của `5.5`, bỏ ô quét, bỏ nút xoá dòng, bỏ tab *Nhập theo dải*, cụm nút còn một nút *Đóng*. **Không vẽ riêng trên Figma** |
| 4 | Ô tìm kiếm SPMM | Input | Chuỗi | **Vẫn dùng được** — tìm là việc xem, không phải việc sửa |
| 5 | Xuất phụ lục | Button | — | Nút duy nhất của hàng công cụ lưới |

## 6. Yêu cầu chức năng không thuộc màn hình nào

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `FR-nhap-kho-001` | **Phần mềm sinh *Mã phiếu* ở lần *Lưu* đầu tiên**, dạng `PNK/<mã đơn vị>/<năm>/<4 số>`, duy nhất trong toàn hệ, **không đổi và không tái sử dụng** kể cả khi phiếu bị xoá | Lưu một phiếu mới → có mã; xoá nó rồi lưu phiếu khác → mã mới, không trùng mã vừa xoá |
| `FR-nhap-kho-002` | **Mã định danh SPMM là duy nhất trong toàn hệ và bị chiếm ngay từ lúc *Lưu*.** Phần mềm kiểm khi *Lưu*, không đợi tới *Xác nhận* — hai người lập hai phiếu cùng lúc thì người lưu sau bị chặn ngay | Lưu phiếu A với serial `X` ở trạng thái *Mới* → lập phiếu B quét `X`: bị chặn với câu *"Serial này đã tồn tại trong hệ thống."* |
| `FR-nhap-kho-003` | **Xác nhận sinh tồn kho theo từng mã định danh.** Mỗi mã sinh một dòng tồn ở đúng *Kho nhập* và *Vị trí* của dòng SPMM đó, ngày phát sinh là *Ngày nhập kho* của phiếu. Đồng thời trừ vào *SL còn lại theo HĐ* và cập nhật *Tiến độ nhập kho* của hợp đồng — `BR-hop-dong-019` | Xác nhận một phiếu 300 cái → tồn kho tăng đúng 300 mã; mở hợp đồng: *SL còn lại theo HĐ* giảm đúng 300 và *Tiến độ nhập kho* đổi giá trị |
| `FR-nhap-kho-004` | **Xoá phiếu *Mới* thì nhả serial ngay.** Toàn bộ mã định danh phiếu đó đang giữ chỗ trở lại dùng được | Lưu phiếu với serial `X`, xoá phiếu → lập phiếu khác quét `X`: nhận bình thường |
| `FR-nhap-kho-005` | **Phiếu *Mới* không giữ chỗ số lượng của hợp đồng.** *SL còn lại theo HĐ* chỉ trừ phần đã *Xác nhận* — hai người lập hai phiếu *Mới* trên cùng hợp đồng đều thấy trần đầy đủ, ai xác nhận trước thì người sau nhận `5.11` | Lưu phiếu A 300 cái ở *Mới* → mở phiếu B cùng hợp đồng: *SL còn lại theo HĐ* chưa giảm. Xác nhận A rồi xác nhận B → B nhận `5.11` |

## 7. Quy tắc nghiệp vụ

Chỉ những quy tắc **xuyên nhiều màn** hoặc **không thuộc màn nào**. Luật của từng ô nằm trong bảng mô tả màn ở Mục 5.

| ID | Quy tắc | Áp ở |
|---|---|---|
| `BR-nhap-kho-001` | **Một phiếu neo đúng MỘT hợp đồng *Đã xác nhận*.** Điều kiện **chưa *Kết thúc*** chỉ kiểm **lúc chọn hợp đồng** ở `5.3` — hợp đồng kết thúc sau đó thì phiếu đã lập vẫn *Lưu*, *Xác nhận*, *Xoá* bình thường, không chặn và không cảnh báo (`BR-hop-dong-020`). Một hợp đồng nhập được **nhiều** phiếu, rải theo đợt giao hàng | `5.2` `[8]`, `5.3` |
| `BR-nhap-kho-002` | **Danh sách SPMM đóng theo hợp đồng.** Phần mềm đổ đủ SPMM của hợp đồng đã chọn; **không thêm được SPMM ngoài hợp đồng, không xoá được dòng**. SPMM không nhận đợt này thì để **trống** *SL nhập kho* | `5.2` `[15]` `[18]` |
| `BR-nhap-kho-003` | ***SL còn lại theo HĐ* chỉ trừ phần đã *Xác nhận*.** Phiếu còn *Mới* của người khác **không hạ trần** — chưa xác nhận thì hàng chưa vào kho, chưa vào kho thì chưa chiếm số của hợp đồng. Nhưng phần đang lập đó **vẫn hiện ở bảng tra khi rê chuột** `5.2` `[17]` để người lập biết mà hỏi lại, và **là con số phần mềm điền sẵn** vào `[18]`. Cùng khuôn `BR-hop-dong-003` | `5.2` `[17]` `[18]`, `FR-nhap-kho-005` |
| `BR-nhap-kho-004` | **Vượt *SL còn lại theo HĐ* thì CHẶN.** Phần mềm không cho *Lưu* dòng có *SL nhập kho* lớn hơn số còn lại; ô tô đỏ, câu lỗi *"Tối đa `<số còn lại>`."*. Nhận thừa so với hợp đồng phải xử lý bằng phụ lục hợp đồng, không phải bằng phiếu nhập kho | `5.2` `[18]`, `5.8` `[1]` |
| `BR-nhap-kho-005` | ***SL nhập kho* và *Số serial đã nhập* phải BẰNG NHAU thì mới xác nhận được.** Lệch thì **chặn *Xác nhận***, gỡ bằng một trong hai cách: **quét bù cho đủ**, hoặc **hạ *SL nhập kho* xuống bằng số đã quét**. Không có đường thứ ba và **không có ô ghi lý do chênh lệch** — nhận thiếu thì phiếu ghi đúng số thật nhận, phần còn nợ nằm ở đợt giao sau. *Ghi chú* của dòng dùng để ghi lại lý do nếu cần | `5.2` `[18]` `[19]`, `5.7` `[6]`, `5.8` `[3]` |
| `BR-nhap-kho-006` | **Ba mốc kiểm số serial, mỗi mốc một cách xử.** **Lúc quét:** vượt *SL nhập kho* thì chặn ngay, không thêm được dòng. **Lúc *Lưu*:** không chặn và **không cảnh báo gì** — quét dở vẫn lưu về, hộp thoại serial cũng đóng được khi quét dở. **Lúc *Xác nhận*:** lệch thì chặn, tô đỏ tại dòng. Quét thiếu không chặn sớm được vì chưa phân biệt được thiếu thật với chưa quét xong | `5.2` `[30]`, `5.5` `[6]` `[12]`, `5.7` `[6]`, `5.8` |
| `BR-nhap-kho-007` | **Mã định danh là duy nhất toàn hệ, kiểm ngay lúc *Lưu*.** Serial trùng bị chặn ở ba lớp: trùng trong chính hộp thoại đang mở, trùng với dòng khác của cùng phiếu, trùng với phiếu khác kể cả phiếu còn *Mới* | `5.5` `[4]` `[5]`, `FR-nhap-kho-002` |
| `BR-nhap-kho-008` | **Khai số trước, quét sau — và serial luôn thuộc về đúng một dòng SPMM.** Nút mở hộp thoại serial của một dòng **chỉ hiện khi dòng đó đã khai *SL nhập kho***, nên không quét được vào dòng chưa khai số. **Ô quét chung `5.2` `[28]` không phá luật này** — nó tự tìm dòng theo tám chữ số đầu của mã, dòng chưa khai *SL nhập kho* thì báo lỗi và không ghi gì. Phần mềm **không tự cộng *SL nhập kho* theo serial quét được** — số đó là số khai theo chứng từ, *Số serial đã nhập* là số đếm thật, hai số giữ độc lập để phép đối chiếu ở `BR-nhap-kho-005` còn nghĩa | `5.2` `[18]` `[26]`, `5.5`, `5.6` |
| `BR-nhap-kho-009` | ***Xác nhận* thực hiện *Lưu* trước.** Bấm *Xác nhận* khi đang sửa dở thì phần vừa sửa được lưu trước, không xác nhận bản cũ. Lưu không qua được thì **không kiểm tiếp** điều kiện xác nhận. Cùng khuôn `BR-hop-dong-018` | `5.7` `[6]` |
| `BR-nhap-kho-010` | ***Đã xác nhận* khoá hẳn.** Không sửa, không xoá, **không huỷ xác nhận**. Hàng đã vào tồn kho và đã trừ vào hợp đồng. Nhập sai xử lý bằng nghiệp vụ điều chỉnh kho, ngoài phạm vi đợt này | Mục 4, `5.13` |
| `BR-nhap-kho-011` | **Hai người xác nhận cùng một phiếu thì ai bấm trước được.** Người bấm sau nhận `5.10` **ngay trong hộp thoại đang mở**, nút chính đổi thành *Đóng*; đóng xong màn nạp lại ở trạng thái *Đã xác nhận*. **Không đẻ thêm hộp thoại, không dùng thông báo nổi** | `5.9` `[6]`, `5.10` |
| `BR-nhap-kho-012` | **Hợp đồng đổi số trong lúc phiếu đang mở thì báo và nạp lại, không tự sửa số của người dùng.** Người dùng nhận `5.11`, bấm *Đồng ý* thì phiếu nạp lại với trần mới và dòng nào vượt bị tô đỏ. Phần mềm **không tự hạ *SL nhập kho*** — số đó là số thật nhận theo chứng từ, chỉ người lập mới sửa được | `5.9` `[7]`, `5.11` |
| `BR-nhap-kho-013` | **Một cách báo thiếu điều kiện duy nhất: tô đỏ tại trường.** Câu lỗi nằm ngay dưới ô, con trỏ nhảy về ô sai đầu tiên, sai bao nhiêu ô thì tô đỏ bấy nhiêu **cùng lúc**. **Không có thông báo nổi và không có hộp thoại nào chỉ để liệt kê mục còn thiếu** — hộp thoại chỉ dùng cho **xác nhận hành động** | `5.2` `[30]`, `5.7` `[6]`, `5.8` |
| `BR-nhap-kho-014` | **Ô tìm kiếm SPMM chỉ đổi CÁCH XEM, không đổi DỮ LIỆU.** Dòng đang bị ẩn vẫn giữ nguyên số đã gõ và serial đã quét, vẫn **cộng vào *Tổng tiền (VND)* và *Tổng cộng (VND)***, vẫn **lên phụ lục**, và vẫn **bị kiểm khi *Lưu* / *Xác nhận*** — sai ở một dòng đang bị ẩn thì phần mềm **xoá chữ đang gõ trong ô tìm kiếm** để dòng đó hiện lại rồi mới tô đỏ. Bảng đóng theo hợp đồng nên tìm kiếm **không thêm bớt dòng nào** | `5.2` `[13]`, `5.7`, `5.13` `[4]` |
| `BR-nhap-kho-015` | ***Vị trí* không bắt buộc, lấy theo vị trí cất giữ mặc định.** Phần mềm điền sẵn vị trí mặc định của SPMM đó trong *Kho nhập* đã chọn; SPMM chưa khai vị trí mặc định thì **để trống**, không hiện giá trị nào và không chặn gì. Sửa lại được trước khi xác nhận | `5.2` `[20]` |
| `BR-nhap-kho-016` | ***Ngày nhập kho* nằm giữa ngày ký hợp đồng và hôm nay.** Chặn ngày sau hôm nay, chặn ngày trước *Ngày chứng từ* của hợp đồng đã chọn; trong khoảng đó thì lùi bao xa cũng được. **Không có khoá kỳ.** Đây là ngày phát sinh của dòng tồn kho nên phiếu lùi ngày vào tháng đã báo cáo **làm báo cáo tháng đó đổi số** | `5.2` `[3]` |
| `BR-nhap-kho-017` | **Tiền theo *SL nhập kho*, không theo số serial.** *Thành tiền trước thuế* = *SL nhập kho* × *Đơn giá*. *Đơn giá* và *% Thuế* lấy nguyên từ hợp đồng, **không sửa tại phiếu**. Hai số phải bằng nhau khi xác nhận nên tiền không lệch với số cái thật nhận. ***Tổng tiền (VND)*** ở *Thông tin chung* = tổng cột *Thành tiền sau thuế* của mọi dòng | `5.2` `[10]` `[21]`–`[24]` |
| `BR-nhap-kho-018` | ***Nguồn kinh phí* ăn theo hợp đồng và đi theo SPMM suốt vòng đời** kể từ khi nhập kho. Ô chỉ đọc trên phiếu, không chọn lại được — `BR-hop-dong-017` | `5.2` `[9]` |
| `BR-nhap-kho-019` | **Phạm vi dữ liệu cắt theo đơn vị của người đăng nhập.** Mỗi đơn vị chỉ thấy phiếu, hợp đồng và kho của chính mình. **Một hợp đồng chỉ có một bên nhập kho** — ký với nhà máy nào thì nhà máy đó nhập | Mục 3, `5.1`, `5.2` `[4]`, `5.3` `[3]` |
| `BR-nhap-kho-020` | **Đổi *Số hợp đồng* khi lưới đã có số hoặc đã có serial thì phải qua hộp thoại `5.4`.** Đồng ý đổi thì toàn bộ danh sách SPMM, số đã gõ và serial đã quét **bị xoá và nạp lại** theo hợp đồng mới, không khôi phục được. Lưới còn trắng thì đổi thẳng, không hỏi. Đổi *Loại hợp đồng* cũng làm trắng lưới theo cách này | `5.2` `[6]` `[8]`, `5.4` |
| `BR-nhap-kho-021` | **Mã định danh SPMM phải đúng khuôn 15 chữ số.** Sáu phần ghép liền theo Mục 1.3; **tám chữ số đầu ràng mã vào đúng một cặp (hợp đồng, SPMM)**, năm chữ số giữa do nhà máy đánh, hai số cuối là năm sản xuất và **không được lớn hơn năm hiện tại**. Mã sai khuôn thì **không vào được phiếu**, dù nhập bằng đường nào — ô quét chung, ô quét trong hộp thoại, hay sinh theo dải | Mục 1.3, `5.2` `[28]`, `5.5` `[3]`, `5.6` |
| `BR-nhap-kho-022` | **Ô quét chung tự đưa mã về đúng dòng SPMM, không hỏi người dùng.** Phần mềm so tám chữ số đầu của mã vừa quét với tám chữ số đầu tính được cho từng dòng trên phiếu. Không dòng nào khớp thì **báo lỗi và không ghi gì** — không cho người dùng tự chọn dòng, vì chọn tay là mở đường cho serial rơi sai SPMM. Đây là **đường tuỳ chọn**: quét trong hộp thoại của từng dòng vẫn giữ nguyên | `5.2` `[28]`, `5.5`, `5.6` |

## 8. Yêu cầu phi chức năng

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `NFR-nhap-kho-001` | **Xác nhận là mốc đóng băng số liệu.** Phiếu *Đã xác nhận* giữ nguyên vĩnh viễn *SL nhập kho*, *Đơn giá*, *% Thuế*, *Thành tiền*, danh sách serial và *Tổng cộng*. Đổi bảng giá, sửa hợp đồng hay đổi bất kỳ danh mục nào sau đó **không làm đổi phiếu cũ** | Xác nhận một phiếu, rồi đổi giá SPMM trong bảng giá → mở lại phiếu: mọi con số giữ nguyên |
| `NFR-nhap-kho-002` | **Quét serial phải chạy được liên tục bằng máy quét mã vạch.** Sau mỗi lần bắn, ô quét tự trắng và tự giữ con trỏ; người dùng **không phải chạm chuột giữa hai lần quét**. Quét trúng serial trùng cũng vậy — hiện lỗi nhưng ô vẫn sẵn sàng cho cái tiếp theo | Bắn liên tiếp 20 mã bằng máy quét, không chạm chuột → bảng có đủ 20 dòng |

## 9. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|:--:|---|---|
| 1 | **Số cái thật nhận và số serial ghi được luôn khớp nhau ở mọi phiếu đã xác nhận** | Gõ *SL nhập kho* 300, quét 297 rồi bấm *Xác nhận* → bị chặn, câu lỗi *"Chưa quét đủ serial."*. Hạ xuống 297 → xác nhận được |
| 2 | **Không phiếu nào nhập vượt số đã đặt của hợp đồng** | Gõ *SL nhập kho* lớn hơn *SL còn lại theo HĐ* rồi *Lưu* → ô tô đỏ, chặn |
| 3 | **Không mã định danh nào vào kho hai lần** | Lưu phiếu A với serial `X` (còn *Mới*) → phiếu B quét `X`: bị chặn ngay lúc quét |
| 4 | **Người lập theo dõi được còn phải nhận bao nhiêu mà không phải tra hợp đồng giấy** | Xác nhận phiếu 300 cái → lập phiếu mới cùng hợp đồng: *SL còn lại theo HĐ* của SPMM đó đã giảm đúng 300 |
| 5 | **Quét cả trăm cái bằng máy quét không phải chạm chuột lần nào** | Mở hộp thoại serial, bắn liên tiếp → mỗi lần bắn thêm đúng một dòng, ô quét luôn sẵn sàng |
| 6 | **Bỏ dở phiếu không khoá mất serial của người khác** | Lưu phiếu *Mới* rồi xoá đi → phiếu khác quét lại đúng những serial đó: nhận bình thường |

## 10. Chưa làm ở đợt này

- ***Hợp đồng thương mại*.** Đợt này chỉ nhập theo *Hợp đồng sản xuất* với nhà máy thuộc Ban. **Ai cấp mã định danh 15 số cho hàng mua của nhà cung cấp ngoài, và cấp lúc nào** — chưa chốt, đi cùng loại hợp đồng này.
- **Huỷ xác nhận và điều chỉnh phiếu đã xác nhận.** Nhập sai hiện phải xử lý ngoài phần mềm.
- **Khoá kỳ kho.** Phần mềm chưa có khái niệm chốt sổ theo kỳ, nên phiếu lùi ngày làm đổi số của báo cáo kỳ đã qua mà không cảnh báo ai — `BR-nhap-kho-016`.
- **Đơn vị tính *Hệ thống*.** Một *Hệ thống* gồm nhiều thiết bị thì đếm và đánh mã định danh thế nào — vấn đề ở tầng danh mục SPMM, chưa chốt, chờ Cục QLKTNVMM.
- ***Serial vật lý* của linh kiện.** Phiếu nhập kho chỉ ghi mã định danh 15 số — Mục 1.3.
- **Nhà máy có phần mềm kho riêng đẩy dữ liệu sang QLSPMM.** Đợt này chỉ có đường nhập tay và quét trực tiếp trên phần mềm. Đường nhận dữ liệu từ hệ thống nhà máy — kèm việc phiếu tự sinh ở trạng thái chờ xác nhận và không sửa được trên QLSPMM — chưa đặc tả.
- **Nhập kho không theo hợp đồng** (hàng biếu tặng, hàng thu hồi tái nhập).

## 📝 Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|---|---|---|---|---|
| 2026-09-03 | thêm mới | 16 khung Figma khu vực 6 file BCY(2) · `docs/cuc-ql/srs/srs-hop-dong.md` | @quynhdtn17 | Bản đầu tiên. Mục 5 gồm 13 màn, 5 yêu cầu chức năng ngoài màn, 20 quy tắc nghiệp vụ, 2 yêu cầu phi chức năng. Chốt mô hình ba cột số lượng: *SL còn lại theo HĐ* chỉ trừ phiếu đã xác nhận, *SL nhập kho* người dùng gõ, *Số serial đã nhập* phần mềm đếm — hai số sau **phải bằng nhau thì mới xác nhận được**, không có ô ghi lý do chênh lệch. Serial chỉ quét trong hộp thoại của từng dòng, và **phải khai *SL nhập kho* trước** thì nút mở hộp thoại mới hiện — giữ đúng cách bản đang chạy làm. Hàng công cụ lưới vì thế chỉ còn *Xuất phụ lục*. Ba mốc kiểm số serial: quét vượt thì chặn ngay, *Lưu* không chặn và không cảnh báo, *Xác nhận* lệch thì chặn và tô đỏ tại dòng. Phạm vi dữ liệu cắt theo đơn vị đăng nhập, một hợp đồng một bên nhập. *Vị trí* không bắt buộc, lấy theo vị trí cất giữ mặc định. *Ngày nhập kho* chặn ngày sau hôm nay, cho lùi ngày tự do, chưa có khoá kỳ. Ô *SL còn lại theo HĐ* bỏ ⓘ tiêu đề cột, thay bằng **bảng tra bốn dòng khi rê chuột** theo khuôn `BR-hop-dong-003` — có dòng *Đang lập (chưa xác nhận)* để thấy phần người khác đang giữ. *SL nhập kho* **điền sẵn bằng dòng *Còn lại***, sửa được lên tới trần. Hợp đồng *Kết thúc* không chặn phiếu đang dở: phiếu *Mới* vẫn xác nhận hoặc xoá bình thường, chỉ không lập thêm phiếu mới. *Số phiếu nhập kho* kiểm trùng trong cùng đơn vị cùng năm khi *Xác nhận*. *Ngày nhập kho* chặn thêm ngày trước *Ngày chứng từ* của hợp đồng. Lưới của phiếu *Đã xác nhận* **bỏ hẳn cột *SL còn lại theo HĐ*** cùng bảng tra. Chốt **khuôn mã định danh 15 chữ số** (Mục 1.3) và thêm **ô *Quét/Nhập serial* chung cho cả phiếu** ở hàng công cụ lưới, tự đưa mã về đúng dòng SPMM theo tám chữ số đầu; tab *Nhập theo dải* khoá *Tiền tố* và *Độ dài*, giữ *Hậu tố* sửa được cho lô sản xuất năm trước. |
| 2026-09-04 | cập nhật | Bản đang chạy — màn `good-receipt` có ô *Tổng tiền (VND)* trong *Thông tin chung* | @quynhdtn17 | Thêm ô *Tổng tiền (VND)* chỉ đọc vào *Thông tin chung* (`5.2` `[10]`), bằng tổng cột *Thành tiền sau thuế*. Dồn lại số thứ tự các dòng sau nó trong bảng Mục 5.2 và mọi chỗ tham chiếu. |
