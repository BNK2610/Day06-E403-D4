# Day06-E403-D4 - AI Vin Learner

AI Vin Learner là trợ lý AI cho phụ huynh học sinh, giúp tra cứu thông tin học tập, điểm danh, điểm số, học phí, thông báo và hỗ trợ tạo ticket/đặt lịch trao đổi với nhà trường. Sản phẩm thuộc track **Learning OS** và được xây dựng theo hướng **augmentation**: AI tổng hợp, gọi tool và điều hướng, nhưng không tự thực hiện các hành động nhạy cảm như thanh toán hay gửi khiếu nại chính thức nếu chưa có xác nhận.

## Thành viên nhóm

| Họ tên | MSV | Phần việc |
| --- | --- | --- |
| Vũ Hải Tuấn | 2A202600958 | Value, problem statement, user stories, tổng hợp SPEC/README |
| Nguyễn Xuân Hiệp | 2A202600670 | Trust design, learning signal, audit log, kiểm thử case AI sai |
| Nguyễn Quang Huy | 2A202600927 | Correction signal, ROI, học phí/payment flow, ticket hỗ trợ |
| Nguyễn Văn Dương | 2A202600637 | Failure modes, mini AI spec, demo script, test cases |
| Bùi Ngọc Khánh | 2A202600743 | Feasibility, database schema/mock data, prototype integration, hướng dẫn chạy |

## Cấu trúc repo

```text
Day06-E403-D4/
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

## Tóm tắt prototype

- Giao diện: Streamlit.
- Database: PostgreSQL schema `school_ai` với mock data phụ huynh, học sinh, giáo viên, điểm số, điểm danh, học phí, thông báo, thực đơn, audit log và support ticket.
- AI layer: LangChain tool-calling agent, LLM provider cấu hình qua `.env`.
- Trust layer: tab `Kiểm chứng AI` lưu câu hỏi, intent, tool/nguồn dữ liệu, câu trả lời và trạng thái escalation.

## Hướng dẫn nhanh

Xem hướng dẫn chạy prototype tại [codebase/README.md](codebase/README.md) và SPEC sản phẩm tại [spec/spec.md](spec/spec.md).
