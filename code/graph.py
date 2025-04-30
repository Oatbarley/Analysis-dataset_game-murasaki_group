import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

# โหลดข้อมูล
df_corr_chi = pd.read_csv('data/sample60c.csv')
df_anova = pd.read_csv('data/sample60_twoway.csv')

# กราฟ Slide 8: Scatter Plot (Correlation)
plt.figure(figsize=(6, 4))
sns.regplot(
    data=df_corr_chi,
    x='How much time do you play "violent" video games specifically?',
    y='BPAQ Score',
    line_kws={"color": "red"},
    scatter_kws={"alpha": 0.6}
)
plt.title("Scatter Plot with Trend Line: Violent Play Time vs BPAQ Score")
plt.xlabel("Violent Play Time")
plt.ylabel("BPAQ Score")
plt.tight_layout()

plt.show()


# กราฟ Slide 9: Bar Chart (Chi-square)
plt.figure(figsize=(6, 4))
chi_plot = pd.crosstab(df_corr_chi['Game Category'], df_corr_chi['Score Category'])
chi_plot.plot(kind='bar', stacked=True)
plt.title("Bar Chart: Game Category vs Score Category")
plt.xlabel("Game Category")
plt.ylabel("Count")
plt.tight_layout()

plt.show()


# กราฟ Slide 10: Boxplot (Two-way ANOVA)
plt.figure(figsize=(8, 5))
sns.boxplot(
    data=df_anova,
    x='how_much_time_do_you_play_violent_video_games_specifically',
    y='bpaq_score',
    hue='game_category'
)
plt.title("Boxplot: BPAQ Score by Play Time and Game Category")
plt.xlabel("Violent Play Time")
plt.ylabel("BPAQ Score")
plt.legend(title="Game Category", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
plt.close()
