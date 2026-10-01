---
type: srs
feature: bao-cao-ton-kho-serial
status: draft
updated: 2026-09-04
---

# Báo cáo tồn kho theo Serial

## 1. Phạm vi

**Trong phạm vi:**

- Màn hình **"Báo cáo tồn kho theo serial"** (menu riêng), cho người dùng được phân quyền tra cứu tồn kho tới từng serial cụ thể tại 1 ngày bất kỳ (mặc định là ngày hiện tại).
- Lọc kết quả theo Serial, Mã SPMM, Vị trí lưu kho, Đơn vị, Kho.
- Xuất kết quả đang xem ra file Excel.

**Ngoài phạm vi:**

| Việc | Ở đâu |
|---|---|
| Xem lịch sử di chuyển chi tiết (toàn bộ các lần nhập/chuyển/xuất trước đó) của 1 serial | Chưa xây dựng — ghi nhận là nhu cầu riêng, sẽ đặc tả thành báo cáo/màn hình khác khi cần |
| Nghiệp vụ nhập kho, điều chuyển, xuất kho (nguồn phát sinh các giao dịch mà báo cáo này đọc) | Các chức năng nhập kho/điều chuyển tương ứng |
| Quản lý danh mục SPMM, Đơn vị, Kho, Vị trí kho | Danh mục tương ứng (ngoài phạm vi) |

## 2. Actors

| Actor | Loại (người/hệ thống/ngoài) | Mục tiêu | Trong scope? |
|-------|------------------------------|----------|---------------|
| Người dùng được phân quyền xem báo cáo | người | Tra cứu vị trí/đơn vị đang giữ của serial cụ thể tại 1 thời điểm | Có |
| Hệ thống | hệ thống | Tính tồn kho từ số dư chốt kỳ + lịch sử giao dịch, áp bộ lọc/phân quyền, xuất Excel | Có |

## 3. Quy trình nghiệp vụ

1. Người dùng được phân quyền truy cập màn hình "Báo cáo tồn kho theo serial".
2. Người dùng **bắt buộc chọn Kho và nhập Ngày báo cáo** trước khi xem kết quả — danh sách kho giới hạn theo phạm vi đơn vị được phân quyền của người xem báo cáo; chưa đủ 2 điều kiện này thì màn hình chưa hiển thị danh sách nào.
3. Sau khi đủ 2 điều kiện bắt buộc, hệ thống hiển thị danh sách serial đang tồn trong Kho đó tại Ngày báo cáo đã chọn, giới hạn theo đơn vị người dùng được phân quyền, đã loại bỏ serial đã xuất kho và serial chưa xác định đơn vị.
4. Người dùng có thể đổi Ngày báo cáo sang 1 ngày khác trong quá khứ, hoặc áp thêm các bộ lọc khác (Serial/Mã SPMM/Vị trí lưu kho/Đơn vị) để thu hẹp kết quả. **Mỗi khi giá trị của bất kỳ bộ lọc nào thay đổi (kể cả Kho, Ngày báo cáo), hệ thống tự động tải lại danh sách kết quả theo điều kiện mới — không cần thao tác xác nhận/bấm nút riêng.**
5. Người dùng bấm "Xuất Excel" để xuất đúng danh sách đang hiển thị.

**Cách tính tồn kho tại 1 ngày (áp dụng cho mọi serial):**

```
Tồn (đến ngày X) = Số dư serial đã chốt của kỳ chứa "Đến ngày X"
                    ĐIỀU CHỈNH theo phát sinh (nhập/chuyển/xuất) từ đầu kỳ đó đến ngày X
```

**6 bước tính:**

