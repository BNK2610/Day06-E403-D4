# SPEC sản phẩm - AI Vin Learner

**Problem statement:** Phụ huynh cần tra cứu thông tin học tập và làm việc với nhà trường một cách nhanh, rõ nguồn và đáng tin cậy; hiện tại họ thường phải đợi giáo viên, hotline hoặc nhiều kênh rời rạc, nên AI Vin Learner đóng vai trò trợ lý 24/7 để tổng hợp dữ liệu, trả lời có kiểm chứng và điều hướng sang người thật khi cần.

**Track:** Learning OS  
**Product:** AI assistant cho phụ huynh học sinh  
**Deployment mode:** Augmentation - AI hỗ trợ tra cứu, tổng hợp và điều hướng; không tự ra quyết định cuối cùng cho các tác vụ nhạy cảm.

---

## 1. Bằng chứng

### Quan sát từ quy trình hiện tại

Nhóm chọn bài toán giao tiếp giữa phụ huynh và nhà trường vì đây là một pain point lặp lại trong môi trường giáo dục. Khi phụ huynh muốn biết tình hình học tập của con, thông tin thường nằm rải rác ở nhiều nơi: giáo viên chủ nhiệm, giáo viên bộ môn, điểm danh, học phí, thông báo, lịch học và các nhận xét hằng ngày. Phụ huynh thường phải chờ phản hồi thủ công hoặc liên hệ nhiều lần để có đủ một bức tranh tổng thể.

Các điểm vướng nhóm quan sát được:

- Phụ huynh không chỉ cần một con số điểm, mà cần hiểu con đang ổn hay cần chú ý ở đâu.
- Giáo viên chủ nhiệm có thể không nắm ngay đủ tất cả dữ liệu của từng môn, nên việc tổng hợp mất thời gian.
- Các câu hỏi lặp lại như điểm số, điểm danh, học phí, thông báo, giáo viên chủ nhiệm tạo tải cho nhà trường.
- Khi dữ liệu sai hoặc chưa đồng bộ, nếu AI trả lời quá tự tin sẽ làm mất niềm tin và có thể dẫn đến hành động sai.

### Bằng chứng từ prototype

Prototype đã được dùng để kiểm tra các pain point trên bằng dữ liệu mock trong PostgreSQL. Hệ thống có các bảng nghiệp vụ như phụ huynh, học sinh, lớp, giáo viên, điểm số, điểm danh, học phí, thông báo, thực đơn, audit log và support ticket. Các luồng demo chính đã chạy được gồm:

- Đăng nhập phụ huynh và gắn phiên với học sinh.
- Hỏi AI về điểm số, chuyên cần, học phí, nhận xét giáo viên.
- Tạo link/QR thanh toán mock thay vì tự thanh toán.
- Tạo ticket khi phụ huynh báo thông tin sai.
- Ghi lại câu hỏi, intent, tool/nguồn dữ liệu và câu trả lời trong tab `Kiểm chứng AI`.

### Giả định cần kiểm chứng thêm

Một số nhận định hiện vẫn là giả định sản phẩm, cần kiểm chứng bằng phỏng vấn phụ huynh/giáo viên hoặc dữ liệu sử dụng thật:

- Phụ huynh sẽ tin dùng chatbot hơn nếu câu trả lời có nguồn/tool và có cách báo sai rõ ràng.
- Chatbot có thể giảm đáng kể số câu hỏi lặp lại gửi đến giáo viên chủ nhiệm.
- Phụ huynh sẵn sàng chuyển sang ticket/người thật khi AI không chắc thay vì yêu cầu AI trả lời bằng mọi giá.

---

## 2. Lát cắt để build

Lát cắt MVP được chọn:

> Một phụ huynh đăng nhập, hỏi về tình hình học tập hoặc học phí của con; AI xác định intent, gọi tool để truy xuất PostgreSQL, trả lời bằng ngôn ngữ tự nhiên có nguồn kiểm chứng; nếu phụ huynh báo dữ liệu sai hoặc cần hỗ trợ, AI điều hướng tạo support ticket thay vì tự xử lý tiếp.

Lát cắt này đủ để chứng minh ý tưởng vì nó gồm cả ba thành phần cốt lõi của AI product:

- **Value:** phụ huynh nhận câu trả lời nhanh hơn so với hỏi giáo viên thủ công.
- **Trust:** câu trả lời được log lại trong `Kiểm chứng AI`, có intent và tool/nguồn dữ liệu.
- **Action:** AI có thể điều hướng sang link/QR thanh toán mock, ticket hỗ trợ hoặc flow đặt lịch.

