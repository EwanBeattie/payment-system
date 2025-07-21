document.addEventListener("DOMContentLoaded", () => {
    const username = localStorage.getItem('username');
    fetch('/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: `query { getUser(username: "${username}") { balance, paymentsMade { amount, dateTime, recipientUsername } } }` })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('balance').innerText = data.data.getUser.balance;
        const transactions = data.data.getUser.paymentsMade;
        const list = document.getElementById('transactions');
        transactions.forEach(t => {
            let li = document.createElement('li');
            li.innerText = `Sent $${t.amount} to ${t.recipientUsername} on ${t.dateTime}`;
            list.appendChild(li);
        });
    });
});