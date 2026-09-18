# Logistics AI Optimization

A Flask-based logistics analytics application that uses machine-learning models to estimate sales, profit, shipping time, delivery risk, and customer or delivery outcomes. It also compares logistics scenarios and produces operational recommendations.

## Features

- Predict sales, profit, shipping days, delivery status, customer segment, and late-delivery risk.
- Calculate an efficiency score and business-risk level.
- Generate recommendations and AI-style explanations from prediction results.
- Compare up to three logistics scenarios using efficiency, sustainability, cost, fuel, emissions, and delivery-risk metrics.
- Optional Power BI preview page using an embed URL from environment configuration.

## Project Structure

```text
App.py                         Flask application entry point
utils/                         Prediction, analytics, and scenario logic
models/                        Saved machine-learning models
dataset/                       Supply-chain dataset
templates/                    HTML templates
static/                       CSS, JavaScript, and images
uploads/                       Local uploaded files (ignored by Git)
cache/                         Local cache files (ignored by Git)
```

## Requirements

- Python 3.10 or newer
- Flask
- pandas
- joblib
- scikit-learn

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Khotso-Matlatsa/logistics_AI.git
   cd logistics_AI
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install Flask pandas joblib scikit-learn
   ```

## Configuration

The Power BI preview is optional. To configure it, copy `.env.example` to `.env` and set `POWERBI_EMBED_URL` to your report embed URL. The current Flask application does not automatically load `.env`; configure the variable in your shell or add environment loading if needed.

## Running the Application

Start the development server from the project root:

```bash
python App.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

Useful pages include:

- `/` - Home page
- `/dashboard` - Prediction dashboard
- `/compare-scenarios` - Compare three logistics scenarios
- `/analytics` - Analytics view
- `/ai-reports` - Reports view
- `/powerbi-preview` - Optional Power BI preview

## Model Files

The application expects the saved models in `models/`. The primary prediction workflow uses:

- `Days_of_shipping_linear.pkl`
- `Latedelivery_logistic.pkl`
- `Saleslinear.pkl`
- `OPPOlinear.pkl`
- `CustSegmentlogistic.pkl`
- `DelStatuslogistic.pkl`

Do not remove or rename these files unless the loading code is updated as well.

## Data Note

The supply-chain CSV is approximately 91 MB. GitHub accepts it because it is below the 100 MB hard limit, but GitHub recommends using Git LFS or external storage for files larger than 50 MB.

## License

No license has been specified for this repository yet.