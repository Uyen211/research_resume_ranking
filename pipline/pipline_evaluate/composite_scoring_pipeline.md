# Tài liệu Kỹ thuật: Hệ thống Đánh giá và Xếp hạng CV Đa tầng (Layered Composite Scoring Pipeline)

Tài liệu này trình bày chi tiết luồng xử lý (Pipeline) của Hệ thống Xếp hạng Ứng viên. Được tinh lọc từ các phương pháp SOTA (State-of-the-Art) tiên tiến nhất hiện nay, hệ thống áp dụng cơ chế **Toán học Hỗn hợp (Hybrid Mathematical Scoring)** cho việc sàng lọc (Screening) tốc độ cao và dùng **Tác tử Thông minh (LLM-as-a-Judge)** cho việc tự động tạo phản hồi ứng viên.

---

## 1. Mạch Tư duy Kiến trúc (Architectural Philosophy)
Hệ thống tuyển dụng thực tiễn phải giải quyết được 3 bài toán: Minh bạch điểm số (Tại sao rớt?), Tốc độ cao (Xử lý hàng vạn CV), và Gợi ý giá trị (Feedback Loop). Do đó, Pipeline đánh giá không thể gộp thành một khối hộp đen, mà được bẻ làm 5 bước xử lý tuần tự (Layered Evaluation).

---

## 2. Chi tiết Quy trình Đánh giá (Scoring Pipeline)

Hệ thống phân rã hồ sơ ứng viên thành 5 thành phần (A, B, C, D, E) riêng biệt, sau đó tổng hợp lại thành 2 rổ điểm chính: **Điểm Nền (Base Score - Tối đa 100đ)** và **Điểm Thưởng (Bonus Score - Không giới hạn)**.

### THÀNH PHẦN A: Kỹ Năng Yêu Cầu (Core Hard Skills)
Đo lường mức độ đáp ứng các bộ kỹ năng bắt buộc và ưu tiên đã được trích xuất từ JD. Nhóm này quyết định **80%** sức nặng của rổ Điểm Nền.
*   **Bảng Trọng số (W_Bucket)**:
    *   **Must_Have (W=1.0)**: Khớp rổ bắt buộc.
    *   **Nice_To_Have_JD (W=0.7)**: Khớp rổ ưu tiên từ JD.
    *   **Nice_To_Have_AI (W=0.3)**: Khớp rổ mở rộng từ AI (Taxonomy gợi ý).
*   **Quy tắc So khớp Kép (Dual-Matching Rule) qua Taxonomy ID**:
    *   *Vấn đề Keyword cũ*: Nếu JD yêu cầu "oracle db" nhưng CV viết "Oracle 10g", máy tính sẽ đánh rớt vì lệch mặt chữ.
    *   *Cơ chế Khắc phục*: Nhờ quá trình Mapping ở Pipeline trước, kỹ năng đã được gắn mã `taxonomy_id = Data.RDBMS_oracle db`. Hệ thống sẽ bóc phần đuôi chuẩn hóa (`oracle db`) VÀ giữ lại tên chữ gốc để quét vào JD. Chỉ cần 1 trong 2 mặt chữ khớp lệnh là được tính điểm (chống đánh rớt oan uổng).
    *   Lưu ý: Nếu `taxonomy_id = null`, hệ thống bắt buộc lấy mặt chữ gốc để đối chiếu với JD trước.
*   **Hệ số Thâm niên (Exp Multiplier)**: Điểm thô của mỗi kỹ năng được bù đắp bằng số năm kinh nghiệm: `Point(i) = W_Bucket(i) * (1 + ln(years_i + 1))`.
*   **Cơ chế Tính Tỷ lệ Cốt lõi (Hard Ratio)**:
    *   Hệ thống giả lập một "Ứng viên hoàn hảo" (Có tất cả skill trong JD, và đạt max 5 năm kinh nghiệm) để làm mẫu số **Max_Hard_Score**.
    *   Ra được Tỷ lệ đáp ứng: `Hard_Ratio = Score_Thực_Tế / Max_Hard_Score`.

### THÀNH PHẦN B: Ràng buộc Cơ bản (Hard Constraints)
Đo lường điều kiện Tiền quyết, quyết định **20%** sức nặng của rổ Điểm Nền. Trả về đúng/sai (1.0 hoặc 0.0) không trừ phạt:
*   **Min Experience_Years:** Nếu `CV_Total_Years >= JD_Min_Years` -> Đạt 1.0.
*   **Required_Degree:** So sánh cấp bậc (Cử nhân < Thạc sĩ < Tiến sĩ) -> Đạt 1.0.

### THÀNH PHẦN C: Kỹ năng Mở rộng (Surplus Balance)
Xử lý các Kỹ năng có trong CV nhưng hoàn toàn không được JD đòi hỏi.
*   Nó được tách biệt hoàn toàn khỏi `Thành phần A` để kiểm soát, ngăn chặn việc lạm phát điểm thô.
*   Điểm: `Score_C = Σ [0.05 * (1 + ln(years_i + 1))]`. Ghi nhận ở rổ Điểm Thưởng.

