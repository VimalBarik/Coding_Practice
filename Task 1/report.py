import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def create_product_issue_plot(product_issues):
    """Create bar plot for main issues by product"""
    plt.figure(figsize=(15, 8))
    products = []
    issues = []
    counts = []
    
    for product, data in product_issues.items():
        products.append(product)
        issues.append(data['main_issue'])
        counts.append(data['issue_count'])
    
    df = pd.DataFrame({
        'Product': products,
        'Main Issue': issues,
        'Count': counts
    })
    
    sns.barplot(data=df, x='Product', y='Count', hue='Main Issue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Main Issues by Product')
    plt.tight_layout()
    return plt.gcf()

def create_color_preference_plot(color_prefs):
    """Create heatmap for color preferences"""
    # Convert to DataFrame
    data = []
    for product in color_prefs:
        for color, count in color_prefs[product].items():
            data.append({'Product': product, 'Color': color, 'Count': count})
    
    df = pd.DataFrame(data)
    pivot_table = df.pivot(index='Product', columns='Color', values='Count').fillna(0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd')
    plt.title('Color Preferences by Product')
    plt.tight_layout()
    return plt.gcf()

def create_sentiment_plot(df):
    """Create sentiment analysis visualization"""
    plt.figure(figsize=(12, 6))
    sentiment_by_issue = df.groupby('issue_type')['sentiment_score'].mean().sort_values()
    
    colors = ['red' if x < 0 else 'green' for x in sentiment_by_issue]
    sentiment_by_issue.plot(kind='bar', color=colors)
    plt.title('Average Sentiment Score by Issue Type')
    plt.xticks(rotation=45, ha='right')
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def create_urgency_plots(df):
    """Create urgency distribution visualizations"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Overall urgency distribution
    sns.countplot(data=df, x='urgency_level', ax=ax1)
    ax1.set_title('Urgency Level Distribution')
    
    # Top urgent products
    urgent_products = df[df['urgency_level'] == 'High']['product'].value_counts().head()
    urgent_products.plot(kind='bar', ax=ax2)
    ax2.set_title('Products with Most High-Urgency Tickets')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return plt.gcf()

def generate_text_report(product_issues, color_prefs, df):
    """Generate detailed text report"""
    report = []
    
    # 1. Product-Specific Issues
    report.append("\n🎯 PRODUCT-SPECIFIC ISSUES")
    report.append("-" * 50)
    for product, data in product_issues.items():
        report.append(f"{product}:")
        report.append(f"  • Main issue: {data['main_issue']} ({data['issue_count']} tickets)")
        report.append(f"  • Sentiment: {data['avg_sentiment']:.3f}")
        report.append(f"  • Common words: {', '.join(data['common_words'][:5])}")
        report.append("")
    
    # 2. Color Preferences
    report.append("\n🎨 COLOR PREFERENCES (General Inquiries)")
    report.append("-" * 50)
    for product in color_prefs:
        if color_prefs[product]:
            report.append(f"{product}:")
            sorted_colors = sorted(color_prefs[product].items(), 
                                key=lambda x: x[1], reverse=True)
            for color, count in sorted_colors:
                report.append(f"  • {color}: {count}")
            report.append("")
    
    # 3. Sentiment Analysis
    report.append("\n😊 SENTIMENT ANALYSIS")
    report.append("-" * 50)
    sentiment_by_issue = df.groupby('issue_type')['sentiment_score'].mean().sort_values()
    report.append("Average Sentiment by Issue Type:")
    for issue, score in sentiment_by_issue.items():
        report.append(f"  • {issue}: {score:.3f}")
    report.append("")
    
    # 4. Urgency Distribution
    report.append("\n⚡ URGENCY DISTRIBUTION")
    report.append("-" * 50)
    urgency_counts = df['urgency_level'].value_counts()
    for level, count in urgency_counts.items():
        report.append(f"  • {level}: {count}")
    
    report.append("\nProducts with Most Urgent Tickets:")
    urgent_products = df[df['urgency_level'] == 'High']['product'].value_counts().head()
    for product, count in urgent_products.items():
        report.append(f"  • {product}: {count}")
    
    return "\n".join(report)

def save_report(df, product_issues, color_prefs, output_dir="reports"):
    """Generate and save complete report with visualizations"""
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate and save plots
    create_product_issue_plot(product_issues).savefig(f"{output_dir}/product_issues.png")
    plt.close()
    
    create_color_preference_plot(color_prefs).savefig(f"{output_dir}/color_preferences.png")
    plt.close()
    
    create_sentiment_plot(df).savefig(f"{output_dir}/sentiment_analysis.png")
    plt.close()
    
    create_urgency_plots(df).savefig(f"{output_dir}/urgency_distribution.png")
    plt.close()
    
    # Generate and save text report
    text_report = generate_text_report(product_issues, color_prefs, df)
    with open(f"{output_dir}/detailed_report.txt", "w") as f:
        f.write(text_report)
    
    return text_report 