1. Xác định kỳ (tháng) chứa "Đến ngày X" — cắt về ngày 01 của chính tháng đó, giống quy ước kỳ đang dùng chung cho báo cáo tồn kho theo mã sản phẩm.
2. Lấy **số dư serial đã chốt** của kỳ đó — danh sách serial kèm vị trí/kho/đơn vị tại thời điểm đóng kỳ (nguồn dùng chung, ngoài phạm vi tài liệu này — xem giả định dưới).
3. Lấy các giao dịch nhập/chuyển/xuất của serial phát sinh trong khoảng từ đầu kỳ đó đến "Đến ngày X".
4. Với mỗi serial có phát sinh, chỉ giữ lại đúng 1 giao dịch **mới nhất** trong khoảng đó.
5. Ghép 2 nguồn theo serial: serial có phát sinh trong kỳ → vị trí lấy theo giao dịch mới nhất (ghi đè số dư đầu kỳ); serial không phát sinh gì → giữ nguyên vị trí ở số dư đầu kỳ; serial mới (chỉ xuất hiện qua phát sinh trong kỳ) → vẫn tính theo giao dịch mới nhất.
6. Loại serial mà vị trí xác định được là từ giao dịch xuất kho (`FR-bao-cao-ton-kho-serial-002`); loại serial không xác định được đơn vị (`FR-bao-cao-ton-kho-serial-003`); ghép Mã/Tên SPMM + tên đơn vị; áp phân quyền theo đơn vị + bộ lọc người dùng chọn; trả kết quả.

> **Giả định phụ thuộc (chưa xác nhận hạ tầng):** bước 2 cần 1 nguồn "số dư serial đã chốt theo kỳ" — đây là năng lực **dùng chung cho mọi báo cáo tồn kho** (không đặc tả cách chốt trong tài liệu này). Nếu tại thời điểm triển khai nguồn này **chưa có sẵn cho serial**, bắt buộc fallback: coi như chưa có kỳ nào được chốt, cộng dồn lũy kế toàn bộ lịch sử giao dịch của serial đến ngày X (không được để trống dữ liệu).

> **Ghi chú kỹ thuật (tham khảo, không bắt buộc — đã khảo sát trực tiếp trên DB 2026-09-04, dev tự xác nhận lại khi thiết kế thật):**
> - **Nguồn danh sách Serial:** `warehouse.item_serial` — dùng làm nguồn gốc để đảm bảo không bỏ sót Serial.
> - **Lịch sử giao dịch:** `warehouse.item_serial_transaction` — nên join bằng `serial_number`, không phụ thuộc `serial_id` do dữ liệu NULL nhiều.
> - **Xác định vị trí hiện tại:** dựa vào giao dịch gần nhất và `reference_id` để tra phiếu nhập/chuyển tương ứng.
> - **Thông tin SPMM/đơn vị:** lấy từ `product_management.san_pham` và `product_management.dm_don_vi`.
> - **Không dùng `owning_department_id`:** dữ liệu hiện tại chưa được cập nhật nhất quán, không đủ tin cậy để xác định đơn vị đang giữ Serial.
> - **Số dư đầu kỳ:** hiện chưa xác định được bảng chốt kỳ dành cho Serial, cần Dev/Architect xác nhận hoặc thiết kế bổ sung (xem câu hỏi mở Mục 9).
> - **Nếu xây mới cơ chế chốt kỳ:** nên dùng mô hình snapshot, mỗi kỳ lưu 1 dòng/Serial thể hiện trạng thái tại thời điểm chốt (kho, vị trí, đơn vị), thay vì lưu từng phát sinh để cộng số lượng như báo cáo tồn theo mã sản phẩm.
>
> **Nguyên tắc kỹ thuật cốt lõi:** Lấy `item_serial` làm danh sách gốc → lấy snapshot kỳ gần nhất (nếu có) → áp dụng các giao dịch phát sinh sau kỳ chốt → giao dịch mới nhất quyết định trạng thái của Serial tại ngày xem.

## 4. Phân quyền

| Vai trò | Phạm vi dữ liệu | Hành động được phép | Hành động bị chặn |
|---------|--------------------|------------------------|----------------------|
| Người dùng được phân quyền xem báo cáo | Serial thuộc đơn vị mình được phân công quản lý — áp dụng cho mọi ngày xem (hiện tại lẫn quá khứ), không có ngoại lệ theo thời gian | Xem danh sách, đổi ngày xem, lọc, xuất Excel | Mọi hành động ghi/sửa dữ liệu tồn kho — báo cáo hoàn toàn read-only |