### THÀNH PHẦN D: Kỹ năng Mềm (Soft Skills - Semantic Match)
Vượt qua rào cản từ ngữ (Vd: "Giao tiếp Tốt" vs "Hoạt ngôn"). Hệ thống sử dụng Không gian Ngữ nghĩa Vector.
*   **Cơ chế**: Dùng mô hình S-BERT (`all-MiniLM-L6-v2`) đo Cosine Similarity. Ngưỡng khớp là `> 0.75`.
*   **Điểm**: `+1.0đ` cho mỗi Soft skill khớp ngữ nghĩa. Ghi nhận ở rổ Điểm Thưởng.

### THÀNH PHẦN E: Chứng chỉ Bổ trợ (Certifications)
*   **Điểm**: `+1.0đ` cho mỗi chứng chỉ bổ sung. Ghi nhận ở rổ Điểm Thưởng.

---

### TỔNG HỢP & BẢO VỆ THANG ĐIỂM (COMPOSITE SCORING FORMULA)
Việc gò ép toán học chặn tình trạng lạm phát điểm số và trôi nổi bảng UI.

**1. Rổ ĐIỂM NỀN (Base Score = Tối đa 100 Điểm Tối Đa)**
Là Điểm đáp ứng cốt lõi. Bắt buộc bị khóa trần 100đ giúp dễ phân định ranh giới Đậu/Rớt:
*   Phần tử Kỹ năng Cứng (Capped): `Min(Hard_Ratio, 100%) * Chiếm 80đ`
*   Phần tử Ràng buộc (B Match): `Thành phần B * Chiếm 20đ`

**2. Rổ ĐIỂM THƯỞNG (Bonus Score - Không Khóa Trần)**
Quy tụ các Giá trị Lợi ích gia tăng (Thành phần C, D, E) & Phần Tràn Khung (Spillover).
*   **Thưởng Vượt Trình Độ (Overqualified Bonus)**: Lượng `% dư thừa` bị tắc lại từ hàm Min của phần tử kỹ năng cứng ở trên sẽ không bị hệ thống vứt bỏ để đảm bảo sự công bằng. Vd: Ứng viên quái vật cày được `Hard_Ratio = 120%`. Mốc 100% đã lọt vào Rổ Điểm Nền để khóa max điểm. `20% thừa` chênh lệch đó sẽ bị đẩy xuống đây (Thưởng Vượt = `20% * 80đ`).
*   **Thưởng Kỹ năng**: Gộp chung Thành phần C (Surplus) + Thành phần D (Mềm) + Thành phần E (Chứng chỉ).

**=> ĐIỂM TỔNG KẾT (TOTAL SCORE) = Base_Score + Bonus_Score**
> **Ví dụ UI thực tế hiển thị cho HR:** `100/100 (+ 8.5 Vượt Trình)`
> (Nhìn vào là hiểu ngay: Ứng viên này đã phủ tuyệt đối toàn bộ JD chuẩn mực (100đ), đồng thời có thêm năng lực sâu vượt trội đánh bay khuôn khổ (Bonus 8.5đ). Đây là mỏ vàng dán nhãn Senior).

### Bước 5: Đóng Vòng Phản hồi (LLM-as-a-Judge & Skill-Gap Analysis)
Ráp AI Tạo Sinh (Generative AI) vào công đoạn cuối để tạo giá trị nhân văn.

*   **Cơ chế:** Sau khi xếp hạng, lấy **TOP K** ứng viên. Hệ thống cung cấp bảng điểm chi tiết và danh sách kỹ năng thiếu hụt (nằm trong rổ `Must_Have` nhưng CV không có) cho LLM.
*   **Bản báo cáo Skill-Gap:** AI sinh ra phản hồi: *"Bạn đạt 85/100 điểm. Bạn rất mạnh về React, tuy nhiên chúng tôi yêu cầu khắt khe về Docker (Must-have) mà bạn chưa thể hiện rõ trong CV. Bạn nên bổ sung..."*
*   **Giá trị:** Tạo trải nghiệm tuyển dụng minh bạch và giúp ứng viên định hướng phát triển.

---

## 3. Phân tích Học thuật: Ưu điểm & Điểm nghẽn Hệ thống

