# 1. Tổng quan nhóm

*   **Nhóm này giải quyết vấn đề gì?**: Tập trung vào cốt lõi kỹ thuật của bài toán Resume Ranking: làm thế nào để chuyển đổi văn bản CV và JD thành các vector số học (embeddings) sao cho máy tính có thể so sánh độ tương đồng một cách chính xác nhất mà không bị đánh lừa bởi từ khóa đơn lẻ.
*   **Tại sao hướng tiếp cận này quan trọng?**: 
    1. **Vượt qua Keyword-matching**: Chuyển từ "so khớp từ" sang "so khớp ý nghĩa". Ví dụ: hiểu rằng "Machine Learning" tương đồng với "Deep Learning" hoặc "Data Science".
    2. **Xử lý ngữ cảnh**: Transformer (BERT, DeBERTa, Llama) hiểu được vị trí và vai trò của từ trong câu (ví dụ: "Senior" đặt trước "Developer" mang ý nghĩa khác với đặt ở nơi khác).
    3. **Tốc độ & Hiệu năng**: Kỹ thuật nhúng cho phép thực hiện tìm kiếm vectơ (vector search) cực nhanh trên quy mô lớn sau khi đã được encode.
*   **Điểm yếu giải quyết được**: Loại bỏ tình trạng "keyword stuffing" (ứng viên nhét từ khóa để qua mặt ATS), xử lý tốt các CV không có cấu trúc chuẩn, và thu hẹp khoảng cách giữa cách hiểu của máy tính và con người.

# 3. So sánh trong nội bộ nhóm

*   **Các hướng tiếp cận**:
    *   **Encoder-only (BERT/S-BERT)**: Tập trung vào việc tạo vector đặc trưng cho từng câu/keyword, tối ưu về tốc độ.
    *   **Hybrid Models**: Kết hợp Transformer với các thuật toán truyền thống (TextRank, Random Forest, TF-IDF) để tăng tính ổn định.
    *   **Decoder-only / LLM Embeddings (Llama/Gemini)**: Xu hướng mới nhất, tạo ra các vector có chiều sâu ngữ nghĩa vượt trội nhưng tốn tài nguyên hơn.
*   **Paper mạnh nhất**: **"Resume2Vec" (Paper 5)**. Đây là nghiên cứu toàn diện nhất, thực hiện benchmark trên nhiều kiến trúc Transformer khác nhau và chứng minh được ưu thế của Llama embeddings với các metric hiện đại (nDCG, RBO).
*   **Trade-off**:
    *   **S-BERT**: Nhanh, nhẹ, nhưng độ sâu ngữ nghĩa không bằng các model lớn.
    *   **Llama/GPT-4**: Cực kỳ chính xác nhưng chi phí API cao và độ trễ lớn.
    *   **Hybrid (DeBERTa + spaCy)**: Cân bằng nhất, giữ được độ chính xác của Deep Learning và độ ổn định của Rule-based.

# 4. Pattern chung rút ra

*   **Dataset thường có đặc điểm gì?**: Phổ biến nhất là **Kaggle Resume Dataset** (2,400 CV) hoặc các bộ dữ liệu ẩn danh thu thập từ các nền tảng tuyển dụng. Dữ liệu thường được chuyển từ PDF sang Text phi cấu trúc.
*   **Feature quan trọng nhất**: 
    *   **Semantic Overlap**: Sự trùng khớp về ý nghĩa ngữ cảnh.
    *   **Skill Clusters**: Các nhóm kỹ năng liên quan.
    *   **Role Alignment**: Sự tương đồng giữa các chức danh công việc (Job Titles).
*   **Mô hình chiếm ưu thế**: **S-BERT** cho ứng dụng thực tế (production) và **Llama/DeBERTa** cho các bài toán đòi hỏi độ chính xác tối đa (high-accuracy).
*   **Những assumption nguy hiểm**: Giả định rằng text sạch hoàn toàn (thực tế CV có rất nhiều lỗi OCR/formatting); giả định rằng người dùng cung cấp Ground Truth chuẩn (HR cũng có thể có định kiến riêng).

# 5. Ứng dụng cho project Resume Ranking

*   **Nếu build hệ thống thật**:
    *   **Nên chọn hướng**: **Hybrid Approach**. Dùng **S-BERT (all-MiniLM-L6-v2)** để làm embedding base vì nó nhanh và hiệu quả. Kết hợp với **spaCy NER** để bóc tách thực thể cứng (Experience years, Degree) nhằm làm filter bước đầu.
    *   **Nên tránh**: Chỉ dựa vào duy nhất điểm Cosine Similarity của một model Transformer mà không có các bước hậu xử lý (post-processing) hoặc kiểm chứng (validation).
*   **Gợi ý kiến trúc hệ thống**:
    1.  **Stage 1 (Embedding)**: Chuyển CV và JD thành vector dùng S-BERT.
    2.  **Stage 2 (Candidate Selection)**: Tính Cosine Similarity để lấy ra top 50 ứng viên.
    3.  **Stage 3 (Fine-grained Ranking)**: Dùng các model mạnh hơn (như DeBERTa hoặc Llama) để so sánh chi tiết top 50 này.
    4.  **Stage 4 (Composite Score)**: Tổng hợp điểm từ Embedding + Điểm trừ (nếu thiếu năm kinh nghiệm) + Điểm cộng (nếu có chứng chỉ đặc biệt).

# 6. Research Gap

*   **Những vấn đề chưa được giải quyết**: 
    *   **Multi-modal Embedding**: Kết hợp nhúng cả văn bản và bố cục (layout) của CV (ví dụ: dùng LayoutLM). 
    *   **Cross-lingual Embedding**: Xử lý trường hợp JD tiếng Anh nhưng CV tiếng Việt (mô hình mBERT/XLM-R).
    *   **Explainable Embedding**: Giải thích tại sao một vector lại nằm gần vector kia (trực quan hóa bằng sơ đồ 2D/3D).
*   **Ý tưởng phát triển**: Xây dựng một **Context-aware Weighted Embedding** - nơi mà các kỹ năng quan trọng trong JD (vị trí đầu, highlight) sẽ được gán trọng số cao hơn trong không gian vector khi so sánh với CV.
