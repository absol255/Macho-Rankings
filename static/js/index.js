(function () {
    const listEl = document.getElementById("rank-list");

    function load() {
        fetch("/api/rankings", { credentials: "include" })
            .then(function (r) {
                if (r.status === 401) {
                    window.location.href = "/login";
                    return null;
                }
                return r.json();
            })
            .then(function (rankings) {
                if (!rankings) return;
                if (!rankings.length) {
                    listEl.innerHTML = "<p>No rankings yet.</p>";
                    return;
                }

                listEl.innerHTML = rankings.map(function (ranking) {
                    return (
                        '<div class="user">' +
                        '<div style="flex:1">' +
                        '<p>' + ranking.username + '</p>' +
                        '<p>' + ranking.ranking + '</p>' +
                        "</div>"
                    );
                }).join("");
            })};

    load();
    

})();