document.addEventListener('DOMContentLoaded', () => {
    const addAccountForm = document.getElementById('add-account-form');
    const accountsList = document.getElementById('accounts');

    addAccountForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const platform = document.getElementById('platform').value;
        const handle = document.getElementById('handle').value;

        const response = await fetch('/api/add_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ platform, handle }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                alert('Account added successfully');
                addAccountForm.reset();
                addAccountToList(result);
            } else {
                alert('Error adding account');
            }
        } else {
            alert('Error adding account');
        }
    });

    function addAccountToList(account) {
        const li = document.createElement('li');
        li.textContent = `${account.platform}: ${account.handle}`;
        li.setAttribute('data-id', account.id);
        accountsList.appendChild(li);
    }

    async function loadAccounts() {
        const response = await fetch('/api/get_analytics');
        const data = await response.json();

        accountsList.innerHTML = '';
        for (const [id, account] of Object.entries(data)) {
            const li = document.createElement('li');
            li.textContent = `${account.platform}: ${account.handle} - Followers: ${account.metrics.followers}, Engagement Rate: ${account.metrics.engagement_rate}%`;
            li.setAttribute('data-id', id);
            accountsList.appendChild(li);
        }
    }

    loadAccounts();
});
