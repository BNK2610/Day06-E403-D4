# Codebase - AI Vin Learner

Thư mục này chứa toàn bộ code prototype của AI Vin Learner.

## Công nghệ sử dụng

- Python 3.10+
- Streamlit cho UI
- PostgreSQL cho database demo
- psycopg2 connection pool cho truy vấn database
- LangChain / LangChain Classic cho tool-calling agent
- OpenAI-compatible LLM provider qua biến môi trường
- pandas và Streamlit dataframe cho bảng tổng quan dữ liệu

## Cấu hình môi trường Conda

```powershell
conda create -n day06-ai python=3.11 -y
conda activate day06-ai
pip install -r requirements.txt
```

## Cấu hình `.env`

Tạo file `.env` trong thư mục `codebase/` dựa trên `.env.example`:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/day06_ai
LLM_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=
```

Nếu dùng provider OpenAI-compatible khác, điền `LLM_BASE_URL` và `LLM_MODEL_NAME` theo endpoint/model của provider đó.

## Khởi tạo database

1. Tạo database PostgreSQL tên `day06_ai` bằng pgAdmin hoặc psql.
2. Chạy script reset schema và nạp mock data:

```powershell
python setup_db.py
```

Script sẽ tạo schema `school_ai` và nạp dữ liệu từ:

- `docs/db_design.sql`
- `docs/mock_data.sql`

## Chạy ứng dụng

```powershell
streamlit run src/app.py
```

Sau khi chạy, mở URL Streamlit hiện trong terminal, thường là:

```text
http://localhost:8501
```

## Tài khoản demo

| Tài khoản | Mật khẩu | Phụ huynh | Học sinh |
| --- | --- | --- | --- |
| `PH001` | `123456` | Nguyen Van An | Nguyen Minh Khang, Nguyen Gia Han |
| `PH002` | `123456` | Tran Thi Lan | Le Bao Chau |
| `PH003` | `123456` | Pham Quoc Huy | Pham Duc Anh |

## Tools AI hiện có

- `get_student_schedule`: tra cứu thời khóa biểu.
- `get_student_grades`: tra cứu điểm số.
- `get_attendance_records`: tra cứu điểm danh/chuyên cần.
- `get_school_announcements`: tra cứu thông báo trường/lớp.
- `get_tuition_status`: kiểm tra học phí.
- `get_academic_summary`: tổng hợp học tập.
- `get_teacher_comments`: tra cứu nhận xét giáo viên.
- `get_teacher_contact_info`: lấy thông tin giáo viên chủ nhiệm.
- `initiate_fee_payment`: tạo link/QR thanh toán mock, không tự thanh toán.
- `report_issue_to_teacher`: tạo ticket hỗ trợ/phản ánh.
- `get_available_meeting_slots`: lấy giờ trống giáo viên đang mock.
- `book_teacher_meeting`: lưu yêu cầu đặt lịch như ticket.

## Luồng demo gợi ý

1. Đăng nhập `PH001 / 123456`.
2. Mở `Tổng quan học tập` để xem bảng điểm, điểm danh, học phí, nhận xét.
3. Hỏi AI: `Tình hình học tập gần đây của con tôi thế nào? Hãy nói cả điểm số, chuyên cần và nhận xét giáo viên.`
4. Hỏi học phí: `Con tôi còn khoản học phí nào chưa thanh toán không?`
5. Tạo link thanh toán: `Nếu còn khoản chưa thanh toán thì tạo giúp tôi link hoặc QR thanh toán.`
6. Chạy failure path: `Thông tin học phí này sai. Tôi đã thanh toán rồi nhưng hệ thống vẫn báo chưa thanh toán.`
7. Tạo ticket hỗ trợ.
8. Hỏi giáo viên chủ nhiệm và đặt lịch gặp giáo viên.
9. Mở `Kiểm chứng AI` để show audit log/tool/source.

## Lưu ý giới hạn prototype

- Password demo đang dùng mock data, production cần hash bằng bcrypt/argon2.
- Một phụ huynh có nhiều con chưa có UI chọn học sinh rõ ràng.
- Giờ trống giáo viên hiện đang mock, chưa có bảng availability riêng.
- Bảng `menus` đã có trong database, nhưng tool tra cứu thực đơn riêng chưa hoàn thiện.
- Thanh toán chỉ sinh link/QR mock, không thực hiện giao dịch thật.
- Không commit file `.env` thật lên repo.
