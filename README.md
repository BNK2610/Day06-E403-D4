# Day06-Lop-NhomXX - AI Vin Learner

AI Vin Learner la tro ly AI cho phu huynh hoc sinh, giup tra cuu thong tin hoc tap, diem danh, diem so, hoc phi, thong bao va ho tro tao ticket/lich trao doi voi nha truong. San pham thuoc track **Learning OS** va duoc xay dung theo huong **augmentation**: AI tong hop, goi tool va dieu huong, nhung khong tu thuc hien cac hanh dong nhay cam nhu thanh toan hay gui khieu nai chinh thuc neu chua co xac nhan.

## Thanh vien nhom

| MSV | Ho va ten | Phan viec chinh |
| --- | --- | --- |
| 2A202600743 | Bui Ngoc Khanh | Value, user stories, eval metrics, tong hop tai lieu |
| 2A202600670 | Nguyen Xuan Hiep | Trust design, learning signal |
| 2A202600927 | Nguyen Quang Huy | Correction signal, ROI |
| 2A202600637 | Nguyen Van Duong | Failure modes, mini AI spec |
| 2A202600958 | Vu Hai Tuan | Feasibility, prototype/codebase |

## Cau truc repo

```text
Day06-Lop-NhomXX/
├── README.md
├── hackathon-rules.md
├── spec/
│   ├── README.md
│   └── spec.md
└── codebase/
    ├── README.md
    ├── .env.example
    ├── requirements.txt
    ├── setup_db.py
    ├── docs/
    └── src/
```

## Tom tat prototype

- Giao dien: Streamlit.
- Database: PostgreSQL schema `school_ai` voi mock data phu huynh, hoc sinh, giao vien, diem so, diem danh, hoc phi, thong bao, thuc don, audit log va support ticket.
- AI layer: LangChain tool-calling agent, LLM provider cau hinh qua `.env`.
- Trust layer: tab `Kiem chung AI` luu cau hoi, intent, tool/nguon du lieu, cau tra loi va trang thai escalation.

## Huong dan nhanh

Xem huong dan chay prototype tai [codebase/README.md](codebase/README.md) va SPEC san pham tai [spec/spec.md](spec/spec.md).
