function makePayment() {
    const username = localStorage.getItem('username');
    const recipient = document.getElementById('recipient').value;
    const amount = parseFloat(document.getElementById('amount').value);
    fetch('/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: `mutation { requestTransaction(amount: ${amount}, payerUsername: "${username}", recipientUsername: "${recipient}") { id } }` })
    })
    .then(res => res.json())
    .then(() => {
        alert('Payment Successful');
        window.location.reload();
    });
}