## 5. Màn hình

### 5.1 Báo cáo tồn kho theo serial — `bao-cao-ton-kho-serial`

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 1 | Ngày báo cáo | Date picker | Date | **Bắt buộc nhập** — không có giá trị mặc định, người dùng phải tự chọn trước khi xem kết quả. Không được chọn ngày lớn hơn ngày hiện tại; chọn ngày tương lai → báo lỗi tại field, chặn xem: "Không thể chọn ngày trong tương lai." (E-bao-cao-ton-kho-serial-001). Chưa nhập → không hiển thị danh sách nào, báo lỗi tại field: "Vui lòng chọn ngày báo cáo." Thay đổi giá trị → hệ thống tự động tải lại danh sách theo `FR-bao-cao-ton-kho-serial-001`/`FR-bao-cao-ton-kho-serial-006`. |
| 2 | Lọc Serial | Textbox (tìm kiếm) | Text | Không bắt buộc. Tìm theo kiểu **chứa chuỗi** (gần đúng) — gõ 1 phần serial vẫn ra kết quả khớp chứa chuỗi đó ở bất kỳ vị trí nào trong serial. |
| 3 | Lọc Mã SPMM | Dropdown (search)/Select | Text | Không bắt buộc. Lọc theo đúng 1 Mã SPMM được chọn. |
| 4 | Lọc Vị trí lưu kho | Dropdown (search)/Select | Text | Không bắt buộc. Danh sách vị trí giới hạn theo Kho đã chọn và theo phạm vi đơn vị được phân quyền (`BR-bao-cao-ton-kho-serial-001`). |
| 5 | Lọc Đơn vị | Dropdown (search)/Select | Text | Không bắt buộc. Danh sách đơn vị hiển thị **chỉ gồm đơn vị trong phạm vi được phân quyền** của người dùng đang đăng nhập — không hiển thị đơn vị ngoài phạm vi (`BR-bao-cao-ton-kho-serial-001`). |
| 6 | Lọc Kho | Dropdown (search)/Select | Text | **Bắt buộc chọn** — không có giá trị mặc định, người dùng phải tự chọn trước khi xem kết quả. Danh sách kho tự động giới hạn theo phạm vi đơn vị được phân quyền của người xem báo cáo (`BR-bao-cao-ton-kho-serial-001`). Chưa chọn → không hiển thị danh sách nào, báo lỗi tại field: "Vui lòng chọn Kho." |
| 7 | [Kết quả] Serial | Label | Text | Số serial cụ thể — cột định danh chính của mỗi dòng kết quả. |
| 8 | [Kết quả] Mã SPMM | Label | Text | Mã sản phẩm mật mã mà serial thuộc về. |
| 9 | [Kết quả] Tên SPMM | Label | Text | Tên đầy đủ của sản phẩm, tra theo Mã SPMM. |
| 10 | [Kết quả] ĐVT | Label | Text | Đơn vị tính của SPMM (vd Cái/Bộ/License). |
| 11 | [Kết quả] Vị trí lưu kho | Label | Text | Vị trí cụ thể trong kho tại ngày xem, xác định theo công thức Mục 3 (`FR-bao-cao-ton-kho-serial-001`, `BR-bao-cao-ton-kho-serial-002`). |
| 12 | [Kết quả] Kho | Label | Text | Kho chứa serial tại ngày xem. |
| 13 | [Kết quả] Đơn vị | Label | Text | Đơn vị đang giữ serial tại ngày xem. Serial không xác định được đơn vị **không xuất hiện** trong danh sách — không hiển thị dòng với ô này để trống (`FR-bao-cao-ton-kho-serial-003`). |
| 14 | Nút "Xuất Excel" | Button | — | Xuất đúng danh sách đang hiển thị trên màn hình tại thời điểm bấm (đã áp ngày xem + mọi bộ lọc đang chọn), theo `FR-bao-cao-ton-kho-serial-005`. Thành công → thông báo "Xuất báo cáo thành công." |
| 15 | [Thông báo trống] | Info banner | — | Khi không có serial nào khớp toàn bộ điều kiện (ngày xem + bộ lọc): "Không tìm thấy serial nào tồn kho phù hợp với điều kiện lọc." |