Những gì nằm ngoài lát cắt MVP:

- Thanh toán thật qua cổng thanh toán.
- Đồng bộ real-time với SIS/ERP thật của trường.
- Đặt lịch thật trên calendar của giáo viên.
- Hệ thống phân quyền đầy đủ cho từng giáo viên/bộ phận.
- UI chọn học sinh hoàn chỉnh cho phụ huynh có nhiều con.

---

## 3. AI Product Canvas

| Ô | Nội dung |
| --- | --- |
| **Value - Giá trị** | User chính là phụ huynh học sinh. Pain lớn nhất là thiếu thông tin kịp thời, phải chờ giáo viên hoặc tự ghép thông tin từ nhiều nguồn. AI giúp tra cứu 24/7, tổng hợp điểm số, chuyên cần, học phí, thông báo và nhận xét thành câu trả lời dễ hiểu. Giá trị thêm của AI nằm ở việc hợp nhất dữ liệu, diễn giải thông tin và giảm câu hỏi lặp lại cho nhà trường. |
| **Trust - Niềm tin** | Rủi ro nghiêm trọng nhất là AI trả lời sai về học sinh, học phí, lịch học hoặc thông báo. Hệ thống giảm rủi ro bằng đăng nhập, gắn session với học sinh, gọi tool lấy dữ liệu thay vì trả lời từ trí nhớ model, lưu audit log, và điều hướng sang giáo viên/support ticket khi phụ huynh báo sai hoặc AI không chắc. |
| **Feasibility - Khả thi** | Prototype dùng Streamlit, PostgreSQL, psycopg2 connection pool và LangChain tool-calling agent. Chi phí demo chủ yếu là LLM API và local/PostgreSQL database. Latency mục tiêu: 1-2 giây cho truy vấn đơn giản, 3-5 giây cho tổng hợp nhiều nguồn. Rủi ro chính khi triển khai thật là dữ liệu không sạch, đồng bộ chậm, permission sai và route nhầm ticket. |
| **Tín hiệu học** | Hệ thống thu correction log, audit log, câu hỏi bị hỏi lại, tỷ lệ báo `Thông tin này sai`, tỷ lệ escalation đúng, tool nào được gọi, và outcome của ticket. Những tín hiệu này giúp cải thiện intent routing, prompt, tool description, demo test set và cách diễn đạt câu trả lời. |

### Metrics và ngưỡng đánh giá

| Metric | Threshold mong muốn | Red flag |
| --- | --- | --- |
| Login success rate với tài khoản hợp lệ | >= 98% | < 95% trong 1 tuần |
| Grounded answer precision cho top intents | >= 95% | < 90% trong 1 tuần |
| Escalation routing accuracy | >= 90% | < 80% trong 2 tuần |
| User-reported wrong info rate | <= 3% phiên | > 7% phiên |
| P50 latency truy vấn đơn giản | < 2 giây | > 4 giây kéo dài |
| P50 latency tổng hợp/hành động | < 5 giây | > 7 giây kéo dài |

### ROI 3 kịch bản

| Kịch bản | Giả định | Lợi ích | Chi phí/Net |
| --- | --- | --- | --- |
| Conservative | 200 phụ huynh hoạt động/ngày, 30% câu hỏi tự phục vụ thành công | Giảm 2-3 giờ/ngày cho giáo viên/bộ phận hỗ trợ | Dương nhẹ nếu chatbot giảm được câu hỏi lặp lại lúc cao điểm |
| Realistic | 600 phụ huynh/ngày, 50% tự phục vụ, 30% ticket lặp lại được hấp thụ | Giảm 6-8 giờ/ngày, phụ huynh tiết kiệm 30-60 phút/tuần | Dương rõ nếu precision và escalation ổn định |
| Optimistic | 1,500 phụ huynh/ngày, 65% tự phục vụ | Giảm 15-20 giờ/ngày trên toàn khối vận hành | Rất dương nếu chất lượng giữ ổn định và ít cần sửa sai thủ công |

**Kill criteria:** Thu hẹp scope nếu sau pilot 6 tuần grounded precision < 90%, tỷ lệ `Thông tin này sai` > 7%, escalation đúng < 80%, hoặc phụ huynh không quay lại dùng chatbot cho các nhu cầu cơ bản.

---

## 4. Tăng năng lực hay tự động hóa

