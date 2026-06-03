(function () {
    const signinCard = document.getElementById("signin-card");
    const usernameInput = document.getElementById("username");
    const bankAccNum = document.getElementById("bankaccnum");
    const signinBtn = document.getElementById("signin-btn");
    const signinMsg = document.getElementById("signin-msg");
    const rankElement = document.getElementById('user-rank');
    const rankValueElement = document.getElementById('rank-value');

    signinBtn.addEventListener("click", function () {
        signinMsg.textContent = "";
        const username = usernameInput.value.trim();
        const bankAccountNumber = bankAccNum.value.trim();

        if (!username || !bankAccountNumber) {
            signinMsg.textContent = "Username and bank account number are required.";
            return;
        }

        fetch("/api/rankings/session", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: username,
                bank_account_number: bankAccountNumber,
            }),
        })
            .then(function (r) {
                return r.json().then(function (d) {
                    return { ok: r.ok, d: d };
                });
            })
            .then(function (res) {
                if (!res.ok) {
                    signinMsg.textContent = res.d.error || "Sign in failed";
                    return;
                }
                return Promise.all([
                    fetch("/api/ranking", {
                        method: "POST",
                        credentials: "include",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            username: username
                        })
                    }).then(function (r) { return r.json(); }),
                ]);
            })
            .then(function (results) {
                if (results && results[0]) {
                    const rank = results[0].ranking;
                    rankValueElement.textContent = rank;
                    signinCard.style.display = 'none';
                    rankElement.style.display = '';
                }
            });
    });
})();