## 6. Yêu cầu chức năng không thuộc màn hình nào

| ID | Yêu cầu | Cách kiểm |
|----|---------|-----------|
| FR-bao-cao-ton-kho-serial-001 | Khi người dùng xem báo cáo tại 1 ngày, hệ thống phải tính vị trí của mỗi serial bằng cách lấy số dư serial đã chốt của kỳ chứa ngày đó, rồi điều chỉnh theo giao dịch nhập/chuyển/xuất mới nhất phát sinh từ đầu kỳ đó đến ngày xem (xem công thức Mục 3). Nếu chưa từng có kỳ nào được chốt trước ngày xem, hệ thống phải cộng dồn lũy kế toàn bộ lịch sử giao dịch của serial đến ngày đó. | Nhánh fallback (chưa có kỳ chốt): chọn 1 serial mẫu có lịch sử giao dịch đã biết, đối chiếu kết quả với tổng hợp thủ công từ toàn bộ lịch sử. Nhánh có kỳ chốt: đối chiếu tương tự nhưng **chỉ áp dụng được sau khi nguồn "số dư đã chốt" (Mục 9) đã sẵn sàng** — hiện chưa test được nhánh này. |
| FR-bao-cao-ton-kho-serial-002 | Nếu giao dịch **phát sinh trong kỳ** xác định vị trí của 1 serial tại ngày xem là giao dịch xuất kho, thì hệ thống phải loại serial đó khỏi kết quả "đang tồn". Với serial không phát sinh gì trong kỳ (lấy nguyên số dư đầu kỳ theo `BR-bao-cao-ton-kho-serial-002`), hệ thống mặc định coi là còn tồn — nguồn số dư đã chốt phải tự đảm bảo không chứa serial đã xuất kho (loại ngay từ lúc chốt kỳ), báo cáo không kiểm tra lại. | Chọn 1 serial có giao dịch xuất kho là giao dịch mới nhất tính đến ngày xem, xác nhận serial không xuất hiện trong kết quả. |
| FR-bao-cao-ton-kho-serial-003 | Nếu 1 serial không xác định được đơn vị đang giữ tại ngày xem, thì hệ thống phải loại serial đó khỏi kết quả. | Chọn 1 serial chưa xác định đơn vị đang giữ tại ngày xem, xác nhận serial không xuất hiện trong kết quả. |
| FR-bao-cao-ton-kho-serial-004 | Khi người dùng xem báo cáo, hệ thống phải giới hạn kết quả chỉ gồm serial thuộc đơn vị mà người dùng được phân quyền quản lý. | Đăng nhập với 2 người dùng thuộc 2 đơn vị khác nhau, xác nhận mỗi người chỉ thấy serial thuộc đơn vị mình. |
| FR-bao-cao-ton-kho-serial-005 | Khi người dùng bấm "Xuất Excel", hệ thống phải xuất đúng danh sách đang hiển thị trên màn hình tại thời điểm đó (đã áp ngày xem và mọi bộ lọc đang chọn). | Áp 1 tổ hợp bộ lọc + đổi ngày xem, bấm xuất Excel, đối chiếu nội dung file với danh sách đang hiển thị trên màn hình. |
| FR-bao-cao-ton-kho-serial-006 | Khi giá trị của bất kỳ bộ lọc nào thay đổi (Ngày báo cáo, Kho, Serial, Mã SPMM, Vị trí lưu kho, Đơn vị), hệ thống phải tự động tải lại danh sách kết quả theo điều kiện mới, không yêu cầu người dùng thao tác xác nhận/bấm nút riêng. | Đổi lần lượt từng bộ lọc, xác nhận danh sách kết quả tự cập nhật ngay không cần thao tác thêm. |
| FR-bao-cao-ton-kho-serial-007 | Khi người dùng chưa chọn đủ Kho và Ngày báo cáo, hệ thống không được hiển thị danh sách kết quả nào. | Vào màn hình lần đầu (chưa chọn Kho/Ngày báo cáo), xác nhận không có danh sách nào hiển thị và có thông báo yêu cầu nhập đủ 2 trường tại field tương ứng. |