Nhóm chọn **tăng năng lực - augmentation**, không chọn automation hoàn toàn.

Lý do:

- Trong giáo dục, trả lời sai về học sinh, học phí hoặc lịch học có thể gây hậu quả thật và làm mất trust.
- AI nên hỗ trợ đọc hiểu, tổng hợp, tra cứu và chuẩn bị hành động; con người hoặc hệ thống xác nhận vẫn giữ bước quyết định cuối.
- Các hành động nhạy cảm như thanh toán, gửi khiếu nại chính thức, đặt lịch gặp giáo viên cần có xác nhận rõ ràng.

AI được phép làm:

- Hiểu câu hỏi của phụ huynh.
- Chọn tool phù hợp.
- Truy xuất dữ liệu trong database.
- Tổng hợp câu trả lời từ dữ liệu có sẵn.
- Tạo link/QR thanh toán mock nếu user yêu cầu.
- Tạo ticket hỗ trợ khi user xác nhận muốn nhà trường tiếp nhận.
- Gợi ý slot đặt lịch và lưu yêu cầu đặt lịch dạng ticket.

AI không tự làm:

- Không tự thanh toán học phí.
- Không tự gửi khiếu nại chính thức nếu user chưa xác nhận.
- Không tự khẳng định khi dữ liệu thiếu, stale hoặc user báo sai.
- Không trả lời thông tin của học sinh khác ngoài phiên đăng nhập.

---

## 5. Bốn đường đi của trải nghiệm

### Feature 1: Tra cứu học tập tổng hợp

**Trigger:** Phụ huynh hỏi: `Tình hình học tập gần đây của con tôi thế nào? Hãy nói cả điểm số, chuyên cần và nhận xét giáo viên.`

| Đường đi | Xử lý |
| --- | --- |
| **Đường thuận** | AI gọi các tool về điểm số, điểm danh, nhận xét/tổng hợp; trả lời ngắn gọn theo học sinh đang đăng nhập. |
| **AI không chắc** | Nếu dữ liệu thiếu hoặc quá ít nhận xét, AI nói rõ chưa đủ dữ liệu và gợi ý xem từng bảng dữ liệu trong `Tổng quan học tập`. |
| **AI sai** | Phụ huynh có thể báo thông tin sai; AI không tranh luận mà đề xuất kiểm tra lại hoặc tạo ticket hỗ trợ. |
| **User sửa** | Hệ thống lưu câu hỏi, intent, tool, câu trả lời và phản hồi sai vào audit/correction log để cải thiện routing và prompt. |

### Feature 2: Học phí và thanh toán

**Trigger:** Phụ huynh hỏi: `Con tôi còn khoản học phí nào chưa thanh toán không?`

| Đường đi | Xử lý |
| --- | --- |
| **Đường thuận** | AI gọi `get_tuition_status`, hiện khoản phí, số tiền, trạng thái. Nếu user muốn, gọi `initiate_fee_payment` để tạo link/QR mock. |
| **AI không chắc** | Nếu dữ liệu đối soát/chưa đồng bộ, AI nói rõ không thể xác nhận tuyệt đối và đề xuất liên hệ bộ phận hỗ trợ. |
| **AI sai** | Nếu user nói đã thanh toán nhưng hệ thống báo chưa, AI thừa nhận khả năng dữ liệu chưa cập nhật và hỏi có muốn tạo ticket không. |
| **User sửa** | Mở ticket `fee_issue`, lưu nội dung phản ánh, học sinh, phụ huynh và câu trả lời trước đó. |

### Feature 3: Liên hệ giáo viên và đặt lịch

**Trigger:** Phụ huynh hỏi: `Giáo viên chủ nhiệm của con tôi là ai? Tôi muốn đặt lịch gặp giáo viên.`

| Đường đi | Xử lý |
| --- | --- |
| **Đường thuận** | AI lấy thông tin GVCN bằng `get_teacher_contact_info`, sau đó gọi `get_available_meeting_slots` để hiện giờ trống mock. |
| **AI không chắc** | Nếu câu hỏi mơ hồ về giáo viên chủ nhiệm hay giáo viên bộ môn, AI hỏi lại thay vì tự chọn sai. |
| **AI sai** | Nếu slot không còn đúng hoặc giáo viên không đúng, user có thể yêu cầu sửa/báo lỗi; AI đề xuất ticket. |
| **User sửa** | User chọn lại ngày/giờ/lý do; `book_teacher_meeting` lưu yêu cầu dạng support ticket. |

