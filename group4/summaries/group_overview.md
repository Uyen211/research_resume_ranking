# 1. Tổng quan nhóm

*   **Nhóm này giải quyết vấn đề gì?**: Tập trung vào việc xây dựng các hệ thống **End-to-End** thực tế, không chỉ dừng lại ở việc so khớp (matching) mà còn mở rộng sang phân tích bố cục (Layout Analysis), xếp hạng đa chiều (Multi-attribute Ranking), và định hướng nghề nghiệp (Career Prognosis).
*   **Tại sao hướng tiếp cận này quan trọng?**: 
    1. **Tính thực tiễn cao**: Giải quyết các bài toán "đau đầu" của ATS truyền thống như: CV có nhiều cột (multi-column), lỗi OCR, hoặc sự thiếu hụt kỹ năng của ứng viên.
    2. **Tăng giá trị thặng dư**: Thay vì chỉ lọc ứng viên, hệ thống còn đưa ra gợi ý (Skill-Gap Analysis) và dự báo nghề nghiệp, tạo ra một hệ sinh thái tuyển dụng thông minh.
    3. **Độ ổn định (Robustness)**: Sử dụng các kỹ thuật như YOLOv9 để hiểu cấu trúc CV trước khi xử lý ngôn ngữ, giúp hệ thống không bị "loạn" khi gặp các hồ sơ có thiết kế lạ.
*   **Nó giải quyết điểm yếu nào của các hướng khác?**: 
    *   Khắc phục sự phụ thuộc quá mức vào text thuần (plain text) của các mô hình Transformer bằng cách thêm lớp **Layout Analysis**.
    *   Khắc phục sự thiếu hụt khả năng phân biệt giữa các ứng viên "ngang tài ngang sức" bằng kỹ thuật **Pairwise/Comparative Ranking**.

# 3. So sánh trong nội bộ nhóm

*   **Các hướng tiếp cận**:
    *   **Rule-based + ML (Paper 1)**: Nhanh, rẻ, phù hợp cho lọc diện rộng giai đoạn đầu (vòng gửi xe).
    *   **Semantic Comparison (Paper 2)**: Chuyên sâu về thuật toán xếp hạng (RankSVM), tốt nhất cho việc chọn lọc top ứng viên xuất sắc nhất.
    *   **End-to-End Prediction (Paper 3)**: Tập trung vào "đầu ra" nghề nghiệp và tư vấn cho ứng viên.
    *   **Multimodal AI (Paper 4)**: Hiện đại nhất, kết hợp Computer Vision (YOLO) và NLP (BERT), xử lý tốt dữ liệu thô từ PDF/Ảnh.
*   **Paper mạnh nhất**: **"Multimodal Resume Ranking Web Application" (Paper 4)**. Vì nó giải quyết được bài toán khó nhất: "Làm sao để đọc được CV có layout phức tạp một cách chính xác nhất?".
*   **Trade-off**: 
    *   Mô hình Paper 4 (YOLO + BERT) tốn tài nguyên server hơn nhiều so với Paper 1 (TF-IDF + KNN).
    *   Paper 2 (RankSVM) cho kết quả tinh tế nhưng tốn thời gian tính toán hơn khi số lượng CV lên tới hàng nghìn.

# 4. Pattern chung rút ra

*   **Dataset thường có đặc điểm gì?**: Đang chuyển dịch mạnh mẽ sang **Multimodal Dataset** (bao gồm cả file ảnh CV để training nhận diện vùng). Quy mô ngày càng lớn (hàng nghìn CV thay vì hàng trăm).
*   **Feature quan trọng nhất**: 
    *   **Skills & Experience**: Luôn là trung tâm.
    *   **Layout Features**: Vị trí các mục trong CV (Header, Sidebar, Body).
    *   **Semantic Consistency**: Sự nhất quán giữa các kỹ năng và kinh nghiệm thực tế.
*   **Mô hình nào đang chiếm ưu thế?**: 
    *   **YOLO family** cho Layout Analysis.
    *   **BERT/RoBERTa** cho Text Classification.
    *   **SVM/Random Forest** cho Ranking/Classification lớp trên cùng (Top-layer).
*   **Những assumption nguy hiểm**: Giả định rằng ứng viên viết thật (cần bước Skill validation như Paper 1); giả định rằng OCR luôn đúng (cần bước Post-processing sửa lỗi chính tả).

# 5. Ứng dụng cho project Resume Ranking

*   **Nếu build hệ thống thật**:
    *   **Nên chọn hướng**: **Multimodal Hybrid**. Cần dùng **mô hình nhận diện vùng (LayoutLM hoặc YOLO)** để tách CV ra từng block (Education, Skills) trước khi dùng **S-BERT/DeBERTa** để tính điểm.
    *   **Nên tránh**: Ném nguyên một khối text khổng lồ thu được từ file PDF vào model embedding mà không phân loại đoạn văn, vì nhiễu từ các phần không liên quan (Contact, Hobbies) sẽ làm loãng điểm số của Skills.
*   **Gợi ý kiến trúc hệ thống**:
    1.  **Module 1 (Vision)**: YOLOv9 nhận dạng 5 vùng quan trọng (Header, Exp, Edu, Skills, Projects).
    2.  **Module 2 (NLP)**: OCR riêng từng vùng -> mBERT phân loại kỹ năng/kinh nghiệm.
    3.  **Module 3 (Intelligence)**: S-BERT tính điểm tương đồng ngữ nghĩa + Skill-Gap Analysis.
    4.  **Module 4 (Ranking)**: SVM hoặc Pairwise Ranking để xếp hạng cuối cùng.

# 6. Research Gap

*   **Những vấn đề chưa được giải quyết**: 
    *   **Xử lý CV tiếng Việt**: Hầu hết các paper chỉ chạy tốt trên tiếng Anh/Châu Âu.
    *   **Xử lý dữ liệu động**: Kinh nghiệm của ứng viên thay đổi theo thời gian, làm sao để update vector nhúng mà không cần re-training toàn bộ.
    *   **Sự giải thích được (Explainability)**: Tại sao AI cho CV này 9 điểm, CV kia 8 điểm? Cần có cơ chế highlight các từ khóa gây ra sự khác biệt điểm số.
*   **Ý tưởng phát triển**: Xây dựng một **BERT-based Explainable Ranking System** cung cấp một "đội ngũ Agent" giải thích: Agent 1 giải thích về Skills, Agent 2 giải thích về Experience, giúp HR tin tưởng vào quyết định của máy.
