#  E-Commerce Shipping Delivery Prediction

A binary classification project that predicts whether an e-commerce shipment will reach the customer **on time or not**, using a deep learning model built with TensorFlow/Keras.

---

##  Problem Statement

E-commerce logistics often struggle with delivery reliability. This project builds a neural network classifier trained on shipment records to predict delivery timeliness — enabling businesses to proactively flag at-risk orders.

**Target Variable:** `Reached.on.Time_Y.N`
- `1` → Shipment reached on time
- `0` → Shipment did NOT reach on time

---

##  Dataset

**File:** `Train.csv`

| Feature | Type | Description |
|---|---|---|
| `ID` | int | Unique shipment identifier (dropped during preprocessing) |
| `Warehouse_block` | categorical | Warehouse block (A/B/C/D/F) |
| `Mode_of_Shipment` | categorical | Shipment mode (Flight / Road / Ship) |
| `Customer_care_calls` | int | Number of customer support calls |
| `Customer_rating` | int | Customer rating (1–5) |
| `Cost_of_the_Product` | int | Product cost in USD |
| `Prior_purchases` | int | Number of prior purchases by the customer |
| `Product_importance` | categorical | Importance level (low / medium / high) |
| `Gender` | categorical | Customer gender (M / F) |
| `Discount_offered` | int | Discount offered on the product (%) |
| `Weight_in_gms` | int | Weight of the shipment in grams |

---

##  Tech Stack

- **Language:** Python 3.x
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Preprocessing:** Scikit-learn (`OneHotEncoder`, `MinMaxScaler`, `train_test_split`)
- **Modelling:** TensorFlow / Keras (`Sequential`, `Dense`, `Dropout`, `Adam`)

---

##  Preprocessing Pipeline

1. **Drop `ID`** column (non-informative identifier)
2. **Split** features into categorical and numerical subsets
3. **OneHotEncode** categorical columns: `Warehouse_block`, `Mode_of_Shipment`, `Product_importance`, `Gender`
4. **MinMaxScale** numerical columns
5. **Concatenate** scaled numerics + OHE-encoded categoricals → final feature matrix of **19 features**
6. **One-hot encode target** using `to_categorical` (2 classes)

---

##  Model Architecture

```
Input (19,)
    │
Dense(128, activation='relu')
    │
Dropout(0.3)
    │
Dense(64, activation='relu')
    │
Dropout(0.3)
    │
Dense(2, activation='softmax')   ← binary output
```

| Hyperparameter | Value |
|---|---|
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Loss | Categorical Crossentropy |
| Metric | Accuracy |
| Epochs | 50 |
| Batch Size | 32 |
| Validation Split | 20% (via `train_test_split`) |

---

##  How to Run

### 1. Clone the repo and install dependencies

```bash
git clone <repo-url>
cd e-commerce-shipping-prediction
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow
```

### 2. Add the dataset

Place `Train.csv` in the project root directory.

### 3. Run the notebook

```bash
jupyter notebook E_Commerce_Shipping_Data.ipynb
```

Execute all cells top-to-bottom.

---

##  Single-Row Inference

A `predict_on_single_row()` utility is included to test the model on a custom shipment record:

```python
user_input = pd.Series({
    'ID': 0,
    'Warehouse_block': 'D',
    'Mode_of_Shipment': 'Flight',
    'Customer_care_calls': 4,
    'Customer_rating': 2,
    'Cost_of_the_Product': 177,
    'Prior_purchases': 3,
    'Product_importance': 'low',
    'Gender': 'F',
    'Discount_offered': 44,
    'Weight_in_gms': 1233
})

predicted_class, result = predict_on_single_row(user_input)
print(result)
# → "The shipment is predicted NOT to reach on time."
```

The function internally handles preprocessing (scaling + encoding) using the fitted `scaler` and `ohe` objects from the training pipeline.

---

##  Project Structure

```
e-commerce-shipping-prediction/
│
├── E_Commerce_Shipping_Data.ipynb   # Main notebook
├── Train.csv                        # Dataset (not included in repo)
└── README.md
```

---

##  Notes

- The `scaler` and `ohe` objects must be fitted on training data before calling `predict_on_single_row()` — run all notebook cells in sequence.
- Categorical input values must exactly match the training distribution (e.g. `'Flight'`, `'low'`, `'F'`) to avoid OHE shape mismatches.