### Feature 4: Trust log / Kiểm chứng AI

**Trigger:** Sau khi hỏi AI, phụ huynh mở tab `Kiểm chứng AI`.

| Đường đi | Xử lý |
| --- | --- |
| **Đường thuận** | User thấy lịch sử câu hỏi, intent, tool/nguồn dữ liệu, câu trả lời và trạng thái escalation. |
| **AI không chắc** | Nếu tool không được gọi hoặc nguồn không rõ, log giúp nhóm phát hiện để sửa routing/tool description. |
| **AI sai** | User/nhóm có bằng chứng để truy vết AI đã dựa vào đâu khi trả lời sai. |
| **User sửa** | Correction/ticket trở thành tín hiệu học cho test set và cải thiện sản phẩm. |

---

## 6. Những kiểu lỗi đáng lo nhất

| # | Failure mode | Hậu quả | Cách prototype xử lý |
| --- | --- | --- | --- |
| 1 | Dữ liệu chưa đồng bộ nhưng AI trả lời như mới nhất | Phụ huynh tin vào thông tin sai về điểm, điểm danh, học phí hoặc lịch học | Ưu tiên trả lời dựa trên database/tool; với dữ liệu nghi ngờ, AI nói rõ không chắc và đề xuất ticket/người thật |
| 2 | Sai mapping phụ huynh - học sinh | Lộ thông tin học sinh khác, mất trust nghiêm trọng | Đăng nhập, gắn session với `student_id`, hiện hồ sơ trong sidebar, chỉ truy vấn theo học sinh đang đăng nhập |
| 3 | Route sai tool/intent | AI trả lời sai nguồn, ví dụ hỏi thực đơn nhưng gọi thông báo | Audit log lưu tool đã gọi; nhóm có thể sửa tool description/routing. Hiện tại thực đơn có bảng `menus` nhưng tool riêng chưa hoàn thiện, nên không đưa làm case demo chính |
| 4 | AI suy luận quá mức khi nhận xét học sinh | Tạo nhận xét không phù hợp, gây hiểu nhầm về học sinh | Prompt giới hạn AI chỉ tổng hợp từ điểm, điểm danh, nhận xét giáo viên; nếu thiếu dữ liệu thì nói rõ và gợi ý liên hệ giáo viên |
| 5 | Hành động nhạy cảm được thực hiện quá sớm | Thanh toán/gửi khiếu nại/đặt lịch khi user chưa xác nhận | Chọn augmentation: thanh toán chỉ tạo link/QR mock; đặt lịch và phản ánh lưu dạng ticket, cần user xác nhận |

---

## 7. Kế hoạch kiểm thử và bằng chứng demo

### Tài khoản demo

| Tài khoản | Mật khẩu | Phụ huynh | Học sinh |
| --- | --- | --- | --- |
| `PH001` | `123456` | Nguyen Van An | Nguyen Minh Khang, Nguyen Gia Han |
| `PH002` | `123456` | Tran Thi Lan | Le Bao Chau |
| `PH003` | `123456` | Pham Quoc Huy | Pham Duc Anh |

### Test cases chính

| Nhóm case | Prompt / thao tác | Kỳ vọng |
| --- | --- | --- |
| Happy path tổng hợp | `Tình hình học tập gần đây của con tôi thế nào? Hãy nói cả điểm số, chuyên cần và nhận xét giáo viên.` | AI tổng hợp nhiều nguồn dữ liệu, trả lời theo học sinh đang đăng nhập |
| Điểm số | `Điểm Toán gần đây nhất của con tôi là bao nhiêu?` | AI lấy dữ liệu điểm và diễn giải ngắn gọn |
| Chuyên cần | `Gần đây con tôi có nghỉ học hoặc đi muộn không?` | AI trả về các bản ghi điểm danh cần chú ý |
| Học phí | `Con tôi còn khoản học phí nào chưa thanh toán không?` | AI gọi tool học phí, nếu có khoản pending thì nêu rõ số tiền/trạng thái |
| Thanh toán an toàn | `Tạo giúp tôi link hoặc QR thanh toán.` | AI tạo link/QR mock, không tự xác nhận đã thanh toán |
| Error/correction | `Thông tin học phí này sai. Tôi đã thanh toán rồi nhưng hệ thống vẫn báo chưa thanh toán.` | AI không khẳng định lại, đề xuất tạo ticket hỗ trợ |
| Giáo viên | `Giáo viên chủ nhiệm của con tôi là ai? Cho tôi thông tin liên hệ.` | AI lấy thông tin GVCN theo lớp của học sinh |
| Đặt lịch | `Tôi muốn gặp giáo viên chủ nhiệm để trao đổi về điểm Toán của con.` | AI hiện slot mock, sau đó lưu yêu cầu đặt lịch nếu user chọn slot |
| Trust log | Mở tab `Kiểm chứng AI` | Hiện câu hỏi, intent, tool/nguồn, câu trả lời, escalation |
| Dashboard | Mở tab `Tổng quan học tập` | Hiện bảng điểm, điểm danh, học phí, nhận xét giáo viên |

