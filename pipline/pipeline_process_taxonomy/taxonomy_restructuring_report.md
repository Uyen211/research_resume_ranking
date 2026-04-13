# Báo cáo Nghiên cứu: Chiến lược Tái cấu trúc và Tối ưu hóa Hệ sinh thái Taxonomy (Tri thức nền) trong Hệ thống Xếp hạng CV

*Tài liệu này ghi chép lại toàn bộ lập luận học thuật, phương pháp luận và quá trình xử lý làm sạch bộ Taxonomy. Báo cáo phục vụ trực tiếp cho việc viết bài nghiên cứu khoa học.*

---

## 1. Đặt vấn đề (Problem Statement)
Trong các mô hình đối sánh ngữ nghĩa (Semantic Matching) giữa Job Description (JD) và Curriculum Vitae (CV), chất lượng của bộ "Từ điển" (Ontology/Taxonomy) đóng vai trò quyết định đến độ chính xác của không gian S-BERT. 

Bộ Taxonomy nguyên bản (`2022.01.21_hierarchy_structure_named.json`) ban đầu được tạo ra từ các thuật toán khai phá và nhóm dữ liệu tự động (ví dụ: LDA Topic Modeling hoặc Clustering) chạy trên hàng ngàn JDs/CVs thô. Dù sở hữu độ phủ rất lớn (phong phú về ngôn ngữ tự nhiên thực tế), hệ thống đang vướng phải hiện tượng **"Nhiễu Ngữ nghĩa" (Semantic Noise)** làm sai lệch kết quả đối sánh. Cụ thể:

1.  **Lệch pha về Domain (Domain Mismatch):** Bộ tự điển nguyên thủy ôm đồm các nhóm ngành không phân mảnh như Y Tế (Childcare, Healthcare), Sản xuất (Manufacturing), Ống nước (Plumbing), vốn dĩ không có giá trị đối sánh cho tệp JD/CV lõi là Công nghệ / Business / Văn phòng. 
2.  **Rác thuật toán (NLP Artifacts):** Các cụm từ bị nối đuôi theo mô hình túi từ (Bag-of-Words), lặp lại các tiền tố/hậu tố dư thừa như `(stakeholders-stakeholder-management)` hoặc `good client relationship - relationships good`.
3.  **Kém nhạy cảm với Kỹ năng Công nghệ (Lacking Hard Skills Depth):** Cấu trúc phân cụm ngôn ngữ tự nhiên không định nghĩa được các tiểu tiết sâu thẳm của Công nghệ Thông tin (ví dụ: Hệ thống không biết `React.js` là `Frontend Framework`). Áp dụng S-BERT lên bộ từ vựng chung chung sẽ làm sụp đổ phương thức đánh giá kỹ năng cứng của lập trình viên.

---

## 2. Giải pháp Cấu trúc: Mô hình "Não Trái - Não Phải" (Dual-Brain Ontology)
Thay vì sử dụng một siêu bản đồ tri thức bị nhiễu, tôi đề xuất chia tách Hệ tri thức thành hai phân mảng độc lập, tương ứng với bản chất của Kỹ năng Cứng và Kỹ năng Mềm:

### 2.1 Não Trái: Kỹ năng Cứng (Hard Tech Skills - `tech_ontology.json`)
*   **Bản chất:** Kỹ năng công nghệ yêu cầu tính "Tuyệt đối" và "Phân cấp nghiêm ngặt" (Strict Hierarchy). Ngôn ngữ IT không chứa đựng tính chất đại khái. `EC2` bắt buộc phải là con của `AWS`.
*   **Chiến lược Tái tạo:** Được xây dựng lại thủ công từ đầu (Top-Down Approach) dựa trên xu hướng hệ sinh thái hiện đại thay vì dùng Unsupervised Machine Learning. 
*   **Cấu trúc dữ liệu:** Bao gồm 6 Domain nòng cốt (`Software_Development`, `Data_and_AI`, `Infrastructure_and_DevOps`, v.v.), mở rộng bao phủ cả `Blockchain/Web3`, `Game Dev`, và `Cybersecurity`. Thiết kế này đảm bảo tỷ lệ Hit-rate (Tỷ lệ trúng) của Jaccard Similarity khi đối sánh CV Kỹ sư luôn đạt lý tưởng.

