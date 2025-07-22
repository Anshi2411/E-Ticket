function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.style.display = sidebar.style.display === "none" ? "block" : "none";
}

function updateBalanceDisplay(balance) {
  const balanceSpan = document.getElementById("balance-amount");
  balanceSpan.textContent = balance;
  sessionStorage.setItem("balance", balance);
}

function loadCachedBalance() {
  const cached = sessionStorage.getItem("balance");
  if (cached) {
    updateBalanceDisplay(cached);
  } else {
    updateBalanceDisplay("...");
  }
}

function fetchBalanceWithGrace() {
  fetch("/get-balance/")
    .then((res) => {
      if (!res.ok) throw new Error("Server returned error status");
      return res.json();
    })
    .then((data) => {
      if (data.success) {
        updateBalanceDisplay(data.balance);
      } else {
        console.warn("Balance fetch failed:", data.message);
      }
    })
    .catch((err) => {
      console.warn("Fetch failed (but not crashing):", err.message);
      // Don't show alert. Show fallback.
      const fallback = sessionStorage.getItem("balance");
      if (fallback) {
        updateBalanceDisplay(fallback);
      } else {
        updateBalanceDisplay("N/A");
      }
    });
}

function loadRecentTicket() {
  const ticket = JSON.parse(sessionStorage.getItem("recentTicket"));
  if (ticket) {
    document.getElementById("recent-ticket").innerHTML = `
      <p><strong>From:</strong> ${ticket.from}</p>
      <p><strong>To:</strong> ${ticket.to}</p>
      <p><strong>Fare:</strong> ₹${ticket.fare}</p>
      <p><strong>Time:</strong> ${ticket.time}</p>
      <p><strong>Date:</strong> ${ticket.date}</p>
    `;
  }
}

window.onload = function () {
  loadCachedBalance();       // Step 1: Load balance from session
  fetchBalanceWithGrace();   // Step 2: Fetch fresh balance
  loadRecentTicket();        // Step 3: Show last ticket if any
};