### Demo script 5 phút

1. Giới thiệu pain point: phụ huynh cần thông tin nhanh, đúng và có nguồn.
2. Đăng nhập `PH001 / 123456`.
3. Mở `Tổng quan học tập` để cho thấy database có dữ liệu thật cho demo.
4. Hỏi AI case tổng hợp học tập.
5. Hỏi học phí và tạo link/QR thanh toán mock.
6. Chạy failure path: user báo học phí sai, AI tạo ticket hỗ trợ.
7. Hỏi giáo viên chủ nhiệm và đặt lịch gặp giáo viên.
8. Mở `Kiểm chứng AI` để chứng minh trust/audit layer.

### Bằng chứng cần giữ khi nộp/demo

- Screenshot giao diện chat với câu trả lời AI.
- Screenshot tab `Tổng quan học tập`.
- Screenshot tab `Kiểm chứng AI` sau khi gọi tool.
- File `docs/db_design.sql` và `docs/mock_data.sql` trong codebase.
- README hướng dẫn chạy bằng Conda và `.env.example`.
- Danh sách test cases ở trên.

### Công cụ/tool AI trong prototype

- `get_student_schedule`: tra cứu thời khóa biểu.
- `get_student_grades`: tra cứu điểm số.
- `get_attendance_records`: tra cứu điểm danh/chuyên cần.
- `get_school_announcements`: tra cứu thông báo.
- `get_tuition_status`: kiểm tra học phí.
- `get_academic_summary`: tổng hợp học tập.
- `get_teacher_comments`: tra cứu nhận xét giáo viên.
- `get_teacher_contact_info`: thông tin giáo viên chủ nhiệm.
- `initiate_fee_payment`: tạo link/QR thanh toán mock, không tự thanh toán.
- `report_issue_to_teacher`: tạo ticket hỗ trợ/phản ánh.
- `get_available_meeting_slots`: lấy giờ trống giáo viên đang mock.
- `book_teacher_meeting`: lưu yêu cầu đặt lịch như ticket.

### Giới hạn prototype cần nói thẳng trong Q&A

- Password demo là mock, production cần hash bằng bcrypt/argon2.
- `PH001` có nhiều học sinh nhưng UI chọn con chưa hoàn chỉnh; MVP hiện gắn với học sinh đang lấy trong session.
- Giờ trống giáo viên đang mock, chưa có bảng availability thật.
- Bảng `menus` có trong database, nhưng tool tra cứu thực đơn riêng chưa hoàn thiện, nên không dùng làm demo case chính.
- Thanh toán chỉ tạo link/QR mock, không thực hiện giao dịch thật.
- Trust log đã có tool/source ở mức audit, nhưng production nên hiện timestamp/source chi tiết hơn ngay trong từng câu trả lời.

---

## 8. Phân công

| Họ tên | MSV | Phần việc |
| --- | --- | --- |
| Bùi Ngọc Khánh | 2A202600743 | Define Value, user stories, eval metrics, tổng hợp tài liệu bản cuối |
| Nguyễn Xuân Hiệp | 2A202600670 | Define Trust, learning signal, cách user báo sai và kiểm chứng AI |
| Nguyễn Quang Huy | 2A202600927 | Correction signal, ROI, case failure/correction |
| Nguyễn Văn Dương | 2A202600637 | Failure modes, mini AI spec, demo narrative |
| Vũ Hải Tuấn | 2A202600958 | Feasibility, database/prototype, codebase và hướng dẫn chạy |

Mỗi thành viên cần nắm được ba câu hỏi khi demo:

- Sản phẩm này là augmentation hay automation? Vì sao?
- Failure mode nguy hiểm nhất là gì và prototype xử lý thế nào?
- Phần mình phụ trách nằm ở đâu trong spec/prototype?