### 🟢 Ưu điểm Vượt Trội (Pros)
1. **Explainable AI (Tính Minh bạch cao):** Khi bị hỏi "Tại sao AI xếp cậu này top 1?", HR dễ dàng xuất file log chứng minh: Điểm Kỹ năng cứng Jaccard của cậu ấy đạt 0.95 do trúng rải rác 8 Framework công nghệ. Trọng tâm quyết định là công khai (Transparent).
2. **Speed & Scalability (Siêu tốc và Rẻ tiền):** Bước 1, 2, 3, 4 chạy hoàn toàn bằng các phép tính Đại số tuyến tính trên không gian RAM. Hệ thống dư sức nghiền nát 10,000 CV trong chớp mắt bằng CPU máy bàn.
3. **Resource Optimization (Tối ưu ngân sách Big Tech API):** Vì LLM đắt đỏ chỉ chạy ở Bước 5 (Chỉ dùng quét top-K ứng viên để sinh chữ), Doanh nghiệp / Startup sẽ tiết kiệm khổng lồ chi phí Token vận hành hàng tháng.

### 🔴 Nhược điểm Tồn đọng & Thử thách (Cons & Challenges)
1. **Suy giảm Chiều sâu Ngữ cảnh (Contextual Depth Loss):** Giao thoa Jaccard chỉ đếm "Sự tồn tại của Từ khóa Công nghệ" mà không truy cứu được độ sâu. Ứng viên *"Biết sơ sơ cách cài đặt Docker"* và ứng viên *"Dùng Docker cứu hệ thống sập 1 triệu requests"* sẽ được nhả ra chung cụm từ `['Docker']` và nhận điểm Jaccard ngang bằng.
2. **Đụng hàng Điểm số (Redundant Quantitative Scores):** Với sự gò ép Toán học chặt chẽ, nếu một loạt ứng viên đều vượt mốc yêu cầu của JD, họ sẽ cùng cầm điểm số xếp loại `88/100` hoặc `92/100` như nhau. (Cách giải quyết: Tương lai cần xem xét cài cắm mô hình Pairwise Ranking phân loại cặp 1-1).
3. **Tính thủ công của Trọng số (Heuristic Tuning):** Thông số `W1, W2, W3` đang phụ thuộc vào kinh nghiệm cá nhân của HR nhập tay lẫy vào thanh trượt (Slider), tiềm ẩn sự chủ quan. Sẽ cần Máy học (Random Forest) học lại các thanh trượt đó dựa trên thói quen nhận việc của HR trong các phiên bản cập nhật Version 2.0 sau này.

---

## 4. Giải pháp Khắc phục Triệt để Nhược điểm (Mitigation Strategies)

Để biến hệ thống từ mức "Tốt" thành "Hoàn hảo" và bít kín các lỗ hổng lý thuyết, bản thiết kế đề xuất tích hợp 3 luồng công nghệ phụ trợ (Auxiliary Pipelines) lấy cảm hứng trực tiếp từ các bài nghiên cứu SOTA:

**1. Khắc phục "Suy giảm Chiều sâu Ngữ cảnh" -> Cơ chế Multi-Level Jaccard**
Thay vì GLiNER chỉ bóc trọc lóc chữ `["Docker"]`, ta lập trình để nó kéo theo các phó từ xung quanh tạo thành cặp Tuple `(Kỹ năng, Mức độ)`. Ví dụ: `("Docker", "3 năm")` hoặc `("Docker", "Expert")`. Lúc này, hàm Jaccard không chỉ đếm 1 điểm cho sự tồn tại, mà nhân thêm hệ số độ sâu (Depth Multiplier). Nếu chỉ "biết sơ sơ" thì nhân hệ số 0.3. Nhờ đó, điểm số phản ánh được bề dày kinh nghiệm thực chiến.

**2. Khắc phục "Đụng hàng Điểm số" -> Cơ chế Xếp hạng Cặp (Pairwise Tie-Breaker)**
Khi hệ thống lọc ra 50 ứng viên có điểm số sàn sàn nhau (ví dụ: cùng rơi vào phổ điểm 85-90), hệ thống sẽ không hiển thị ngẫu nhiên. Lúc này, thuật toán **RankSVM** (So sánh cặp) sẽ được kích hoạt ẩn. Nó gắp từng cặp ứng viên (A và B) ra so đọ xem ai có tỷ lệ trường Đại học tốt hơn, hoặc ai có vector Kỹ năng mềm "đẹp" hơn để tự động đẩy người đó lên Top 1. Thứ hạng cuối cùng là Unique (Duy nhất).

**3. Khắc phục "Trọng số Thủ công" -> Khép kín Vòng lặp Máy học (Auto-ML Feedback Loop)**
Không ép HR phải kéo thanh trượt `W1, W2, W3` một cách mù mờ nữa. Ta tích hợp một mô hình Phân loại (Random Forest/Logistic Regression) chạy ngầm. Khi luồng CV đổ về, nếu HR bấm nút "Nhận phỏng vấn" ứng viên A (Giỏi toán) và gạt bỏ ứng viên B (Giỏi giao tiếp), thuật toán Random Forest lập tức tự động học được hành vi này và ngầm điều chỉnh đẩy hệ số `W1` (Kỹ năng cứng) lên cao cho lần sau. Trọng số tự tiến hóa theo "Gu" của doanh nghiệp.