### 2.2 Não Phải: Kỹ năng Mềm & Quản trị (Soft Skills & Governance - `soft_skills_ontology.json`)
*   **Bản chất:** Thái độ, giao tiếp, và năng lực quản lý thường mơ hồ, đa dạng về từ biểu đạt (Polymorphic). Cấu trúc sinh ra nhờ thống kê tần suất từ CV thực tế (Bottom-Up) như bộ file 2022 ban đầu là một kho báu hoàn hảo. Vấn đề chỉ nằm ở khâu làm sạch.

---

## 3. Quá trình tiền xử lý kỹ thuật (Data Cleansing Process) trên Taxonomy Cũ
Để thu gọn và trích lọc mỏ vàng lý thuyết từ file `2022.01.21_...`, thuật toán làm toán dữ liệu đa tầng đã được triển khai:

### Bước 1: Thanh lọc miền tri thức (Domain Truncation)
Quyết định loại bỏ hoàn toàn các cấu trúc gốc như `Health and care`, `Childcare and Education`, `Food, cleaning and safety`. Mặc dù khiến Database mất đi lượng lớn "nodes", điều này giải phóng phần bộ nhớ tính toán (Memory) và bắt S-BERT chỉ tập trung định hướng vector cho các miền liên quan trực tiếp đến Data, Management và IT.

### Bước 2: Làm phẳng dữ liệu (Hierarchical Flattening)
Cấu trúc Clustering gốc lưu trữ dữ liệu rất sâu rác: `[Chuyên Mục] -> [Nhóm] -> [Leaf] -> [ID dạng số tự động] = "Cụm câu"`. Các ID này không đại diện cho giá trị Semantic. 
**Thuật toán:** Đã loại bỏ tầng Key ID, đồng thời gom (Aggregate) tất cả các cụm câu vào duy nhất một tập set nằm dưới trướng của Leaf Category. Cấu trúc chuyển từ mạng nhện (Graph) về dạng phẳng, thuận lợi cho việc duyệt Cây nhị phân/Tìm kiếm.

### Bước 3: Định dạng lại Văn bản (Textual Normalization & Regex)
Chạy bộ lọc biểu thức chính quy (Regex) vào sâu từng Node văn bản để:
*   Loại bỏ các cụm định danh tag thừa (Xóa toàn bộ ký tự trong ngoặc `()`).
*   Loại bỏ hiện tượng nhại từ (Xóa những chùm hậu tố sau dấu gạch ngang `-` mà sinh ra bởi thuật toán LDA thời cổ đại).
*   Không đưa các từ quá ngắn mang tính chất giới từ hoặc ký hiệu vô nghĩa vào bộ nhớ. 

### Bước 4: Khử nhiễu Trùng lặp (Deduplication)
Bằng cách đẩy dữ liệu qua tập tin lưu trữ bằng Set structure, các độ lệch biến thể nhỏ và trùng lặp hoàn toàn được "ép" thành một dòng quy chuẩn duy nhất.
**=> Kết quả định lượng:** File gốc chứa **6,685** cụm từ thô. Sau quá trình chuẩn hóa, Hệ thống làm sạch xuống còn chính xác **2,876** Node giá trị cốt lõi. Hiệu suất lọc giảm được ~57% chi phí nhiễu.

---

## 4. Giá trị Học thuật Đóng góp (Academic Contribution / Conclusion)
Sự kết hợp giữa `tech_ontology` (Determinism - Kiên định) và `soft_skills_ontology` (Probabilistic Semantic - Ngữ nghĩa Xác suất) tạo nên tính biện luận vượt trội cho Pipeline 0:
1.  **Explainable AI (AI Minh bạch):** Khi một Model đánh giá ứng viên, nó tham chiếu vị trí tọa độ của kỹ năng trong Không gian Ontology đã chuẩn hóa này thay vì dùng một con số "ảo" từ LLM trả về.
2.  **Tốc độ thực thi (Inference Acceleration):** Nhờ việc giảm lượng lớn nhiễu ở Não Phải, Matrix S-BERT dùng cho phép so sánh Cosine Similarity trở nên nhẹ nhàng, có khả năng vận hành trơn tru hoàn toàn bằng CPU mà không yêu cầu GPU tài nguyên lớn. 
3.  **Future-Proof (Ngăn ngừa lỗi thời):** Từ điển có sự phân tách rõ ràng. Khi xuất hiện các từ khóa công nghệ mới, ta chỉ cần chèn 1 dòng string đơn giản vào `tech_ontology.json` là toàn bộ hệ thống lại hiểu luật chơi, đáp ứng ưu điểm độc lập cho hệ thống Product dài hạn.
