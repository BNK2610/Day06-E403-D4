# Codebase - AI Vin Learner

Thu muc nay chua toan bo code prototype cua AI Vin Learner.

## Cong nghe su dung

- Python 3.10+
- Streamlit cho UI
- PostgreSQL cho database demo
- psycopg2 connection pool cho truy van database
- LangChain / LangChain Classic cho tool-calling agent
- OpenAI-compatible LLM provider qua bien moi truong
- pandas va Streamlit dataframe cho bang tong quan du lieu

## Cau hinh moi truong

```powershell
pip install -r requirements.txt
```

## Cau hinh `.env`

Tao file `.env` trong thu muc `codebase/` dua tren `.env.example`:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/day06_ai
LLM_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=
```

Neu dung provider OpenAI-compatible khac, dien `LLM_BASE_URL` va `LLM_MODEL_NAME` theo endpoint/model cua provider do.

## Khoi tao database

1. Tao database PostgreSQL ten `day06_ai` bang pgAdmin hoac psql.
2. Chay script reset schema va nap mock data:

```powershell
python setup_db.py
```

Script se tao schema `school_ai` va nap du lieu tu:

- `docs/db_design.sql`
- `docs/mock_data.sql`

## Chay ung dung

```powershell
streamlit run src/app.py
```

Sau khi chay, mo URL Streamlit hien trong terminal, thuong la:

```text
http://localhost:8501
```

## Tai khoan demo

| Tai khoan | Mat khau | Phu huynh | Hoc sinh |
| --- | --- | --- | --- |
| `PH001` | `123456` | Nguyen Van An | Nguyen Minh Khang, Nguyen Gia Han |
| `PH002` | `123456` | Tran Thi Lan | Le Bao Chau |
| `PH003` | `123456` | Pham Quoc Huy | Pham Duc Anh |

## Tools AI hien co

- `get_student_schedule`: tra cuu thoi khoa bieu.
- `get_student_grades`: tra cuu diem so.
- `get_attendance_records`: tra cuu diem danh/chuyen can.
- `get_school_announcements`: tra cuu thong bao truong/lop.
- `get_tuition_status`: kiem tra hoc phi.
- `get_academic_summary`: tong hop hoc tap.
- `get_teacher_comments`: tra cuu nhan xet giao vien.
- `get_teacher_contact_info`: lay thong tin giao vien chu nhiem.
- `initiate_fee_payment`: tao link/QR thanh toan mock, khong tu thanh toan.
- `report_issue_to_teacher`: tao ticket ho tro/phan anh.
- `get_available_meeting_slots`: lay gio trong giao vien dang mock.
- `book_teacher_meeting`: luu yeu cau dat lich nhu ticket.

## Luong demo goi y

1. Dang nhap `PH001 / 123456`.
2. Mo `Tong quan hoc tap` de xem bang diem, diem danh, hoc phi, nhan xet.
3. Hoi AI: `Tinh hinh hoc tap gan day cua con toi the nao? Hay noi ca diem so, chuyen can va nhan xet giao vien.`
4. Hoi hoc phi: `Con toi con khoan hoc phi nao chua thanh toan khong?`
5. Tao link thanh toan: `Neu con khoan chua thanh toan thi tao giup toi link hoac QR thanh toan.`
6. Chay failure path: `Thong tin hoc phi nay sai. Toi da thanh toan roi nhung he thong van bao chua thanh toan.`
7. Tao ticket ho tro.
8. Hoi giao vien chu nhiem va dat lich gap giao vien.
9. Mo `Kiem chung AI` de show audit log/tool/source.

## Luu y gioi han prototype

- Password demo dang dung mock data, production can hash bang bcrypt/argon2.
- Mot phu huynh co nhieu con chua co UI chon hoc sinh ro rang.
- Gio trong giao vien hien dang mock, chua co bang availability rieng.
- Bang `menus` da co trong database, nhung tool tra cuu thuc don rieng chua hoan thien.
- Thanh toan chi sinh link/QR mock, khong thuc hien giao dich that.
- Khong commit file `.env` that len repo.