## 7. Quy tắc nghiệp vụ

**Nguyên tắc chung:** Báo cáo tồn kho Serial tại một thời điểm được xác định từ kỳ chốt gần nhất trước thời điểm xem và các giao dịch phát sinh sau kỳ chốt; giao dịch mới nhất quyết định đơn vị/vị trí hiện tại. Nếu chưa có kỳ chốt thì tính từ toàn bộ lịch sử giao dịch. Dữ liệu hiển thị phải tuân theo phạm vi phân quyền của người dùng.

| ID | Quy tắc | Áp ở |
|----|---------|------|
| BR-bao-cao-ton-kho-serial-001 | **Phân quyền:** Chỉ hiển thị đơn vị/vị trí lưu kho thuộc phạm vi người dùng được phân quyền. | Mục 5.1 field 4-6, FR-bao-cao-ton-kho-serial-004 |
| BR-bao-cao-ton-kho-serial-002 | **Xác định tồn tại thời điểm xem:** Trạng thái hiện tại của Serial được xác định từ số dư đầu kỳ + các giao dịch phát sinh đến ngày xem. Nếu có phát sinh thì lấy phát sinh mới nhất; không có thì giữ số dư đầu kỳ; không có ở cả hai nguồn thì Serial chưa tồn tại. Số dư đầu kỳ (snapshot) phải tự đảm bảo không chứa Serial đã xuất kho tại thời điểm chốt — báo cáo không kiểm tra lại loại giao dịch của các Serial lấy từ số dư đầu kỳ. | FR-bao-cao-ton-kho-serial-001, FR-bao-cao-ton-kho-serial-003 |
| BR-bao-cao-ton-kho-serial-003 | **Nhiều giao dịch:** Nếu Serial có nhiều giao dịch trong kỳ, lấy giao dịch có ngày giờ ghi nhận muộn nhất để xác định đơn vị/vị trí đang giữ. | FR-bao-cao-ton-kho-serial-001 |
| BR-bao-cao-ton-kho-serial-004 | **Chưa có kỳ chốt:** Nếu chưa có số dư kỳ chốt trước ngày xem, coi đầu kỳ = rỗng và tính lũy kế toàn bộ lịch sử giao dịch đến ngày xem. | FR-bao-cao-ton-kho-serial-001 |

## 8. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|---|----------|---------|
| SC-bao-cao-ton-kho-serial-01 | Người dùng được phân quyền tra được vị trí/đơn vị đang giữ của 1 serial cụ thể tại bất kỳ ngày nào trong quá khứ, không cần kiểm kê tay hay hỏi thủ công đơn vị khác. | Khảo sát người dùng sau go-live xác nhận không còn dùng cách kiểm kê thủ công cho mục đích tra cứu vị trí/đơn vị của serial. |

## 9. Câu hỏi mở

> Cột "Mức": `Block` (chặn go-live, phải chốt trước triển khai) / `Hold` (có thể trì hoãn, không chặn go-live) / `Info` (chỉ cần biết, không chặn gì).

| Mức | Câu hỏi | Vì sao quan trọng | Người chốt |
|-----|---------|----------------------|-------------|
| Block | Nguồn "số dư serial đã chốt theo kỳ" dùng ở bước 2 của công thức (Mục 3) — năng lực dùng chung cho mọi báo cáo tồn kho — hiện có sẵn cho serial hay cần xây mới, và ai/khi nào thực hiện chốt kỳ. Nếu quyết định go-live giai đoạn 1 chỉ chạy nhánh fallback (cộng dồn toàn bộ lịch sử), cần xác nhận rõ để hạ mức xuống Hold. | `FR-bao-cao-ton-kho-serial-001` không xác định được nhánh chính nếu chưa chốt câu này — dev không biết implement nhánh nào là chính thức, chỉ có thể làm tạm nhánh fallback | chưa xác định |

## 10. Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|-----------------|------------------|-----------------------------------|-------------------|-------------------------|
