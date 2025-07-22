// Helper function to retrieve a cookie value by name
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string begins with the name we want
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function generateTicket() {
  const from = document.getElementById("fromStation").value.trim();
  const to = document.getElementById("toStation").value.trim();
  const ticketCount = parseInt(document.getElementById("ticketCount").value);
  const farePerTicket = 16;
  const totalFare = farePerTicket * ticketCount;

  // Log values to debug
  console.log("Generating ticket for:", from, "→", to, "x", ticketCount, "Total:", totalFare);

  if (!from || !to || isNaN(ticketCount)) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const response = await fetch("/buy/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({ from, to, fare: totalFare })
    });

    const data = await response.json();

    if (data.success) {
      localStorage.setItem("from", from);
      localStorage.setItem("to", to);
      localStorage.setItem("ticketDate", new Date().toLocaleDateString());
      localStorage.setItem("newBalance", data.newBalance);
      window.location.href = "/ticket/";
    } else {
      alert(data.message);
    }
  } catch (err) {
    alert("Error: " + err.message);
  }
}
