CodeGraph AI — Smart Code Passport

Understand Code. Unlock AI Insights. Powered by PayPal.

Overview

CodeGraph AI is a Python-based code intelligence project that helps developers explore Python repositories, identify relevant files, and understand relationships between modules.

Smart Code Passport extends CodeGraph AI with AI-generated repository reports and a PayPal Sandbox payment workflow.

Features

* Python repository indexing and code search
* Graph-based analysis of file relationships
* AI-generated Code Passport reports
* PayPal Sandbox checkout using the Orders v2 API
* Payment verification before premium report access

Technologies

* Python — Code analysis and application logic
* Gemini 3.1 Flash Lite — AI-generated explanations
* PayPal Developer Platform — Sandbox payment processing
* PayPal Orders v2 API — Order creation, approval, capture, and verification
* Google Colab — Development and integration testing
* GitHub — Source code and version control

How It Works

1. CodeGraph AI indexes a Python repository.
2. The application identifies relevant files and relationships.
3. A $1 USD test order is created using PayPal Sandbox.
4. The buyer approves the simulated payment.
5. The payment is captured and verified through PayPal.
6. Gemini generates a premium Smart Code Passport using the repository analysis results.

Security

* All payments are simulated using PayPal Sandbox.
* PayPal credentials and Gemini API keys are stored in Google Colab Secrets during development.
* Payment status is checked through PayPal’s API.
* No real payment card information is collected.

Current Development Status

The CodeGraph analysis engine, PayPal Sandbox payment workflow, and Gemini report generation have been tested in Google Colab.

The integrated, reusable application and automated report-unlocking workflow are being prepared for the final demonstration.


## Setup Instructions

### Requirements
- Python 3.10 or newer
- Git
- PayPal Developer Sandbox account
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/fhalhashimi1-creator/Fatima.git
cd Fatima
```

### 2. Run CodeGraph AI

```bash
python -m codegraph.Codegraph . index --limit 3
```

### 3. Configure PayPal Sandbox

1. Create a Sandbox application at https://developer.paypal.com/
2. Obtain your Sandbox Client ID and Client Secret.
3. Store these credentials securely using Google Colab Secrets.

Required secret names:
- `PAYPAL_CLIENT_ID`
- `PAYPAL_CLIENT_SECRET`
- `PAYPAL_ORDER_ID`

The order ID must belong to a successfully captured Sandbox payment.

### 4. Configure Google Gemini

1. Obtain a Gemini API key from https://aistudio.google.com/
2. Save it in Google Colab Secrets as `GEMINI_API_KEY`.
3. Grant the notebook permission to access the secrets.

### 5. Generate a Smart Code Passport

Run the CodeGraph analysis, verify the completed PayPal Sandbox payment, and generate an AI report using Gemini.

The premium integration is a prototype demonstrated in Google Colab. A completed Sandbox payment and valid API credentials are required to reproduce the premium workflow.

### Technologies Used

- Python
- Google Gemini AI
- PayPal REST API and Sandbox
- Google Colab
- GitHub
- OAuth 2.0
- JSON and Markdown

### License

This project is licensed under the MIT License. See the `LICENSE` file.
  

Source Code

https://github.com/fhalhashimi1-creator/Fatima

License

An open-source license will be added before final submission.
