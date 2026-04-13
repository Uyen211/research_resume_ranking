# 1. Tổng quan nhóm

*   **Nhóm này giải quyết vấn đề gì?**: Nhóm nghiên cứu này tập trung vào việc tạo nền tảng vững chắc cho hệ thống Resume Ranking thông qua việc hệ thống hóa kiến thức (Review), xây dựng dữ liệu quy mô lớn (Datasets) và thiết lập các tiêu chuẩn đánh giá khách quan (Benchmarks). Nó giải quyết bài toán "làm sao để đo lường sự hiệu quả" và "huấn luyện mô hình trên dữ liệu nào".
*   **Tại sao hướng tiếp cận này quan trọng?**: Không có dữ liệu và benchmark chuẩn, việc phát triển các mô hình AI sẽ giống như "mò kim đáy bể". Việc hiểu các vấn đề hiện hữu (định kiến, đa định dạng) giúp thiết kế hệ thống có khả năng chống chịu tốt với dữ liệu thực tế.
*   **Điểm yếu giải quyết được**: Khắc phục tình trạng các hệ thống Resume Ranking đời đầu thường dựa trên so khớp từ khóa đơn giản (Keyword matching), không có khả năng suy luận về năng lực (Competency reasoning) và dễ bị đánh lừa bởi các mẹo format CV.

# 3. So sánh trong nội bộ nhóm

*   **Các hướng tiếp cận**:
    *   **Review & Survey**: Tập trung vào bức tranh toàn cảnh, so sánh ưu/nhược điểm của hàng chục phương pháp khác nhau (Bài báo 1 & 4).
    *   **Dataset Building**: Tập trung vào việc giải quyết sự khan hiếm dữ liệu nhãn bằng cách thu thập và OCR quy mô lớn (Bài báo 2 - ResumeAtlas).
    *   **Benchmarking & Diagnostics**: Tập trung vào việc "mổ xẻ" các lỗi của hệ thống tìm kiếm thay vì chỉ chấm điểm (Bài báo 3 - PJB).
*   **Paper mạnh nhất/Phù hợp nhất**: Bài báo **PJB: A Reasoning-Aware Benchmark** mang lại giá trị thực tiễn cao nhất cho việc build hệ thống thực tế vì nó cung cấp mindset về "Diagnostic" - giúp ta biết chính xác hệ thống đang yếu ở ngành nghề nào để tối ưu.
*   **Trade-off**: 
    *   LLM hiện đại (Gemma, BERT) mang lại độ chính xác cực cao nhưng đánh đổi bằng chi phí tính toán (GPU) và độ trễ (Latency).
    *   Các phương pháp ML truyền thống (SVM, XGBoost) nhanh, nhẹ nhưng kém trong việc hiểu các kỹ năng tương đương (semantic gap).

# 4. Pattern chung rút ra

*   **Đặc điểm Dataset**: Thường là dữ liệu phi cấu trúc (PDF/Ảnh), đòi hỏi bước Parsing hoặc OCR cực kỳ chính xác. Dữ liệu có tính mất cân bằng cao giữa các ngành nghề (Tech thường nhiều dữ liệu nhất).
*   **Feature quan trọng nhất**: 
    *   Job Title & Role (thường nằm ở 300-500 từ đầu tiên).
    *   Professional Skills (kỹ năng chuyên môn).
    *   Contextual Evidence (bằng chứng về năng lực trong các dự án cụ thể).
*   **Mô hình chiếm ưu thế**: Transformers (BERT, SentenceBERT) và các mô hình Decoder-only (Gemma, LLM) đang thống trị nhờ khả năng hiểu ngữ cảnh vượt trội.
*   **Assumption nguy hiểm**: 
    *   "Parsing luôn đúng": Thực tế parsing sai sẽ làm hỏng toàn bộ pipeline.
    *   "Từ khóa là tất cả": Việc lạm dụng matching từ khóa sẽ bỏ qua các ứng viên tài năng nhưng dùng bộ thuật ngữ khác.
    *   "Điểm accuracy trung bình cao là tốt": Có thể model chỉ tốt ở các ngành phổ thông và hoàn toàn lỗi ở các ngành đặc thù.

# 5. Ứng dụng cho project Resume Ranking

*   **Nếu build hệ thống thật**:
    *   **Nên chọn**: Hướng **Dense Retrieval + Reranking**. Sử dụng Embedding (ví dụ: bge-m3 hoặc model fine-tuned trong domain tuyển dụng) để tìm kiếm ứng viên tiềm năng, sau đó dùng một model LLM nhỏ để Rerank chính xác dựa trên tiêu chuẩn năng lực.
    *   **Nên tránh**: Chỉ dựa vào từ khóa hoặc các thư viện parsing miễn phí có độ chính xác thấp.
*   **Gợi ý kiến trúc hệ thống**:
    1.  **Data Ingestion**: Xử lý PDF đa định dạng (sử dụng các tool mạnh như MinerU để giữ cấu trúc).
    2.  **Indexing**: Chuyển CV sang Vector dùng Domain-Specific Embedding.
    3.  **Retrieval phase**: Tìm Top-100 ứng viên nhanh chóng bằng Vector Search.
    4.  **Reranking phase**: Sử dụng LLM (Gemini 1.5 hoặc Llama 3) để phân tích sâu Top-20 ứng viên, đưa ra giải thích (Explainable AI - XAI).

# 6. Research Gap

*   **Vấn đề chưa được giải quyết**: 
    *   Sự thay đổi nhanh chóng của các kỹ năng (Concept Drift) - kỹ năng hot hôm nay có thể lỗi thời ngày mai.
    *   Khả năng đánh giá "Soft skills" qua văn bản một cách khách quan.
    *   Xử lý CV đa ngôn ngữ và đặc thù văn hóa vùng miền (ví dụ CV phong cách Nhật vs Mỹ).
*   **Ý tưởng phát triển**:
    *   Xây dựng một "Skill-Transfer Knowledge Graph" cho thị trường Việt Nam (tự động hiểu các kỹ năng tương đương trong tiếng Việt).
    *   Hệ thống AI giải thích thứ hạng (Explainable Ranking) để giúp nhà tuyển dụng tin tưởng hơn vào kết quả.
