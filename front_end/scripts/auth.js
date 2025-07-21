function login() {
    const username = document.getElementById('username').value;
    fetch('/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: `query { getUser(username: "${username}") { id, balance } }` })
    })
    .then(res => res.json())
    .then(data => {
        if (data.data.getUser) {
            localStorage.setItem('username', username);
            window.location.href = 'wallet.html';
        } else {
            alert('User not found');
        }
    });
}