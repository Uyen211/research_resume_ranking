
> 📌 **File Code Triển Khai Thực Tế (Colab):** [preprocessDataCV.ipynb](../../../code/cv_processing/preprocessDataCV.ipynb)

## 3. Pipeline 1: Tiền xử lý Văn bản (Text Preprocessing)

Mục tiêu của Pipeline này là làm sạch dữ liệu nhiễu nhưng vẫn bảo vệ tối đa ngữ nghĩa và các thực thể kỹ thuật.

*   **Đầu vào (Input)**: Văn bản thô (Raw text) được chuyển đổi từ file .docx hoặc .pdf sang Markdown.
*   **Các bước thực hiện**:
    1.  **Chuẩn hóa Unicode**: Sử dụng `unicodedata.normalize('NFC', text)` để đưa các ký tự tiếng Việt về định dạng chuẩn, tránh lỗi tách dấu trong các mô hình Embedding.
    2.  **Làm sạch ký tự điều hướng**: Chuyển đổi các dấu đầu dòng không chuẩn (•, ➢, ■) thành dấu gạch ngang `-`.
    3.  **Chuẩn hóa khoảng trắng**: Rút gọn nhiều khoảng trắng/xuống dòng liên tiếp thành một khoảng duy nhất để tiết kiệm Token Context cho LLM.
*   **Đầu ra (Output)**: Văn bản sạch (Cleaned text) sẵn sàng cho việc phân đoạn.

---

## 3. Pipeline 2: Phân đoạn & Chưng cất DNA Profile (DNA Extraction)

Pipeline này giải quyết bài toán CV siêu dài (>6000 từ) bằng cách nén thông tin mà không làm mất thực thể.

*   **Mô hình sử dụng**: **Gemini 3.1 Flash Lite Preview** (Tối ưu tốc độ và Context window lớn).
*   **Quy trình xử lý**:
    1.  **Phân loại độ dài**: Nếu CV > 2000 từ -> Sử dụng **Prompt 1 (Phân đoạn & Tóm tắt)**; Nếu CV <= 2000 từ -> Sử dụng **Prompt 2 (Phân đoạn thuần)**.
    2.  **Cấu trúc Tags chuẩn**: Dữ liệu được ép vào 5 thẻ: `<INFORMATION_SECTION>`, `<SUMMARY_SECTION>`, `<SKILLS_SECTION>`, `<EXPERIENCE_SECTION>`, `<EDUCATION_SECTION>`.
    3.  **Chuẩn hóa Experience**: Mỗi khối kinh nghiệm bắt buộc định dạng: `[Company|Project] | [Title|Role] | [Dates]` (Dates dùng định dạng `MM/YYYY`).
    4.  **Bóc tách Environment**: Mọi công cụ kỹ thuật được liệt kê cuối mỗi khối kinh nghiệm dưới dạng `Environment: [Tool1, Tool2, ...]`.
*   **Đầu vào (Input)**: Văn bản đã tiền xử lý.
*   **Đầu ra (Output)**: File JSON có cấu trúc (Segmented JSON) chứa DNA Profile của ứng cử viên.

