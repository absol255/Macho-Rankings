(function () {
    const machoFlagBuy = document.getElementById("macho-flag-buy");
    const machoFlagAmount = document.getElementById("macho-flag-amount");
    const machoFlagBank = document.getElementById("macho-flag-bank");
    const machoBadgeBuy = document.getElementById("macho-badge-buy");
    const machoBadgeAmount = document.getElementById("macho-badge-amount");
    const machoBadgeBank = document.getElementById("macho-badge-bank");
    const machoEraserBuy = document.getElementById("macho-eraser-buy");
    const machoEraserAmount = document.getElementById("macho-eraser-amount");
    const machoEraserBank = document.getElementById("macho-eraser-bank");
    const machoPencilTopperBuy = document.getElementById("macho-penciltopper-buy");
    const machoPencilTopperAmount = document.getElementById("macho-penciltopper-amount");
    const machoPencilTopperBank = document.getElementById("macho-penciltopper-bank");
    const macho3dPrintBuy = document.getElementById("macho-3dprint-buy");
    const macho3dPrintAmount = document.getElementById("macho-3dprint-amount");
    const macho3dPrintBank = document.getElementById("macho-3dprint-bank");
    const machoCowEraserBuy = document.getElementById("macho-coweraser-buy");
    const machoCowEraserAmount = document.getElementById("macho-coweraser-amount");
    const machoCowEraserBank = document.getElementById("macho-coweraser-bank");
    const machoKeychainBuy = document.getElementById("macho-keychain-buy");
    const machoKeychainAmount = document.getElementById("macho-keychain-amount");
    const machoKeychainBank = document.getElementById("macho-keychain-bank");
    const machoPenBuy = document.getElementById("macho-pen-buy");
    const machoPenAmount = document.getElementById("macho-pen-amount");
    const machoPenBank = document.getElementById("macho-pen-bank");

    machoFlagBuy.addEventListener('click', function () {
        const amount = parseInt(machoFlagAmount.value);
        const bank = parseInt(machoFlagBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "flag", item_cost: 7 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho flag");
                    return;
                }
                alert("Bought a macho flag!")
    })});

    machoBadgeBuy.addEventListener('click', function () {
        const amount = parseInt(machoBadgeAmount.value);
        const bank = parseInt(machoBadgeBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "badge", item_cost: 3 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho badge");
                    return;
                }
                alert("Bought a macho badge!")
    })});

    machoEraserBuy.addEventListener('click', function () {
        const amount = parseInt(machoEraserAmount.value);
        const bank = parseInt(machoEraserBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "eraser", item_cost: 5 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho pink eraser");
                    return;
                }
                alert("Bought a macho pink eraser!")
    })});

    machoPencilTopperBuy.addEventListener('click', function () {
        const amount = parseInt(machoPencilTopperAmount.value);
        const bank = parseInt(machoPencilTopperBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "penciltopper", item_cost: 10 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho pencil topper");
                    return;
                }
                alert("Bought a macho pencil topper!")
    })});

    macho3dPrintBuy.addEventListener('click', function () {
        const amount = parseInt(macho3dPrintAmount.value);
        const bank = parseInt(macho3dPrintBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "3dprint", item_cost: 15 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho 3d print");
                    return;
                }
                alert("Bought a macho 3d print!")
    })});

    machoCowEraserBuy.addEventListener('click', function () {
        const amount = parseInt(machoCowEraserAmount.value);
        const bank = parseInt(machoCowEraserBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "coweraser", item_cost: 30 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho cow eraser");
                    return;
                }
                alert("Bought a macho cow eraser!")
    })});

    machoKeychainBuy.addEventListener('click', function () {
        const amount = parseInt(machoKeychainAmount.value);
        const bank = parseInt(machoKeychainBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "keychain", item_cost: 12 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho keychain");
                    return;
                }
                alert("Bought a macho keychain!")
    })});

    machoPenBuy.addEventListener('click', function () {
        const amount = parseInt(machoPenAmount.value);
        const bank = parseInt(machoPenBank.value);

        fetch("/api/buy", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({bank: bank, amount: amount, item: "pen", item_cost: 8 || 0 }),
        })
            .then(async function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    alert(res.d.error || "Could not buy a macho pen");
                    return;
                }
                alert("Bought a macho pen!")
    })});

})();