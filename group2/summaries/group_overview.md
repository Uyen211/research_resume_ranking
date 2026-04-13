# 1. Tổng quan nhóm

*   **Nhóm này giải quyết vấn đề gì?**: Tập trung vào việc ứng dụng kiến trúc **Multi-Agent (Đa tác tử)** và **LLM Automation/RPA** để biến quy trình resume ranking từ một "hộp đen" tĩnh thành một quy trình hội thoại, minh bạch và có khả năng tự động hóa cao. Nó giải quyết sự thiếu hụt phản hồi cho ứng viên và sự cồng kềnh trong xử lý dữ liệu cho nhà tuyển dụng.
*   **Tại sao hướng tiếp cận này quan trọng?**: 
    1. **Tính linh hoạt**: Các agent chuyên biệt có thể xử lý các khía cạnh khác nhau (kỹ thuật, văn hóa, trích xuất) tốt hơn một mô hình duy nhất.
    2. **Khả năng giải thích (Explainability)**: Cung cấp lý do tại sao một ứng viên phù hợp hoặc không phù hợp thông qua tóm tắt và tranh luận giữa các agent.
    3. **Hiệu suất (Efficiency)**: Kết hợp RPA giúp xử lý quy mô lớn (hàng nghìn CV) với tốc độ vượt trội.
*   **Điểm yếu giải quyết được**: Loại bỏ sự phụ thuộc vào so khớp từ khóa (keyword matching) của các ATS cũ, giảm ảo giác (hallucination) của LLM đơn lẻ thông qua kiểm soát chéo (Moderator), và cung cấp phản hồi có giá trị hành động (actionable feedback) cho cả ứng viên.

# 3. So sánh trong nội bộ nhóm

*   **Các hướng tiếp cận**:
    *   **Agentic Evaluation (Paper 1)**: Tập trung vào chất lượng đánh giá nội bộ doanh nghiệp bằng RAG và sự phối hợp CEO/CTO/HR agents.
    *   **User-Centric Feedback (Paper 2)**: Tập trung vào trải nghiệm của ứng viên, cung cấp bộ đôi Recruiter/Mentor để giải thích kết quả.
    *   **High-Volume RPA (Paper 3)**: Tập trung vào tốc độ và quy trình tự động hóa e2e (end-to-end) trên quy mô lớn.
*   **Paper mạnh nhất**: **P. Lo et al. (Paper 1)** và **Aditya et al. (Paper 2)**. Paper 1 mạnh về mặt kỹ thuật/kiến trúc (RAG + Multi-agent), Paper 2 mạnh về mặt thiết kế trải nghiệm và tính nhân văn của hệ thống.
*   **Trade-off**:
    *   **Agentic Systems**: Độ trễ (latency) cao do phải gọi LLM nhiều lần và chờ các agent tranh luận.
    *   **RPA Integration**: Tốc độ cực nhanh nhưng logic chấm điểm có thể đơn giản hơn so với hệ thống agent chuyên sâu.

# 4. Pattern chung rút ra

*   **Dataset thường có đặc điểm gì?**: Dữ liệu thực tế từ web (LinkedIn, Kaggle), ẩn danh hóa, và thường được dán nhãn bởi các chuyên gia HR (Ground truth) để đo lường độ tương quan (Pearson/Spearman).
*   **Feature quan trọng nhất**: 
    *   **Skills Gap**: Khoảng cách giữa những gì ứng viên có và JD yêu cầu.
    *   **Reasoning Evidence**: Các bằng chứng về năng lực thực tế trong CV để agent đưa ra tóm tắt.
    *   **Company Context**: Tiêu chí riêng biệt được nạp qua RAG.
*   **Mô hình chiếm ưu thế**: GPT-4 (Turbo/o), DeepSeek-V3, Qwen, Gemini. Các framework như **CrewAI** và **LangChain** là tiêu chuẩn để xây dựng phối hợp giữa các agent.
*   **Những assumption nguy hiểm**: 
    *   **Bias**: AI có thể học theo các định kiến trong dữ liệu lịch sử nếu không được kiểm soát qua Moderator agent.
    *   **Amnestic Syndrome**: Giả định agent nhớ mọi thứ trong hội thoại dài là sai lầm; cần hệ thống quản lý memory tốt.

# 5. Ứng dụng cho project Resume Ranking

*   **Nếu build hệ thống thật**:
    *   **Nên chọn hướng**: Kiến trúc **Moderator-led Multi-agent**. Dùng một Agent mạnh (GPT-4/Claude 3.5) điều phối các Agent nhỏ hơn (Llama 3/GPT-4o-mini) cho từng nhiệm vụ (Parsing, Ranking, Feedback).
    *   **Nên tránh**: Chậm trễ trong giao diện (cần có loading stream hoặc tóm tắt từng phần); tránh để AI tự quyết định gửi mail từ chối mà không có sự kiểm duyệt của con người (Human-in-the-loop).
*   **Gợi ý kiến trúc hệ thống**:
    1.  **Input Layer**: Resume & JD (OCR/MinerU).
    2.  **Agent Layer**: 
        - Agent A (Extractor): Chuyển CV sang cấu trúc JSON.
        - Agent B (RAG-Evaluator): Truy vấn tiêu chí công ty và chấm điểm.
        - Agent C (Critic/Mentor): Phân tích điểm yếu và đưa ra lời khuyên.
    3.  **Controller Layer**: Moderator quản lý tranh luận và tổng hợp báo cáo cuối cùng.
    4.  **Output Layer**: Dashboard cho HR & Interactive Feedback cho ứng viên.

# 6. Research Gap

*   **Những vấn đề chưa được giải quyết**: 
    *   **Real-time skill updating**: Tự động cập nhật tiêu chí ranking theo xu hướng thị trường mà không cần can thiệp thủ công.
    *   **Multimodal Agents**: Đánh giá ứng viên qua video/audio phỏng vấn kết hợp với CV.
    *   **Cost optimization**: Giảm chi phí API khi phải chạy quá nhiều agent cho hàng nghìn CV (sử dụng Small Language Models - SLMs).
*   **Ý tưởng phát triển**: Xây dựng hệ thống agent có khả năng "tự học" từ các quyết định thực tế của HR trong quá khứ thông qua Reinforcement Learning from Human Feedback (RLHF) quy mô nhỏ tại doanh nghiệp.
