import json

def create_notebook():
    cells = []
    
    def add_md(content):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in content.split('\n')]
        })
        
    def add_code(content):
        cells.append({
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [line + "\n" for line in content.split('\n')]
        })

    # Cell 1
    add_md("""# HỆ THỐNG XẾP HẠNG CV ĐA TẦNG (Composite Scoring Pipeline)
Dựa trên kiến trúc: `pipline/pipline_evaluate/composite_scoring_pipeline.md`
Mục tiêu: Đọc JSON Resume và JD, kết xuất bảng xếp hạng (.csv) với cơ chế Chặn đỉnh 100 điểm, Điểm Bonus vượt trần và Exp-weighted Jaccard.""")

    add_md("""## 1. Cài đặt Môi trường Google Colab""")
    add_code("""!pip install sentence-transformers tqdm pandas numpy""")

    add_md("""## 2. Kết nối Google Drive & Import Thư viện""")
    add_code("""import os
import json
import math
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import logging
from sentence_transformers import SentenceTransformer, util

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Khai báo đường dẫn Workspace gốc
BASE_DIR = '/content/drive/MyDrive/Nlp resume ranker'
RESUME_DIR = os.path.join(BASE_DIR, 'last_resumes')
JD_DIR = os.path.join(BASE_DIR, 'Cleaned_JD_V2')
CHROMA_DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
OUTPUT_DIR = os.path.join(BASE_DIR, 'scoring')

os.makedirs(OUTPUT_DIR, exist_ok=True)
logger.info("Paths configured successfully.")""")

    add_md("""## 3. Class Tiện ích: Phân tích Kỹ năng Mềm (Soft Skill Matcher)
Sử dụng SentenceTransformers để kiểm tra Semantic Match giữa JD và CV (Ngưỡng 0.75).""")
    add_code("""class SoftSkillMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.75):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold
        logger.info(f"Loaded Semantic Model: {model_name}")

    def count_matches(self, jd_soft_skills, cv_soft_skills):
        if not jd_soft_skills or not cv_soft_skills:
            return 0
        
        cv_texts = []
        for s in cv_soft_skills:
            if isinstance(s, dict):
                cv_texts.append(s.get('skill', ''))
            else:
                cv_texts.append(str(s))
                
        jd_embeddings = self.model.encode(jd_soft_skills, convert_to_tensor=True)
        cv_embeddings = self.model.encode(cv_texts, convert_to_tensor=True)
        
        cosine_scores = util.cos_sim(cv_embeddings, jd_embeddings)
        
        match_count = 0
        for i in range(len(cv_texts)):
            # Nếu skill CV này có điểm cos_sim > threshold với BAT KY skill nào trong JD
            if torch.max(cosine_scores[i]).item() > self.threshold:
                match_count += 1
                
        return match_count""")

    add_md("""## 4. Lõi Chấm Điểm Tuyển Dụng (Composite Scoring Engine)
Cài đặt chính xác các thuật toán Toán học trong đặc tả Benchmark SOTA.""")
    add_code("""class CompositeScorer:
    def __init__(self):
        # Trọng số Cốt lõi (Tổng 100%)
        self.W_HARD = 0.8
        self.W_CONSTRAINTS = 0.2
        
        # Trọng số Rổ kỹ năng
        self.W_MUST_HAVE = 1.0
        self.W_NICE_TO_HAVE = 0.7
        self.W_EXPANSION = 0.3
        self.W_SURPLUS = 0.05
        
        # Cấu hình tính Max Score
        self.MAX_IDEAL_YEARS = 5.0
        
        # Trọng số Thưởng (Vượt trần)
        self.B_SOFT = 1.0 
        self.B_CERT = 1.0

    def _get_degree_rank(self, degree_str):
        if not degree_str: return 0
        s = str(degree_str).lower()
        if any(x in s for x in ['phd', 'doctor', 'tiến sĩ']): return 3
        if any(x in s for x in ['master', 'm.s', 'm.a', 'thạc sĩ']): return 2
        if any(x in s for x in ['bachelor', 'b.s', 'b.a', 'cử nhân']): return 1
        return 0

    def _process_constraints(self, jd_data, cv_data):
        jd_const = jd_data.get('Hard_Constraints', {})
        cv_info = cv_data.get('Information', {})
        cv_edu = cv_data.get('Education', {})
        
        jd_yoe = jd_const.get('Min_Experience_Years', 0)
        cv_yoe = cv_info.get('Years_of_Exp') or 0.0
        
        jd_deg = jd_const.get('Required_Degree', '')
        cv_deg = cv_edu.get('Degree', '')
        
        score_yoe = 1.0 if cv_yoe >= jd_yoe else 0.0
        score_deg = 1.0 if self._get_degree_rank(cv_deg) >= self._get_degree_rank(jd_deg) else 0.0
        
        return (score_yoe * 0.5) + (score_deg * 0.5)

    def evaluate(self, jd_data, cv_data, soft_match_count=0):
        # 1. TÍNH TOÁN MAX IDEAL SCORE
        jd_hard = jd_data.get('Hard_Skills', {})
        must_have = jd_hard.get('Must_Have', {}).get('Tech_Skills', [])
        nice_have = jd_hard.get('Nice_To_Have', {}).get('From_JD_Desirable', [])
        expansion = jd_hard.get('Nice_To_Have', {}).get('From_Taxonomy_Expansion', [])
        
        ideal_multiplier = 1.0 + math.log(self.MAX_IDEAL_YEARS + 1.0)
        
        max_score = 0.0
        max_score += len(must_have) * self.W_MUST_HAVE * ideal_multiplier
        max_score += len(nice_have) * self.W_NICE_TO_HAVE * ideal_multiplier
        max_score += len(expansion) * self.W_EXPANSION * ideal_multiplier
        
        if max_score == 0: max_score = 1.0 # Tránh chia 0
            
        # 2. TÍNH ĐIỂM KỸ NĂNG ỨNG VIÊN
        cv_skills = cv_data.get('Hard_Skills', {}).get('Direct_Mention', [])
        
        mh_set = set(x.lower() for x in must_have)
        nh_set = set(x.lower() for x in nice_have)
        ex_set = set(x.lower() for x in expansion)
        
        cand_hard_score = 0.0
        cand_surplus_score = 0.0
        
        for sk in cv_skills:
            raw_name = sk.get('skill', '').lower()
            tax_id = sk.get('taxonomy_id')
            # Trích xuất tên chuẩn hóa từ taxonomy_id (VD: "Data.RDBMS_oracle db" -> "oracle db")
            norm_name = tax_id.split('_')[-1].lower() if tax_id else raw_name
            
            years = sk.get('years', 0.0)
            multiplier = 1.0 + math.log(years + 1.0)
            
            # Quét match dựa trên cả [Tên chuẩn hóa từ Taxonomy] VÀ [Tên gốc]
            if norm_name in mh_set or raw_name in mh_set:
                cand_hard_score += self.W_MUST_HAVE * multiplier
                mh_set.discard(norm_name)
                mh_set.discard(raw_name)
            elif norm_name in nh_set or raw_name in nh_set:
                cand_hard_score += self.W_NICE_TO_HAVE * multiplier
                nh_set.discard(norm_name)
                nh_set.discard(raw_name)
            elif norm_name in ex_set or raw_name in ex_set:
                cand_hard_score += self.W_EXPANSION * multiplier
                ex_set.discard(norm_name)
                ex_set.discard(raw_name)
            else:
                cand_surplus_score += self.W_SURPLUS * multiplier # Gọi riêng vào thang Bonus Surplus
            
        # 3. CHUẨN HÓA VÀ TRÀN ĐIỂM (CAP & SPILLOVER)
        hard_ratio = cand_hard_score / max_score
        capped_ratio = min(hard_ratio, 1.0)
        overflow_ratio = max(0.0, hard_ratio - 1.0)
        
        # 4. RÀNG BUỘC
        constraint_score = self._process_constraints(jd_data, cv_data)
        
        # 5. GHÉP BASE SCORE (MAX 100)
        base_score = (capped_ratio * self.W_HARD * 100) + (constraint_score * self.W_CONSTRAINTS * 100)
        
        # 6. ĐIỂM THƯỞNG BONUS
        overqualified_bonus = overflow_ratio * self.W_HARD * 100
        soft_bonus = soft_match_count * self.B_SOFT
        cert_count = len(cv_data.get('Hard_Skills', {}).get('Certifications', []))
        cert_bonus = cert_count * self.B_CERT
        
        # NOTE: Surplus bonus được đánh giá riêng lẻ không đội Base Score
        total_bonus = overqualified_bonus + soft_bonus + cert_bonus + cand_surplus_score
        
        final_score = base_score + total_bonus
        
        return {
            'Base_Score': round(base_score, 2),
            'Bonus_Score': round(total_bonus, 2),
            'Total_Score': round(final_score, 2),
            'Is_Overqualified': overflow_ratio > 0
        }""")

    add_md("""## 5. Khởi tạo Engine Chấm Điểm""")
    add_code("""import torch # for soft skill matcher

# Khởi tạo Engine
soft_matcher = SoftSkillMatcher()
engine = CompositeScorer()""")

    add_md("""## 6. Mẫu Test Một Chạm (Tùy chọn)
Giúp quan sát đầu ra rõ ràng trước khi chạy hàng loạt. Bạn có thể bỏ qua block này nếu muốn chạy luôn Batch Pipeline.""")
    add_code("""# Lấy thử 1 JD và 1 CV
try:
    sample_jd_path = os.path.join(JD_DIR, os.listdir(JD_DIR)[0])
    sample_cv_path = os.path.join(RESUME_DIR, os.listdir(RESUME_DIR)[0])
    
    with open(sample_jd_path, 'r', encoding='utf-8') as f:
        jd_test = json.load(f)
    with open(sample_cv_path, 'r', encoding='utf-8') as f:
        cv_test = json.load(f)
        
    jd_soft = jd_test.get('Soft_Skills', [])
    cv_soft = cv_test.get('Soft_Skills', [])
    
    match_count = soft_matcher.count_matches(jd_soft, cv_soft)
    res = engine.evaluate(jd_test, cv_test, soft_match_count=match_count)
    
    print(f"\\nTESTING REPORT")
    print(f"JD: {os.path.basename(sample_jd_path)}")
    print(f"CV: {os.path.basename(sample_cv_path)}")
    print(f"Base Score: {res['Base_Score']}/100")
    print(f"Bonus Score: +{res['Bonus_Score']}")
    print(f"Final Score: {res['Total_Score']}")
    
except Exception as e:
    logger.error(f"Test failed: {e}")""")

    add_md("""## 7. Chạy Hàng Loạt & Xuất CSV (Batch Pipeline)""")
    add_code("""def process_all(jd_dir, cv_dir, output_dir):
    jds = []
    for f in os.listdir(jd_dir):
        if f.endswith('.json'):
            path = os.path.join(jd_dir, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    jds.append({"name": f.replace('.json', ''), "data": json.load(file)})
            except: continue
            
    cv_files = [f for f in os.listdir(cv_dir) if f.endswith('.json')]
    
    results = []
    # Dict lưu trữ kết quả chi tiết từng JD
    jd_specific_results = {jd['name']: [] for jd in jds}
    
    for cv_f in tqdm(cv_files, desc="Ranking Resumes"):
        cv_path = os.path.join(cv_dir, cv_f)
        try:
            with open(cv_path, 'r', encoding='utf-8') as file:
                cv_data = json.load(file)
        except Exception as e:
            logger.warning(f"Failed to read {cv_f}: {e}")
            continue
            
        cv_name = cv_f.replace('.json', '')
        row = {'file_name': cv_name}
        cv_soft_skills = cv_data.get('Soft_Skills', [])
        
        for jd in jds:
            jd_soft = jd['data'].get('Soft_Skills', [])
            jd_name = jd['name']
            try:
                match_count = soft_matcher.count_matches(jd_soft, cv_soft_skills)
                res = engine.evaluate(jd['data'], cv_data, soft_match_count=match_count)
                
                # Ghi nhận vào bảng tổng
                row[jd_name] = res['Total_Score']
                
                # Ghi nhận chi tiết vào bảng riêng của JD đó
                jd_specific_results[jd_name].append({
                    'file_name': cv_name,
                    'Base Score': res['Base_Score'],
                    'Bonus Score': res['Bonus_Score'],
                    'Final Score': res['Total_Score']
                })
                
            except Exception as e:
                row[jd_name] = 0.0
                jd_specific_results[jd_name].append({
                    'file_name': cv_name,
                    'Base Score': 0.0,
                    'Bonus Score': 0.0,
                    'Final Score': 0.0
                })
                
        results.append(row)
        
    # Bảng tổng hợp chứa tất cả JD
    df_main = pd.DataFrame(results)
    out_path_main = os.path.join(output_dir, 'final_ranking_scores.csv')
    df_main.to_csv(out_path_main, index=False)
    logger.info(f"Đã lưu bảng tổng hợp: {out_path_main}")
    
    # Bảng chi tiết cho từng JD
    for jd_name, rows in jd_specific_results.items():
        df_jd = pd.DataFrame(rows)
        df_jd = df_jd.sort_values(by='Final Score', ascending=False)
        out_path_jd = os.path.join(output_dir, f"{jd_name}_ranking_scores.csv")
        df_jd.to_csv(out_path_jd, index=False)
        
    logger.info(f"Hoàn thành! Đã tạo thêm {len(jds)} file CSV chi tiết theo JD.")
    return df_main

# Khởi chạy Pipeline
df_result = process_all(JD_DIR, RESUME_DIR, OUTPUT_DIR)
# df_result.head()""")

    # Build final notebook struct
    nb = {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    with open('d:/Study/AI/Project/resume_ranking/research-resumeRanking/scratch/composite_scoring_colab.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    create_notebook()