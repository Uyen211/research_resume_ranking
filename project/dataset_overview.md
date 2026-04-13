# Tổng quan Dataset & Phân tích Vấn đề (Resume Ranking Project)

## 1. Thành phần Dataset hiện tại

*   **Số lượng**: 228 hồ sơ (CV).
*   **Định dạng gốc**: Microsoft Word (.docx) - hiện đang được cung cấp dưới dạng Markdown (.md) để xử lý.
*   **Đặc điểm văn bản**:
    *   **Độ dài cực lớn**: Trung bình ~2600 từ, tối đa >6000 từ. Điều này gây thách thức cho các mô hình Embedding truyền thống (thường giới hạn 512-1024 token) và tốn tài nguyên khi sử dụng LLM.
    *   **Nội dung chuyên sâu**: Chứa nhiều thuật ngữ kỹ thuật, kỹ năng hiếm (Hadoop, Kafka, Spark, Microservices, SAFe, v.v.).
    *   **Bố cục phức tạp**: CV thực tế ở dạng .docx thường có bảng biểu (Skills matrix), cột đôi (Sidebar), và định dạng không đồng nhất giữa các ứng viên.

## 2. Phân tích bài toán "Noisy Labels" (Job Titles)

Qua danh sách Job Titles được trích xuất sơ bộ, bộ dữ liệu đang gặp các vấn đề nghiêm trọng về chuẩn hóa dữ liệu:

### 2.1. Sự phân mảnh ngữ nghĩa (Semantic Fragmentation)
Các chức danh thực chất thuộc cùng một nhóm nhưng đang bị tách rời:
*   **Nhóm Business Analyst**: "Business Analyst" (28), "Sr. Business Analyst" (14), "BUSINESS ANALYST" (1), "Senior Business Analyst" (3).
*   **Nhóm Java Developer**: "Sr. Java" (18), "Sr. Java Developer" (10), "Java Developer" (7), "Senior Java Developer" (4), "Sr Java Developer" (1).
*   **Nhóm Agile/Scrum**: "Scrum Master" (22), "Certified Scrum Master" (3), "SCRUM Master" (2), "Agile Coach" (2).

### 2.2. Biến thể về định dạng và Casing
*   **Case sensitivity**: "PROJECT MANAGER" vs "Project Manager" vs "project manager".
*   **Viết tắt**: "BSA" vs "Business Systems Analyst".
*   **Ký tự đặc biệt**: "Certified ""SCRUM MASTER"" & ""PO""".

### 2.3. Nhãn thiếu thông tin (Broad/Noisy Labels)
Một số nhãn quá chung chung hoặc bị trích xuất lỗi, không phản ánh đúng vị trí:
*   "Project" (1), "Java" (1), "Hadoop" (1).
*   "Senior IT" (1), "Consultant" (4), "SME" (1).

## 3. Các thách thức kỹ thuật chính

1.  **Vấn đề Context Window**: Với các CV >6000 từ, việc đưa toàn bộ văn bản vào một lần prompt hoặc một lần embedding sẽ dẫn đến mất mát thông tin (Loss in the middle) hoặc vượt giới hạn token.
2.  **Mất cấu trúc khi chuyển đổi (.docx -> .md)**: Mặc dù Markdown dễ đọc cho LLM, nhưng các thông tin về vị trí (Layout) vốn quan trọng để phân biệt giữa "Kỹ năng mục tiêu" và "Dự án đã làm" có thể bị nhòa đi.
3.  **Khoảng cách ngữ nghĩa (Semantic Gap)**: Job Title trong CV có thể là "Sr. Java Developer" nhưng JD có thể yêu cầu "Software Engineer II". Hệ thống cần một lớp Mapping/Taxonomy trung gian.
4.  **Thiếu nhãn chuẩn (Ground Truth)**: Danh sách Job Title hiện tại là "Noisy", không thể dùng làm mục tiêu huấn luyện trực tiếp (Supervised Learning) mà cần quy trình lọc (Refinement).
