document.getElementById('currency-form').addEventListener('submit', function(event) {
            event.preventDefault();

            const fromCurrency = document.getElementById('from-currency').value;
            const toCurrency = document.getElementById('to-currency').value;
            const amount = document.getElementById('amount').value;

            console.log(`Converting ${amount} ${fromCurrency} to ${toCurrency}`);


        });