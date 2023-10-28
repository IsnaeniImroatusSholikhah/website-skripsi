from flask import Flask, render_template, request, jsonify
import joblib
import time

app = Flask(__name__)

model = joblib.load("models/credit_card_fraud_detection_model123.pkl")


@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/fraud-prevention")
def fraud_prevention():
    return render_template("fraud_prevention.html")


@app.route("/index")
def index():
    form_values = {}  # Inisialisasi form_values
    return render_template("index.html", form_values=form_values)


@app.route("/", methods=["GET", "POST"])
def predict():
    form_values = {}  # Inisialisasi form_values
    if request.method == "POST":
        try:
            form_values = request.form  # Menyimpan semua data form dalam form_values
            CUST_ID = form_values["CUST_ID"]
            BALANCE = float(form_values["BALANCE"]) if form_values["BALANCE"] else None
            BALANCE_FREQUENCY = (
                float(form_values["BALANCE_FREQUENCY"])
                if form_values["BALANCE_FREQUENCY"]
                else None
            )
            PURCHASES = (
                float(form_values["PURCHASES"]) if form_values["PURCHASES"] else None
            )
            ONEOFF_PURCHASES = (
                float(form_values["ONEOFF_PURCHASES"])
                if form_values["ONEOFF_PURCHASES"]
                else None
            )
            INSTALLMENTS_PURCHASES = (
                float(form_values["INSTALLMENTS_PURCHASES"])
                if form_values["INSTALLMENTS_PURCHASES"]
                else None
            )
            CASH_ADVANCE = (
                float(form_values["CASH_ADVANCE"])
                if form_values["CASH_ADVANCE"]
                else None
            )
            PURCHASES_FREQUENCY = (
                float(form_values["PURCHASES_FREQUENCY"])
                if form_values["PURCHASES_FREQUENCY"]
                else None
            )
            ONEOFF_PURCHASES_FREQUENCY = (
                float(form_values["ONEOFF_PURCHASES_FREQUENCY"])
                if form_values["ONEOFF_PURCHASES_FREQUENCY"]
                else None
            )
            PURCHASES_INSTALLMENTS_FREQUENCY = (
                float(form_values["PURCHASES_INSTALLMENTS_FREQUENCY"])
                if form_values["PURCHASES_INSTALLMENTS_FREQUENCY"]
                else None
            )
            CASH_ADVANCE_FREQUENCY = (
                float(form_values["CASH_ADVANCE_FREQUENCY"])
                if form_values["CASH_ADVANCE_FREQUENCY"]
                else None
            )
            CASH_ADVANCE_TRX = (
                float(form_values["CASH_ADVANCE_TRX"])
                if form_values["CASH_ADVANCE_TRX"]
                else None
            )
            PURCHASES_TRX = (
                float(form_values["PURCHASES_TRX"])
                if form_values["PURCHASES_TRX"]
                else None
            )
            CREDIT_LIMIT = (
                float(form_values["CREDIT_LIMIT"])
                if form_values["CREDIT_LIMIT"]
                else None
            )
            PAYMENTS = (
                float(form_values["PAYMENTS"]) if form_values["PAYMENTS"] else None
            )
            MINIMUM_PAYMENTS = (
                float(form_values["MINIMUM_PAYMENTS"])
                if form_values["MINIMUM_PAYMENTS"]
                else None
            )
            PRC_FULL_PAYMENT = (
                float(form_values["PRC_FULL_PAYMENT"])
                if form_values["PRC_FULL_PAYMENT"]
                else None
            )
            TENURE = float(form_values["TENURE"]) if form_values["TENURE"] else None

            # Validasi input
            if None in (
                BALANCE,
                BALANCE_FREQUENCY,
                PURCHASES,
                ONEOFF_PURCHASES,
                INSTALLMENTS_PURCHASES,
                CASH_ADVANCE,
                PURCHASES_FREQUENCY,
                ONEOFF_PURCHASES_FREQUENCY,
                PURCHASES_INSTALLMENTS_FREQUENCY,
                CASH_ADVANCE_FREQUENCY,
                CASH_ADVANCE_TRX,
                PURCHASES_TRX,
                CREDIT_LIMIT,
                PAYMENTS,
                MINIMUM_PAYMENTS,
                PRC_FULL_PAYMENT,
                TENURE,
            ):
                return jsonify({"error": "Harap isi semua bidang"})

            input_data = [
                [
                    BALANCE,
                    BALANCE_FREQUENCY,
                    PURCHASES,
                    ONEOFF_PURCHASES,
                    INSTALLMENTS_PURCHASES,
                    CASH_ADVANCE,
                    PURCHASES_FREQUENCY,
                    ONEOFF_PURCHASES_FREQUENCY,
                    PURCHASES_INSTALLMENTS_FREQUENCY,
                    CASH_ADVANCE_FREQUENCY,
                    CASH_ADVANCE_TRX,
                    PURCHASES_TRX,
                    CREDIT_LIMIT,
                    PAYMENTS,
                    MINIMUM_PAYMENTS,
                    PRC_FULL_PAYMENT,
                    TENURE,
                ]
            ]

            prediction = model.predict(input_data)

            if prediction[0] == 1:
                result = "Penipuan"
                fraud_reasons = [
                    "Tingginya frekuensi pembelian dan jumlah pembelian yang tidak biasa.",
                    "Penggunaan kartu dengan saldo yang tidak mencukupi.",
                    "Polanya pembelian yang tidak biasa.",
                    "Tingginya frekuensi penarikan tunai.",
                ]
            else:
                result = "Non-Penipuan"
                fraud_reasons = []

            return jsonify({"prediction": result, "fraud_reasons": fraud_reasons})

        except Exception as e:
            return jsonify(
                {"error": f"Terjadi kesalahan dalam memproses prediksi: {str(e)}"}
            )


if __name__ == "__main__":
    app.run(debug=True)
