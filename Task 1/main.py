# main.py
import sys
from data_preprocessing import preprocess_file
from feature_eng import run_feature_engineering
from report import save_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_xls_file>")
        return
    
    input_file = sys.argv[1]
    print("\n🔄 Step 1: Data Preprocessing")
    print("Processing:", input_file)
    
    # Run preprocessing
    cleaned_df = preprocess_file(input_file)
    cleaned_file = input_file.replace('.xls', '_cleaned.csv')
    
    print("\n🔍 Step 2: Feature Engineering")
    # Run feature engineering on the cleaned data
    enhanced_df, product_issues, color_prefs = run_feature_engineering(cleaned_file)
    
    print("\n📊 Step 3: Generating Reports")
    # Generate reports and visualizations
    text_report = save_report(enhanced_df, product_issues, color_prefs)
    
    print("\n✨ Pipeline complete! Check the output files:")
    print(f"1. Cleaned data: {cleaned_file}")
    print(f"2. Enhanced features: {cleaned_file.replace('.csv', '_enhanced_features.csv')}")
    print("3. Reports and visualizations: ./reports/")
    print("\n📝 Detailed Report:")
    print(text_report)

if __name__ == "__main__":
    main()