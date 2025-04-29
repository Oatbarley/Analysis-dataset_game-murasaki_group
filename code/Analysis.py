import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# โหลดไฟล์ sample60.csv
df = pd.read_csv('data/sample60.csv')

# ตรวจสอบชื่อคอลัมน์ให้ตรงก่อนรัน
print(df.columns)

# วิเคราะห์ Two-way ANOVA
# สมมุติชื่อคอลัมน์คือ 'ViolentPlayTime', 'Game_Category', 'BPAQ_Score'
model = ols('bpaq_score ~ C(how_much_time_do_you_play_violent_video_games_specifically) * C(game_category)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print("\n=== Two-way ANOVA Result ===")
print(anova_table)
# ------------------------------------------------

from scipy.stats import pearsonr, chi2_contingency

# โหลดไฟล์ sample60c.csv
dfc = pd.read_csv('data/sample60c.csv')

r, p = pearsonr(
    dfc['How much time do you play "violent" video games specifically?'],
    dfc['BPAQ Score']
)
print("\n=== Correlation Result ===")
print("Correlation coefficient (r):", round(r, 4))
print("P-value:", round(p, 4))


# สมมุติชื่อคอลัมน์คือ 'Game_Category' กับ 'Score_Category'
ct = pd.crosstab(dfc['Game Category'], dfc['Score Category'])
chi2, pval, dof, expected = chi2_contingency(ct)

print("\n=== Chi-square Test Result ===")
print("Chi-square statistic:", round(chi2, 4))
print("P-value:", round(pval, 4))
