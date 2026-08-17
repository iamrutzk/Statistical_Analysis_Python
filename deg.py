# ==========================================================
# 🧬 Differential Gene Expression Analysis using t-test
# ==========================================================
# This script identifies genes that show significant differences 
# in expression between two experimental conditions (e.g., CAUT vs SHAM).
# It performs data normalization, statistical testing, visualization, 
# and result extraction for biological interpretation.
# ==========================================================


# --- Step 1: Import necessary libraries ---
import pandas as pd                # For handling tabular data
import numpy as np                 # For numerical operations
import seaborn as sns              # For visualization
import matplotlib.pyplot as plt    # For plotting
from scipy.stats import ttest_ind  # For performing statistical t-tests
from bioinfokit import visuz       # For volcano plot visualization

# --- Step 2: Load the dataset ---
# Reads an Excel file containing gene expression data.
# Each row = a gene, each column = a sample.
# One column ("Accession") holds gene identifiers.
df = pd.read_excel(r"/content/drive/MyDrive/L2-LSSSDC batch-Jan 2025/LSSSDC_ Feb 2025/Statistics using python/Session9/PythonRAT.xlsx")

# Set 'Accession' column as the index for easy access to gene names.
df.set_index("Accession", inplace=True)


# --- Step 3: Log2 transformation ---
# Converts expression values to log2 scale.
# Reason: Expression data often spans large ranges and may be skewed.
# Log transformation stabilizes variance and makes data more normally distributed,
# which is required for parametric tests like the t-test.
df_log2 = np.log2(df + 1)  # Adding 1 prevents taking log of zero values.


# --- Step 4: Split data into experimental groups ---
# Separates samples into two groups (CAUT and SHAM) using column name patterns.
# This allows independent comparison between treatment and control.
group_caut = df_log2.loc[:, df_log2.columns.str.contains("Caut", case=False)]
group_sham = df_log2.loc[:, df_log2.columns.str.contains("SHAM", case=False)]


# --- Step 5: Visualize overall expression distribution ---
# Helps verify normalization — after log2 transformation, 
# expression values should roughly follow a normal-like distribution.
plt.figure(figsize=(8,5))
sns.histplot(df_log2.values.flatten(), bins=40, kde=True, color="purple")
plt.title("Distribution of log2 Expression Values")
plt.xlabel("Expression Level (Log2)")
plt.show()


# --- Step 6: Perform statistical comparison (t-test) ---
# For each gene:
#   - Perform an independent t-test between CAUT and SHAM samples.
#   - Compute the average expression difference (log2 Fold Change).
# Welch’s t-test is used (equal_var=False) because biological data 
# often have unequal variances between groups.
p_value = []
log2FC = []

for gene in df_log2.index:
    _, p = ttest_ind(group_caut.loc[gene], group_sham.loc[gene], equal_var=False)
    p_value.append(p)
    log2FC.append(group_caut.loc[gene].mean() - group_sham.loc[gene].mean())


# --- Step 7: Create a result summary table ---
# Combines each gene’s p-value and log2 fold change into a single dataframe.
# This table is the foundation for identifying significantly altered genes.
result = pd.DataFrame({
    "Gene": df_log2.index,
    "P_value": p_value,
    "log2FC": log2FC
})
result.set_index("Gene", inplace=True)


# --- Step 8: Visualize results with a Volcano Plot ---
# A volcano plot helps quickly identify genes with both:
#   - statistically significant p-values (y-axis)
#   - large fold changes (x-axis)
# It visually separates upregulated, downregulated, and unchanged genes.
visuz.GeneExpression.volcano(
    df=result,
    lfc='log2FC',
    pv='P_value',
    plotlegend=True,
    legendpos='upper right',
    legendanchor=(1.45, 1),
    color=("blue", "grey", "red"),
    markerdot="*",
    dotsize=20
)


# --- Step 9: Cluster heatmap of top 10 significant genes ---
# Selects top 10 genes with the smallest p-values (most significant).
# Displays a heatmap showing expression patterns across samples.
# Clustering groups genes and samples with similar profiles.
top_10_genes = result.sort_values("P_value").head(10).index
sns.clustermap(df_log2.loc[top_10_genes], cmap="viridis", figsize=(8,6))
plt.title("Top 10 Most Significant Genes (Log2 Expression)")
plt.show()


# --- Step 10: Filter significantly differentially expressed genes ---
# Criteria for "significance":
#   - P-value ≤ 0.05 → statistically significant
#   - |log2FC| ≥ 1 → biologically meaningful fold change (2-fold difference)
# Adjust these thresholds depending on your study design.
significant_genes = result[(result["P_value"] <= 0.05) & (abs(result["log2FC"]) >= 1)]


# --- Step 11: Save significant genes to file ---
# Exports the list of significant genes to Excel for further biological analysis.
significant_genes.to_excel("Significant_Genes.xlsx", index=True)

# Displays the number of genes passing the significance threshold.
print(f"✅ Total significant genes found: {len(significant_genes)}")
